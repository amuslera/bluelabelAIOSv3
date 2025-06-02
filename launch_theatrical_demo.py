#!/usr/bin/env python3
"""
Launch Theatrical Demo - Easy launcher for the theatrical monitoring system

This script provides multiple ways to experience the theatrical agent orchestration:
1. Console-only mode with colored output
2. Dashboard mode with rich TUI interface  
3. Side-by-side mode running both simultaneously
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_banner():
    """Print the demo banner."""
    print("🎭" + "="*80)
    print("    AIOSV3 THEATRICAL AGENT ORCHESTRATION DEMO")
    print("    Real-time Multi-Agent Collaboration Visualization")
    print("="*84)
    print()


def print_menu():
    """Print the demo menu options."""
    print("Select demo mode:")
    print()
    print("1. 🖥️  Console Mode - Colored terminal output with step-by-step progress")
    print("2. 📊 Dashboard Mode - Rich TUI interface with real-time monitoring")
    print("3. 🔄 Side-by-Side - Run both console and dashboard simultaneously")
    print("4. ❓ Quick Demo - Fast 30-second overview")
    print("5. 🔧 Custom Settings - Configure timing and verbosity")
    print("6. ❌ Exit")
    print()


async def run_console_mode():
    """Run console-only theatrical orchestration."""
    from theatrical_orchestrator import demo_theatrical_orchestration
    
    print("🎭 Starting Console Mode...")
    print("   - Colored terminal output")
    print("   - Step-by-step agent interactions") 
    print("   - 2-second theatrical delays")
    print()
    
    await demo_theatrical_orchestration()


async def run_dashboard_mode():
    """Run dashboard TUI interface."""
    from theatrical_monitoring_dashboard import TheatricalMonitoringApp
    
    print("📊 Starting Dashboard Mode...")
    print("   - Rich TUI interface")
    print("   - Real-time agent status")
    print("   - Live event logging")
    print("   - Performance metrics")
    print()
    print("💡 Use 's' to start demo, 'q' to quit")
    print()
    
    app = TheatricalMonitoringApp()
    await app.run_async()


async def run_side_by_side():
    """Run both console and dashboard simultaneously."""
    import subprocess
    import time
    
    print("🔄 Starting Side-by-Side Mode...")
    print("   - Console output in this terminal")
    print("   - Dashboard will open in new window")
    print()
    
    # Start dashboard in background
    dashboard_process = subprocess.Popen([
        sys.executable, 
        str(project_root / "theatrical_monitoring_dashboard.py")
    ])
    
    # Give dashboard time to start
    time.sleep(2)
    
    try:
        # Run console orchestration
        from theatrical_orchestrator import demo_theatrical_orchestration
        await demo_theatrical_orchestration()
    finally:
        # Clean up dashboard process
        dashboard_process.terminate()
        dashboard_process.wait()


async def run_quick_demo():
    """Run a quick 30-second overview."""
    from theatrical_orchestrator import TheatricalOrchestrator
    
    print("❓ Starting Quick Demo...")
    print("   - 30-second overview")
    print("   - Fast agent interactions")
    print("   - Abbreviated project")
    print()
    
    orchestrator = TheatricalOrchestrator(
        theatrical_delay=0.5,  # Fast timing
        show_details=False     # Less verbose
    )
    
    try:
        await orchestrator.initialize()
        
        # Quick project
        project = "Simple Todo App with basic CRUD operations"
        print(f"🚀 Building: {project}")
        print()
        
        await orchestrator.orchestrate_project(project)
        
    except Exception as e:
        print(f"❌ Quick demo failed: {e}")
    finally:
        await orchestrator.shutdown()


async def run_custom_settings():
    """Run with custom timing and verbosity settings."""
    from theatrical_orchestrator import TheatricalOrchestrator
    
    print("🔧 Custom Settings Mode")
    print()
    
    # Get user preferences
    try:
        delay = float(input("Theatrical delay (seconds, default 2.0): ") or "2.0")
        show_details = input("Show detailed metrics? (y/n, default y): ").lower() != "n"
        project = input("Project description (or press Enter for default): ").strip()
        
        if not project:
            project = "Modern Web Application with React frontend, FastAPI backend, and PostgreSQL database"
        
        print()
        print(f"⚙️ Configuration:")
        print(f"   - Delay: {delay}s")
        print(f"   - Details: {'Yes' if show_details else 'No'}")
        print(f"   - Project: {project}")
        print()
        
        orchestrator = TheatricalOrchestrator(
            theatrical_delay=delay,
            show_details=show_details
        )
        
        await orchestrator.initialize()
        await orchestrator.orchestrate_project(project)
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted")
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        if 'orchestrator' in locals():
            await orchestrator.shutdown()


async def main():
    """Main demo launcher."""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                await run_console_mode()
            elif choice == "2":
                await run_dashboard_mode()
            elif choice == "3":
                await run_side_by_side()
            elif choice == "4":
                await run_quick_demo()
            elif choice == "5":
                await run_custom_settings()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                continue
            
            print()
            print("🎭 Demo completed!")
            print()
            
            # Ask if user wants to run another demo
            again = input("Run another demo? (y/n): ").lower()
            if again != "y":
                break
                
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue
    
    print("👋 Thank you for using AIOSv3 Theatrical Demo!")


if __name__ == "__main__":
    # Check dependencies
    try:
        import textual  # Required for dashboard mode
    except ImportError:
        print("⚠️  Warning: textual not installed. Dashboard mode will not work.")
        print("   Install with: pip install textual")
        print()
    
    asyncio.run(main())