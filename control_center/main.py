#!/usr/bin/env python3
"""
AIOSv3 Control Center Main Application

The central command interface for managing the multi-agent AI system.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Header, Footer, Button
from textual.screen import Screen
from textual.reactive import reactive

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from control_center.components.agent_orchestra import AgentOrchestraPanel
from control_center.components.activity_monitor import ActivityMonitorPanel
from control_center.components.task_manager import TaskManagerPanel
from control_center.components.pr_review import PRReviewPanel


class MainScreen(Screen):
    """Main screen with 4-panel layout."""
    
    def compose(self) -> ComposeResult:
        """Create the main layout."""
        yield Header()
        
        # Main grid with 4 panels
        with Grid(classes="main-grid"):
            yield AgentOrchestraPanel(classes="panel")
            yield ActivityMonitorPanel(classes="panel")
            yield TaskManagerPanel(classes="panel")
            yield PRReviewPanel(classes="panel")
            
        yield Footer()


class ControlCenterApp(App):
    """AIOSv3 Control Center Application."""
    
    CSS_PATH = "styles.css"
    TITLE = "AIOSv3 Control Center"
    SUB_TITLE = "Multi-Agent AI System Management"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("r", "refresh", "Refresh"),
        Binding("t", "toggle_theme", "Theme"),
        Binding("h", "show_help", "Help"),
        Binding("ctrl+s", "screenshot", "Screenshot"),
    ]
    
    # Connection status
    monitoring_connected = reactive(False)
    redis_connected = reactive(False)
    
    def __init__(self):
        super().__init__()
        self.monitoring_url = os.getenv("MONITORING_URL", "ws://localhost:8765")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
    def on_mount(self) -> None:
        """Initialize when app mounts."""
        self.push_screen(MainScreen())
        
        # Start background connection tasks
        self.check_connections_task = asyncio.create_task(self.check_connections())
        
    def compose(self) -> ComposeResult:
        """Create the app layout."""
        # The main screen handles the layout
        yield from []
        
    async def check_connections(self):
        """Periodically check service connections."""
        while True:
            try:
                # Check monitoring server
                # In production, actually test the connection
                self.monitoring_connected = await self._test_monitoring_connection()
                
                # Check Redis
                self.redis_connected = await self._test_redis_connection()
                
                # Update footer status
                self.update_footer()
                
            except Exception as e:
                self.log.error(f"Connection check error: {e}")
                
            await asyncio.sleep(5)  # Check every 5 seconds
            
    async def _test_monitoring_connection(self) -> bool:
        """Test monitoring server connection."""
        # Simplified for now - in production, actually test WebSocket
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                url = self.monitoring_url.replace("ws://", "http://") + "/health"
                async with session.get(url, timeout=2) as response:
                    return response.status == 200
        except:
            return False
            
    async def _test_redis_connection(self) -> bool:
        """Test Redis connection."""
        # Simplified for now - in production, use redis client
        try:
            import redis.asyncio as redis
            client = await redis.from_url(self.redis_url)
            await client.ping()
            await client.close()
            return True
        except:
            return False
            
    def update_footer(self):
        """Update footer with connection status."""
        status_parts = []
        
        if self.monitoring_connected:
            status_parts.append("[green]Monitor: Connected[/green]")
        else:
            status_parts.append("[red]Monitor: Disconnected[/red]")
            
        if self.redis_connected:
            status_parts.append("[green]Redis: Connected[/green]")
        else:
            status_parts.append("[red]Redis: Disconnected[/red]")
            
        status = " | ".join(status_parts)
        self.sub_title = status
        
    def action_refresh(self) -> None:
        """Refresh all panels."""
        # Send refresh event to all panels
        for panel in self.query(".panel"):
            panel.refresh()
        self.notify("Refreshed all panels", severity="information")
        
    def action_toggle_theme(self) -> None:
        """Toggle between light and dark themes."""
        self.dark = not self.dark
        theme = "dark" if self.dark else "light"
        self.notify(f"Switched to {theme} theme", severity="information")
        
    def action_show_help(self) -> None:
        """Show help screen."""
        help_text = """
# AIOSv3 Control Center Help

## Keyboard Shortcuts:
- **q**: Quit the application
- **r**: Refresh all panels
- **t**: Toggle theme (dark/light)
- **h**: Show this help
- **Tab**: Navigate between panels
- **Enter**: Activate selected item
- **Escape**: Cancel current operation

## Panel Overview:

### Agent Orchestra (Top Left)
Shows all active agents with their status and current tasks.
- Green: Agent is active and healthy
- Yellow: Agent is busy processing
- Red: Agent has encountered an error

### Activity Monitor (Top Right)
Real-time feed of all system activities.
Color coding indicates activity type.

### Task Manager (Bottom Left)
Current sprint tasks and their assignment status.
Use this to assign tasks to agents.

### PR Review (Bottom Right)
Review and manage pull requests from agents.
Approve or request changes directly from here.

## Tips:
- Check connection status in the footer
- Use refresh (r) if data seems stale
- Monitor agent health regularly
        """
        self.notify(help_text, title="Help", severity="information")
        
    def action_screenshot(self) -> None:
        """Take a screenshot."""
        filename = f"control_center_{int(asyncio.get_event_loop().time())}.svg"
        self.save_screenshot(filename)
        self.notify(f"Screenshot saved: {filename}", severity="success")


async def run_async():
    """Run the app with async support."""
    app = ControlCenterApp()
    await app.run_async()


def main():
    """Main entry point."""
    # Check for required dependencies
    try:
        import textual
        import aiohttp
        import websockets
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install textual aiohttp websockets")
        sys.exit(1)
        
    # Run the app
    if sys.platform == "win32":
        # Windows event loop policy
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
    app = ControlCenterApp()
    app.run()


if __name__ == "__main__":
    main()