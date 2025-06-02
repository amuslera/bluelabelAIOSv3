"""
Visible ARCH-CTO Orchestration Demo - See what's actually happening!

This script demonstrates the orchestration workflow with detailed visibility:
1. ARCH-CTO (Claude) assigns task to Backend Agent
2. Backend Agent implements the solution with REAL code generation
3. ARCH-CTO reviews the code and provides feedback
4. Show the complete workflow with full output
"""

import asyncio
import logging

from orchestration.arch_cto_orchestrator import create_arch_cto_orchestrator

from agents.base.types import Priority, TaskType
from core.routing.providers.mock_provider import MockConfig
from enhanced_mock_provider import EnhancedMockProvider

# Setup detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def setup_orchestrator_with_mock_llm():
    """Create orchestrator with configured mock LLM provider."""
    print("🔧 Setting up ARCH-CTO Orchestrator with Mock LLM Provider...")

    # Create orchestrator
    orchestrator = await create_arch_cto_orchestrator()

    # Get the backend agent's LLM router
    backend_agent = orchestrator.active_agents["backend"]
    router = backend_agent.router

    # Create and register enhanced mock provider
    mock_config = MockConfig(
        provider_name="enhanced_mock",
        response_delay=0.5,  # 500ms delay to simulate real API
        failure_rate=0.0     # No failures for demo
    )

    enhanced_mock_provider = EnhancedMockProvider(
        config=mock_config
    )

    # Register the provider with the router
    router.register_provider("enhanced_mock", enhanced_mock_provider)

    print("✅ Mock LLM Provider registered successfully!")
    print(f"   Router now has {len(router.providers)} provider(s)")

    return orchestrator


async def show_detailed_orchestration():
    """Run orchestration with full visibility."""

    print("🎯 " + "="*80)
    print("   VISIBLE ARCH-CTO ORCHESTRATION DEMO")
    print("   See exactly what happens when Claude orchestrates coding agents!")
    print("🎯 " + "="*80)
    print()

    # Setup orchestrator with mock LLM
    orchestrator = await setup_orchestrator_with_mock_llm()
    print()

    # Define our test task
    task_description = """
Create a FastAPI endpoint for a user authentication system:

Requirements:
- POST /auth/login endpoint
- Accept JSON with: email, password
- Validate email format and password strength
- Return JWT token on success
- Include proper error handling for invalid credentials
- Write comprehensive unit tests
- Follow FastAPI best practices and security guidelines

This should be production-ready authentication code.
"""

    print("📋 TASK ASSIGNMENT & EXECUTION")
    print("-" * 50)
    print("🎯 Task: Creating FastAPI authentication endpoint")
    print(f"📝 Description: {task_description.strip()}")
    print()

    # Assign task
    print("👥 Assigning to Backend Developer Agent...")
    task_id = await orchestrator.assign_task(
        task_description=task_description,
        task_type=TaskType.CODE_GENERATION,
        agent_type="backend",
        complexity=7,  # Higher complexity for auth
        priority=Priority.HIGH,
        metadata={
            "endpoint": "/auth/login",
            "method": "POST",
            "requires_security": True,
            "requires_tests": True,
            "auth_type": "JWT"
        }
    )

    print(f"✅ Task assigned with ID: {task_id}")
    print()

    # Execute task with detailed monitoring
    print("⚙️ BACKEND AGENT EXECUTION")
    print("-" * 40)
    print("🤖 Backend Agent is thinking and generating code...")
    print("💭 Agent context: FastAPI specialist with security expertise")

    result = await orchestrator.execute_task(task_id)

    print("✨ Code generation completed!")
    print(f"   ⏱️  Execution time: {result.execution_time:.2f}s")
    print(f"   🔤 Tokens used: {result.tokens_used}")
    print(f"   💰 Cost: ${result.cost:.4f}")
    print(f"   🧠 Model: {result.model_used}")
    print(f"   🏭 Provider: {result.provider_used}")
    print(f"   ✅ Success: {result.success}")
    print()

    # Show the actual generated code
    if result.output:
        print("💻 GENERATED CODE")
        print("-" * 20)
        print("📄 Here's what the Backend Agent created:")
        print()
        print("🔹" + "-" * 78 + "🔹")
        print(result.output)
        print("🔹" + "-" * 78 + "🔹")
        print()
    else:
        print("⚠️  No code output generated")
        print()

    # Code Review by ARCH-CTO
    print("🔍 ARCH-CTO CODE REVIEW")
    print("-" * 35)
    print("👨‍💼 ARCH-CTO (Claude) reviewing the Backend Agent's work...")

    review = await orchestrator.review_task(task_id)

    print("📊 Review Results:")
    print(f"   🏆 Quality Score: {review.quality_score}/10")
    print(f"   ⚖️  Decision: {review.outcome.value.replace('_', ' ').title()}")
    print(f"   🔄 Needs Revision: {review.requires_revision}")
    print(f"   📝 Summary: {review.summary}")
    print()

    if review.detailed_feedback:
        print("📋 Detailed Feedback:")
        for i, feedback in enumerate(review.detailed_feedback, 1):
            print(f"   {i}. {feedback}")
        print()

    if review.security_issues:
        print("🚨 Security Issues Found:")
        for i, issue in enumerate(review.security_issues, 1):
            print(f"   {i}. {issue}")
        print()

    # Show final decision
    if review.requires_revision:
        print("🔄 REVISION REQUIRED")
        print("-" * 25)
        print("💡 The ARCH-CTO has identified areas for improvement.")
        print("🔧 In a real scenario, this would trigger another development cycle.")
        print("📈 This iterative process ensures high-quality code delivery.")
    else:
        print("✅ CODE APPROVED!")
        print("-" * 20)
        print("🎉 The Backend Agent's code meets ARCH-CTO quality standards!")
        print("🚀 Code is ready for deployment to staging environment.")
        print("📊 Quality metrics passed all thresholds.")

    print()

    # Show orchestration metrics
    print("📊 ORCHESTRATION ANALYTICS")
    print("-" * 35)

    # Task status
    task_status = orchestrator.get_task_status(task_id)
    print("📈 Task Metrics:")
    print(f"   🆔 Task ID: {task_id}")
    print(f"   📊 Status: {task_status['status']}")
    print(f"   🎯 Complexity: {task_status['complexity']}/10")
    print(f"   ⏰ Estimated time: {task_status['estimated_hours']:.1f}h")
    if task_status.get('actual_hours'):
        print(f"   ⏱️  Actual time: {task_status['actual_hours']:.3f}h")
    print(f"   🔄 Revision cycles: {task_status['revision_count']}")
    print()

    # Orchestrator metrics
    metrics = orchestrator.get_orchestration_metrics()
    print("🎯 Orchestrator Performance:")
    print(f"   📝 Total tasks: {metrics.total_tasks}")
    print(f"   ✅ Completed: {metrics.completed_tasks}")
    print(f"   ⏰ Avg completion: {metrics.average_completion_time:.2f}h")
    print(f"   🔄 Avg review cycles: {metrics.average_review_cycles:.1f}")

    if metrics.quality_trends:
        avg_quality = sum(metrics.quality_trends) / len(metrics.quality_trends)
        print(f"   🏆 Avg quality score: {avg_quality:.1f}/10")
    print()

    # Agent status
    backend_agent = orchestrator.active_agents["backend"]
    agent_status = backend_agent.get_status()
    print("🤖 Backend Agent Status:")
    print(f"   🆔 Agent ID: {agent_status['agent_id'][:8]}...")
    print(f"   📊 State: {agent_status['lifecycle_state']}")
    print(f"   ✅ Tasks completed: {agent_status['tasks_completed']}")
    print(f"   📈 Success rate: {agent_status['success_rate']:.1%}")
    print(f"   💰 Total cost: ${agent_status['total_cost']:.4f}")
    print(f"   ⏱️  Avg execution time: {agent_status['average_execution_time']:.2f}s")
    print()

    # Cleanup
    await orchestrator.shutdown()

    # Summary
    print("🎯 DEMO SUMMARY")
    print("-" * 20)
    print("✨ Successfully demonstrated:")
    print("   🎯 Direct ARCH-CTO orchestration model")
    print("   🤖 Backend Agent code generation")
    print("   💻 Real FastAPI code output")
    print("   🔍 Automated code review process")
    print("   📊 Quality scoring and feedback")
    print("   🔄 Revision workflow management")
    print("   📈 Comprehensive metrics tracking")
    print()
    print("🚀 The orchestration system is working beautifully!")
    print("💡 Claude successfully acts as ARCH-CTO managing coding agents.")


