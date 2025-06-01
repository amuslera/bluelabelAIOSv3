# AIOSv3 Control Center

A unified terminal user interface for managing and monitoring the multi-agent AI system.

## Features

### 🎭 Agent Orchestra
- Real-time view of all active agents
- Status indicators (active, busy, error, offline)
- Current task progress tracking
- Launch and stop agent controls

### 📊 Activity Monitor
- Live WebSocket feed from monitoring server
- Color-coded activity types
- Automatic reconnection with backoff
- JWT authentication

### 📋 Task Manager
- Sprint task tracking
- Task assignment to agents
- Status updates (pending, in-progress, completed, blocked)
- Load tasks from sprint files

### 🔍 PR Review
- Review agent-generated pull requests
- View diffs in modal dialog
- Approve or request changes
- Automatic PR detection

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install textual aiohttp websockets redis
```

## Usage

### Basic Usage

```bash
# Run from control_center directory
python run_control_center.py

# Or run from project root
python control_center/run_control_center.py
```

### With Custom Configuration

```bash
# Set custom monitoring server URL
export MONITORING_URL=ws://localhost:8765

# Set custom Redis URL
export REDIS_URL=redis://localhost:6379

python run_control_center.py
```

## Keyboard Shortcuts

- **q**: Quit the application
- **r**: Refresh all panels
- **t**: Toggle theme (dark/light)
- **h**: Show help
- **Tab**: Navigate between panels
- **Enter**: Select/activate item
- **Ctrl+S**: Take screenshot

## Panel Navigation

Use **Tab** to move between panels. Each panel has its own controls:

### Agent Orchestra
- Select agent with arrow keys
- Press Enter to view details
- Use buttons to launch/stop agents

### Activity Monitor
- Automatically scrolls with new activities
- Shows connection status at top
- Reconnects automatically if disconnected

### Task Manager
- Select task with arrow keys
- "Assign Task" opens assignment dialog
- "Update Status" cycles through statuses
- "Load Sprint" reloads from file

### PR Review
- "View Diff" shows git diff in modal
- "Approve" merges the PR
- "Request Changes" creates feedback
- "Scan for PRs" looks for new PRs

## Architecture

```
control_center/
├── main.py              # Main application
├── styles.css           # Textual CSS styling
├── components/
│   ├── agent_orchestra.py   # Agent management panel
│   ├── activity_monitor.py  # Real-time activity feed
│   ├── task_manager.py      # Task assignment panel
│   └── pr_review.py         # PR review panel
└── run_control_center.py    # Entry point script
```

## Integration

The Control Center integrates with:

1. **Monitoring Server** (WebSocket)
   - Receives real-time events
   - JWT authentication required
   - Auto-reconnection on failure

2. **Redis** (Agent Registry)
   - Gets agent information
   - Stores task assignments
   - Tracks agent health

3. **Git** (PR Management)
   - Reads PR info files
   - Executes merge commands
   - Shows diffs

## Customization

### Styling

Edit `styles.css` to customize appearance. The app uses Textual CSS with support for:
- Colors and backgrounds
- Borders and padding
- Grid layouts
- Custom classes

### Adding Panels

To add a new panel:

1. Create component in `components/`
2. Import in `main.py`
3. Add to grid layout
4. Update styles.css

## Troubleshooting

### Connection Issues

If panels show disconnected:
1. Check monitoring server is running
2. Verify Redis is accessible
3. Check URLs in environment variables

### Display Issues

If layout appears broken:
1. Ensure terminal is at least 80x24
2. Try toggling theme with 't'
3. Resize terminal window

### Performance

For better performance:
1. Limit activity log to recent items
2. Reduce refresh frequency
3. Close unused panels

## Development

### Running Tests

```bash
# From project root
pytest control_center/tests/
```

### Adding Features

1. Follow existing component patterns
2. Use reactive attributes for state
3. Handle errors gracefully
4. Add keyboard shortcuts sparingly

## Screenshots

Take screenshots with **Ctrl+S**. Files are saved as `control_center_<timestamp>.svg`.