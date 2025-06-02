"""
QA Engineer Agent - Specializes in testing, validation, and quality assurance.

This agent focuses on:
- Test strategy and planning
- Unit test creation and maintenance
- Integration and E2E test development
- Test automation frameworks
- Performance testing
- Security testing
- Accessibility validation
- Test coverage analysis
"""

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


class QAAgentConfig(EnhancedAgentConfig):
    """Enhanced configuration for QA Engineer Agent."""

    def __init__(self, **kwargs):
        # Set QA Engineer-specific defaults
        defaults = {
            "agent_type": AgentType.QA_ENGINEER,
            "name": "AIOSv3 QA Engineer",
            "description": "QA Engineer agent specializing in testing strategies, test automation, and quality validation",
            "capabilities": [
                AgentCapability.TESTING,
                AgentCapability.CODE_REVIEW,
                AgentCapability.SECURITY_AUDIT,
                AgentCapability.DOCUMENTATION
            ],
            "default_routing_strategy": RoutingStrategy.BALANCED,
            "max_tokens": 4096,  # Moderate for test code
            "temperature": 0.2,  # Low temperature for consistent test generation
            "health_check_interval": 15
        }
        # Override with provided kwargs
        defaults.update(kwargs)
        super().__init__(**defaults)


class QAEngineerAgent(EnhancedBaseAgent):
    """
    QA Engineer Agent for comprehensive testing and quality assurance.

    Specializes in:
    - Test strategy development and planning
    - Unit test creation (pytest, Jest, unittest)
    - Integration test development
    - End-to-end test automation (Playwright, Cypress, Selenium)
    - Performance testing (JMeter, Locust)
    - Security testing and vulnerability scanning
    - Accessibility testing (WCAG compliance)
    - Test coverage analysis and reporting
    """

    def __init__(self, config: Optional[QAAgentConfig] = None):
        """Initialize QA Engineer Agent with specialized configuration."""
        if config is None:
            config = QAAgentConfig()

        super().__init__(config)

        # QA-specific knowledge areas
        self.expertise_areas = [
            "pytest",
            "jest",
            "playwright",
            "cypress",
            "selenium",
            "testing_strategies",
            "test_automation",
            "performance_testing",
            "security_testing",
            "accessibility_testing",
            "coverage_analysis"
        ]

        # Test templates and patterns
        self.test_templates = {
            "unit_test": self._get_unit_test_template(),
            "integration_test": self._get_integration_test_template(),
            "e2e_test": self._get_e2e_test_template(),
            "performance_test": self._get_performance_test_template(),
            "test_strategy": self._get_test_strategy_template()
        }

        # Quality standards
        self.quality_standards = {
            "coverage_target": "Minimum 80% code coverage, 100% for critical paths",
            "test_isolation": "Tests must be independent and idempotent",
            "test_speed": "Unit tests < 100ms, integration < 1s, E2E < 30s",
            "test_clarity": "Clear test names describing what is being tested",
            "error_scenarios": "Test both happy paths and edge cases",
            "maintainability": "DRY principles, reusable fixtures and utilities"
        }

    async def _on_initialize(self) -> None:
        """QA Agent initialization - load testing knowledge."""
        # Store QA Engineer expertise
        await self.store_knowledge(
            content="QA Engineer Agent specialized in comprehensive testing strategies, test automation, and quality validation",
            category="agent_identity",
            keywords=["qa", "testing", "quality", "automation", "validation"]
        )

        # Store testing best practices
        best_practices = """
        QA Engineering Best Practices:
        1. Test Strategy: Pyramid approach (unit > integration > E2E)
        2. Test Coverage: Focus on critical paths and edge cases
        3. Test Independence: Each test should be atomic and isolated
        4. Test Data: Use factories and fixtures for consistent data
        5. Test Naming: Descriptive names following given-when-then pattern
        6. Performance: Optimize test execution time
        7. Maintenance: Keep tests DRY and maintainable
        8. CI/CD Integration: All tests must run in pipeline
        """

        await self.store_knowledge(
            content=best_practices,
            category="testing_practices",
            keywords=["best_practices", "testing", "strategy", "coverage", "automation"]
        )

        # Store project-specific testing context
        project_context = """
        AIOSv3 Testing Stack:
        - Backend: pytest, pytest-asyncio, pytest-cov
        - Frontend: Jest, React Testing Library, Vitest
        - E2E: Playwright for cross-browser testing
        - API Testing: pytest with httpx/requests
        - Performance: Locust for load testing
        - Security: Bandit, safety, OWASP checks
        - Coverage: Coverage.py, Istanbul
        - CI/CD: GitHub Actions, pre-commit hooks
        """

        await self.store_knowledge(
            content=project_context,
            category="project_context",
            keywords=["aiosv3", "testing_stack", "tools", "frameworks"]
        )

    async def _on_shutdown(self) -> None:
        """QA Agent shutdown - save testing context."""
        # Could save current test suite status or metrics
        pass

    async def _process_response(self, response: LLMResponse, task: EnhancedTask) -> str:
        """Process and structure QA Engineer responses with test formatting."""
        content = response.content

        # Structure different types of QA responses
        if task.task_type == TaskType.TESTING:
            return self._format_testing_response(content, task)
        elif task.task_type == TaskType.CODE_REVIEW:
            return self._format_review_response(content, task)
        elif task.task_type == TaskType.DOCUMENTATION:
            return self._format_test_documentation_response(content, task)
        elif task.task_type == TaskType.PERFORMANCE_ANALYSIS:
            return self._format_performance_test_response(content, task)
        else:
            return self._format_general_qa_response(content, task)

    def _format_testing_response(self, content: str, task: EnhancedTask) -> str:
        """Format test creation responses with proper structure."""
        return f"""# 🧪 QA Testing Implementation

## Test Requirements
{task.prompt}

## Test Implementation

{content}

## Quality Checklist
- [ ] Tests are independent and isolated
- [ ] Clear test names following conventions
- [ ] Both happy paths and edge cases covered
- [ ] Proper setup and teardown
- [ ] No hardcoded test data
- [ ] Tests run quickly and reliably
- [ ] Coverage targets met

## Test Execution
{self._extract_test_execution_notes(content)}

## Coverage Analysis
{self._extract_coverage_analysis(content)}

## Next Steps
{self._extract_next_steps(content)}

---
*QA Engineer Agent | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_review_response(self, content: str, task: EnhancedTask) -> str:
        """Format code review responses focused on quality."""
        return f"""# 🔍 QA Code Review

