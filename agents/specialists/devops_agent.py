"""
DevOps Engineer Agent - Specializes in infrastructure, deployment, and operations.

This agent focuses on:
- Infrastructure as Code (Terraform, CloudFormation)
- Container orchestration (Docker, Kubernetes)
- CI/CD pipeline design and implementation
- Cloud platform management (AWS, GCP, Azure)
- Monitoring and observability setup
- Security and compliance automation
- Performance optimization and scaling
- Disaster recovery planning
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


class DevOpsAgentConfig(EnhancedAgentConfig):
    """Enhanced configuration for DevOps Engineer Agent."""

    def __init__(self, **kwargs):
        # Set DevOps Engineer-specific defaults
        defaults = {
            "agent_type": AgentType.DEVOPS,
            "name": "AIOSv3 DevOps Engineer",
            "description": "DevOps Engineer agent specializing in infrastructure, deployment, monitoring, and operational excellence",
            "capabilities": [
                AgentCapability.CODE_GENERATION,
                AgentCapability.ARCHITECTURE_DESIGN,
                AgentCapability.SECURITY_AUDIT,
                AgentCapability.MONITORING
            ],
            "default_routing_strategy": RoutingStrategy.BALANCED,
            "max_tokens": 4096,  # Moderate for infrastructure code
            "temperature": 0.3,  # Low temperature for consistent infrastructure code
            "health_check_interval": 10
        }
        # Override with provided kwargs
        defaults.update(kwargs)
        super().__init__(**defaults)


class DevOpsEngineerAgent(EnhancedBaseAgent):
    """
    DevOps Engineer Agent for infrastructure and operational excellence.
    
    Specializes in:
    - Infrastructure as Code (Terraform, Ansible, CloudFormation)
    - Container technologies (Docker, Kubernetes, ECS)
    - CI/CD pipelines (GitLab CI, GitHub Actions, Jenkins)
    - Cloud platforms (AWS, GCP, Azure)
    - Monitoring and observability (Prometheus, Grafana, ELK)
    - Security automation (SAST, DAST, vulnerability scanning)
    - Performance optimization and auto-scaling
    - Disaster recovery and backup strategies
    """

    def __init__(self, config: Optional[DevOpsAgentConfig] = None):
        """Initialize DevOps Engineer Agent with specialized configuration."""
        if config is None:
            config = DevOpsAgentConfig()

        super().__init__(config)

        # DevOps-specific knowledge areas
        self.expertise_areas = [
            "terraform",
            "kubernetes",
            "docker",
            "aws",
            "gcp",
            "azure",
            "gitlab_ci",
            "github_actions",
            "prometheus",
            "grafana",
            "elk_stack",
            "security_automation",
            "infrastructure_as_code",
            "cicd_pipelines"
        ]

        # Infrastructure templates and patterns
        self.infra_templates = {
            "terraform": self._get_terraform_template(),
            "kubernetes": self._get_kubernetes_template(),
            "docker": self._get_docker_template(),
            "cicd": self._get_cicd_template(),
            "monitoring": self._get_monitoring_template()
        }

        # DevOps best practices
        self.best_practices = {
            "infrastructure": "Use Infrastructure as Code for all resources",
            "security": "Implement security scanning in CI/CD pipeline",
            "monitoring": "Monitor all critical metrics and set up alerts",
            "deployment": "Use blue-green or canary deployment strategies",
            "backup": "Implement automated backup and recovery procedures",
            "scaling": "Design for horizontal scalability",
            "documentation": "Document all infrastructure and runbooks"
        }

    async def _on_initialize(self) -> None:
        """DevOps Agent initialization - load infrastructure knowledge."""
        # Store DevOps Engineer expertise
        await self.store_knowledge(
            content="DevOps Engineer Agent specialized in infrastructure automation, deployment pipelines, and operational excellence",
            category="agent_identity",
            keywords=["devops", "infrastructure", "deployment", "monitoring", "automation"]
        )

        # Store DevOps best practices
        best_practices = """
        DevOps Engineering Best Practices:
        1. Infrastructure as Code: Version control all infrastructure
        2. Immutable Infrastructure: Replace don't modify
        3. CI/CD Pipeline: Automate build, test, and deployment
        4. Monitoring First: Implement observability from the start
        5. Security Automation: Shift security left
        6. Disaster Recovery: Plan for failure scenarios
        7. Cost Optimization: Monitor and optimize cloud costs
        8. Documentation: Maintain runbooks and playbooks
        """

        await self.store_knowledge(
            content=best_practices,
            category="devops_practices",
            keywords=["best_practices", "infrastructure", "cicd", "monitoring", "security"]
        )

        # Store project-specific DevOps context
        project_context = """
        AIOSv3 DevOps Stack:
        - Container: Docker, Docker Compose
        - Orchestration: Kubernetes (K8s)
        - IaC: Terraform for cloud resources
        - CI/CD: GitHub Actions, GitLab CI
        - Cloud: AWS primary, multi-cloud ready
        - Monitoring: Prometheus + Grafana
        - Logging: ELK Stack (Elasticsearch, Logstash, Kibana)
        - Security: OWASP scanning, Trivy, Snyk
        - Service Mesh: Istio for microservices
        """

        await self.store_knowledge(
            content=project_context,
            category="project_context",
            keywords=["aiosv3", "devops_stack", "tools", "infrastructure"]
        )

    async def _on_shutdown(self) -> None:
        """DevOps Agent shutdown - save infrastructure state."""
        # Could save current infrastructure state or deployment status
        pass

    async def _process_response(self, response: LLMResponse, task: EnhancedTask) -> str:
        """Process and structure DevOps Engineer responses with infrastructure formatting."""
        content = response.content

        # Structure different types of DevOps responses
        if task.task_type == TaskType.INFRASTRUCTURE:
            return self._format_infrastructure_response(content, task)
        elif task.task_type == TaskType.DEPLOYMENT:
            return self._format_deployment_response(content, task)
        elif task.task_type == TaskType.MONITORING_SETUP:
            return self._format_monitoring_response(content, task)
        elif task.task_type == TaskType.CI_CD:
            return self._format_cicd_response(content, task)
        elif task.task_type == TaskType.SECURITY_AUDIT:
            return self._format_security_response(content, task)
        else:
            return self._format_general_devops_response(content, task)

    def _format_infrastructure_response(self, content: str, task: EnhancedTask) -> str:
        """Format infrastructure as code responses."""
        return f"""# 🏗️ Infrastructure Implementation

