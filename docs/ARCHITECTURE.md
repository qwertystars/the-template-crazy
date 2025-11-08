# FlexiBase Architecture Documentation

## Overview

FlexiBase is designed as a universal platform framework that can transform into different types of applications through configuration, without changing the core codebase. This document describes the architectural decisions and patterns used.

## Architecture Principles

### 1. Modularity
- **Feature Modules**: Self-contained modules (commerce, donation, subscription)
- **Plug-and-Play**: Enable/disable modules through configuration
- **Isolation**: Each module has its own models, routes, services, and components

### 2. Flexibility
- **JSONB Fields**: Flexible metadata storage for varying use cases
- **Polymorphic Relationships**: Generic foreign keys for universal relationships
- **Configuration-Driven**: Platform behavior controlled by JSON configuration

### 3. Scalability
- **Async Operations**: FastAPI with async/await for high concurrency
- **Connection Pooling**: Efficient database connection management
- **Stateless API**: JWT tokens for horizontal scaling
- **Caching Ready**: Redis integration for performance

### 4. Security
- **Defense in Depth**: Multiple security layers
- **Least Privilege**: Role-based access control
- **Input Validation**: Pydantic schemas for all inputs
- **Secure Defaults**: Security-first configuration

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  (Browser, Mobile App, Third-party Integrations)            │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Next.js)                  │
├─────────────────────────────────────────────────────────────┤
│  • Server Components (SSR)                                   │
│  • Client Components (Interactive UI)                        │
│  • Zustand State Management                                  │
│  • API Client with Auth Interceptors                         │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   API Gateway / Reverse Proxy                │
│                        (Nginx - Optional)                    │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Layer (FastAPI)                   │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Middleware  │  │   Routers    │  │   Services   │      │
│  │  - Auth      │  │  - Auth      │  │  - Business  │      │
│  │  - CORS      │  │  - Users     │  │    Logic     │      │
│  │  - Module    │  │  - Entities  │  │  - Payment   │      │
│  │    Check     │  │  - Trans.    │  │  - Email     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Feature Modules                          │  │
│  │  • Commerce  • Donation  • Subscription              │  │
│  │  • Community • Impact Tracking                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
├──────────────────────┬──────────────────────┬───────────────┤
│   PostgreSQL         │      Redis           │  File Storage │
│   (Primary Data)     │   (Cache/Session)    │   (Uploads)   │
└──────────────────────┴──────────────────────┴───────────────┘
```

## Backend Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (Routes)                      │
│  • Request validation                                        │
│  • Response serialization                                    │
│  • Dependency injection                                      │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                             │
│  • Business logic                                            │
│  • Transaction management                                    │
│  • External integrations                                     │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Access Layer (Models)                 │
│  • SQLAlchemy ORM                                           │
│  • Database operations                                       │
│  • Relationship management                                   │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Patterns

#### 1. Dependency Injection
- FastAPI's built-in DI for database sessions
- Middleware dependencies for authentication
- Service layer injection for testability

#### 2. Repository Pattern
- Models encapsulate data structure
- Services handle business logic
- Clear separation of concerns

#### 3. Factory Pattern
- Token creation factories
- Dynamic module loading
- Configuration builders

## Frontend Architecture

### Component Hierarchy

```
App Layout
├── Header (Client Component)
│   ├── Navigation
│   ├── User Menu
│   └── Cart Icon
├── Main Content (Server/Client)
│   ├── Page Components
│   │   ├── Product List (Server)
│   │   ├── Product Details (Server)
│   │   └── Interactive Elements (Client)
│   └── Module Components
│       ├── Commerce Module
│       ├── Donation Module
│       └── Subscription Module
└── Footer (Server Component)
```

### State Management

```
┌─────────────────────────────────────────────────────────────┐
│                    Zustand Stores                            │
├──────────────────────┬──────────────────────┬───────────────┤
│   Auth Store         │   Config Store       │  Cart Store   │
│   • User data        │   • Platform config  │  • Items      │
│   • Tokens           │   • Active modules   │  • Totals     │
│   • Auth state       │   • Theme settings   │  • Actions    │
└──────────────────────┴──────────────────────┴───────────────┘
```

### Data Flow

```
User Action
    ↓