## Review Scope
{task.prompt}

## Quality Assessment

{content}

## Testing Recommendations
{self._extract_testing_recommendations(content)}

## Coverage Gaps
{self._extract_coverage_gaps(content)}

## Risk Assessment
- **High Risk Areas**: Critical paths needing more tests
- **Medium Risk Areas**: Features with partial coverage
- **Low Risk Areas**: Well-tested components

## Action Items
{self._extract_action_items(content)}

---
*QA Code Reviewer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_test_documentation_response(self, content: str, task: EnhancedTask) -> str:
        """Format test documentation responses."""
        return f"""# 📚 Test Documentation

## Documentation Scope
{task.prompt}

## Test Documentation

{content}

## Test Strategy Overview
{self._extract_test_strategy(content)}

## Test Coverage Matrix
{self._extract_coverage_matrix(content)}

## Running Tests
{self._extract_test_running_guide(content)}

## Maintenance Guide
{self._extract_maintenance_guide(content)}

---
*QA Documentation Specialist | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_performance_test_response(self, content: str, task: EnhancedTask) -> str:
        """Format performance testing responses."""
        return f"""# ⚡ Performance Testing Implementation

## Performance Requirements
{task.prompt}

## Performance Test Implementation

{content}

## Performance Metrics
- **Response Time**: Target vs Actual
- **Throughput**: Requests per second
- **Resource Usage**: CPU, Memory, I/O
- **Error Rate**: Failure percentage under load
- **Scalability**: Performance at different load levels

## Load Test Scenarios
{self._extract_load_scenarios(content)}

## Performance Recommendations
{self._extract_performance_recommendations(content)}

---
*Performance Testing Specialist | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_general_qa_response(self, content: str, task: EnhancedTask) -> str:
        """Format general QA responses."""
        return f"""# 🎯 QA Engineering Task

## Requirement
{task.prompt}

## Solution

{content}

## Quality Assurance Notes
{self._extract_qa_notes(content)}

## Validation Steps
{self._extract_validation_steps(content)}

---
*QA Engineer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _extract_test_execution_notes(self, content: str) -> str:
        """Extract test execution guidance."""
        return """Run tests with:
