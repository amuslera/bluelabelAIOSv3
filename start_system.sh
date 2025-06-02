#!/bin/bash
# Start the AIOSv3 System

echo "🚀 Starting AIOSv3 System..."
echo "================================"

# Check if Redis is running
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis not running. Starting it..."
    brew services start redis
    sleep 2
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis started successfully"
    else
        echo "❌ Failed to start Redis"
        exit 1
    fi
fi

# Function to open new terminal
open_terminal() {
    local title=$1
    local command=$2
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e "
        tell application \"Terminal\"
            do script \"cd $(pwd) && $command\"
            set custom title of front window to \"$title\"
        end tell"
    else
        # Linux/other - try gnome-terminal
        gnome-terminal --title="$title" -- bash -c "cd $(pwd) && $command; exec bash" &
    fi
}

echo ""
echo "📡 Starting Monitoring Server..."
open_terminal "AIOSv3 Monitoring" "python3 monitoring_system/run_monitoring.py"

# Wait for monitoring server to start
echo "⏳ Waiting for monitoring server to start..."
sleep 3

echo ""
echo "🖥️  Starting Control Center..."
open_terminal "AIOSv3 Control Center" "python3 control_center/run_control_center.py"

echo ""
echo "✨ System is starting!"
echo ""
echo "📋 Quick Test Commands:"
echo ""
echo "Get auth token:"
echo "  curl -X POST http://localhost:8765/auth/token -H 'Content-Type: application/json' -d '{\"agent_id\":\"test_agent\"}'"
echo ""
echo "Check health:"
echo "  curl http://localhost:8765/health"
echo ""
echo "View metrics:"
echo "  curl http://localhost:9090/metrics"
echo ""
echo "Connect via WebSocket (requires token):"
echo "  wscat -c ws://localhost:8765/ws"
echo ""
echo "💡 Tips:"
echo "- Control Center shortcuts: q=quit, r=refresh, t=theme, h=help"
echo "- Both terminals will stay open for monitoring"
echo "- Stop with Ctrl+C in each terminal"
echo ""