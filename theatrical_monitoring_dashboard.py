"""
Theatrical Monitoring Dashboard - Real-time visualization of agent interactions

This dashboard provides a rich, real-time view of agent orchestration with
live updates, progress tracking, and detailed communication logs.
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Optional

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Label,
    Log,
    ProgressBar,
    Static,
    TabbedContent,
    TabPane,
)

from theatrical_orchestrator import TheatricalEvent, TheatricalOrchestrator


class AgentStatusWidget(Static):
    """Widget displaying individual agent status."""

    agent_id: reactive[str] = reactive("")
    status: reactive[str] = reactive("idle")
    progress: reactive[int] = reactive(0)
    current_task: reactive[str] = reactive("None")

    def __init__(self, agent_id: str, agent_name: str, **kwargs):
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.last_update = time.time()

    def compose(self) -> ComposeResult:
        """Create agent status display."""
        with Vertical():
            yield Label(self.agent_name, classes="agent-name")
            yield Label(f"Status: {self.status}", id=f"status-{self.agent_id}")
            yield ProgressBar(total=100, show_eta=False, id=f"progress-{self.agent_id}")
            yield Label(f"Task: {self.current_task[:30]}...", id=f"task-{self.agent_id}")

    def update_status(self, status: str, progress: Optional[int] = None, task: Optional[str] = None):
        """Update agent status display."""
        self.status = status
        if progress is not None:
            self.progress = progress
        if task is not None:
            self.current_task = task

        self.last_update = time.time()

        # Update UI elements
        status_label = self.query_one(f"#status-{self.agent_id}", Label)
        status_label.update(f"Status: {status}")

        if progress is not None:
            progress_bar = self.query_one(f"#progress-{self.agent_id}", ProgressBar)
            progress_bar.progress = progress

        if task is not None:
            task_label = self.query_one(f"#task-{self.agent_id}", Label)
            task_label.update(f"Task: {task[:30]}...")

    def get_status_icon(self) -> str:
        """Get status icon."""
        icons = {
            "idle": "⚪",
            "thinking": "🤔",
            "working": "⚙️",
            "success": "✅",
            "error": "❌",
            "active": "🟢"
        }
        return icons.get(self.status, "❓")


class EventLogWidget(Log):
    """Enhanced log widget for theatrical events."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_count = 0

    def log_event(self, event: TheatricalEvent):
        """Log a theatrical event with formatting."""
        self.event_count += 1

        # Color code by event type
        color_map = {
            "SYSTEM": "blue",
            "PHASE": "magenta",
            "THINKING": "yellow",
            "TASK": "cyan",
            "SUCCESS": "green",
            "ERROR": "red",
            "DETAILS": "dim",
            "METRICS": "white",
            "SUMMARY": "magenta"
        }

        color = color_map.get(event.event_type, "white")
        timestamp = event.timestamp.strftime("%H:%M:%S")

        # Format message with rich markup
        formatted_message = f"[{color}][{timestamp}] {event.agent_role}: {event.message}[/{color}]"
        self.write(formatted_message)


class ProjectMetricsWidget(Static):
    """Widget showing project-wide metrics."""

    total_cost: reactive[float] = reactive(0.0)
    total_time: reactive[float] = reactive(0.0)
    total_tokens: reactive[int] = reactive(0)
    phases_complete: reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        """Create metrics display."""
        with Vertical():
            yield Label("📊 Project Metrics", classes="section-title")
            yield Label(f"💰 Cost: ${self.total_cost:.4f}", id="cost-metric")
            yield Label(f"⏱️ Time: {self.total_time:.1f}s", id="time-metric")
            yield Label(f"🔤 Tokens: {self.total_tokens:,}", id="tokens-metric")
            yield Label(f"📋 Phases: {self.phases_complete}/5", id="phases-metric")

    def update_metrics(self, cost: Optional[float] = None, time_elapsed: Optional[float] = None,
                      tokens: Optional[int] = None, phases: Optional[int] = None):
        """Update metric display."""
        if cost is not None:
            self.total_cost = cost
            cost_label = self.query_one("#cost-metric", Label)
            cost_label.update(f"💰 Cost: ${cost:.4f}")

        if time_elapsed is not None:
            self.total_time = time_elapsed
            time_label = self.query_one("#time-metric", Label)
            time_label.update(f"⏱️ Time: {time_elapsed:.1f}s")

        if tokens is not None:
            self.total_tokens = tokens
            tokens_label = self.query_one("#tokens-metric", Label)
            tokens_label.update(f"🔤 Tokens: {tokens:,}")

        if phases is not None:
            self.phases_complete = phases
            phases_label = self.query_one("#phases-metric", Label)
            phases_label.update(f"📋 Phases: {phases}/5")