- Unit tests: `pytest tests/unit -v --cov`
- Integration: `pytest tests/integration -v`
- E2E: `playwright test`
- All tests: `npm test && pytest`"""

    def _extract_coverage_analysis(self, content: str) -> str:
        """Extract coverage analysis."""
        return "Target: 80% overall, 100% for critical paths. Generate reports with coverage tools."

    def _extract_next_steps(self, content: str) -> str:
        """Extract next steps."""
        return "1. Run test suite\n2. Analyze coverage gaps\n3. Add missing edge cases\n4. Integrate with CI/CD"

    def _extract_testing_recommendations(self, content: str) -> str:
        """Extract testing recommendations."""
        return "Add unit tests for new functions, integration tests for API endpoints, E2E for user flows."

    def _extract_coverage_gaps(self, content: str) -> str:
        """Extract coverage gaps."""
        return "Identify untested code paths, missing error scenarios, and integration points."

    def _extract_action_items(self, content: str) -> str:
        """Extract action items from review."""
        return "1. Add missing tests\n2. Improve test isolation\n3. Update test documentation\n4. Fix flaky tests"

    def _extract_test_strategy(self, content: str) -> str:
        """Extract test strategy."""
        return "Follow test pyramid: many unit tests, some integration tests, few E2E tests."

    def _extract_coverage_matrix(self, content: str) -> str:
        """Extract coverage matrix."""
        return "Map features to test types: unit, integration, E2E, performance, security."

    def _extract_test_running_guide(self, content: str) -> str:
        """Extract test running guide."""
        return "Setup test environment, install dependencies, run test commands, analyze results."

    def _extract_maintenance_guide(self, content: str) -> str:
        """Extract maintenance guide."""
        return "Keep tests updated with code changes, refactor duplicate test code, update test data."

    def _extract_load_scenarios(self, content: str) -> str:
        """Extract load test scenarios."""
        return "Normal load, peak load, stress test, spike test, endurance test scenarios."

    def _extract_performance_recommendations(self, content: str) -> str:
        """Extract performance recommendations."""
        return "Optimize slow queries, implement caching, use connection pooling, scale horizontally."

    def _extract_qa_notes(self, content: str) -> str:
        """Extract QA notes."""
        return "Ensure test coverage, validate edge cases, check error handling, verify performance."

    def _extract_validation_steps(self, content: str) -> str:
        """Extract validation steps."""
        return "1. Unit test pass\n2. Integration verified\n3. E2E scenarios work\n4. Performance acceptable"

    async def _customize_prompt(self, task: EnhancedTask, context: str) -> str:
        """Customize prompts with QA Engineer-specific expertise and standards."""

        # Build QA Engineer-specific context
        qa_context = """
You are a Senior QA Engineer working on AIOSv3, a modular AI agent platform. Your expertise includes:

**Core Testing Skills:**
- Test strategy and planning (test pyramid approach)
- Unit testing (pytest, Jest, unittest)
- Integration testing (API, database, service)
- E2E testing (Playwright, Cypress, Selenium)
- Performance testing (Locust, JMeter)
- Security testing (OWASP, penetration testing)
- Accessibility testing (WCAG 2.1 compliance)

**Testing Standards:**
- Achieve minimum 80% code coverage, 100% for critical paths
- Write independent, isolated, and idempotent tests
- Follow given-when-then pattern for test names
- Test both happy paths and edge cases
- Maintain fast test execution times
- Ensure tests are maintainable and DRY

**Quality Principles:**
- Shift-left testing approach
- Risk-based test prioritization
- Continuous testing in CI/CD
- Test data management best practices
- Defect prevention over detection
- Automated regression testing

**Tools & Frameworks:**
- Backend: pytest, pytest-asyncio, pytest-cov, httpx
- Frontend: Jest, React Testing Library, Vitest
- E2E: Playwright, Cypress
- Performance: Locust, k6
- Security: Bandit, OWASP ZAP
- Coverage: Coverage.py, Istanbul
"""

        # Task-specific guidance
        task_guidance = {
            TaskType.TESTING: """
