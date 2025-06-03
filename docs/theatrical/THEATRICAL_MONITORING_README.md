# 🎭 Theatrical Agent Monitoring System

This system provides rich, real-time visualization of multi-agent orchestration with deliberate delays so humans can observe and understand the collaborative AI process.

## 🌟 Key Features

### 1. **Theatrical Orchestrator** (`theatrical_orchestrator.py`)
- **Slowed-down execution** with configurable delays (default 2-3 seconds)
- **Color-coded terminal output** for different event types
- **Step-by-step progress tracking** through 5 development phases
- **Rich event logging** with timestamps and agent roles
- **Performance metrics** including cost, time, and token usage

### 2. **Real-time Dashboard** (`theatrical_monitoring_dashboard.py`)
- **Live agent status panels** showing current activity
- **Real-time event log** with color coding
- **Performance metrics sidebar** with cost/time tracking
- **Interactive controls** for start/pause/reset
- **Tabbed interface** for different views (Agents, Events, Performance)

### 3. **Demo Launcher** (`launch_theatrical_demo.py`)
- **Multiple viewing modes**: Console, Dashboard, or Side-by-Side
- **Customizable settings** for timing and verbosity
- **Quick demo mode** for 30-second overview
- **Easy-to-use menu interface**

## 🚀 Quick Start

### Run the Demo
```bash
# Make executable (first time only)
chmod +x launch_theatrical_demo.py

# Launch interactive demo
python3 launch_theatrical_demo.py
```

### Demo Modes

1. **🖥️ Console Mode**
   - Colored terminal output
   - Step-by-step agent interactions
   - Perfect for following the logic flow

2. **📊 Dashboard Mode** 
   - Rich TUI interface with live updates
   - Agent status panels and progress bars
   - Real-time event logging and metrics

3. **🔄 Side-by-Side Mode**
   - Console output + Dashboard simultaneously
   - Best of both experiences

4. **❓ Quick Demo**
   - 30-second overview with fast timing
   - Great for presentations

## 🎯 What You'll See

### Agent Collaboration Phases
1. **🏛️ Phase 1: Architecture** - CTO designs system
2. **⚙️ Phase 2: Backend** - Backend dev implements API
3. **🎨 Phase 3: Frontend** - Frontend dev creates UI
4. **🧪 Phase 4: Testing** - QA engineer writes tests
5. **🚀 Phase 5: Deployment** - DevOps sets up infrastructure

### Event Types
- **🤔 THINKING** - Agent analyzing requirements
- **💻 TASK** - Agent executing work
- **✅ SUCCESS** - Task completed successfully
- **❌ ERROR** - Task failed
- **📊 METRICS** - Performance statistics
- **🎉 SUMMARY** - Phase or project completion

### Real-time Metrics
- **💰 Cost**: Total LLM API costs
- **⏱️ Time**: Execution time per phase and total
- **🔤 Tokens**: Token usage across all agents
- **📋 Progress**: Phases completed

## 🎛️ Configuration

### Timing Control
```python
# Fast demo (0.5s delays)
orchestrator = TheatricalOrchestrator(theatrical_delay=0.5)

# Normal demo (2s delays) 
orchestrator = TheatricalOrchestrator(theatrical_delay=2.0)

# Slow demo (5s delays)
orchestrator = TheatricalOrchestrator(theatrical_delay=5.0)
```

### Verbosity Control
```python
# Detailed output with metrics
orchestrator = TheatricalOrchestrator(show_details=True)

# Minimal output
orchestrator = TheatricalOrchestrator(show_details=False)
```

## 🔧 Technical Details

### Dependencies
```bash
# Core requirements
pip install textual  # For dashboard UI
pip install asyncio  # For async orchestration

# Already included in project
- agents/specialists/*  # All specialist agents
- core/routing/*       # LLM routing system
```

### Architecture
- **Event-driven design** with TheatricalEvent objects
- **Async/await pattern** for non-blocking delays
- **Reactive UI updates** with Textual framework
- **Color-coded output** using ANSI escape sequences

### Agent Integration
- Works with all existing specialist agents
- Uses real LLM providers (Claude, OpenAI)
- Tracks actual costs and token usage
- Maintains production-quality code generation

## 🎪 Example Output

```
🎭 Theatrical Agent Orchestration Demo
=====================================

[14:32:15] 🎭 Orchestrator: 🎬 Starting Project: E-commerce Platform
[14:32:18] 🏛️ CTO: 🤔 Analyzing project requirements...
[14:32:21] 🏛️ CTO: 📋 Creating technical specification...
[14:32:35] 🏛️ CTO: ✅ Architecture specification completed!
[14:32:35] 🏛️ CTO: 📄 Cost: $0.0234 | Time: 12.4s

[14:32:38] ⚙️ Backend Dev: 🤔 Reviewing architecture specifications...
[14:32:41] ⚙️ Backend Dev: 💻 Implementing backend API...
[14:32:56] ⚙️ Backend Dev: ✅ Backend API implementation completed!
[14:32:56] ⚙️ Backend Dev: 📊 Generated 847 lines of backend code
```

## 🎯 Use Cases

### 1. **Understanding Multi-Agent AI**
- See how agents hand off work between phases
- Understand the decision-making process
- Observe real LLM interactions

### 2. **Demonstrations & Presentations**
- Show stakeholders how AI collaboration works
- Demonstrate the value of multi-agent systems
- Explain complex AI orchestration simply

### 3. **Development & Debugging**
- Monitor agent performance in real-time
- Identify bottlenecks and failures
- Track costs and resource usage

### 4. **Education & Training**
- Teach multi-agent AI concepts
- Show practical implementation
- Demonstrate best practices

## 🚦 Status Indicators

### Agent Status
- **⚪ Idle** - Waiting for tasks
- **🤔 Thinking** - Analyzing requirements  
- **⚙️ Working** - Executing tasks
- **✅ Success** - Task completed
- **❌ Error** - Task failed

### System Status
- **🟢 Active** - System running normally
- **🟡 Busy** - High activity
- **🔴 Error** - System error occurred

## 📋 Next Steps

1. **Run the demo** to see multi-agent collaboration
2. **Try different modes** (console, dashboard, side-by-side)
3. **Experiment with timing** to find your preferred pace
4. **Customize projects** to see different agent behaviors
5. **Use for presentations** to show AI capabilities

The theatrical monitoring system makes multi-agent AI collaboration visible, understandable, and engaging for human observers! 🎭✨