"""
Frontend Developer Agent - Specializes in client-side development and UI implementation.

This agent focuses on:
- React/Vue component development
- State management (Redux, Zustand, Pinia)
- UI/UX implementation with modern frameworks
- Frontend testing (Jest, React Testing Library, Playwright)
- API integration and data fetching
- Responsive design and accessibility
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base.enhanced_agent import (
    AgentCapability,
    EnhancedAgentConfig,
    EnhancedBaseAgent,
    EnhancedTask,
)
from agents.base.types import AgentType, TaskType
from core.routing.providers.base import LLMResponse
from core.routing.router import RoutingStrategy


class FrontendAgentConfig(EnhancedAgentConfig):
    """Enhanced configuration for Frontend Developer Agent."""

    def __init__(self, **kwargs):
        # Set Frontend Developer-specific defaults
        defaults = {
            "agent_type": AgentType.FRONTEND_DEV,
            "name": "AIOSv3 Frontend Developer",
            "description": "Frontend Developer agent specializing in React, Vue, and modern UI development",
            "capabilities": [
                AgentCapability.CODE_GENERATION,
                AgentCapability.UI_DESIGN,
                AgentCapability.TESTING,
                AgentCapability.DOCUMENTATION
            ],
            "default_routing_strategy": RoutingStrategy.PERFORMANCE_OPTIMIZED,
            "max_tokens": 6144,  # Higher for code generation
            "temperature": 0.3,  # Slightly higher for creative UI solutions
            "health_check_interval": 15
        }
        # Override with provided kwargs
        defaults.update(kwargs)
        super().__init__(**defaults)


class FrontendDeveloperAgent(EnhancedBaseAgent):
    """
    Frontend Developer Agent for client-side development.
    
    Specializes in:
    - React component development with hooks and functional patterns
    - Vue 3 composition API and component design
    - State management (Redux Toolkit, Zustand, Pinia)
    - UI frameworks (Tailwind CSS, Material-UI, Ant Design)
    - Frontend testing (Jest, React Testing Library, Vitest)
    - API integration with Axios/Fetch
    - Responsive design and accessibility (WCAG)
    """

    def __init__(self, config: Optional[FrontendAgentConfig] = None):
        """Initialize Frontend Developer Agent with specialized configuration."""
        if config is None:
            config = FrontendAgentConfig()

        super().__init__(config)

        # Frontend-specific knowledge areas
        self.expertise_areas = [
            "react",
            "vue",
            "typescript",
            "javascript",
            "tailwindcss",
            "jest",
            "webpack",
            "vite",
            "state_management",
            "ui_design",
            "accessibility",
            "responsive_design"
        ]

        # Code templates and patterns
        self.code_templates = {
            "react_component": self._get_react_template(),
            "vue_component": self._get_vue_template(),
            "redux_slice": self._get_redux_template(),
            "jest_test": self._get_test_template(),
            "api_service": self._get_api_service_template()
        }

        # Quality standards
        self.quality_standards = {
            "code_style": "Follow ESLint and Prettier standards",
            "component_design": "Small, reusable, and testable components",
            "state_management": "Predictable state updates with proper patterns",
            "accessibility": "WCAG 2.1 AA compliance",
            "performance": "Lazy loading, code splitting, optimized renders",
            "testing": "Unit tests for logic, integration tests for user flows"
        }

    async def _on_initialize(self) -> None:
        """Frontend Agent initialization - load development knowledge."""
        # Store Frontend Developer expertise
        await self.store_knowledge(
            content="Frontend Developer Agent specialized in React, Vue, and modern JavaScript/TypeScript development",
            category="agent_identity",
            keywords=["frontend", "react", "vue", "typescript", "ui", "ux"]
        )

        # Store development best practices
        best_practices = """
        Frontend Development Best Practices:
        1. Component Design: Small, focused, reusable components
        2. State Management: Immutable updates, single source of truth
        3. Performance: Virtual DOM optimization, lazy loading, memoization
        4. Accessibility: Semantic HTML, ARIA labels, keyboard navigation
        5. Testing: Component tests, integration tests, E2E tests
        6. API Integration: Error handling, loading states, caching
        7. Responsive Design: Mobile-first, fluid layouts, breakpoints
        """

        await self.store_knowledge(
            content=best_practices,
            category="development_practices",
            keywords=["best_practices", "components", "state", "testing", "accessibility"]
        )

        # Store project-specific context
        project_context = """
        AIOSv3 Frontend Stack:
        - React 18 with TypeScript for primary UI
        - Vue 3 as alternative framework option
        - Tailwind CSS for utility-first styling
        - Zustand/Redux Toolkit for state management
        - Axios for API communication
        - Jest + React Testing Library for testing
        - Vite for build tooling
        - ESLint + Prettier for code quality
        """

        await self.store_knowledge(
            content=project_context,
            category="project_context",
            keywords=["aiosv3", "stack", "framework", "tooling"]
        )

    async def _on_shutdown(self) -> None:
        """Frontend Agent shutdown - save work context."""
        # Could save current development context or progress
        pass

    async def _process_response(self, response: LLMResponse, task: EnhancedTask) -> str:
        """Process and structure Frontend Developer responses with code formatting."""
        content = response.content

        # Structure different types of frontend development responses
        if task.task_type == TaskType.CODE_GENERATION:
            return self._format_code_response(content, task)
        elif task.task_type == TaskType.SYSTEM_DESIGN:
            return self._format_ui_response(content, task)
        elif task.task_type == TaskType.TESTING:
            return self._format_testing_response(content, task)
        else:
            return self._format_general_frontend_response(content, task)

    def _format_code_response(self, content: str, task: EnhancedTask) -> str:
        """Format code generation responses with proper structure."""
        return f"""# 🎨 Frontend Code Implementation

