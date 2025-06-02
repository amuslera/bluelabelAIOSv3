#!/usr/bin/env python3
"""
Multi-Agent Orchestration Demo: Build a Todo API

Demonstrates how specialized agents collaborate to build a complete application:
1. CTO creates specification
2. Backend implements API  
3. Frontend creates UI
4. QA writes tests
5. DevOps creates deployment

With comprehensive logging to track the entire process.
"""

import asyncio
import json
import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.specialists.backend_agent import create_backend_agent
from agents.specialists.frontend_agent import create_frontend_agent  
from agents.specialists.qa_agent import create_qa_agent
from agents.specialists.devops_agent import create_devops_agent
from agents.base.enhanced_agent import EnhancedTask
from agents.base.types import TaskType
from enhanced_mock_provider import EnhancedMockProvider
from core.routing.providers.mock_provider import MockConfig
from core.routing.router import LLMRouter, RoutingStrategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class OrchestrationLogger:
    """Centralized logging for multi-agent orchestration"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.events = []
    
    def log_phase_start(self, phase: str, agent: str, description: str):
        """Log the start of a phase"""
        event = {
            "type": "phase_start",
            "phase": phase,
            "agent": agent,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        logger.info(f"🚀 Phase Started: {phase} ({agent}) - {description}")
    
    def log_phase_complete(self, phase: str, agent: str, 
                          output_size: int, execution_time: float):
        """Log completion of a phase"""
        event = {
            "type": "phase_complete",
            "phase": phase,
            "agent": agent,
            "output_size": output_size,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        logger.info(f"✅ Phase Complete: {phase} ({agent}) - {output_size} bytes in {execution_time:.2f}s")
    
    def log_artifact_handoff(self, from_agent: str, to_agent: str,
                           artifact_type: str, artifact_size: int):
        """Log artifact handoff between agents"""
        event = {
            "type": "artifact_handoff",
            "from_agent": from_agent,
            "to_agent": to_agent,
            "artifact_type": artifact_type,
            "artifact_size": artifact_size,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        logger.info(f"🤝 Artifact Handoff: {from_agent} → {to_agent} ({artifact_type}, {artifact_size} bytes)")
    
    def log_error(self, agent: str, error: str):
        """Log an error"""
        event = {
            "type": "error",
            "agent": agent,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        logger.error(f"❌ Error in {agent}: {error}")
    
    def generate_summary(self) -> str:
        """Generate a summary of the orchestration"""
        total_time = (datetime.now() - self.start_time).total_seconds()
        phases_completed = len([e for e in self.events if e["type"] == "phase_complete"])
        errors = len([e for e in self.events if e["type"] == "error"])
        
        summary = f"""
# Orchestration Summary
- Total Time: {total_time:.2f} seconds
- Phases Completed: {phases_completed}
- Errors: {errors}
- Events Logged: {len(self.events)}
"""
        return summary


class TodoAppOrchestrator:
    """Orchestrates multiple agents to build a Todo application"""
    
    def __init__(self, use_real_llm: bool = False):
        self.use_real_llm = use_real_llm
        self.logger = OrchestrationLogger()
        self.artifacts = {}
    
    async def setup_agents(self):
        """Initialize all agents with appropriate routing"""
        logger.info("Setting up agent team...")
        
        # Initialize mock provider
        mock_config = MockConfig(
            provider_name="mock",
            api_key="mock-key",
            response_delay=0.5,
            failure_rate=0.0
        )
        mock_provider = EnhancedMockProvider(mock_config)
        
        # Create router
        self.router = LLMRouter()
        self.router.providers["mock"] = mock_provider
        await self.router.initialize()
        
        # Create agents
        self.backend_agent = await create_backend_agent()
        self.frontend_agent = await create_frontend_agent()
        self.qa_agent = await create_qa_agent()
        self.devops_agent = await create_devops_agent()
        
        # Assign router to all agents
        for agent in [self.backend_agent, self.frontend_agent, 
                     self.qa_agent, self.devops_agent]:
            agent.router = self.router
        
        logger.info("Agent team ready!")
    
    async def phase1_specification(self) -> Dict[str, Any]:
        """Phase 1: CTO creates technical specification"""
        self.logger.log_phase_start("specification", "CTO", 
                                   "Creating technical specification for Todo API")
        
        # As the CTO, I'll create the specification directly
        spec = {
            "project": "Todo API with React Frontend",
            "architecture": {
                "backend": {
                    "framework": "FastAPI",
                    "database": "In-memory (for demo)",
                    "endpoints": [
                        "GET /todos - List all todos",
                        "POST /todos - Create a todo",
                        "DELETE /todos/{id} - Delete a todo",
                        "GET /health - Health check"
                    ]
                },
                "frontend": {
                    "framework": "React with TypeScript",
                    "features": [
                        "List todos",
                        "Add new todo",
                        "Delete todo",
                        "Loading states",
                        "Error handling"
                    ]
                },
                "deployment": {
                    "containerization": "Docker",
                    "orchestration": "Kubernetes",
                    "ci_cd": "GitHub Actions"
                }
            },
            "data_model": {
                "todo": {
                    "id": "string (UUID)",
                    "title": "string (required)",
                    "completed": "boolean (default: false)",
                    "created_at": "datetime"
                }
            },
            "quality_requirements": {
                "test_coverage": "80% minimum",
                "performance": "< 100ms response time",
                "availability": "99.9% uptime"
            }
        }
        
        spec_json = json.dumps(spec, indent=2)
        self.artifacts["specification"] = spec_json
        
        self.logger.log_phase_complete("specification", "CTO", 
                                      len(spec_json), 0.1)
        
        logger.info(f"CTO Specification created with {spec_json.count(chr(10))} lines")
        return spec
    
    async def phase2_backend(self, spec: Dict[str, Any]) -> str:
        """Phase 2: Backend Developer implements API"""
        self.logger.log_phase_start("backend", "Backend Developer",
                                   "Implementing FastAPI backend")
        
        # Create task for backend agent
        backend_task = EnhancedTask(
            task_type=TaskType.CODE_GENERATION,
            prompt=f"""
