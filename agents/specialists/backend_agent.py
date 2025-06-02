"""
Backend Developer Agent - Specializes in server-side development and API implementation.

This agent focuses on:
- FastAPI endpoint development
- Database model creation and migrations
- Business logic implementation
- API integration and service layer development
- Backend testing (unit and integration tests)
"""

import re
from datetime import datetime
from typing import Any, Dict, Optional

from agents.base.enhanced_agent import (
    AgentCapability,
    EnhancedAgentConfig,
    EnhancedBaseAgent,
    EnhancedTask,
)
from agents.base.types import AgentType, TaskType
from core.routing.providers.base import LLMResponse
from core.routing.router import RoutingStrategy


class BackendAgentConfig(EnhancedAgentConfig):
    """Enhanced configuration for Backend Developer Agent."""

    def __init__(self, **kwargs):
        # Set Backend Developer-specific defaults
        defaults = {
            "agent_type": AgentType.BACKEND_DEV,
            "name": "AIOSv3 Backend Developer",
            "description": "Backend Developer agent specializing in FastAPI, database design, and server-side logic",
            "capabilities": [
                AgentCapability.CODE_GENERATION,
                AgentCapability.API_DESIGN,
                AgentCapability.ARCHITECTURE_DESIGN,
                AgentCapability.TESTING
            ],
            "default_routing_strategy": RoutingStrategy.PERFORMANCE_OPTIMIZED,
            "max_tokens": 6144,  # Higher for code generation
            "temperature": 0.2,  # Lower temperature for more consistent code
            "health_check_interval": 15
        }
        # Override with provided kwargs
        defaults.update(kwargs)
        super().__init__(**defaults)


class BackendDeveloperAgent(EnhancedBaseAgent):
    """
    Backend Developer Agent for server-side development.

    Specializes in:
    - FastAPI endpoint development and routing
    - SQLAlchemy model creation and database design
    - Business logic implementation and service layers
    - API integration and external service communication
    - Backend testing (pytest, unit tests, integration tests)
    - Error handling and validation
    """

    def __init__(self, config: Optional[BackendAgentConfig] = None):
        """Initialize Backend Developer Agent with specialized configuration."""
        if config is None:
            config = BackendAgentConfig()

        super().__init__(config)

        # Backend-specific knowledge areas
        self.expertise_areas = [
            "fastapi",
            "sqlalchemy",
            "pydantic",
            "pytest",
            "uvicorn",
            "database_design",
            "api_development",
            "authentication",
            "validation",
            "error_handling"
        ]

        # Code templates and patterns
        self.code_templates = {
            "fastapi_endpoint": self._get_fastapi_template(),
            "sqlalchemy_model": self._get_model_template(),
            "pydantic_schema": self._get_schema_template(),
            "pytest_test": self._get_test_template(),
            "service_layer": self._get_service_template()
        }

        # Quality standards
        self.quality_standards = {
            "code_style": "Follow PEP 8 and project standards",
            "error_handling": "Comprehensive error handling with proper HTTP status codes",
            "validation": "Input validation using Pydantic models",
            "testing": "Unit tests for all business logic, integration tests for endpoints",
            "documentation": "Clear docstrings and inline comments",
            "security": "No hardcoded secrets, proper authentication patterns"
        }

    async def _on_initialize(self) -> None:
        """Backend Agent initialization - load development knowledge."""
        # Store Backend Developer expertise
        await self.store_knowledge(
            content="Backend Developer Agent specialized in FastAPI, SQLAlchemy, and Python server-side development",
            category="agent_identity",
            keywords=["backend", "fastapi", "python", "api", "database"]
        )

        # Store development best practices
        best_practices = """
        Backend Development Best Practices:
        1. API Design: RESTful patterns, consistent response formats
        2. Database: Proper indexing, migrations, relationship design
        3. Error Handling: Structured error responses, proper HTTP codes
        4. Security: Input validation, authentication, authorization
        5. Testing: Unit tests for logic, integration tests for endpoints
        6. Performance: Query optimization, caching strategies
        7. Documentation: OpenAPI schemas, clear docstrings
        """

        await self.store_knowledge(
            content=best_practices,
            category="development_practices",
            keywords=["best_practices", "api", "database", "testing", "security"]
        )

        # Store project-specific context
        project_context = """
        AIOSv3 Project Context:
        - FastAPI framework for REST APIs
        - SQLAlchemy for database ORM
        - Pydantic for data validation and serialization
        - Pytest for testing framework
        - Redis for caching and sessions
        - PostgreSQL for primary database
        - Docker for containerization
        """

        await self.store_knowledge(
            content=project_context,
            category="project_context",
            keywords=["aiosv3", "stack", "framework", "database"]
        )

    async def _on_shutdown(self) -> None:
        """Backend Agent shutdown - save work context."""
        # Could save current development context or progress
        pass

    async def _process_response(self, response: LLMResponse, task: EnhancedTask) -> str:
        """Process and structure Backend Developer responses with code formatting."""
        content = response.content

        # Structure different types of backend development responses
        if task.task_type == TaskType.CODE_GENERATION:
            return self._format_code_response(content, task)
        elif task.task_type == TaskType.SYSTEM_DESIGN:
            return self._format_api_response(content, task)
        elif task.task_type == TaskType.TESTING:
            return self._format_testing_response(content, task)
        else:
            return self._format_general_backend_response(content, task)

    def _format_code_response(self, content: str, task: EnhancedTask) -> str:
        """Format code generation responses with proper structure."""
        return f"""# 🚀 Backend Code Implementation

## Task Summary
{task.prompt}

## Implementation

{content}

## Code Quality Checklist
- [ ] Follows PEP 8 style guidelines
- [ ] Includes proper error handling
- [ ] Has comprehensive docstrings
- [ ] Includes input validation
- [ ] Has corresponding unit tests
- [ ] No hardcoded secrets or sensitive data

## Testing Notes
{self._extract_testing_guidance(content)}

## Next Steps
{self._extract_implementation_steps(content)}

---
*Backend Developer Agent | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_api_response(self, content: str, task: EnhancedTask) -> str:
        """Format API development responses."""
        return f"""# 🌐 API Development Implementation