## Task Summary
{task.prompt}

## Implementation

{content}

## Code Quality Checklist
- [ ] Follows ESLint and Prettier standards
- [ ] Components are reusable and testable
- [ ] Proper TypeScript types/interfaces
- [ ] Accessibility attributes included
- [ ] Loading and error states handled
- [ ] Responsive design implemented
- [ ] Unit tests written

## Testing Notes
{self._extract_testing_guidance(content)}

## Next Steps
{self._extract_implementation_steps(content)}

---
*Frontend Developer Agent | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_ui_response(self, content: str, task: EnhancedTask) -> str:
        """Format UI development responses."""
        return f"""# 🎨 UI Component Implementation

## Component Overview
{task.prompt}

## UI Implementation

{content}

## UI/UX Considerations
- **Accessibility**: WCAG 2.1 AA compliance
- **Responsive Design**: Mobile, tablet, desktop breakpoints
- **Performance**: Optimized rendering and loading
- **User Experience**: Intuitive interactions and feedback
- **Design System**: Consistent with project standards
- **Browser Support**: Modern browsers + graceful degradation

## Component Usage
{self._extract_usage_examples(content)}

## Styling Notes
{self._extract_styling_notes(content)}

---
*Frontend UI Developer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_testing_response(self, content: str, task: EnhancedTask) -> str:
        """Format testing implementation responses."""
        return f"""# 🧪 Frontend Testing Implementation

## Testing Scope
{task.prompt}

## Test Implementation

{content}

## Testing Coverage
- **Unit Tests**: Component logic and utilities
- **Integration Tests**: Component interactions
- **Accessibility Tests**: A11y compliance checks
- **Visual Tests**: UI consistency (if applicable)
- **E2E Tests**: User flow validation

## Test Execution
{self._extract_test_execution_notes(content)}

## Coverage Goals
{self._extract_coverage_notes(content)}