Component Event Handler
    ↓
Zustand Store Action
    ↓
API Call (via Axios)
    ↓
Backend API Endpoint
    ↓
Service Layer Processing
    ↓
Database Operation
    ↓
Response to Frontend
    ↓
Store Update
    ↓
Component Re-render
```

## Database Design

### Schema Patterns

#### 1. Universal User Model
```sql
users
├── id (PK)
├── email (unique)
├── role (enum: admin, customer, donor, subscriber, beneficiary)
├── metadata (JSONB) -- Flexible attributes
└── ... (standard fields)
```

#### 2. Polymorphic Entity Model
```sql
entities
├── id (PK)
├── entity_type (enum: product, cause, subscription_tier, etc.)
├── status (enum: draft, active, inactive, archived)
├── metadata (JSONB) -- Type-specific attributes
└── ... (common fields)
```

#### 3. Universal Transaction Log
```sql
transactions
├── id (PK)
├── transaction_type (enum: purchase, donation, subscription, etc.)
├── user_id (FK)
├── entity_id (FK)
├── metadata (JSONB) -- Transaction-specific data
└── ... (financial fields)
```

### Indexing Strategy

- Primary keys: Clustered B-tree indexes
- Foreign keys: Non-clustered indexes
- Email, username: Unique indexes
- Status, type fields: B-tree indexes for filtering
- JSONB fields: GIN indexes for queries
- Created_at: B-tree for time-based queries

## Security Architecture

### Authentication Flow

```
1. User submits credentials
2. Backend validates credentials
3. Password verified with bcrypt
4. JWT tokens generated
   • Access token (short-lived)
   • Refresh token (long-lived)
5. Tokens returned to client
6. Access token stored in memory/localStorage
7. Refresh token stored securely
8. Access token sent in Authorization header
9. Backend validates token on each request
10. Token refreshed when expired
```

### Authorization Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Request Flow                              │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              1. Authentication Middleware                    │
│              • Verify JWT token                              │
│              • Extract user info                             │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              2. Role-Based Access Control                    │
│              • Check user role                               │
│              • Verify permissions                            │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              3. Resource-Level Authorization                 │
│              • Check resource ownership                      │
│              • Validate access rights                        │
└─────────────────────────────────────────────────────────────┘
                              ▼
                        Execute Request
```

## Module System

### Module Structure

Each module follows this structure:

```
module_name/
├── models.py         # Database models
├── schemas.py        # Pydantic schemas
├── routes.py         # API endpoints
├── services.py       # Business logic
└── __init__.py       # Module initialization
```

### Module Registration

```python
# Dynamic module loading based on configuration
active_modules = config.get("activeModules")

for module_name in active_modules:
    module = import_module(f"app.modules.{module_name}")
    if hasattr(module, 'router'):
        app.include_router(module.router)
```

## Performance Optimization

### Backend Optimizations
- Async/await for I/O operations
- Database connection pooling
- Query optimization with indexes
- Lazy loading of relationships
- Response caching with Redis

### Frontend Optimizations
- Server-side rendering (SSR)
- Static generation where possible
- Image optimization with Next.js Image
- Code splitting by route
- State management with Zustand (minimal re-renders)

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- JWT tokens (no server-side sessions)
- Database connection pooling
- Redis for shared state

### Vertical Scaling
- Async operations for CPU efficiency
- Optimized queries for database performance
- Caching to reduce database load

### Database Scaling
- Read replicas for read-heavy workloads
- Partitioning large tables
- Archive old data
- Connection pooling

## Monitoring and Observability

### Logging
- Structured logging in backend
- Request/response logging
- Error logging with stack traces
- Audit logging for sensitive operations

### Metrics
- API response times
- Database query performance
- Error rates
- User activity

### Health Checks
- `/health` endpoint for service health
- Database connectivity check
- External service availability

## Future Enhancements

### Planned Features
- WebSocket support for real-time updates
- GraphQL API alongside REST
- Microservices architecture option
- Event-driven architecture with message queues
- Multi-tenancy support
- Advanced caching strategies

### Module Extensions
- CMS module
- Analytics module
- Notification system
- Workflow engine
- Reporting system