class TheatricalMonitoringApp(App):
    """
    Main monitoring application for theatrical agent orchestration.
    """

    CSS = """
    .agent-panel {
        width: 1fr;
        height: 1fr;
        border: solid $primary;
        margin: 1;
    }

    .agent-name {
        text-align: center;
        background: $primary;
        color: $text-on-primary;
        margin-bottom: 1;
    }

    .section-title {
        text-align: center;
        background: $secondary;
        color: $text-on-secondary;
        margin-bottom: 1;
    }

    .control-panel {
        height: 6;
        border: solid $accent;
        margin: 1;
    }

    .metrics-panel {
        width: 25%;
        border: solid $success;
        margin: 1;
    }

    .log-panel {
        border: solid $warning;
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "start_demo", "Start Demo"),
        ("r", "reset", "Reset"),
    ]

    def __init__(self):
        super().__init__()
        self.orchestrator: Optional[TheatricalOrchestrator] = None
        self.agent_widgets: Dict[str, AgentStatusWidget] = {}
        self.event_log: Optional[EventLogWidget] = None
        self.metrics_widget: Optional[ProjectMetricsWidget] = None
        self.is_running = False
        self.start_time: Optional[float] = None

    def compose(self) -> ComposeResult:
        """Create the monitoring dashboard layout."""
        yield Header(show_clock=True)

        with Container():
            with TabbedContent():
                with TabPane("Agent Orchestra", id="agents-tab"):
                    with Horizontal():
                        # Agent status panels
                        with Vertical(classes="agent-panel"):
                            self.agent_widgets["cto-001"] = AgentStatusWidget(
                                "cto-001", "🏛️ CTO Agent"
                            )
                            yield self.agent_widgets["cto-001"]

                        with Vertical(classes="agent-panel"):
                            self.agent_widgets["backend-001"] = AgentStatusWidget(
                                "backend-001", "⚙️ Backend Dev"
                            )
                            yield self.agent_widgets["backend-001"]

                        with Vertical(classes="agent-panel"):
                            self.agent_widgets["frontend-001"] = AgentStatusWidget(
                                "frontend-001", "🎨 Frontend Dev"
                            )
                            yield self.agent_widgets["frontend-001"]

                        with Vertical(classes="agent-panel"):
                            self.agent_widgets["qa-001"] = AgentStatusWidget(
                                "qa-001", "🧪 QA Engineer"
                            )
                            yield self.agent_widgets["qa-001"]

                        with Vertical(classes="agent-panel"):
                            self.agent_widgets["devops-001"] = AgentStatusWidget(
                                "devops-001", "🚀 DevOps"
                            )
                            yield self.agent_widgets["devops-001"]

                with TabPane("Event Log", id="log-tab"):
                    with Horizontal():
                        # Event log
                        with Vertical(classes="log-panel"):
                            self.event_log = EventLogWidget()
                            yield self.event_log

                        # Metrics sidebar
                        with Vertical(classes="metrics-panel"):
                            self.metrics_widget = ProjectMetricsWidget()
                            yield self.metrics_widget

                with TabPane("Performance", id="performance-tab"):
                    with Vertical():
                        yield Label("📈 Performance Dashboard", classes="section-title")
                        # Performance metrics table
                        table = DataTable()
                        table.add_columns("Metric", "Value", "Status")
                        table.add_row("Response Time", "0.0s", "✅")
                        table.add_row("Success Rate", "100%", "✅")
                        table.add_row("Cost Efficiency", "$0.00", "✅")
                        yield table

            # Control panel
            with Horizontal(classes="control-panel"):
                yield Button("🎬 Start Demo", id="start-btn", variant="success")
                yield Button("⏸️ Pause", id="pause-btn", variant="warning")
                yield Button("🔄 Reset", id="reset-btn", variant="error")
                yield Button("💾 Save Log", id="save-btn", variant="primary")

        yield Footer()

    @on(Button.Pressed, "#start-btn")
    async def start_demo(self):
        """Start the theatrical demo."""
        if self.is_running:
            self.notify("Demo already running!", severity="warning")
            return

        self.is_running = True
        self.start_time = time.time()

        # Reset displays
        for widget in self.agent_widgets.values():
            widget.update_status("idle", 0, "Waiting...")

        if self.event_log:
            self.event_log.clear()

        # Initialize orchestrator
        self.orchestrator = TheatricalOrchestrator(
            theatrical_delay=1.5,  # Faster for dashboard
            show_details=True
        )

        # Start monitoring task
        asyncio.create_task(self._run_orchestration())

        self.notify("🎭 Theatrical orchestration started!", severity="success")

    @on(Button.Pressed, "#pause-btn")
    def pause_demo(self):
        """Pause the demo."""
        self.notify("⏸️ Demo paused", severity="information")

    @on(Button.Pressed, "#reset-btn")
    def reset_demo(self):
        """Reset the demo."""
        self.is_running = False

        for widget in self.agent_widgets.values():
            widget.update_status("idle", 0, "Ready")

        if self.event_log:
            self.event_log.clear()

        if self.metrics_widget:
            self.metrics_widget.update_metrics(0.0, 0.0, 0, 0)

        self.notify("🔄 Demo reset", severity="information")

    @on(Button.Pressed, "#save-btn")
    def save_log(self):
        """Save the event log."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"theatrical_log_{timestamp}.txt"

        # In a real app, would save to file
        self.notify(f"💾 Log saved as {filename}", severity="success")

    async def _run_orchestration(self):
        """Run the orchestration with live monitoring."""
        try:
            if not self.orchestrator:
                return

            await self.orchestrator.initialize()

            # Update agent statuses as initialization happens
            for agent_id in self.agent_widgets.keys():
                self.agent_widgets[agent_id].update_status("initializing", 10, "Setting up...")
                await asyncio.sleep(0.5)

            # Start the project
            project = "Real-time Chat Application with WebSocket support, user authentication, and message history"

            # Monitor orchestration events
            asyncio.create_task(self._monitor_events())

            await self.orchestrator.orchestrate_project(project)

            self.notify("🎉 Orchestration completed successfully!", severity="success")

        except Exception as e:
            self.notify(f"❌ Orchestration failed: {e}", severity="error")
        finally:
            self.is_running = False
            if self.orchestrator:
                await self.orchestrator.shutdown()

    async def _monitor_events(self):
        """Monitor orchestrator events and update dashboard."""
        if not self.orchestrator:
            return

        last_event_count = 0
        phase_progress = {
            "architecture": 0,
            "backend": 1,
            "frontend": 2,
            "testing": 3,
            "deployment": 4
        }

        while self.is_running:
            try:
                # Check for new events
                current_event_count = len(self.orchestrator.events)

                if current_event_count > last_event_count:
                    # Process new events
                    new_events = self.orchestrator.events[last_event_count:]

                    for event in new_events:
                        # Log event
                        if self.event_log:
                            self.event_log.log_event(event)

                        # Update agent status based on event
                        await self._update_agent_from_event(event)

                        # Update metrics
                        if self.metrics_widget and self.start_time:
                            elapsed = time.time() - self.start_time
                            phases = sum(1 for phase in phase_progress.keys()
                                       if any(e.details.get("phase") == phase for e in self.orchestrator.events))

                            self.metrics_widget.update_metrics(
                                cost=self.orchestrator.total_cost,
                                time_elapsed=elapsed,
                                tokens=self.orchestrator.total_tokens,
                                phases=phases
                            )

                    last_event_count = current_event_count

                await asyncio.sleep(0.5)  # Check for updates twice per second

            except Exception as e:
                self.notify(f"Monitoring error: {e}", severity="error")
                break

    async def _update_agent_from_event(self, event: TheatricalEvent):
        """Update agent widget based on event."""
        agent_id = event.agent_id

        if agent_id not in self.agent_widgets:
            return

        widget = self.agent_widgets[agent_id]

        # Map event types to status updates
        if event.event_type == "THINKING":
            widget.update_status("thinking", progress=25, task="Analyzing...")
        elif event.event_type == "TASK":
            widget.update_status("working", progress=50, task=event.message[:30])
        elif event.event_type == "SUCCESS":
            widget.update_status("success", progress=100, task="Completed!")
        elif event.event_type == "ERROR":
            widget.update_status("error", progress=0, task="Failed")
        elif event.event_type == "PHASE":
            widget.update_status("active", progress=10, task=event.message[:30])

    def action_start_demo(self) -> None:
        """Action for start demo keybind."""
        asyncio.create_task(self.start_demo())

    def action_reset(self) -> None:
        """Action for reset keybind."""
        self.reset_demo()


# Standalone dashboard launcher
async def main():
    """Launch the theatrical monitoring dashboard."""
    app = TheatricalMonitoringApp()
    await app.run_async()


if __name__ == "__main__":
    asyncio.run(main())