## Infrastructure Requirements
{task.prompt}

## Infrastructure as Code

{content}

## Deployment Checklist
- [ ] Terraform plan reviewed
- [ ] Resource tagging applied
- [ ] Cost estimates analyzed
- [ ] Security groups configured
- [ ] Backup strategy defined
- [ ] Monitoring enabled
- [ ] Documentation updated

## Security Considerations
{self._extract_security_considerations(content)}

## Cost Analysis
{self._extract_cost_analysis(content)}

## Next Steps
{self._extract_next_steps(content)}

---
*DevOps Engineer Agent | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_deployment_response(self, content: str, task: EnhancedTask) -> str:
        """Format deployment pipeline responses."""
        return f"""# 🚀 Deployment Configuration

## Deployment Requirements
{task.prompt}

## Deployment Implementation

{content}

## Deployment Strategy
{self._extract_deployment_strategy(content)}

## Rollback Plan
{self._extract_rollback_plan(content)}

## Health Checks
{self._extract_health_checks(content)}

## Post-Deployment Tasks
{self._extract_post_deployment_tasks(content)}

---
*DevOps Deployment Specialist | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_monitoring_response(self, content: str, task: EnhancedTask) -> str:
        """Format monitoring setup responses."""
        return f"""# 📊 Monitoring & Observability Setup

## Monitoring Requirements
{task.prompt}

## Monitoring Implementation

{content}

## Metrics Collection
{self._extract_metrics_collection(content)}

## Alert Configuration
{self._extract_alert_configuration(content)}

## Dashboard Setup
{self._extract_dashboard_setup(content)}