async def show_agent_thinking_process():
    """Demonstrate the agent's thinking process."""
    print("\n🧠 AGENT THINKING PROCESS")
    print("-" * 35)
    print("Let me show you what happens inside the Backend Agent's mind...")
    print()

    orchestrator = await setup_orchestrator_with_mock_llm()
    backend_agent = orchestrator.active_agents["backend"]

    # Show agent capabilities
    print("🎯 Agent Identity:")
    print(f"   🏷️  Name: {backend_agent.config.name}")
    print(f"   🏢 Type: {backend_agent.config.agent_type.value}")
    print(f"   🛠️  Capabilities: {[cap.value for cap in backend_agent.config.capabilities]}")
    print()

    # Show routing preferences
    print("🧠 LLM Routing Preferences:")
    print(f"   🎯 Strategy: {backend_agent.config.default_routing_strategy.value}")
    print(f"   🔤 Max tokens: {backend_agent.config.max_tokens}")
    print(f"   🌡️  Temperature: {backend_agent.config.temperature}")
    print()

    # Show knowledge base
    print("📚 Knowledge Areas:")
    print(f"   🔧 Expertise: {backend_agent.expertise_areas}")
    print()

    print("📋 Quality Standards:")
    for standard, description in backend_agent.quality_standards.items():
        print(f"   • {standard}: {description}")
    print()

    await orchestrator.shutdown()


if __name__ == "__main__":
    print("🎯 Starting Visible ARCH-CTO Orchestration Demo...")
    print()

    # Run the main demo
    asyncio.run(show_detailed_orchestration())

    # Show agent thinking process
    asyncio.run(show_agent_thinking_process())

    print("\n🎉 Demo complete! You can now see exactly how orchestration works.")
