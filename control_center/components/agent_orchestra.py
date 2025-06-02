"""
Agent Orchestra Panel - Shows all active agents and their status
"""

import asyncio
import time
from typing import Optional

import redis.asyncio as redis
from redis.exceptions import RedisError
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import Button, DataTable, Label


class AgentInfo:
    """Container for agent information."""
    def __init__(self, agent_id: str, name: str, role: str, status: str = "idle",
                 progress: int = 0, current_task: str = "None"):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.status = status
        self.progress = progress
        self.current_task = current_task
        self.last_seen = time.time()

    def get_status_icon(self) -> str:
        """Get status icon based on current status."""
        icons = {
            "active": "🟢",
            "busy": "🟡",
            "error": "🔴",
            "idle": "⚪",
            "offline": "⚫"
        }
        return icons.get(self.status, "❓")


class AgentOrchestraPanel(Widget):
    """Panel showing all agents and their current status."""

    agents: reactive[dict[str, AgentInfo]] = reactive({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_client: Optional[redis.Redis] = None
        self.refresh_timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        """Create the panel layout."""
        with Vertical():
            yield Label("🎭 Agent Orchestra", classes="panel-title")

            # Agent table
            table = DataTable(classes="agent-table")
            table.add_columns("Status", "Agent", "Role", "Task", "Progress")
            table.cursor_type = "row"
            yield table

            # Control buttons
            with Horizontal():
                yield Button("Launch Agent", id="launch-agent", classes="primary-button")
                yield Button("Stop All", id="stop-all", classes="danger-button")

    def on_mount(self) -> None:
        """Initialize when panel mounts."""
        # Connect to Redis
        asyncio.create_task(self.connect_redis())

        # Load initial agent data
        asyncio.create_task(self.load_agents())

        # Start auto-refresh
        self.refresh_timer = self.set_interval(5, self.refresh_agents)

        # Add some demo agents if none exist
        if not self.agents:
            asyncio.create_task(self.add_demo_agents())

    async def connect_redis(self):
        """Connect to Redis for agent registry."""
        try:
            self.redis_client = await redis.from_url(
                "redis://localhost:6379",
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
        except Exception as e:
            self.app.log.error(f"Redis connection failed: {e}")
            self.redis_client = None

    async def load_agents(self):
        """Load agent information from Redis."""
        if not self.redis_client:
            return

        try:
            # Get all registered agents
            agent_keys = await self.redis_client.keys("agent:*:info")

            new_agents = {}
            for key in agent_keys:
                agent_data = await self.redis_client.hgetall(key)
                if agent_data:
                    agent_id = key.split(":")[1]
                    agent = AgentInfo(
                        agent_id=agent_id,
                        name=agent_data.get("name", f"Agent {agent_id}"),
                        role=agent_data.get("role", "unknown"),
                        status=agent_data.get("status", "idle"),
                        progress=int(agent_data.get("progress", 0)),
                        current_task=agent_data.get("current_task", "None")
                    )
                    new_agents[agent_id] = agent

            self.agents = new_agents
            self.update_table()

        except RedisError as e:
            self.app.log.error(f"Failed to load agents: {e}")

    async def add_demo_agents(self):
        """Add demonstration agents."""
        demo_agents = [
            AgentInfo("marcus-001", "Marcus Chen", "backend-dev", "active", 75, "MON-001: Monitoring Server"),
            AgentInfo("alex-001", "Alex Rivera", "frontend-dev", "busy", 30, "CC-002: Agent Orchestra"),
            AgentInfo("sam-001", "Sam Martinez", "qa-engineer", "idle", 0, "None"),
            AgentInfo("jordan-001", "Jordan Kim", "devops", "active", 90, "Setting up CI/CD")
        ]

        for agent in demo_agents:
            self.agents[agent.agent_id] = agent

            # Store in Redis if available
            if self.redis_client:
                try:
                    key = f"agent:{agent.agent_id}:info"
                    await self.redis_client.hset(key, mapping={
                        "name": agent.name,
                        "role": agent.role,
                        "status": agent.status,
                        "progress": str(agent.progress),
                        "current_task": agent.current_task
                    })
                    await self.redis_client.expire(key, 3600)  # 1 hour
                except:
                    pass

        self.update_table()

    def update_table(self):
        """Update the data table with current agent information."""
        table = self.query_one(DataTable)
        table.clear()

        for agent in self.agents.values():
            # Check if agent is stale (not seen in 30 seconds)
            if time.time() - agent.last_seen > 30:
                agent.status = "offline"


            table.add_row(
                agent.get_status_icon(),
                agent.name,
                agent.role,
                agent.current_task[:40] + "..." if len(agent.current_task) > 40 else agent.current_task,
                f"{agent.progress}%"
            )

    async def refresh_agents(self):
        """Refresh agent information."""
        await self.load_agents()

    def refresh(self):
        """Public refresh method."""
        asyncio.create_task(self.refresh_agents())

    @on(Button.Pressed, "#launch-agent")
    def handle_launch_agent(self):
        """Handle launch agent button."""
        # In production, this would open agent configuration dialog
        self.app.notify("Agent launch dialog would open here", severity="information")

    @on(Button.Pressed, "#stop-all")
    def handle_stop_all(self):
        """Handle stop all agents button."""
        self.app.notify("Stopping all agents...", severity="warning")

        # Update all agents to idle
        for agent in self.agents.values():
            agent.status = "idle"
            agent.progress = 0
            agent.current_task = "None"

        self.update_table()

    @on(DataTable.RowSelected)
    def handle_row_selected(self, event: DataTable.RowSelected):
        """Handle agent selection."""
        if event.row_index < len(self.agents):
            agent = list(self.agents.values())[event.row_index]
            self.app.notify(
                f"Selected: {agent.name} ({agent.role})\n"
                f"Status: {agent.status}\n"
                f"Task: {agent.current_task}",
                title="Agent Details"
            )