Create a FastAPI backend for a Todo application with these endpoints:
{json.dumps(spec['architecture']['backend']['endpoints'], indent=2)}

Data model:
{json.dumps(spec['data_model'], indent=2)}

Include proper error handling, validation, and in-memory storage.
""",
            complexity=6,
            metadata={"project": "todo_api", "spec": spec}
        )
        
        result = await self.backend_agent.process_task(backend_task)
        
        if result.success:
            self.artifacts["backend_code"] = result.output
            self.logger.log_phase_complete("backend", "Backend Developer",
                                         len(result.output), result.execution_time)
            self.logger.log_artifact_handoff("Backend Developer", "Frontend Developer",
                                           "API specification", len(result.output))
        else:
            self.logger.log_error("Backend Developer", "Failed to generate code")
            
        return result.output if result.success else ""
    
    async def phase3_frontend(self, spec: Dict[str, Any], backend_code: str) -> str:
        """Phase 3: Frontend Developer creates React UI"""
        self.logger.log_phase_start("frontend", "Frontend Developer",
                                   "Creating React frontend")
        
        # Extract API info from backend code
        api_endpoints = spec['architecture']['backend']['endpoints']
        
        frontend_task = EnhancedTask(
            task_type=TaskType.CODE_GENERATION,
            prompt=f"""
Create a React TypeScript component for a Todo application that:
- Fetches todos from GET /todos
- Creates new todos with POST /todos
- Deletes todos with DELETE /todos/{{id}}
- Has proper loading states and error handling
- Uses modern React hooks and best practices

API endpoints: {json.dumps(api_endpoints, indent=2)}
""",
            complexity=6,
            metadata={"project": "todo_ui", "spec": spec}
        )
        
        result = await self.frontend_agent.process_task(frontend_task)
        
        if result.success:
            self.artifacts["frontend_code"] = result.output
            self.logger.log_phase_complete("frontend", "Frontend Developer",
                                         len(result.output), result.execution_time)
            self.logger.log_artifact_handoff("Frontend Developer", "QA Engineer",
                                           "Frontend code", len(result.output))
        else:
            self.logger.log_error("Frontend Developer", "Failed to generate code")
            
        return result.output if result.success else ""
    
    async def phase4_testing(self, backend_code: str, frontend_code: str) -> str:
        """Phase 4: QA Engineer creates comprehensive tests"""
        self.logger.log_phase_start("testing", "QA Engineer",
                                   "Creating test suite")
        
        qa_task = EnhancedTask(
            task_type=TaskType.TESTING,
            prompt="""
Create comprehensive tests for a Todo application including:
- Unit tests for FastAPI backend endpoints
- React component tests using React Testing Library
- Integration tests for API calls
- Test both success and error cases
- Aim for 80% code coverage
""",
            complexity=7,
            metadata={"backend_code": backend_code[:500], 
                     "frontend_code": frontend_code[:500]}
        )
        
        result = await self.qa_agent.process_task(qa_task)
        
        if result.success:
            self.artifacts["test_suite"] = result.output
            self.logger.log_phase_complete("testing", "QA Engineer",
                                         len(result.output), result.execution_time)
            self.logger.log_artifact_handoff("QA Engineer", "DevOps Engineer",
                                           "Test suite", len(result.output))
        else:
            self.logger.log_error("QA Engineer", "Failed to generate tests")
            
        return result.output if result.success else ""
    
    async def phase5_deployment(self, spec: Dict[str, Any]) -> str:
        """Phase 5: DevOps Engineer creates deployment configuration"""
        self.logger.log_phase_start("deployment", "DevOps Engineer",
                                   "Creating deployment configuration")
        
        devops_task = EnhancedTask(
            task_type=TaskType.DEPLOYMENT,
            prompt=f"""