Focus on:
- Comprehensive test coverage
- Clear test structure and naming
- Proper test isolation
- Edge case identification
- Performance considerations
- Maintainable test code
""",
            TaskType.CODE_REVIEW: """
Focus on:
- Test coverage analysis
- Code quality issues
- Security vulnerabilities
- Performance bottlenecks
- Maintainability concerns
- Best practice violations
""",
            TaskType.PERFORMANCE_ANALYSIS: """
Focus on:
- Load testing scenarios
- Performance benchmarks
- Resource utilization
- Scalability testing
- Bottleneck identification
- Optimization recommendations
"""
        }

        guidance = task_guidance.get(task.task_type, """
Provide comprehensive QA analysis and testing solutions.
""")

        return f"""{qa_context}

{guidance}

**Task Details:**
- **Complexity**: {task.complexity}/10
- **Privacy Sensitive**: {task.privacy_sensitive}
- **Context**: {context if context else "No additional context provided"}

**Current Task:**
{task.prompt}

Please provide a complete QA solution with:
1. Comprehensive test implementation
2. Clear test structure and naming
3. Edge case coverage
4. Performance considerations
5. Documentation and execution guides

Ensure all tests follow best practices and are ready for CI/CD integration."""

    def _get_unit_test_template(self) -> str:
        """Get unit test template."""
        return """
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

class TestComponent:
    \"\"\"Unit tests for Component functionality.\"\"\"

    @pytest.fixture
    def setup(self):
        \"\"\"Test setup and fixtures.\"\"\"
        # Arrange test data
        return {
            "mock_dependency": Mock(),
            "test_data": {"id": 1, "name": "test"}
        }

    def test_happy_path(self, setup):
        \"\"\"Test normal operation with valid inputs.\"\"\"
        # Given
        component = Component(setup["mock_dependency"])

        # When
        result = component.process(setup["test_data"])

        # Then
        assert result.success is True
        assert result.data["id"] == 1
        setup["mock_dependency"].save.assert_called_once()

    def test_edge_case_empty_input(self, setup):
        \"\"\"Test behavior with empty input.\"\"\"
        # Given
        component = Component(setup["mock_dependency"])

        # When/Then
        with pytest.raises(ValueError, match="Input cannot be empty"):
            component.process({})

    @pytest.mark.parametrize("invalid_input,expected_error", [
        (None, "Input cannot be None"),
        ({"id": -1}, "ID must be positive"),
        ({"name": ""}, "Name cannot be empty")
    ])
    def test_invalid_inputs(self, setup, invalid_input, expected_error):
        \"\"\"Test various invalid input scenarios.\"\"\"
        component = Component(setup["mock_dependency"])

        with pytest.raises(ValueError, match=expected_error):
            component.process(invalid_input)
"""

    def _get_integration_test_template(self) -> str:
        """Get integration test template."""
        return """
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.integration
class TestAPIIntegration:
    \"\"\"Integration tests for API endpoints.\"\"\"

    @pytest.fixture
    async def client(self, app):
        \"\"\"Create test client.\"\"\"
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client

    @pytest.fixture
    async def db_session(self):
        \"\"\"Create test database session.\"\"\"
        # Setup test database
        async with AsyncSession() as session:
            yield session
            # Cleanup after test
            await session.rollback()

    async def test_create_resource_integration(self, client, db_session):
        \"\"\"Test creating resource through API with database.\"\"\"
        # Given
        payload = {
            "name": "Test Resource",
            "description": "Integration test"
        }

        # When
        response = await client.post("/api/resources", json=payload)

        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]

        # Verify database
        result = await db_session.get(Resource, data["id"])
        assert result is not None
        assert result.name == payload["name"]
"""

    def _get_e2e_test_template(self) -> str:
        """Get E2E test template."""
        return """
import { test, expect } from '@playwright/test';