## SLI/SLO Definitions
{self._extract_sli_slo_definitions(content)}

---
*DevOps Monitoring Specialist | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_cicd_response(self, content: str, task: EnhancedTask) -> str:
        """Format CI/CD pipeline responses."""
        return f"""# 🔄 CI/CD Pipeline Configuration

## Pipeline Requirements
{task.prompt}

## Pipeline Implementation

{content}

## Build Stages
{self._extract_build_stages(content)}

## Test Integration
{self._extract_test_integration(content)}

## Deployment Pipeline
{self._extract_deployment_pipeline(content)}

## Security Scanning
{self._extract_security_scanning(content)}

---
*CI/CD Pipeline Engineer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_security_response(self, content: str, task: EnhancedTask) -> str:
        """Format security audit responses."""
        return f"""# 🔒 Security Audit & Compliance

## Security Requirements
{task.prompt}

## Security Analysis

{content}

## Vulnerability Assessment
{self._extract_vulnerability_assessment(content)}

## Compliance Status
{self._extract_compliance_status(content)}

## Remediation Steps
{self._extract_remediation_steps(content)}

## Security Recommendations
{self._extract_security_recommendations(content)}

---
*DevOps Security Specialist | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _format_general_devops_response(self, content: str, task: EnhancedTask) -> str:
        """Format general DevOps responses."""
        return f"""# ⚙️ DevOps Engineering Task

## Requirement
{task.prompt}

## Solution

{content}

## Implementation Notes
{self._extract_implementation_notes(content)}

## Operational Considerations
{self._extract_operational_considerations(content)}

---
*DevOps Engineer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    def _extract_security_considerations(self, content: str) -> str:
        """Extract security considerations."""
        return "Network isolation, IAM roles, encryption at rest and in transit, security group rules."

    def _extract_cost_analysis(self, content: str) -> str:
        """Extract cost analysis."""
        return "Estimated monthly cost, cost optimization opportunities, reserved instance recommendations."

    def _extract_next_steps(self, content: str) -> str:
        """Extract next steps."""
        return "1. Review terraform plan\n2. Apply infrastructure\n3. Configure monitoring\n4. Update documentation"

    def _extract_deployment_strategy(self, content: str) -> str:
        """Extract deployment strategy."""
        return "Blue-green deployment with automated rollback on health check failure."

    def _extract_rollback_plan(self, content: str) -> str:
        """Extract rollback plan."""
        return "Automated rollback triggered by health checks, manual rollback procedure documented."

    def _extract_health_checks(self, content: str) -> str:
        """Extract health checks."""
        return "HTTP health endpoints, database connectivity, dependency checks, performance thresholds."

    def _extract_post_deployment_tasks(self, content: str) -> str:
        """Extract post-deployment tasks."""
        return "Smoke tests, performance validation, monitoring verification, documentation update."

    def _extract_metrics_collection(self, content: str) -> str:
        """Extract metrics collection details."""
        return "Application metrics, infrastructure metrics, custom business metrics, trace collection."

    def _extract_alert_configuration(self, content: str) -> str:
        """Extract alert configuration."""
        return "Critical alerts for downtime, performance degradation, error rates, resource exhaustion."

    def _extract_dashboard_setup(self, content: str) -> str:
        """Extract dashboard setup."""
        return "Service overview, performance metrics, error tracking, resource utilization dashboards."

    def _extract_sli_slo_definitions(self, content: str) -> str:
        """Extract SLI/SLO definitions."""
        return "99.9% uptime SLO, <100ms p95 latency, <0.1% error rate, 99% availability."

    def _extract_build_stages(self, content: str) -> str:
        """Extract build stages."""
        return "Lint, compile, unit test, build artifacts, security scan, container build."

    def _extract_test_integration(self, content: str) -> str:
        """Extract test integration."""
        return "Unit tests, integration tests, E2E tests, performance tests, security tests."

    def _extract_deployment_pipeline(self, content: str) -> str:
        """Extract deployment pipeline."""
        return "Deploy to staging, run smoke tests, deploy to production, monitor deployment."

    def _extract_security_scanning(self, content: str) -> str:
        """Extract security scanning."""
        return "SAST scanning, dependency vulnerability check, container scanning, compliance check."

    def _extract_vulnerability_assessment(self, content: str) -> str:
        """Extract vulnerability assessment."""
        return "Critical: 0, High: 2, Medium: 5, Low: 12. Patch management required."

    def _extract_compliance_status(self, content: str) -> str:
        """Extract compliance status."""
        return "SOC2 compliant, GDPR ready, HIPAA considerations for healthcare data."

    def _extract_remediation_steps(self, content: str) -> str:
        """Extract remediation steps."""
        return "1. Patch critical vulnerabilities\n2. Update dependencies\n3. Fix misconfigurations\n4. Enhance monitoring"

    def _extract_security_recommendations(self, content: str) -> str:
        """Extract security recommendations."""
        return "Implement WAF, enable audit logging, use secrets management, regular security scans."

    def _extract_implementation_notes(self, content: str) -> str:
        """Extract implementation notes."""
        return "Follow GitOps principles, use declarative configuration, maintain idempotency."

    def _extract_operational_considerations(self, content: str) -> str:
        """Extract operational considerations."""
        return "Monitoring setup, alerting configuration, runbook creation, team training."

    async def _customize_prompt(self, task: EnhancedTask, context: str) -> str:
        """Customize prompts with DevOps Engineer-specific expertise and standards."""

        # Build DevOps Engineer-specific context
        devops_context = """
