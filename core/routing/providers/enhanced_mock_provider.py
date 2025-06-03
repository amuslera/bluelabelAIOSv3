"""
Enhanced mock provider with better backend development responses.
"""

from core.routing.providers.mock_provider import MockProvider


class EnhancedMockProvider(MockProvider):
    """Enhanced mock provider with specialized backend responses."""

    def _generate_mock_content(self, user_content: str) -> str:
        """Generate enhanced mock content with better backend responses."""
        user_lower = user_content.lower()

        # QA/Testing responses (check first as it's most specific)
        if any(word in user_lower for word in ["test", "pytest", "unit test", "qa", "quality", "coverage", "testing"]):
            return self._mock_qa_testing_code()

        # DevOps/Infrastructure responses
        elif any(word in user_lower for word in ["terraform", "kubernetes", "docker", "infrastructure", "deployment", "cicd", "monitoring", "devops"]):
            return self._mock_devops_infrastructure()

        # Frontend/React/Vue development responses
        elif any(word in user_lower for word in ["react", "vue", "frontend", "component", "ui", "login form", "user interface"]):
            return self._mock_frontend_development()

        # Backend/FastAPI development responses
        elif any(word in user_lower for word in ["fastapi", "endpoint", "api", "backend", "post", "users", "profile"]):
            return self._mock_fastapi_development()

        # Python code generation
        elif any(word in user_lower for word in ["python", "class", "function", "def", "import"]):
            return self._mock_python_code()

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
    age: Optional[int] = Field(None, ge=0, le=120, description="User's age")

    @validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip()

# Response Models
class UserProfileResponse(BaseModel):
    user_id: str
    name: str
    email: str
    age: Optional[int]
    created_at: datetime
    message: str

# Endpoints
@router.post("/profile", response_model=UserProfileResponse, status_code=201)
async def create_user_profile(user_data: UserProfileRequest):
    \"\"\"
    Create a new user profile.

    Args:
        user_data: User profile information

    Returns:
        UserProfileResponse: Created user profile with ID and timestamp

    Raises:
        HTTPException: If email already exists (example)
    \"\"\"
    try:
        # In real implementation, check if email exists in database
        # if await user_exists(user_data.email):
        #     raise HTTPException(status_code=409, detail="Email already registered")

        # Generate user ID
        user_id = str(uuid.uuid4())

        # In real implementation, save to database
        # await save_user_to_db(user_id, user_data)

        # Return response
        return UserProfileResponse(
            user_id=user_id,
            name=user_data.name,
            email=user_data.email,
            age=user_data.age,
            created_at=datetime.utcnow(),
            message="User profile created successfully"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log error in production
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/profile/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str):
    \"\"\"Get user profile by ID.\"\"\"
    # Example implementation
    # user = await get_user_from_db(user_id)
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # Mock response for now
    return UserProfileResponse(
        user_id=user_id,
        name="Test User",
        email="test@example.com",
        age=25,
        created_at=datetime.utcnow(),
        message="User profile retrieved successfully"
    )

# Health check endpoint
@router.get("/health")
async def health_check():
    \"\"\"Check if the user service is running.\"\"\"
    return {"status": "healthy", "service": "user-profile"}
```

```python
# tests/test_user_profile.py
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.routers.users import router