## Endpoint Overview
{task.prompt}

## API Implementation

{content}

## API Design Considerations
- **HTTP Methods**: Proper REST verb usage
- **Status Codes**: Appropriate response codes for different scenarios
- **Request/Response**: Consistent data structures
- **Error Handling**: Structured error responses
- **Authentication**: Security middleware integration
- **Documentation**: OpenAPI schema generation

## Testing Strategy
{self._extract_testing_guidance(content)}

## Integration Notes
{self._extract_integration_notes(content)}

---
*Backend API Developer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_database_response(self, content: str, task: EnhancedTask) -> str:
        """Format database design responses."""
        return f"""# 🗄️ Database Design Implementation

## Database Requirements
{task.prompt}

## Database Implementation

{content}

## Database Design Principles
- **Normalization**: Proper table relationships and foreign keys
- **Indexing**: Performance optimization strategies
- **Migrations**: Safe database schema changes
- **Constraints**: Data integrity enforcement
- **Security**: Proper access controls and validation

## Migration Strategy
{self._extract_migration_notes(content)}

## Performance Considerations
{self._extract_performance_notes(content)}

---
*Backend Database Developer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_testing_response(self, content: str, task: EnhancedTask) -> str:
        """Format testing implementation responses."""
        return f"""# 🧪 Backend Testing Implementation

## Testing Scope
{task.prompt}

## Test Implementation

{content}

## Testing Coverage
- **Unit Tests**: Business logic and individual functions
- **Integration Tests**: API endpoints and database interactions
- **Edge Cases**: Error conditions and boundary testing
- **Performance Tests**: Load and stress testing considerations

## Test Execution
{self._extract_test_execution_notes(content)}

## Coverage Goals
{self._extract_coverage_notes(content)}

