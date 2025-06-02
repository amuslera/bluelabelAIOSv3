#!/usr/bin/env python3
"""
Multi-Terminal Agent Launcher

Launch Enhanced BaseAgents with collaboration capabilities for multi-terminal teamwork.

Usage:
    Terminal 1: python3 launch_agent.py --role=human --name="Product Owner"
    Terminal 2: python3 launch_agent.py --role=cto --name="CTO Agent"
    Terminal 3: python3 launch_agent.py --role=backend-dev --name="Backend Developer"
    Terminal 4: python3 launch_agent.py --role=qa --name="QA Engineer"
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

# Load environment
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.collaborative_agent import (
    CollaborativeAgent,
    CollaborativeAgentConfig,
    create_collaborative_backend_agent,
    create_collaborative_cto_agent,
    create_collaborative_qa_agent,
)
from core.routing.providers.claude import ClaudeConfig, ClaudeProvider
from core.routing.router import LLMRouter, RoutingPolicy, RoutingStrategy

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentTerminal:
    """Interactive terminal for collaborative agents."""

    def __init__(self, agent: CollaborativeAgent):
        self.agent = agent
        self.running = True

    def print_banner(self):
        """Print agent terminal banner."""
        print("=" * 80)
        print("🚀 AIOSv3 COLLABORATIVE AGENT TERMINAL")
        print("=" * 80)
        print(f"Agent: {self.agent.config.name} ({self.agent.role})")
        print(f"ID: {self.agent.agent_id}")
        print(f"Repository: {Path.cwd()}")
        print("=" * 80)
        print()

    def show_help(self):
        """Show available commands."""
        print(f"\n💡 Commands for {self.agent.role}:")
        print("   chat <message>     - Send message to team")
        print("   status <status>    - Update status (active/busy/idle)")
        print("   task <description> - Create and announce new task")
        print("   team               - Show team status")
        print("   help               - Show this help")
        print("   quit               - Leave collaboration")

        if self.agent.role == "human":
            print("\n🎯 As Product Owner:")
            print("   - Define requirements and ask questions")
            print("   - Coordinate team activities")
            print("   - Make product decisions")

        elif self.agent.role == "cto":
            print("\n🎯 As CTO:")
            print("   - Provide technical architecture guidance")
            print("   - Make technology decisions")
            print("   - Review technical approaches")

        elif self.agent.role == "backend-dev":
            print("\n🎯 As Backend Developer:")
            print("   - Implement server-side features")
            print("   - Design APIs and data models")
            print("   - Write and review code")

        elif self.agent.role == "qa":
            print("\n🎯 As QA Engineer:")
            print("   - Create testing strategies")
            print("   - Validate implementations")
            print("   - Ensure quality standards")

    async def run_terminal(self):
        """Run the interactive terminal."""
        self.print_banner()

        # Wait a moment for agent to connect
        await asyncio.sleep(1)

        if not self.agent.connected:
            print("❌ Failed to connect to collaboration server")
            print("💡 Make sure the collaboration server is running:")
            print("   python3 collaboration_server.py")
            return

        print("✅ Connected to collaboration team!")
        self.show_help()

        try:
            while self.running and self.agent.connected:
                try:
                    # Get user input
                    user_input = await asyncio.get_event_loop().run_in_executor(
                        None, input, f"\n{self.agent.role}> "
                    )

                    if not user_input.strip():
                        continue

                    await self.handle_command(user_input.strip())

                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
                except Exception as e:
                    logger.error(f"Error in terminal: {e}")

        finally:
            print(f"\n👋 {self.agent.config.name} leaving collaboration...")
            await self.agent.stop()

    async def handle_command(self, command_line: str):
        """Handle user commands."""
        parts = command_line.split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "quit":
            self.running = False

        elif command == "help":
            self.show_help()

        elif command == "chat":
            if args:
                await self.agent.send_collaboration_message({
                    "type": "chat",
                    "from_id": self.agent.agent_id,
                    "content": args,
                    "metadata": {"manual_message": True}
                })
                print(f"💬 Sent: {args}")
            else:
                print("Usage: chat <message>")

        elif command == "status":
            if args:
                await self.agent.send_collaboration_message({
                    "type": "status_update",
                    "from_id": self.agent.agent_id,
                    "status": args,
                    "current_task": None
                })
                print(f"🔄 Status updated to: {args}")
            else:
                print("Usage: status <active/busy/idle>")

        elif command == "task":
            if args:
                task_id = f"task_{int(asyncio.get_event_loop().time())}"
                await self.agent.send_collaboration_message({
                    "type": "task_update",
                    "task": {
                        "id": task_id,
                        "title": args,
                        "assigned_to": "",
                        "status": "planned",
                        "created_by": self.agent.agent_id
                    }
                })
                print(f"📋 Created task: {args}")
            else:
                print("Usage: task <description>")

        elif command == "team":
            print("👥 Current Team:")
            for collab_id, collab in self.agent.collaborators.items():
                status_icon = "🟢" if collab.get("status") == "active" else "🟡"
                task_info = f" - {collab.get('current_task')}" if collab.get('current_task') else ""
                print(f"   {status_icon} {collab.get('name')} ({collab.get('role')}){task_info}")

        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")


async def create_llm_router() -> Optional[LLMRouter]:
    """Create shared LLM router for agents."""
    try:
        policy = RoutingPolicy(
            strategy=RoutingStrategy.COST_OPTIMIZED,
            max_cost_per_request=0.25,
            max_response_time_ms=45000
        )

        router = LLMRouter(default_policy=policy)

        # Configure Claude provider
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning("No ANTHROPIC_API_KEY found, agents will use mock responses")
            return None

        claude_config = ClaudeConfig(
            provider_name="claude",
            api_key=api_key,
            timeout=45.0,
            max_retries=3
        )

        claude_provider = ClaudeProvider(claude_config)
        router.register_provider("claude", claude_provider)
        await router.initialize()

        logger.info("✅ LLM Router initialized with Claude provider")
        return router

    except Exception as e:
        logger.error(f"Failed to create LLM router: {e}")
        return None


async def create_agent(role: str, name: str, collaboration_server: str) -> CollaborativeAgent:
    """Create appropriate collaborative agent based on role."""

    # Create shared LLM router
    llm_router = await create_llm_router()

    if role == "cto":
        return await create_collaborative_cto_agent(collaboration_server, llm_router)
    elif role == "backend-dev":
        return await create_collaborative_backend_agent(collaboration_server, llm_router)
    elif role == "qa":
        return await create_collaborative_qa_agent(collaboration_server, llm_router)
    else:
        # Create generic collaborative agent
        config = CollaborativeAgentConfig(
            role=role,
            collaboration_server=collaboration_server,
            name=name
        )
        agent = CollaborativeAgent(config, llm_router)
        await agent.initialize()
        return agent


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Launch AIOSv3 Collaborative Agent")
    parser.add_argument("--role", required=True,
                       choices=["human", "cto", "backend-dev", "frontend-dev", "qa", "devops"],
                       help="Agent role in the collaboration")
    parser.add_argument("--name", help="Agent name (defaults based on role)")
    parser.add_argument("--server", default="ws://localhost:8765",
                       help="Collaboration server URL")

    args = parser.parse_args()

    # Set default name if not provided
    if not args.name:
        role_names = {
            "human": "Product Owner",
            "cto": "CTO Agent",
            "backend-dev": "Backend Developer",
            "frontend-dev": "Frontend Developer",
            "qa": "QA Engineer",
            "devops": "DevOps Engineer"
        }
        args.name = role_names.get(args.role, f"{args.role.title()} Agent")

    print(f"🚀 Launching {args.name} ({args.role})...")
    print(f"📡 Connecting to: {args.server}")
    print(f"📁 Repository: {Path.cwd()}")

    try:
        # Create collaborative agent
        agent = await create_agent(args.role, args.name, args.server)

        # Create and run terminal
        terminal = AgentTerminal(agent)
        await terminal.run_terminal()

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        logger.error(f"Failed to launch agent: {e}")
        print(f"❌ Failed to launch agent: {e}")

        if "Connection refused" in str(e):
            print("\n💡 Make sure the collaboration server is running:")
            print("   python3 collaboration_server.py")


if __name__ == "__main__":
    asyncio.run(main())