---
*Frontend Testing Specialist | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_general_frontend_response(self, content: str, task: EnhancedTask) -> str:
        """Format general frontend development responses."""
        return f"""# ⚛️ Frontend Development Task

## Requirement
{task.prompt}

## Solution

{content}

## Implementation Notes
{self._extract_implementation_notes(content)}

## Quality Assurance
{self._extract_qa_notes(content)}

---
*Frontend Developer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _extract_testing_guidance(self, content: str) -> str:
        """Extract testing guidance from response."""
        test_patterns = [
            r"(?:## Testing|# Testing|Test.*:)(.*?)(?=\n#|\n##|\Z)",
            r"(?:jest|test.*case|describe.*it)(.*?)(?=\n|\Z)"
        ]

        for pattern in test_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Implement unit tests for all components and integration tests for user interactions."

    def _extract_implementation_steps(self, content: str) -> str:
        """Extract implementation steps from response."""
        return "1. Review component structure\n2. Run tests\n3. Check accessibility\n4. Test responsive design\n5. Optimize performance"

    def _extract_usage_examples(self, content: str) -> str:
        """Extract component usage examples."""
        return "Import and use the component with proper props. See implementation for detailed usage."

    def _extract_styling_notes(self, content: str) -> str:
        """Extract styling considerations."""
        return "Uses Tailwind utility classes. Ensure dark mode compatibility and responsive breakpoints."

    def _extract_test_execution_notes(self, content: str) -> str:
        """Extract test execution guidance."""
        return "Run tests with: `npm test` or `npm run test:coverage` for coverage report"

    def _extract_coverage_notes(self, content: str) -> str:
        """Extract coverage requirements."""
        return "Target minimum 80% test coverage. Focus on user interactions and edge cases."

    def _extract_implementation_notes(self, content: str) -> str:
        """Extract general implementation notes."""
        return "Follow React/Vue best practices and ensure TypeScript types are properly defined."

    def _extract_qa_notes(self, content: str) -> str:
        """Extract QA considerations."""
        return "Test across browsers, validate accessibility, and ensure responsive design works."

    async def _customize_prompt(self, task: EnhancedTask, context: str) -> str:
        """Customize prompts with Frontend Developer-specific expertise and standards."""

        # Build Frontend Developer-specific context
        frontend_context = """
You are a Senior Frontend Developer working on AIOSv3, a modular AI agent platform. Your expertise includes:

**Core Technologies:**
- React 18 with hooks and functional components
- Vue 3 with Composition API
- TypeScript for type-safe development
- Tailwind CSS for utility-first styling
- State management (Redux Toolkit, Zustand, Pinia)
- Modern build tools (Vite, Webpack)

**Development Standards:**
- Follow ESLint and Prettier configuration
- Write small, focused, reusable components
- Implement proper TypeScript types and interfaces
- Ensure WCAG 2.1 AA accessibility compliance
- Include comprehensive error handling and loading states
- Write unit and integration tests for all components

**UI/UX Principles:**
- Mobile-first responsive design
- Intuitive user interactions with proper feedback
- Consistent design system usage
- Performance optimization (lazy loading, memoization)
- Progressive enhancement approach
- Cross-browser compatibility

**Quality Requirements:**
- All code must be production-ready
- Components must be fully typed with TypeScript
- Include proper error boundaries and fallbacks
- Implement loading and error states
- Write corresponding tests
- Ensure accessibility standards are met
"""

        # Task-specific guidance
        task_guidance = {
            TaskType.CODE_GENERATION: """
Focus on:
- Clean, modular component architecture
- Proper separation of concerns
- Reusable hooks for shared logic
- Type-safe props and state
- Performance optimization
- Accessibility from the start
""",
            TaskType.SYSTEM_DESIGN: """
Focus on:
- User-centered design principles
- Responsive layout implementation
- Consistent spacing and typography
- Interactive feedback and animations
- Dark mode support
- Accessibility features
""",
            TaskType.TESTING: """
Focus on:
- Component unit tests
- User interaction tests
- Accessibility testing
- Visual regression tests (if applicable)
- Performance testing
- Cross-browser testing
"""
        }

        guidance = task_guidance.get(task.task_type, """
Provide high-quality frontend solution following best practices.
""")

        return f"""{frontend_context}

{guidance}

**Task Details:**
- **Complexity**: {task.complexity}/10
- **Privacy Sensitive**: {task.privacy_sensitive}
- **Context**: {context if context else "No additional context provided"}

**Current Task:**
{task.prompt}

Please provide a complete, production-ready frontend solution with:
1. Clean, well-structured components
2. Proper TypeScript types
3. Accessibility features
4. Responsive design
5. Error handling and loading states
6. Corresponding tests

Ensure all code follows project standards and modern best practices."""

    def _get_react_template(self) -> str:
        """Get React component template."""
        return """
import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';

interface ComponentProps {
  // Define props with TypeScript
}