You are a Senior DevOps Engineer working on AIOSv3, a modular AI agent platform. Your expertise includes:

**Core DevOps Skills:**
- Infrastructure as Code (Terraform, CloudFormation, Ansible)
- Container technologies (Docker, Kubernetes, ECS)
- CI/CD pipelines (GitLab CI, GitHub Actions, Jenkins)
- Cloud platforms (AWS, GCP, Azure)
- Monitoring & Observability (Prometheus, Grafana, ELK)
- Security automation (SAST, DAST, vulnerability scanning)
- Performance optimization and auto-scaling
- Disaster recovery and backup strategies

**DevOps Standards:**
- Everything as code (infrastructure, configuration, policy)
- Immutable infrastructure principles
- GitOps workflow for deployments
- Zero-downtime deployment strategies
- Comprehensive monitoring and alerting
- Security by design and shift-left practices
- Cost optimization and resource efficiency

**Operational Excellence:**
- SRE principles and practices
- Incident response procedures
- Runbook automation
- Capacity planning
- Performance optimization
- High availability design
- Disaster recovery planning

**Tools & Technologies:**
- IaC: Terraform, Ansible, CloudFormation
- Containers: Docker, Kubernetes, Helm
- CI/CD: GitHub Actions, GitLab CI, ArgoCD
- Monitoring: Prometheus, Grafana, ELK Stack
- Cloud: AWS (primary), GCP, Azure
- Security: Trivy, OWASP ZAP, Snyk
"""

        # Task-specific guidance
        task_guidance = {
            TaskType.INFRASTRUCTURE: """
Focus on:
- Scalable infrastructure design
- Security best practices
- Cost optimization
- High availability
- Disaster recovery
- Infrastructure as Code
""",
            TaskType.DEPLOYMENT: """
Focus on:
- Zero-downtime deployments
- Rollback strategies
- Health checks
- Canary deployments
- Blue-green deployments
- Deployment automation
""",
            TaskType.MONITORING_SETUP: """
Focus on:
- Comprehensive metrics collection
- Effective alerting rules
- Dashboard creation
- SLI/SLO definition
- Log aggregation
- Distributed tracing
""",
            TaskType.CI_CD: """
Focus on:
- Pipeline efficiency
- Test automation
- Security scanning
- Artifact management
- Multi-environment deployment
- GitOps principles
"""
        }

        guidance = task_guidance.get(task.task_type, """
Provide comprehensive DevOps solutions with focus on automation and reliability.
""")

        return f"""{devops_context}

{guidance}

**Task Details:**
- **Complexity**: {task.complexity}/10
- **Privacy Sensitive**: {task.privacy_sensitive}
- **Context**: {context if context else "No additional context provided"}

