"""
Enhanced mock provider with better backend development responses.
"""

from core.routing.providers.mock_provider import MockProvider, MockConfig

class EnhancedMockProvider(MockProvider):
    """Enhanced mock provider with specialized backend responses."""
    
    def _generate_mock_content(self, user_content: str) -> str:
        """Generate enhanced mock content with better backend responses."""
        user_lower = user_content.lower()
        
        # Backend/FastAPI development responses
        if any(word in user_lower for word in ["fastapi", "endpoint", "api", "backend", "post", "users", "profile"]):
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