test.describe('User Authentication Flow', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/');
    });

    test('complete login flow', async ({ page }) => {
        // Navigate to login
        await page.click('text=Sign In');
        await expect(page).toHaveURL('/login');

        // Fill login form
        await page.fill('[name="email"]', 'test@example.com');
        await page.fill('[name="password"]', 'testpassword123');

        // Submit form
        await page.click('button[type="submit"]');

        // Verify redirect to dashboard
        await expect(page).toHaveURL('/dashboard');
        await expect(page.locator('h1')).toContainText('Welcome');

        // Verify user menu
        await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
    });

    test('handle login errors', async ({ page }) => {
        await page.goto('/login');

        // Submit with invalid credentials
        await page.fill('[name="email"]', 'wrong@example.com');
        await page.fill('[name="password"]', 'wrongpassword');
        await page.click('button[type="submit"]');

        // Verify error message
        await expect(page.locator('.error-message')).toContainText('Invalid credentials');
        await expect(page).toHaveURL('/login');
    });
});
"""

    def _get_performance_test_template(self) -> str:
        """Get performance test template."""
        return """
from locust import HttpUser, task, between
import json

class APIPerformanceTest(HttpUser):
    \"\"\"Performance tests for API endpoints.\"\"\"
    wait_time = between(1, 3)

    def on_start(self):
        \"\"\"Setup: authenticate user.\"\"\"
        response = self.client.post("/auth/login", json={
            "email": "perf@test.com",
            "password": "testpass"
        })
        self.token = response.json()["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_resources(self):
        \"\"\"Test GET /resources endpoint.\"\"\"
        with self.client.get("/api/resources",
                           headers=self.headers,
                           catch_response=True) as response:
            if response.elapsed.total_seconds() > 1.0:
                response.failure("Response time > 1s")

    @task(1)
    def create_resource(self):
        \"\"\"Test POST /resources endpoint.\"\"\"
        payload = {
            "name": f"Resource {self.environment.runner.user_count}",
            "value": 100
        }
        self.client.post("/api/resources",
                        json=payload,
                        headers=self.headers)
"""

    def _get_test_strategy_template(self) -> str:
        """Get test strategy template."""
        return """
# Test Strategy Document

## Testing Objectives
- Ensure functional correctness
- Validate performance requirements
- Verify security standards
- Confirm accessibility compliance

## Test Levels
1. **Unit Tests** (70%)
   - Component logic
   - Utility functions
   - Data transformations

2. **Integration Tests** (20%)
   - API endpoints
   - Database operations
   - External services

3. **E2E Tests** (10%)
   - Critical user journeys
   - Cross-browser compatibility
   - Mobile responsiveness

## Test Types
- Functional Testing
- Performance Testing
- Security Testing
- Accessibility Testing
- Usability Testing

## Success Criteria
- 80% code coverage minimum
- All critical paths tested
- Zero high-severity bugs
- Performance SLAs met
- WCAG 2.1 AA compliance
"""


# Factory function for easy QA Agent creation
async def create_qa_agent(custom_config: Optional[Dict[str, Any]] = None) -> QAEngineerAgent:
    """Create and initialize a QA Engineer Agent with optional custom configuration."""

    config_params = custom_config or {}
    config = QAAgentConfig(**config_params)

    agent = QAEngineerAgent(config)
    await agent.initialize()

    return agent


# Example usage and testing
if __name__ == "__main__":

    async def test_qa_agent():
        """Test QA Engineer Agent functionality."""

        # Create QA Agent
        qa = await create_qa_agent()

        # Test creation task
        test_task = EnhancedTask(
            task_type=TaskType.TESTING,
            prompt="Create comprehensive unit tests for a user authentication service that handles login, logout, and token refresh. Include tests for success cases, error handling, and edge cases.",
            complexity=6,
            metadata={
                "test_type": "unit",
                "framework": "pytest",
                "coverage_target": "90%"
            }
        )

        print("🧪 Testing QA Agent - Test Creation")
        result = await qa.process_task(test_task)
        print(f"Success: {result.success}")
        print(f"Cost: ${result.cost:.4f}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Model used: {result.model_used}")
        print("\n" + "="*80)
        print(result.output[:1000] + "..." if len(result.output) > 1000 else result.output)

        # Get agent status
        status = qa.get_status()
        print("\n📊 QA Agent Status:")
        print(f"Tasks completed: {status['tasks_completed']}")
        print(f"Success rate: {status['success_rate']:.1%}")
        print(f"Total cost: ${status['total_cost']:.4f}")

        await qa.stop()

    # Run test
    # import asyncio
    # asyncio.run(test_qa_agent())