---
*Backend Testing Specialist | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_general_backend_response(self, content: str, task: EnhancedTask) -> str:
        """Format general backend development responses."""
        return f"""# ⚙️ Backend Development Task

## Requirement
{task.prompt}

## Solution

{content}

## Implementation Notes
{self._extract_implementation_notes(content)}

## Quality Assurance
{self._extract_qa_notes(content)}

---
*Backend Developer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _extract_testing_guidance(self, content: str) -> str:
        """Extract testing guidance from response."""
        test_patterns = [
            r"(?:## Testing|# Testing|Test.*:)(.*?)(?=\n#|\n##|\Z)",
            r"(?:pytest|test.*case|unit.*test)(.*?)(?=\n|\Z)"
        ]

        for pattern in test_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Implement comprehensive unit and integration tests for all functionality."

    def _extract_implementation_steps(self, content: str) -> str:
        """Extract implementation steps from response."""
        steps_patterns = [
            r"(?:## Steps|# Steps|Implementation.*:)(.*?)(?=\n#|\n##|\Z)",
            r"(?:## Next|# Next|Following.*:)(.*?)(?=\n#|\n##|\Z)"
        ]

        for pattern in steps_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "1. Review code for quality\n2. Run tests\n3. Update documentation\n4. Deploy to staging"

    def _extract_integration_notes(self, content: str) -> str:
        """Extract integration notes from response."""
        integration_patterns = [
            r"(?:## Integration|# Integration)(.*?)(?=\n#|\n##|\Z)",
            r"(?:middleware|authentication|cors)(.*?)(?=\n|\Z)"
        ]

        for pattern in integration_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Ensure proper integration with existing middleware and authentication systems."

    def _extract_migration_notes(self, content: str) -> str:
        """Extract database migration notes."""
        return "Create migration scripts for any schema changes. Test migrations on staging first."

    def _extract_performance_notes(self, content: str) -> str:
        """Extract performance considerations."""
        return "Consider query optimization, indexing strategy, and caching for high-traffic endpoints."

    def _extract_test_execution_notes(self, content: str) -> str:
        """Extract test execution guidance."""
        return "Run tests with: `pytest tests/ -v --cov=app --cov-report=html`"

    def _extract_coverage_notes(self, content: str) -> str:
        """Extract coverage requirements."""
        return "Target minimum 80% test coverage. Focus on critical business logic and error paths."

    def _extract_implementation_notes(self, content: str) -> str:
        """Extract general implementation notes."""
        return "Follow project coding standards and review checklist before submission."

    def _extract_qa_notes(self, content: str) -> str:
        """Extract QA considerations."""
        return "Validate input/output, test error conditions, and ensure security best practices."

    async def _customize_prompt(self, task: EnhancedTask, context: str) -> str:
        """Customize prompts with Backend Developer-specific expertise and standards."""

        # Build Backend Developer-specific context
        backend_context = """
You are a Senior Backend Developer working on AIOSv3, a modular AI agent platform. Your expertise includes:

**Core Technologies:**
- FastAPI for REST API development
- SQLAlchemy for database ORM and migrations
- Pydantic for data validation and serialization
- Pytest for comprehensive testing
- Redis for caching and session management
- PostgreSQL for relational data storage

**Development Standards:**
- Follow PEP 8 and project coding standards
- Implement comprehensive error handling with proper HTTP status codes
- Use Pydantic models for request/response validation
- Write unit tests for business logic, integration tests for endpoints
- Include clear docstrings and comments
- Never hardcode secrets or sensitive configuration

**Project Architecture:**
- Clean architecture with service layer separation
- Repository pattern for data access
- Dependency injection for testability
- Structured error responses
- Comprehensive logging and monitoring
- Docker containerization ready

**Quality Requirements:**
- All code must be production-ready
- Include proper error handling and validation
- Write corresponding tests for new functionality
- Follow security best practices
- Optimize for performance and scalability
- Maintain backward compatibility when possible
"""

        # Task-specific guidance
        task_guidance = {
            TaskType.CODE_GENERATION: """
Focus on:
- Clean, readable, and maintainable code
- Proper function signatures and type hints
- Comprehensive error handling
- Input validation and sanitization
- Appropriate use of design patterns
""",
            TaskType.SYSTEM_DESIGN: """
Focus on:
- RESTful API design principles
- Proper HTTP methods and status codes
- Request/response model validation
- Authentication and authorization
- Rate limiting and security headers
- OpenAPI documentation generation
""",
            TaskType.TESTING: """
Focus on:
- Unit tests for business logic
- Integration tests for API endpoints
- Test fixtures and data factories
- Mock external dependencies
- Edge case and error condition testing
- Performance and load testing considerations
"""
        }

        guidance = task_guidance.get(task.task_type, """
Provide high-quality backend development solution following best practices.
""")

        return f"""{backend_context}