# Setup test app
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
        error_data = response.json()
        assert "age" in str(error_data).lower()

    def test_create_user_profile_empty_name(self):
        \"\"\"Test validation with empty name.\"\"\"
        payload = {
            "name": "   ",
            "email": "john.doe@example.com",
            "age": 30
        }

        response = client.post("/users/profile", json=payload)

        assert response.status_code == 422

    def test_get_user_profile_success(self):
        \"\"\"Test retrieving user profile.\"\"\"
        user_id = "test-user-123"

        response = client.get(f"/users/profile/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert "name" in data
        assert "email" in data
        assert "created_at" in data

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
            created_user = response.json()
            created_users.append(created_user)

            # Verify we can retrieve the user
            get_response = client.get(f"/users/profile/{created_user['user_id']}")
            assert get_response.status_code == 200

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

    def _mock_qa_testing_code(self) -> str:
        """Generate mock QA testing code response."""
        return """# 🧪 QA Testing Implementation

## Test Requirements
Create comprehensive unit tests for a user authentication service that handles login, logout, and token refresh. Include tests for success cases, error handling, and edge cases.

## Test Implementation

```python
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
import jwt
import bcrypt

from app.services.auth_service import AuthService
from app.models.user import User
from app.exceptions import AuthenticationError, TokenError

class TestAuthService:
    \"\"\"Comprehensive test suite for authentication service.\"\"\"

    @pytest.fixture
    def mock_user_repo(self):
        \"\"\"Mock user repository.\"\"\"
        repo = Mock()
        repo.find_by_email = AsyncMock()
        repo.create = AsyncMock()
        repo.update = AsyncMock()
        return repo

    @pytest.fixture
    def mock_token_store(self):
        \"\"\"Mock token store for session management.\"\"\"
        store = Mock()
        store.store_token = AsyncMock()
        store.get_token = AsyncMock()
        store.revoke_token = AsyncMock()
        return store

    @pytest.fixture
    def auth_service(self, mock_user_repo, mock_token_store):
        \"\"\"Create auth service with mocked dependencies.\"\"\"
        return AuthService(
            user_repository=mock_user_repo,
            token_store=mock_token_store,
            jwt_secret="test-secret-key",
            token_expiry_minutes=30
        )

    @pytest.fixture
    def valid_user(self):
        \"\"\"Create a valid test user.\"\"\"
        hashed_password = bcrypt.hashpw(b"validpass123", bcrypt.gensalt())
        return User(
            id="user-123",
            email="test@example.com",
            password_hash=hashed_password.decode(),
            is_active=True,
            created_at=datetime.utcnow()
        )

    # Success Cases
    @pytest.mark.asyncio
    async def test_login_with_valid_credentials(self, auth_service, mock_user_repo, valid_user):
        \"\"\"Test successful login with valid credentials.\"\"\"
        # Given
        mock_user_repo.find_by_email.return_value = valid_user
        credentials = {"email": "test@example.com", "password": "validpass123"}

        # When
        result = await auth_service.login(credentials)

        # Then
        assert result["success"] is True
        assert "token" in result
        assert "user" in result
        assert result["user"]["email"] == "test@example.com"
        mock_user_repo.find_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_token_generation_contains_required_claims(self, auth_service, valid_user):
        \"\"\"Test JWT token contains all required claims.\"\"\"
        # When
        token = auth_service._generate_token(valid_user)
        decoded = jwt.decode(token, "test-secret-key", algorithms=["HS256"])

        # Then
        assert decoded["sub"] == "user-123"
        assert decoded["email"] == "test@example.com"
        assert "exp" in decoded
        assert "iat" in decoded
        assert decoded["exp"] > decoded["iat"]

    # Error Cases
    @pytest.mark.asyncio
    async def test_login_with_invalid_email(self, auth_service, mock_user_repo):
        \"\"\"Test login fails with non-existent email.\"\"\"
        # Given
        mock_user_repo.find_by_email.return_value = None
        credentials = {"email": "nonexistent@example.com", "password": "anypass"}

        # When/Then
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await auth_service.login(credentials)

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(self, auth_service, mock_user_repo, valid_user):
        \"\"\"Test login fails with incorrect password.\"\"\"
        # Given
        mock_user_repo.find_by_email.return_value = valid_user
        credentials = {"email": "test@example.com", "password": "wrongpassword"}

        # When/Then
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await auth_service.login(credentials)

    # Edge Cases
    @pytest.mark.asyncio
    async def test_login_with_empty_credentials(self, auth_service):
        \"\"\"Test login fails with empty credentials.\"\"\"
        # Given
        test_cases = [
            {"email": "", "password": "password"},
            {"email": "test@example.com", "password": ""},
            {"email": "", "password": ""},
            {},
            None
        ]

        # When/Then
        for credentials in test_cases:
            with pytest.raises((AuthenticationError, ValueError)):
                await auth_service.login(credentials)

    @pytest.mark.parametrize("invalid_email", [
        "notanemail",
        "@example.com",
        "user@",
        "user@.com",
        "user@domain",
        "user space@example.com",
        None,
        123,
        ["user@example.com"]
    ])
    @pytest.mark.asyncio
    async def test_login_with_invalid_email_formats(self, auth_service, invalid_email):
        \"\"\"Test login rejects various invalid email formats.\"\"\"
        # Given
        credentials = {"email": invalid_email, "password": "password"}

        # When/Then
        with pytest.raises((AuthenticationError, ValueError)):
            await auth_service.login(credentials)

# Integration Tests
@pytest.mark.integration
class TestAuthServiceIntegration:
    \"\"\"Integration tests for authentication service with real dependencies.\"\"\"

    @pytest.fixture
    async def real_auth_service(self, test_db, redis_client):
        \"\"\"Create auth service with real dependencies.\"\"\"
        from app.repositories.user_repository import UserRepository
        from app.services.token_store import RedisTokenStore

        user_repo = UserRepository(test_db)
        token_store = RedisTokenStore(redis_client)

        return AuthService(
            user_repository=user_repo,
            token_store=token_store,
            jwt_secret="integration-test-secret",
            token_expiry_minutes=30
        )

    @pytest.mark.asyncio
    async def test_full_authentication_flow(self, real_auth_service):
        \"\"\"Test complete authentication flow: register, login, refresh, logout.\"\"\"
        # Register
        registration_data = {
            "email": "newuser@example.com",
            "password": "securepass123",
            "name": "Test User"
        }
        user = await real_auth_service.register(registration_data)
        assert user["email"] == "newuser@example.com"

        # Login
        login_result = await real_auth_service.login({
            "email": "newuser@example.com",
            "password": "securepass123"
        })
        assert login_result["success"] is True
        token = login_result["token"]

        # Validate token
        validation = await real_auth_service.validate_token(token)
        assert validation["valid"] is True

        # Refresh token
        new_token = await real_auth_service.refresh_token(token)
        assert new_token != token

        # Logout
        logout_result = await real_auth_service.logout(new_token)
        assert logout_result["success"] is True

        # Verify token is revoked
        with pytest.raises(TokenError):
            await real_auth_service.validate_token(new_token)
```

## Quality Checklist
- ✅ Tests are independent and isolated
- ✅ Clear test names following conventions
- ✅ Both happy paths and edge cases covered
- ✅ Proper setup and teardown
- ✅ No hardcoded test data
- ✅ Tests run quickly and reliably
- ✅ Coverage targets met

## Test Execution
Run tests with:
- Unit tests: `pytest tests/unit -v --cov`
- Integration: `pytest tests/integration -v`
- E2E: `playwright test`
- All tests: `npm test && pytest`

## Coverage Analysis
Target: 80% overall, 100% for critical paths. Generate reports with coverage tools.

## Next Steps
1. Run test suite
2. Analyze coverage gaps
3. Add missing edge cases
4. Integrate with CI/CD

---
*QA Engineer Agent | 2025-06-01 19:58*
"""

    def _mock_devops_infrastructure(self) -> str:
        """Generate mock DevOps infrastructure response."""
        return """# 🏗️ Infrastructure Implementation

## Infrastructure Requirements
Create Terraform configuration for a highly available Kubernetes cluster on AWS with auto-scaling, monitoring, and security best practices.

## Infrastructure as Code

```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket  = "aiosv3-terraform-state"
    key     = "infrastructure/terraform.tfstate"
    region  = "us-west-2"
    encrypt = true
  }
}

# VPC Module
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "aiosv3-${var.environment}"
  cidr = "10.0.0.0/16"

  azs             = data.aws_availability_zones.available.names
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false
  enable_dns_hostnames = true

  tags = local.common_tags
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.0"

  cluster_name    = "aiosv3-${var.environment}"
  cluster_version = "1.27"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    application = {
      desired_size = 3
      min_size     = 3
      max_size     = 10

      instance_types = ["t3.large"]

      labels = {
        Environment = var.environment
        Role        = "application"
      }

      taints = []

      update_config = {
        max_unavailable_percentage = 50
      }
    }
  }

  manage_aws_auth_configmap = true

  tags = local.common_tags
}

# RDS Aurora PostgreSQL
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"

  name           = "aiosv3-${var.environment}"
  engine         = "aurora-postgresql"
  engine_version = "15.3"

  instances = {
    1 = {
      instance_class      = "db.r6g.large"
      publicly_accessible = false
    }
    2 = {
      instance_class      = "db.r6g.large"
      publicly_accessible = false
    }
  }

  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name

  create_security_group = true
  allowed_cidr_blocks   = module.vpc.private_subnets_cidr_blocks

  storage_encrypted = true

  backup_retention_period = 30
  preferred_backup_window = "03:00-04:00"

  enabled_cloudwatch_logs_exports = ["postgresql"]

  tags = local.common_tags
}

# ElastiCache Redis Cluster
resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "aiosv3-${var.environment}"
  replication_group_description = "Redis cluster for AIOSv3"

  engine               = "redis"
  engine_version       = "7.0"
  node_type           = "cache.r6g.large"
  number_cache_clusters = 2

  subnet_group_name = aws_elasticache_subnet_group.redis.name
  security_group_ids = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  automatic_failover_enabled = true
  multi_az_enabled          = true

  snapshot_retention_limit = 5
  snapshot_window         = "03:00-05:00"

  tags = local.common_tags
}

# Application Load Balancer
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "8.0.0"

  name = "aiosv3-${var.environment}"

  load_balancer_type = "application"

  vpc_id          = module.vpc.vpc_id
  subnets         = module.vpc.public_subnets
  security_groups = [aws_security_group.alb.id]

  target_groups = [
    {
      name_prefix      = "app-"
      backend_protocol = "HTTP"
      backend_port     = 80
      target_type      = "ip"

      health_check = {
        enabled             = true
        interval            = 30
        path                = "/health"
        port                = "traffic-port"
        healthy_threshold   = 2
        unhealthy_threshold = 2
        timeout             = 5
        protocol            = "HTTP"
      }
    }
  ]

  https_listeners = [
    {
      port               = 443
      protocol           = "HTTPS"
      certificate_arn    = aws_acm_certificate.main.arn
      target_group_index = 0
    }
  ]

  http_tcp_listeners = [
    {
      port        = 80
      protocol    = "HTTP"
      action_type = "redirect"
      redirect = {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }
  ]

  tags = local.common_tags
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "application" {
  name              = "/aws/eks/aiosv3-${var.environment}/application"
  retention_in_days = 30

  tags = local.common_tags
}

# Outputs
output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "aurora_cluster_endpoint" {
  value = module.aurora.cluster_endpoint
  sensitive = true
}

output "redis_primary_endpoint" {
  value = aws_elasticache_replication_group.redis.primary_endpoint_address
  sensitive = true
}

output "alb_dns_name" {
  value = module.alb.lb_dns_name
}
```

```hcl
# terraform/variables.tf
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "enable_deletion_protection" {
  description = "Enable deletion protection for critical resources"
  type        = bool
  default     = true
}

locals {
  common_tags = {
    Environment = var.environment
    Project     = "AIOSv3"
    ManagedBy   = "Terraform"
    CreatedBy   = "DevOps Team"
  }
}
```

## Kubernetes Deployment

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: aiosv3
  labels:
    name: aiosv3
    environment: production

---
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aiosv3-backend
  namespace: aiosv3
  labels:
    app: aiosv3
    component: backend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: aiosv3
      component: backend
  template:
    metadata:
      labels:
        app: aiosv3
        component: backend
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: aiosv3-backend
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: backend
        image: aiosv3/backend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: aiosv3-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: aiosv3-secrets
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: aiosv3-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - aiosv3
              topologyKey: kubernetes.io/hostname
```

## CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  AWS_REGION: us-west-2
  ECR_REPOSITORY: aiosv3-backend
  EKS_CLUSTER_NAME: aiosv3-production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Build, tag, and push image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --name ${{ env.EKS_CLUSTER_NAME }} --region ${{ env.AWS_REGION }}

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/aiosv3-backend backend=${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }} -n aiosv3
        kubectl rollout status deployment/aiosv3-backend -n aiosv3 --timeout=300s

    - name: Run smoke tests
      run: |
        ./scripts/smoke-tests.sh ${{ secrets.APP_URL }}
```

## Deployment Checklist
- ✅ Terraform plan reviewed and approved
- ✅ Resource tagging applied consistently
- ✅ Cost estimates analyzed (estimated $450/month)
- ✅ Security groups configured with least privilege
- ✅ Backup strategy defined (30-day retention)
- ✅ Monitoring and alerting enabled
- ✅ Documentation updated

## Security Considerations
- All data encrypted at rest and in transit
- IAM roles follow least privilege principle
- Network isolation with private subnets
- Security group rules restrict access
- Secrets managed via AWS Secrets Manager
- Container image scanning enabled

## Cost Analysis
Estimated monthly costs:
- EKS Cluster: $73 (control plane)
- EC2 Instances: $220 (3x t3.large)
- RDS Aurora: $145 (2x db.r6g.large)
- ElastiCache: $100 (2x cache.r6g.large)
- Load Balancer: $25
- Data Transfer: ~$50
- Total: ~$613/month

## Next Steps
1. Review and approve Terraform plan
2. Apply infrastructure changes
3. Configure monitoring dashboards
4. Update runbooks and documentation
5. Schedule disaster recovery drill

---
*DevOps Engineer Agent | 2025-06-01 20:45*
"""

    def _mock_frontend_development(self) -> str:
        """Generate mock React/Vue frontend development response."""
        return r"""# 🎨 Frontend Code Implementation

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
        </form>
      </div>
    </div>
  );
};
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
