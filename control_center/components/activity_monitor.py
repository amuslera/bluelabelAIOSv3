"""
Activity Monitor Panel - Real-time activity feed from the monitoring server
"""

import asyncio
import json
import time
from collections import deque
from datetime import datetime
from typing import Optional, Deque

import aiohttp
import websockets
from textual.app import ComposeResult
from textual.containers import Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, Label, RichLog


class Activity:
    """Container for activity information."""
    def __init__(self, event_type: str, agent_id: str, timestamp: float, data: dict):
        self.event_type = event_type
        self.agent_id = agent_id
        self.timestamp = timestamp
        self.data = data
        
    def format(self) -> str:
        """Format activity for display."""
        time_str = datetime.fromtimestamp(self.timestamp).strftime("%H:%M:%S")
        
        # Color based on event type
        color_map = {
            "agent_status_update": "blue",
            "task_assigned": "cyan",
            "task_completed": "green",
            "error_occurred": "red",
            "metric_update": "yellow",
            "connection": "magenta"
        }
        
        color = color_map.get(self.event_type, "white")
        
        # Format message based on event type
        if self.event_type == "agent_status_update":
            status = self.data.get("status", "unknown")
            message = f"{self.agent_id} status → {status}"
        elif self.event_type == "task_assigned":
            task_id = self.data.get("task_id", "unknown")
            message = f"{self.agent_id} assigned {task_id}"
        elif self.event_type == "task_completed":
            task_id = self.data.get("task_id", "unknown")
            message = f"{self.agent_id} completed {task_id}"
        elif self.event_type == "error_occurred":
            error = self.data.get("error", "unknown error")
            message = f"{self.agent_id} error: {error}"
        elif self.event_type == "connection":
            status = self.data.get("status", "unknown")
            message = f"{self.agent_id} {status}"
        else:
            message = f"{self.agent_id}: {self.event_type}"
            
        return f"[dim]{time_str}[/dim] [{color}]{message}[/{color}]"


class ActivityMonitorPanel(Widget):
    """Panel showing real-time system activities."""
    
    activities: reactive[Deque[Activity]] = reactive(deque)
    connected: reactive[bool] = reactive(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ws_url = "ws://localhost:8765/ws"
        self.websocket = None
        self.auth_token = None
        self.connection_task = None
        
    def compose(self) -> ComposeResult:
        """Create the panel layout."""
        with Vertical():
            yield Label("📊 Activity Monitor", classes="panel-title")
            
            # Connection status
            self.status_label = Label("⚪ Connecting...", id="connection-status")
            yield self.status_label
            
            # Activity log
            self.activity_log = RichLog(highlight=True, markup=True, 
                                       max_lines=100, classes="activity-log")
            yield self.activity_log
            
    async def on_mount(self) -> None:
        """Initialize when panel mounts."""
        # Get authentication token
        await self.get_auth_token()
        
        # Start WebSocket connection
        self.connection_task = asyncio.create_task(self.maintain_connection())
        
        # Add some demo activities
        self.add_demo_activities()
        
    async def get_auth_token(self):
        """Get authentication token from monitoring server."""
        try:
            async with aiohttp.ClientSession() as session:
                url = "http://localhost:8765/auth/token"
                data = {"agent_id": "control_center", "role": "admin"}
                
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.auth_token = result.get("token")
                        self.app.log.info("Got auth token")
                    else:
                        self.app.log.error(f"Failed to get token: {response.status}")
        except Exception as e:
            self.app.log.error(f"Auth token error: {e}")
            
    async def maintain_connection(self):
        """Maintain WebSocket connection with reconnection logic."""
        retry_delay = 1
        
        while True:
            try:
                await self.connect_to_monitoring()
            except Exception as e:
                self.app.log.error(f"WebSocket error: {e}")
                self.connected = False
                self.update_status("🔴 Disconnected")
                
                # Exponential backoff
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 30)
                
    async def connect_to_monitoring(self):
        """Connect to monitoring server via WebSocket."""
        if not self.auth_token:
            self.update_status("🔴 No auth token")
            return
            
        self.update_status("🟡 Connecting...")
        
        async with websockets.connect(self.ws_url) as websocket:
            self.websocket = websocket
            
            # Authenticate
            await websocket.send(json.dumps({
                "type": "authenticate",
                "token": self.auth_token
            }))
            
            # Wait for auth response
            auth_response = await websocket.recv()
            auth_data = json.loads(auth_response)
            
            if auth_data.get("status") == "success":
                self.connected = True
                self.update_status("🟢 Connected")
                self.app.log.info("WebSocket connected")
                
                # Listen for messages
                async for message in websocket:
                    await self.handle_message(json.loads(message))
            else:
                self.update_status("🔴 Auth failed")
                raise Exception("Authentication failed")
                
    async def handle_message(self, data: dict):
        """Handle incoming WebSocket message."""
        event_type = data.get("event_type", data.get("type"))
        
        if event_type and event_type != "heartbeat":
            activity = Activity(
                event_type=event_type,
                agent_id=data.get("agent_id", "unknown"),
                timestamp=data.get("timestamp", time.time()),
                data=data.get("data", {})
            )
            
            self.add_activity(activity)
            
    def add_activity(self, activity: Activity):
        """Add activity to the log."""
        # Add to deque (limited to 100 items)
        if len(self.activities) >= 100:
            self.activities.popleft()
        self.activities.append(activity)
        
        # Add to visual log
        self.activity_log.write(activity.format())
        
    def add_demo_activities(self):
        """Add demonstration activities."""
        demo_activities = [
            Activity("connection", "control_center", time.time() - 30, 
                    {"status": "connected"}),
            Activity("agent_status_update", "marcus-001", time.time() - 25,
                    {"status": "active"}),
            Activity("task_assigned", "marcus-001", time.time() - 20,
                    {"task_id": "MON-001"}),
            Activity("agent_status_update", "alex-001", time.time() - 15,
                    {"status": "busy"}),
            Activity("task_assigned", "alex-001", time.time() - 10,
                    {"task_id": "CC-002"}),
            Activity("metric_update", "metrics_collector", time.time() - 5,
                    {"cpu_usage": 45.2, "memory_mb": 512}),
        ]
        
        for activity in demo_activities:
            self.add_activity(activity)
            
    def update_status(self, status: str):
        """Update connection status display."""
        self.status_label.update(status)
        
    def refresh(self):
        """Public refresh method."""
        # Clear and reload activities
        self.activity_log.clear()
        for activity in self.activities:
            self.activity_log.write(activity.format())
            
    async def on_unmount(self):
        """Cleanup when panel unmounts."""
        if self.connection_task:
            self.connection_task.cancel()
            
        if self.websocket:
            await self.websocket.close()