{guidance}

**Task Details:**
- **Complexity**: {task.complexity}/10
- **Privacy Sensitive**: {task.privacy_sensitive}
- **Context**: {context if context else "No additional context provided"}

**Current Task:**
{task.prompt}

Please provide a complete, production-ready backend solution with:
1. Clean, well-documented code
2. Proper error handling and validation
3. Corresponding unit/integration tests
4. Implementation notes and considerations

Ensure all code follows project standards and is ready for code review."""

    def _get_fastapi_template(self) -> str:
        """Get FastAPI endpoint template."""
        return """
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter()

class RequestModel(BaseModel):
    # Define request structure
    pass

class ResponseModel(BaseModel):
    # Define response structure
    pass

@router.post("/endpoint", response_model=ResponseModel)
async def endpoint_function(
    request: RequestModel,
    # Add dependencies like auth, db session
):
    try:
        # Implementation logic
        return ResponseModel()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

    def _get_model_template(self) -> str:
        """Get SQLAlchemy model template."""
        return """
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class ModelName(Base):
    __tablename__ = "table_name"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add model fields

    def __repr__(self):
        return f"<ModelName(id={self.id})>"
"""

    def _get_schema_template(self) -> str:
        """Get Pydantic schema template."""
        return """
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class SchemaBase(BaseModel):
    # Common fields
    pass

class SchemaCreate(SchemaBase):
    # Fields for creation
    pass

class SchemaUpdate(SchemaBase):
    # Fields for updates
    pass

class SchemaResponse(SchemaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
"""

    def _get_test_template(self) -> str:
        """Get pytest test template."""
        return """
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestEndpoint:
    def test_successful_request(self):
        response = client.post("/endpoint", json={})
        assert response.status_code == 200

    def test_invalid_request(self):
        response = client.post("/endpoint", json={"invalid": "data"})
        assert response.status_code == 422

    def test_error_handling(self):
        # Test error conditions
        pass
"""

    def _get_service_template(self) -> str:
        """Get service layer template."""
        return """
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import ModelName
from app.schemas import SchemaCreate, SchemaUpdate

class ServiceName:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: SchemaCreate) -> ModelName:
        db_obj = ModelName(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, id: int) -> Optional[ModelName]:
        return self.db.query(ModelName).filter(ModelName.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelName]:
        return self.db.query(ModelName).offset(skip).limit(limit).all()

    def update(self, id: int, obj_in: SchemaUpdate) -> Optional[ModelName]:
        db_obj = self.get(id)
        if db_obj:
            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        db_obj = self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
"""


# Factory function for easy Backend Agent creation
async def create_backend_agent(custom_config: Optional[Dict[str, Any]] = None) -> BackendDeveloperAgent:
    """Create and initialize a Backend Developer Agent with optional custom configuration."""

    config_params = custom_config or {}
    config = BackendAgentConfig(**config_params)

    agent = BackendDeveloperAgent(config)
    await agent.initialize()

    return agent


# Example usage and testing
if __name__ == "__main__":

    async def test_backend_agent():
        """Test Backend Developer Agent functionality."""

        # Create Backend Agent
        backend = await create_backend_agent()

        # Test API development task
        api_task = EnhancedTask(
            task_type=TaskType.CODE_GENERATION,
            prompt="Create a FastAPI endpoint for user registration that accepts email and password, validates the input, hashes the password, stores the user in database, and returns a success response.",
            complexity=6,
            metadata={
                "endpoint": "/auth/register",
                "method": "POST",
                "validation": "email format, password strength",
                "security": "password hashing required"
            }
        )

        print("🚀 Testing Backend Agent - API Development")
        result = await backend.process_task(api_task)
        print(f"Success: {result.success}")
        print(f"Cost: ${result.cost:.4f}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Model used: {result.model_used}")
        print("\n" + "="*80)
        print(result.output[:1000] + "..." if len(result.output) > 1000 else result.output)

        # Get agent status
        status = backend.get_status()
        print("\n📊 Backend Agent Status:")
        print(f"Tasks completed: {status['tasks_completed']}")
        print(f"Success rate: {status['success_rate']:.1%}")
        print(f"Total cost: ${status['total_cost']:.4f}")

        await backend.stop()

    # Run test
    # asyncio.run(test_backend_agent())