Create deployment configuration for a Todo application:
- Dockerfile for both backend (FastAPI) and frontend (React)
- Kubernetes manifests for deployment
- GitHub Actions CI/CD pipeline
- Include health checks and monitoring

Requirements: {json.dumps(spec['architecture']['deployment'], indent=2)}
""",
            complexity=8,
            metadata={"project": "todo_deployment", "spec": spec}
        )
        
        result = await self.devops_agent.process_task(devops_task)
        
        if result.success:
            self.artifacts["deployment"] = result.output
            self.logger.log_phase_complete("deployment", "DevOps Engineer",
                                         len(result.output), result.execution_time)
        else:
            self.logger.log_error("DevOps Engineer", "Failed to generate deployment")
            
        return result.output if result.success else ""
    
    async def orchestrate(self):
        """Run the complete orchestration"""
        logger.info("Starting Multi-Agent Todo App Build with agents: CTO, Backend, Frontend, QA, DevOps")
        
        try:
            # Setup
            await self.setup_agents()
            
            # Phase 1: Specification
            spec = await self.phase1_specification()
            
            # Phase 2: Backend Implementation
            backend_code = await self.phase2_backend(spec)
            
            # Phase 3: Frontend Implementation  
            frontend_code = await self.phase3_frontend(spec, backend_code)
            
            # Phase 4: Testing
            test_suite = await self.phase4_testing(backend_code, frontend_code)
            
            # Phase 5: Deployment
            deployment = await self.phase5_deployment(spec)
            
            # Generate final report
            await self.generate_report()
            
        except Exception as e:
            self.logger.log_error("Orchestrator", str(e))
            logger.exception("Orchestration failed")
            raise
        finally:
            # Cleanup
            await self.cleanup()
    
    async def generate_report(self):
        """Generate final project report"""
        logger.info("Generating project report...")
        
        report = f"""
# 📋 Multi-Agent Todo App Build Report

{self.logger.generate_summary()}

## Artifacts Generated

### 1. Technical Specification
- Size: {len(self.artifacts.get('specification', ''))} bytes
- Created by: CTO (Claude)

### 2. Backend Code  
- Size: {len(self.artifacts.get('backend_code', ''))} bytes
- Technology: FastAPI

### 3. Frontend Code
- Size: {len(self.artifacts.get('frontend_code', ''))} bytes  
- Technology: React + TypeScript

### 4. Test Suite
- Size: {len(self.artifacts.get('test_suite', ''))} bytes
- Coverage: Unit + Integration + E2E

### 5. Deployment Configuration
- Size: {len(self.artifacts.get('deployment', ''))} bytes
- Technologies: Docker, Kubernetes, GitHub Actions

## Agent Collaboration Flow
```
CTO -> Backend Dev -> Frontend Dev -> QA Engineer -> DevOps Engineer
 |         |              |              |               |
 v         v              v              v               v
Spec -> API Code -> UI Code -> Test Suite -> Deployment
```

## Total Project Size: {sum(len(v) for v in self.artifacts.values())} bytes

---
*Generated by AIOSv3 Multi-Agent Orchestration System*
"""
        
        # Save report
        with open("todo_app_report.md", "w") as f:
            f.write(report)
        
        # Save artifacts
        for name, content in self.artifacts.items():
            filename = f"todo_app_{name}.md"
            with open(filename, "w") as f:
                f.write(content)
        
        logger.info(f"Report generated: {len(self.artifacts) + 1} files, {sum(len(v) for v in self.artifacts.values())} total bytes")
    
    async def cleanup(self):
        """Cleanup agents"""
        logger.info("Cleaning up agents...")
        for agent in [self.backend_agent, self.frontend_agent,
                     self.qa_agent, self.devops_agent]:
            if hasattr(self, agent.__class__.__name__.lower()):
                await agent.stop()


async def main():
    """Run the multi-agent orchestration demo"""
    print("""
    ╔══════════════════════════════════════════════╗
    ║  🤖 AIOSv3 Multi-Agent Orchestration Demo 🤖 ║
    ║         Building a Todo App Together         ║
    ╚══════════════════════════════════════════════╝
    """)
    
    orchestrator = TodoAppOrchestrator(use_real_llm=False)
    await orchestrator.orchestrate()
    
    print("\n✅ Orchestration complete! Check the generated files:")
    print("- todo_app_report.md (Full report)")
    print("- todo_app_*.md (Individual artifacts)")


if __name__ == "__main__":
    asyncio.run(main())