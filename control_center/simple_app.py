#!/usr/bin/env python3
"""
Simplified Control Center that works with Textual 3.x
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import DataTable, Footer, Header, RichLog, Static


class SimpleControlCenter(App):
    """Simplified Control Center Application."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 2;
        grid-gutter: 1;
    }
    
    .panel {
        border: solid green;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        """Create the layout."""
        yield Header()

        # Agent Orchestra
        with Vertical(classes="panel"):
            yield Static("🎭 Agent Orchestra", classes="title")
            agent_table = DataTable()
            agent_table.add_columns("Status", "Agent", "Role", "Progress")
            agent_table.add_row("🟢", "Marcus Chen", "Backend", "75%")
            agent_table.add_row("🟡", "Alex Rivera", "Frontend", "45%")
            agent_table.add_row("⚪", "Sam Martinez", "QA", "0%")
            yield agent_table

        # Activity Monitor
        with Vertical(classes="panel"):
            yield Static("📊 Activity Monitor", classes="title")
            log = RichLog(highlight=True, markup=True)
            log.write("[dim]16:45:32[/dim] [green]System started[/green]")
            log.write("[dim]16:45:35[/dim] [blue]Marcus: Working on monitoring[/blue]")
            log.write("[dim]16:45:40[/dim] [yellow]Alex: Building UI[/yellow]")
            yield log

        # Task Manager
        with Vertical(classes="panel"):
            yield Static("📋 Task Manager", classes="title")
            task_table = DataTable()
            task_table.add_columns("ID", "Title", "Status", "Assigned")
            task_table.add_row("MON-001", "Monitoring Server", "✅ Done", "Marcus")
            task_table.add_row("CC-001", "Control Center", "🔵 Active", "Alex")
            task_table.add_row("CC-002", "Agent Panel", "⚪ Pending", "Alex")
            yield task_table

        # PR Review
        with Vertical(classes="panel"):
            yield Static("🔍 PR Review", classes="title")
            yield Static("PR #142: Complete monitoring server")
            yield Static("Author: Marcus Chen")
            yield Static("Branch: feature/monitoring")
            yield Static("Files: 8 changed")
            yield Static("\n[green]✓ Ready to merge[/green]", markup=True)

        yield Footer()

    def action_refresh(self):
        """Refresh action."""
        self.notify("Refreshed!", severity="information")

def main():
    """Run the simplified app."""
    app = SimpleControlCenter()
    app.run()

if __name__ == "__main__":
    main()
