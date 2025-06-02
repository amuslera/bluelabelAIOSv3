"""
Enhanced mock provider with better backend development responses.
"""

from core.routing.providers.mock_provider import MockProvider, MockConfig

class EnhancedMockProvider(MockProvider):
    """Enhanced mock provider with specialized backend responses."""
    
    def _generate_mock_content(self, user_content: str) -> str:
        """Generate enhanced mock content with better backend responses."""
        user_lower = user_content.lower()
        
        # Frontend/React/Vue development responses
        if any(word in user_lower for word in ["react", "vue", "frontend", "component", "ui", "login", "form", "authentication"]):
            return self._mock_frontend_development()
        
        # Backend/FastAPI development responses
        elif any(word in user_lower for word in ["fastapi", "endpoint", "api", "backend", "post", "users", "profile"]):
            return self._mock_fastapi_development()
        
        # Python code generation
        elif any(word in user_lower for word in ["python", "class", "function", "def", "import"]):
            return self._mock_python_code()
        
        # Testing responses
        elif any(word in user_lower for word in ["test", "pytest", "unit test"]):
            return self._mock_testing_code()
        
        # Default to parent's logic
        else:
            return super()._generate_mock_content(user_content)
    
    def _mock_fastapi_development(self) -> str:
        """Generate mock FastAPI backend development response."""
        return """# 🚀 Backend Code Implementation

## Task Summary
Create a FastAPI endpoint for a simple user profile system with validation and testing.

## Implementation

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional
import uuid
from datetime import datetime
import re

router = APIRouter(prefix="/users", tags=["users"])

# Request Models
class UserProfileRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., description="User's email address")
    age: int = Field(..., gt=0, le=120, description="User's age")
    
    @validator('email')
    def validate_email(cls, v):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

# Response Models
class UserProfileResponse(BaseModel):
    user_id: str
    name: str
    email: str
    age: int
    created_at: datetime
    message: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

# Endpoint Implementation
@router.post("/profile", 
             response_model=UserProfileResponse,
             status_code=201,
             responses={
                 400: {"model": ErrorResponse, "description": "Invalid input data"},
                 422: {"model": ErrorResponse, "description": "Validation error"}
             })
async def create_user_profile(request: UserProfileRequest):
    \"\"\"
    Create a new user profile with validation.
    
    - **name**: User's full name (1-100 characters)
    - **email**: Valid email address
    - **age**: Age between 1 and 120
    
    Returns the created user profile with generated ID.
    \"\"\"
    try:
        # Generate unique user ID
        user_id = str(uuid.uuid4())
        
        # Simulate business logic (e.g., check if email exists)
        # In real implementation, this would interact with database
        
        # Create response
        user_profile = UserProfileResponse(
            user_id=user_id,
            name=request.name,
            email=request.email,
            age=request.age,
            created_at=datetime.utcnow(),
            message="User profile created successfully"
        )
        
        return user_profile
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred"
        )

# Health check endpoint
@router.get("/health")
async def health_check():
    \"\"\"Health check for user service.\"\"\"
    return {"status": "healthy", "service": "user-profile"}
```

## Unit Tests

```python
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from main import router  # Assuming main.py contains the router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

class TestUserProfile:
    \"\"\"Test suite for user profile endpoints.\"\"\"
    
    def test_create_user_profile_success(self):
        \"\"\"Test successful user profile creation.\"\"\"
        payload = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30
        }
        
        response = client.post("/users/profile", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john.doe@example.com"
        assert data["age"] == 30
        assert "user_id" in data
        assert "created_at" in data
        assert data["message"] == "User profile created successfully"
    
    def test_create_user_profile_invalid_email(self):
        \"\"\"Test validation with invalid email.\"\"\"
        payload = {
            "name": "John Doe",
            "email": "invalid-email",
            "age": 30
        }
        
        response = client.post("/users/profile", json=payload)
        
        assert response.status_code == 422
        error_data = response.json()
        assert "email" in str(error_data).lower()
    
    def test_create_user_profile_invalid_age(self):
        \"\"\"Test validation with invalid age.\"\"\"
        payload = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": -5
        }
        
        response = client.post("/users/profile", json=payload)
        
        assert response.status_code == 422
    
    def test_create_user_profile_empty_name(self):
        \"\"\"Test validation with empty name.\"\"\"
        payload = {
            "name": "",
            "email": "john.doe@example.com",
            "age": 30
        }
        
        response = client.post("/users/profile", json=payload)
        
        assert response.status_code == 422
    
    def test_create_user_profile_missing_fields(self):
        \"\"\"Test validation with missing required fields.\"\"\"
        payload = {
            "name": "John Doe"
            # Missing email and age
        }
        
        response = client.post("/users/profile", json=payload)
        
        assert response.status_code == 422
    
    def test_health_check(self):
        \"\"\"Test health check endpoint.\"\"\"
        response = client.get("/users/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "user-profile"

# Integration test
class TestUserProfileIntegration:
    \"\"\"Integration tests for user profile workflow.\"\"\"
    
    def test_full_user_creation_workflow(self):
        \"\"\"Test complete user creation workflow.\"\"\"
        # Test data
        users = [
            {"name": "Alice Smith", "email": "alice@example.com", "age": 25},
            {"name": "Bob Johnson", "email": "bob@example.com", "age": 35},
            {"name": "Carol Wilson", "email": "carol@example.com", "age": 28}
        ]
        
        created_users = []
        
        for user_data in users:
            response = client.post("/users/profile", json=user_data)
            assert response.status_code == 201
            
            user_profile = response.json()
            created_users.append(user_profile)
            
            # Verify all fields are present and correct
            assert user_profile["name"] == user_data["name"]
            assert user_profile["email"] == user_data["email"]
            assert user_profile["age"] == user_data["age"]
            assert len(user_profile["user_id"]) > 0
        
        # Verify all users have unique IDs
        user_ids = [user["user_id"] for user in created_users]
        assert len(set(user_ids)) == len(user_ids)
```

## Code Quality Checklist
- [x] Follows PEP 8 style guidelines
- [x] Includes proper error handling
- [x] Has comprehensive docstrings
- [x] Includes input validation
- [x] Has corresponding unit tests
- [x] No hardcoded secrets or sensitive data

## Testing Notes
Run tests with: `pytest tests/ -v --cov=app --cov-report=html`

## Next Steps
1. Integrate with actual database (PostgreSQL/SQLAlchemy)
2. Add authentication middleware
3. Implement rate limiting
4. Add logging and monitoring
5. Deploy to staging environment

---
*Backend Developer Agent | 2025-06-01 18:58*
"""
    
    def _mock_python_code(self) -> str:
        """Generate mock Python code response."""
        return """# 🐍 Python Implementation

```python
import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DataProcessor:
    \"\"\"Enhanced data processing with async capabilities.\"\"\"
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.processed_count = 0
        
    async def process_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        \"\"\"Process a batch of items asynchronously.\"\"\"
        results = []
        
        for item in items:
            try:
                processed_item = await self._process_single_item(item)
                results.append(processed_item)
                self.processed_count += 1
            except Exception as e:
                logger.error(f"Failed to process item {item.get('id', 'unknown')}: {e}")
                
        return results
    
    async def _process_single_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Process a single item with validation.\"\"\"
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        return {
            **item,
            "processed_at": datetime.utcnow().isoformat(),
            "processor": "DataProcessor",
            "status": "completed"
        }
```

Production-ready Python code with proper error handling and async patterns.
"""
    
    def _mock_testing_code(self) -> str:
        """Generate mock testing code response."""
        return """# 🧪 Backend Testing Implementation

## Testing Scope
Comprehensive test suite for backend functionality with pytest.

## Test Implementation

```python
import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime

class TestUserService:
    \"\"\"Test suite for user service functionality.\"\"\"
    
    @pytest.fixture
    def mock_database(self):
        \"\"\"Mock database connection.\"\"\"
        db = Mock()
        db.execute.return_value = Mock()
        return db
    
    @pytest.fixture
    def user_service(self, mock_database):
        \"\"\"Create user service with mocked dependencies.\"\"\"
        from app.services.user_service import UserService
        return UserService(database=mock_database)
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service, mock_database):
        \"\"\"Test successful user creation.\"\"\"
        # Arrange
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "age": 25
        }
        mock_database.execute.return_value.fetchone.return_value = {
            "id": "user_123",
            **user_data,
            "created_at": datetime.utcnow()
        }
        
        # Act
        result = await user_service.create_user(user_data)
        
        # Assert
        assert result["name"] == user_data["name"]
        assert result["email"] == user_data["email"]
        assert "id" in result
        mock_database.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, user_service, mock_database):
        \"\"\"Test user creation with duplicate email.\"\"\"
        # Arrange
        user_data = {"name": "Test", "email": "existing@example.com", "age": 25}
        mock_database.execute.side_effect = Exception("Email already exists")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Email already exists"):
            await user_service.create_user(user_data)
    
    def test_validate_email_format(self, user_service):
        \"\"\"Test email validation.\"\"\"
        valid_emails = [
            "test@example.com",
            "user.name+tag@domain.co.uk",
            "user123@test-domain.com"
        ]
        
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user@domain",
            ""
        ]
        
        for email in valid_emails:
            assert user_service.validate_email(email) == True
            
        for email in invalid_emails:
            assert user_service.validate_email(email) == False

@pytest.mark.integration
class TestUserAPI:
    \"\"\"Integration tests for user API endpoints.\"\"\"
    
    @pytest.fixture
    def client(self):
        \"\"\"Create test client.\"\"\"
        from fastapi.testclient import TestClient
        from app.main import app
        return TestClient(app)
    
    def test_create_user_endpoint_success(self, client):
        \"\"\"Test successful user creation via API.\"\"\"
        payload = {
            "name": "Integration Test User",
            "email": "integration@test.com",
            "age": 30
        }
        
        response = client.post("/users/profile", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["email"] == payload["email"]
        assert "user_id" in data
    
    def test_create_user_endpoint_validation_error(self, client):
        \"\"\"Test API validation errors.\"\"\"
        invalid_payloads = [
            {"name": "", "email": "test@example.com", "age": 25},  # Empty name
            {"name": "Test", "email": "invalid-email", "age": 25},  # Invalid email
            {"name": "Test", "email": "test@example.com", "age": -1},  # Invalid age
            {"email": "test@example.com", "age": 25},  # Missing name
        ]
        
        for payload in invalid_payloads:
            response = client.post("/users/profile", json=payload)
            assert response.status_code == 422

# Performance tests
@pytest.mark.performance
class TestPerformance:
    \"\"\"Performance tests for critical paths.\"\"\"
    
    @pytest.mark.asyncio
    async def test_concurrent_user_creation(self, user_service):
        \"\"\"Test concurrent user creation performance.\"\"\"
        import time
        
        # Create test data
        users = [
            {"name": f"User {i}", "email": f"user{i}@test.com", "age": 25}
            for i in range(100)
        ]
        
        # Measure concurrent creation time
        start_time = time.time()
        
        tasks = [user_service.create_user(user) for user in users]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Performance assertions
        assert duration < 5.0  # Should complete within 5 seconds
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) == len(users)
```

## Testing Coverage
- **Unit Tests**: Business logic and individual functions
- **Integration Tests**: API endpoints and database interactions  
- **Edge Cases**: Error conditions and boundary testing
- **Performance Tests**: Load and stress testing considerations

## Test Execution
Run tests with: `pytest tests/ -v --cov=app --cov-report=html`

## Coverage Goals
Target minimum 80% test coverage. Focus on critical business logic and error paths.

---
*Backend Testing Specialist | 2025-06-01 18:58*
"""
    
    def _mock_frontend_development(self) -> str:
        """Generate mock React/Vue frontend development response."""
        return """# 🎨 Frontend Code Implementation

## Task Summary
Create a React component for user authentication that includes a login form with email/password fields, validation, error handling, and integration with a backend API.

## Implementation

```tsx
// LoginForm.tsx
import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { apiService } from '../../services/api';

interface LoginFormData {
  email: string;
  password: string;
}

interface LoginResponse {
  token: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<Partial<LoginFormData>>({});
  const [showPassword, setShowPassword] = useState(false);

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: (data: LoginFormData) => apiService.auth.login(data),
    onSuccess: (response: LoginResponse) => {
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      toast.success('Login successful!');
      navigate('/dashboard');
    },
    onError: (error: any) => {
      const message = error.response?.data?.message || 'Login failed';
      toast.error(message);
    }
  });

  // Validation
  const validateForm = (): boolean => {
    const newErrors: Partial<LoginFormData> = {};
    
    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      loginMutation.mutate(formData);
    }
  };

  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error for this field
    if (errors[name as keyof LoginFormData]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined
      }));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Welcome back! Please enter your details.
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            {/* Email Field */}
            <div className="mb-4">
              <label htmlFor="email" className="sr-only">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.email ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Email address"
                value={formData.email}
                onChange={handleChange}
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? 'email-error' : undefined}
              />
              {errors.email && (
                <p id="email-error" className="mt-2 text-sm text-red-600">
                  {errors.email}
                </p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  className={`appearance-none rounded-none relative block w-full px-3 py-2 pr-10 border ${
                    errors.password ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleChange}
                  aria-invalid={!!errors.password}
                  aria-describedby={errors.password ? 'password-error' : undefined}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? (
                    <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  ) : (
                    <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  )}
                </button>
              </div>
              {errors.password && (
                <p id="password-error" className="mt-2 text-sm text-red-600">
                  {errors.password}
                </p>
              )}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>

            <div className="text-sm">
              <a href="/forgot-password" className="font-medium text-indigo-600 hover:text-indigo-500">
                Forgot your password?
              </a>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loginMutation.isPending}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loginMutation.isPending ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Signing in...
                </>
              ) : (
                'Sign in'
              )}
            </button>
          </div>

          <div className="text-center">
            <span className="text-sm text-gray-600">
              Don't have an account?{' '}
              <a href="/signup" className="font-medium text-indigo-600 hover:text-indigo-500">
                Sign up
              </a>
            </span>
          </div>
        </form>
      </div>
    </div>
  );
};
```

```tsx
// LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { LoginForm } from './LoginForm';
import { apiService } from '../../services/api';

// Mock API service
jest.mock('../../services/api');

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false }
  }
});

const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      {children}
    </BrowserRouter>
  </QueryClientProvider>
);

describe('LoginForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders login form correctly', () => {
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    expect(screen.getByText('Sign in to your account')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Email address')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeInTheDocument();
  });

  it('validates email field', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    const submitButton = screen.getByRole('button', { name: 'Sign in' });
    
    // Submit without email
    await user.click(submitButton);
    expect(screen.getByText('Email is required')).toBeInTheDocument();
    
    // Invalid email format
    const emailInput = screen.getByPlaceholderText('Email address');
    await user.type(emailInput, 'invalid-email');
    await user.click(submitButton);
    expect(screen.getByText('Invalid email format')).toBeInTheDocument();
  });

  it('validates password field', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    const emailInput = screen.getByPlaceholderText('Email address');
    const passwordInput = screen.getByPlaceholderText('Password');
    const submitButton = screen.getByRole('button', { name: 'Sign in' });
    
    // Valid email, short password
    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInput, 'short');
    await user.click(submitButton);
    
    expect(screen.getByText('Password must be at least 8 characters')).toBeInTheDocument();
  });

  it('toggles password visibility', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    const passwordInput = screen.getByPlaceholderText('Password');
    const toggleButton = screen.getByLabelText('Show password');
    
    // Initially password is hidden
    expect(passwordInput).toHaveAttribute('type', 'password');
    
    // Click to show password
    await user.click(toggleButton);
    expect(passwordInput).toHaveAttribute('type', 'text');
    
    // Click to hide password again
    await user.click(screen.getByLabelText('Hide password'));
    expect(passwordInput).toHaveAttribute('type', 'password');
  });

  it('is accessible', () => {
    const { container } = render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    // Check for proper ARIA attributes
    const emailInput = screen.getByPlaceholderText('Email address');
    const passwordInput = screen.getByPlaceholderText('Password');
    
    expect(emailInput).toHaveAttribute('aria-invalid', 'false');
    expect(passwordInput).toHaveAttribute('aria-invalid', 'false');
    
    // Check for labels (even if visually hidden)
    expect(screen.getByLabelText('Email address')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
  });
});
```

## Code Quality Checklist
- ✅ Follows ESLint and Prettier standards
- ✅ Components are reusable and testable
- ✅ Proper TypeScript types/interfaces
- ✅ Accessibility attributes included
- ✅ Loading and error states handled
- ✅ Responsive design implemented
- ✅ Unit tests written

## Testing Notes
Run tests with: `npm test` or `npm run test:coverage`

## Next Steps
1. Add form validation library (react-hook-form or formik)
2. Implement remember me functionality
3. Add social login options
4. Create signup form component
5. Add password strength indicator

---
*Frontend Developer Agent | Generated with enhanced mock provider*
"""