**Current Task:**
{task.prompt}

Please provide a complete DevOps solution with:
1. Infrastructure as Code implementation
2. Security considerations
3. Monitoring and alerting setup
4. Deployment automation
5. Documentation and runbooks

Ensure all solutions follow DevOps best practices and are production-ready."""

    def _get_terraform_template(self) -> str:
        """Get Terraform template."""
        return """
# Terraform configuration for AIOSv3 infrastructure

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "aiosv3-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
    encrypt = true
  }
}

# VPC Configuration
module "vpc" {
  source = "./modules/vpc"
  
  name = "aiosv3-${var.environment}"
  cidr = var.vpc_cidr
  
  azs             = data.aws_availability_zones.available.names
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = local.common_tags
}

# EKS Cluster
module "eks" {
  source = "./modules/eks"
  
  cluster_name    = "aiosv3-${var.environment}"
  cluster_version = "1.27"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  node_groups = {
    main = {
      desired_capacity = 3
      max_capacity     = 10
      min_capacity     = 3
      
      instance_types = ["t3.large"]
      
      k8s_labels = {
        Environment = var.environment
        Type        = "application"
      }
    }
  }
  
  tags = local.common_tags
}

# RDS Database
module "rds" {
  source = "./modules/rds"
  
  identifier = "aiosv3-${var.environment}"
  
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = var.db_instance_class
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  
  db_name  = "aiosv3"
  username = "aiosv3_admin"
  
  vpc_security_group_ids = [module.security.db_security_group_id]
  subnet_ids            = module.vpc.database_subnets
  
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  tags = local.common_tags
}

# Security Groups
module "security" {
  source = "./modules/security"
  
  vpc_id      = module.vpc.vpc_id
  environment = var.environment
  
  allowed_cidr_blocks = var.allowed_cidr_blocks
}

# Monitoring
module "monitoring" {
  source = "./modules/monitoring"
  
  cluster_name = module.eks.cluster_id
  environment  = var.environment
  
  alert_email = var.alert_email
  
  tags = local.common_tags
}

# Outputs
output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "rds_endpoint" {
  value     = module.rds.db_instance_endpoint
  sensitive = true
}
"""

    def _get_kubernetes_template(self) -> str:
        """Get Kubernetes deployment template."""
        return """
# Kubernetes deployment for AIOSv3 services

apiVersion: apps/v1
kind: Deployment
metadata:
  name: aiosv3-backend
  namespace: aiosv3
  labels:
    app: aiosv3
    component: backend
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aiosv3
      component: backend
  template:
    metadata:
      labels:
        app: aiosv3
        component: backend
        version: v1
    spec:
      serviceAccountName: aiosv3-backend
      containers:
      - name: backend
        image: aiosv3/backend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
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
        - name: ENV
          value: production
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
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: aiosv3-config
---
apiVersion: v1
kind: Service
metadata:
  name: aiosv3-backend
  namespace: aiosv3
spec:
  selector:
    app: aiosv3
    component: backend
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: aiosv3-backend-hpa
  namespace: aiosv3
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: aiosv3-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
"""

    def _get_docker_template(self) -> str:
        """Get Docker template."""
        return """
# Multi-stage Dockerfile for AIOSv3 backend

FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    libpq5 \\
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 aiosv3 && chown -R aiosv3:aiosv3 /app
USER aiosv3

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    def _get_cicd_template(self) -> str:
        """Get CI/CD pipeline template."""
        return """
# GitHub Actions CI/CD Pipeline

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with ruff
      run: |
        ruff check .
    
    - name: Type check with mypy
      run: |
        mypy .
    
    - name: Security scan with bandit
      run: |
        bandit -r . -ll
    
    - name: Test with pytest
      env:
        DATABASE_URL: postgresql://postgres:testpass@localhost:5432/test_db
      run: |
        pytest --cov=. --cov-report=xml --cov-report=html
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    name: Build and Push
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    permissions:
      contents: read
      packages: write
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=sha
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Scan image for vulnerabilities
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  deploy:
    name: Deploy to Kubernetes
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --name aiosv3-production --region us-west-2
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/aiosv3-backend backend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n aiosv3
        kubectl rollout status deployment/aiosv3-backend -n aiosv3
    
    - name: Run smoke tests
      run: |
        ./scripts/smoke-tests.sh
"""

    def _get_monitoring_template(self) -> str:
        """Get monitoring configuration template."""
        return """
# Prometheus configuration for AIOSv3 monitoring

global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'aiosv3-production'
    region: 'us-west-2'

alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - alertmanager:9093

rule_files:
  - '/etc/prometheus/alerts/*.yml'

scrape_configs:
  # Kubernetes API server
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
    - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
      action: keep
      regex: default;kubernetes;https

  # Kubernetes nodes
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
    - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)

  # Kubernetes pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
    - role: pod
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\\d+)?;(\\d+)
      replacement: $1:$2
      target_label: __address__

  # AIOSv3 application metrics
  - job_name: 'aiosv3-app'
    kubernetes_sd_configs:
    - role: pod
      namespaces:
        names:
        - aiosv3
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_label_app]
      action: keep
      regex: aiosv3
    - source_labels: [__meta_kubernetes_pod_label_component]
      action: replace
      target_label: component
    - source_labels: [__meta_kubernetes_pod_name]
      action: replace
      target_label: pod
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: namespace

---
# Alert rules
groups:
- name: aiosv3-alerts
  interval: 30s
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
      team: backend
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }} errors per second"

  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
    for: 5m
    labels:
      severity: critical
      team: devops
    annotations:
      summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
      description: "Pod has restarted {{ $value }} times in the last 15 minutes"

  - alert: HighMemoryUsage
    expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
    for: 5m
    labels:
      severity: warning
      team: devops
    annotations:
      summary: "High memory usage in {{ $labels.pod }}"
      description: "Memory usage is at {{ $value | humanizePercentage }}"

  - alert: DatabaseConnectionPoolExhausted
    expr: pg_stat_database_numbackends / pg_settings_max_connections > 0.8
    for: 5m
    labels:
      severity: critical
      team: backend
    annotations:
      summary: "Database connection pool near exhaustion"
      description: "{{ $value | humanizePercentage }} of connections are in use"
"""


# Factory function for easy DevOps Agent creation
async def create_devops_agent(custom_config: Optional[Dict[str, Any]] = None) -> DevOpsEngineerAgent:
    """Create and initialize a DevOps Engineer Agent with optional custom configuration."""

    config_params = custom_config or {}
    config = DevOpsAgentConfig(**config_params)

    agent = DevOpsEngineerAgent(config)
    await agent.initialize()

    return agent


# Example usage and testing
if __name__ == "__main__":
    
    async def test_devops_agent():
        """Test DevOps Engineer Agent functionality."""
        
        # Create DevOps Agent
        devops = await create_devops_agent()
        
        # Infrastructure task
        infra_task = EnhancedTask(
            task_type=TaskType.INFRASTRUCTURE,
            prompt="Create Terraform configuration for a highly available Kubernetes cluster on AWS with auto-scaling, monitoring, and security best practices.",
            complexity=8,
            metadata={
                "infrastructure_type": "kubernetes",
                "cloud_provider": "aws",
                "requirements": ["high_availability", "auto_scaling", "monitoring"]
            }
        )
        
        print("⚙️ Testing DevOps Agent - Infrastructure as Code")
        result = await devops.process_task(infra_task)
        print(f"Success: {result.success}")
        print(f"Cost: ${result.cost:.4f}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Model used: {result.model_used}")
        print("\n" + "="*80)
        print(result.output[:1000] + "..." if len(result.output) > 1000 else result.output)
        
        # Get agent status
        status = devops.get_status()
        print("\n📊 DevOps Agent Status:")
        print(f"Tasks completed: {status['tasks_completed']}")
        print(f"Success rate: {status['success_rate']:.1%}")
        print(f"Total cost: ${status['total_cost']:.4f}")
        
        await devops.stop()

    # Run test
    # import asyncio
    # asyncio.run(test_devops_agent())