export const ComponentName: React.FC<ComponentProps> = ({ /* props */ }) => {
  const [state, setState] = useState<StateType>(initialState);
  
  // Data fetching
  const { data, isLoading, error } = useQuery({
    queryKey: ['dataKey'],
    queryFn: fetchData,
  });
  
  // Event handlers
  const handleAction = async () => {
    try {
      // Implementation
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <div className="container">
      {/* Component JSX */}
    </div>
  );
};
"""

    def _get_vue_template(self) -> str:
        """Get Vue component template."""
        return """
<template>
  <div class="component-container">
    <div v-if="isLoading" class="loading">
      <LoadingSpinner />
    </div>
    <div v-else-if="error" class="error">
      <ErrorMessage :error="error" />
    </div>
    <div v-else>
      <!-- Component template -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useQuery } from '@tanstack/vue-query';

interface Props {
  // Define props
}

const props = defineProps<Props>();
const emit = defineEmits<{
  // Define events
}>();

// State
const state = ref<StateType>(initialValue);

// Composables
const { data, isLoading, error } = useQuery({
  queryKey: ['dataKey'],
  queryFn: fetchData,
});

// Methods
const handleAction = async () => {
  try {
    // Implementation
  } catch (error) {
    console.error('Error:', error);
  }
};

// Lifecycle
onMounted(() => {
  // Setup logic
});
</script>

<style scoped>
/* Component styles */
</style>
"""

    def _get_redux_template(self) -> str:
        """Get Redux slice template."""
        return """
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../../store';

interface SliceState {
  // Define state shape
}

const initialState: SliceState = {
  // Initial values
};

const sliceName = createSlice({
  name: 'sliceName',
  initialState,
  reducers: {
    actionName: (state, action: PayloadAction<PayloadType>) => {
      // State update logic
    },
  },
});

export const { actionName } = sliceName.actions;
export const selectState = (state: RootState) => state.sliceName;
export default sliceName.reducer;
"""

    def _get_test_template(self) -> str:
        """Get frontend test template."""
        return """
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName />);
    expect(screen.getByRole('heading')).toBeInTheDocument();
  });
  
  it('handles user interaction', async () => {
    const user = userEvent.setup();
    render(<ComponentName />);
    
    const button = screen.getByRole('button');
    await user.click(button);
    
    await waitFor(() => {
      expect(screen.getByText('Expected text')).toBeInTheDocument();
    });
  });
  
  it('is accessible', () => {
    const { container } = render(<ComponentName />);
    expect(container).toBeAccessible();
  });
});
"""

    def _get_api_service_template(self) -> str:
        """Get API service template."""
        return """
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // API methods
  async getData() {
    const response = await apiClient.get('/endpoint');
    return response.data;
  },
  
  async postData(data: DataType) {
    const response = await apiClient.post('/endpoint', data);
    return response.data;
  },
};
"""


# Factory function for easy Frontend Agent creation
async def create_frontend_agent(custom_config: Optional[Dict[str, Any]] = None) -> FrontendDeveloperAgent:
    """Create and initialize a Frontend Developer Agent with optional custom configuration."""

    config_params = custom_config or {}
    config = FrontendAgentConfig(**config_params)

    agent = FrontendDeveloperAgent(config)
    await agent.initialize()

    return agent


# Example usage and testing
if __name__ == "__main__":
    
    async def test_frontend_agent():
        """Test Frontend Developer Agent functionality."""
        
        # Create Frontend Agent
        frontend = await create_frontend_agent()
        
        # Test React component task
        component_task = EnhancedTask(
            task_type=TaskType.CODE_GENERATION,
            prompt="Create a React component for user authentication that includes a login form with email/password fields, validation, error handling, and integration with a backend API.",
            complexity=6,
            metadata={
                "framework": "react",
                "features": ["form validation", "api integration", "error handling"],
                "styling": "tailwindcss"
            }
        )
        
        print("🎨 Testing Frontend Agent - React Component Development")
        result = await frontend.process_task(component_task)
        print(f"Success: {result.success}")
        print(f"Cost: ${result.cost:.4f}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Model used: {result.model_used}")
        print("\n" + "="*80)
        print(result.output[:1000] + "..." if len(result.output) > 1000 else result.output)
        
        # Get agent status
        status = frontend.get_status()
        print("\n📊 Frontend Agent Status:")
        print(f"Tasks completed: {status['tasks_completed']}")
        print(f"Success rate: {status['success_rate']:.1%}")
        print(f"Total cost: ${status['total_cost']:.4f}")
        
        await frontend.stop()

    # Run test
    # import asyncio
    # asyncio.run(test_frontend_agent())