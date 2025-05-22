# Real Estate Agent Helper API

A FastAPI application that helps real estate agents manage properties, schedules, and clients.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Running with Docker

1. Clone the repository:

```bash
git clone <repository-url>
cd real-state-agent-fastapi
```

2. Build and start the application using Docker Compose:

```bash
docker-compose up -d
```

This will start:

- The FastAPI application on <http://localhost:8000>
- A PostgreSQL database

3. API Documentation:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### Development

If you want to run the application without Docker:

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install uv
uv pip install -e .
```

2. Set up the PostgreSQL database and update the DATABASE_URL in your environment variables.

3. Run migrations:

```bash
alembic upgrade head
```

4. Start the application:

```bash
uvicorn main:app --reload
```

## API Endpoints

The API includes several endpoints:

- **Authentication**: User registration and login
- **Properties**: Register and search properties
- **Agents**: Schedule calls with agents
- **Real Estate Agent Management**: Manage agent schedules

For detailed API documentation, check the Swagger UI after starting the application.

## Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant AuthRouter
    participant PropertyRouter
    participant AgentRouter
    participant RealEstateAgentRouter
    participant AuthUseCase
    participant PropertyUseCase
    participant AgentUseCase
    participant RealEstateAgentUseCase
    participant Database

    %% Authentication Flow
    Client->>FastAPI: POST /auth/signup
    FastAPI->>AuthRouter: Route request
    AuthRouter->>AuthUseCase: RegisterUserUseCase.execute()
    AuthUseCase->>Database: Store user data
    AuthUseCase-->>AuthRouter: Return email
    AuthRouter-->>Client: Email confirmation message

    Client->>FastAPI: POST /auth/login
    FastAPI->>AuthRouter: Route request
    AuthRouter->>AuthUseCase: LoginUserUseCase.execute()
    AuthUseCase->>Database: Validate credentials
    AuthUseCase-->>AuthRouter: Return JWT token
    AuthRouter-->>Client: Authentication token

    %% Property Management Flow
    Client->>FastAPI: POST /property (with JWT)
    FastAPI->>PropertyRouter: Route request
    PropertyRouter->>PropertyUseCase: RegisterPropertyUseCase.execute()
    PropertyUseCase->>Database: Store property data
    PropertyUseCase-->>PropertyRouter: Property details
    PropertyRouter-->>Client: Property response

    Client->>FastAPI: GET /property/search?query=xyz
    FastAPI->>PropertyRouter: Route request
    PropertyRouter->>PropertyUseCase: SearchPropertyUseCase.execute()
    PropertyUseCase->>Database: Search properties
    PropertyUseCase-->>PropertyRouter: Matching properties
    PropertyRouter-->>Client: Property list response

    %% Agent Management Flow
    Client->>FastAPI: POST /schedule-call (with JWT)
    FastAPI->>AgentRouter: Route request
    AgentRouter->>AgentUseCase: ScheduleCallUseCase.execute()
    AgentUseCase->>Database: Store call schedule
    AgentUseCase-->>AgentRouter: Call details
    AgentRouter-->>Client: Call confirmation

    %% Real Estate Agent Management Flow
    Client->>FastAPI: POST /real-estate-agent/schedule (with JWT)
    FastAPI->>RealEstateAgentRouter: Route request
    RealEstateAgentRouter->>RealEstateAgentUseCase: ManageAgentScheduleUseCase.create_schedule()
    RealEstateAgentUseCase->>Database: Store agent schedule
    RealEstateAgentUseCase-->>RealEstateAgentRouter: Schedule details
    RealEstateAgentRouter-->>Client: Schedule response

    Client->>FastAPI: GET /real-estate-agent/schedule (with JWT)
    FastAPI->>RealEstateAgentRouter: Route request
    RealEstateAgentRouter->>RealEstateAgentUseCase: ManageAgentScheduleUseCase.get_agent_schedules()
    RealEstateAgentUseCase->>Database: Fetch agent schedules
    RealEstateAgentUseCase-->>RealEstateAgentRouter: Schedule list
    RealEstateAgentRouter-->>Client: Schedules response
```

## Roadmap

The following features are planned for upcoming releases:

### 1. Agent-Assisted Deal Matching

Our AI-powered deal matching system will:

- Continuously monitor agent portfolios to identify optimal collaboration opportunities
- Provide commission-split negotiation assistance based on game theory principles
- Maximize revenue through strategic portfolio sharing

### 2. Portfolio Risk Management

Intelligent risk management will help agents:

- Analyze portfolio risk and identify diversification opportunities through strategic sharing
- Implement dynamic hedging strategies through collaborative agreements

### 3. Process Automation for Collaborative Deals

Workflow automation for multi-agent transactions will:

- Handle the complexity of document sharing, signatures, and approvals
- Coordinate schedules and responsibilities automatically
- Ensure transparent commission distribution
- Reduce administrative overhead and eliminate errors in collaborative deals

### 4. Microservices Architecture

To improve performance and deployment flexibility, we'll break the application into microservices:

- Split into separate services for auth, property management, agent interactions, and analytics
- Implement containerized deployments with smaller, optimized Docker images
- Enable independent scaling of high-demand components
- Improve development velocity through parallel feature implementation
