# FlexiBase - Universal Platform Framework

A modular, full-stack web platform that can be dynamically configured to transform into different types of websites (e-commerce, donation platform, subscription service, social impact solutions) through configuration changes, without modifying core codebase.

## Features

- **Universal Architecture**: One codebase, multiple platform types
- **Dynamic Configuration**: Transform your platform through JSON configuration
- **Modular Design**: Enable/disable features on demand
- **Full-Stack Solution**: FastAPI backend + Next.js frontend
- **Enterprise Ready**: JWT authentication, role-based access, PostgreSQL database
- **Production Ready**: Docker support, comprehensive API documentation
- **Type Safe**: TypeScript frontend, Python type hints backend

## Tech Stack

### Backend
- **FastAPI** (Python 3.10+) - High-performance async API framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Async ORM with type hints
- **Alembic** - Database migration management
- **JWT** - Secure authentication
- **Stripe** - Payment processing (abstracted for multi-gateway)

### Frontend
- **Next.js 14+** - React framework with App Router
- **React 18+** - Modern UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Zustand** - Lightweight state management
- **Axios** - HTTP client with interceptors

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd the-template-crazy
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

### Local Development Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start development server:
```bash
python -m uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```bash
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

4. Start development server:
```bash
npm run dev
```

## Project Structure

```
flexibase/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       └── router.py
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── middleware/     # Middleware (auth, etc.)
│   │   ├── modules/        # Feature modules
│   │   ├── utils/          # Utilities
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database setup
│   │   └── main.py         # Application entry
│   ├── alembic/            # Database migrations
│   ├── tests/              # Tests
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   │   ├── ui/           # Base UI components
│   │   ├── modules/      # Module-specific components
│   │   └── shared/       # Shared components
│   ├── lib/              # Utilities and API client
│   ├── store/            # Zustand stores
│   ├── hooks/            # Custom React hooks
│   ├── types/            # TypeScript types
│   └── package.json      # Node dependencies
│
├── docker-compose.yml     # Development compose file
├── docker-compose.prod.yml # Production compose file
└── README.md             # This file
```

## Database Schema

### Core Tables

#### Users
Universal user model supporting multiple roles:
- `id` - Primary key
- `email` - Unique email address
- `username` - Optional username
- `hashed_password` - Bcrypt hashed password
- `role` - User role (admin, customer, donor, subscriber, beneficiary)
- `is_active`, `is_verified`, `is_superuser` - Status flags
- `metadata` - JSONB for flexible attributes

#### Entities
Abstract content items (products, causes, subscription tiers):
- `id` - Primary key
- `entity_type` - Type of entity
- `status` - Current status (draft, active, inactive, archived)
- `name`, `slug`, `description` - Basic info
- `price`, `currency` - Pricing information
- `stock_quantity`, `track_inventory` - Inventory management
- `metadata` - JSONB for type-specific attributes

#### Transactions
Universal transaction log:
- `id` - Primary key
- `transaction_type` - Type (purchase, donation, subscription, etc.)
- `status` - Transaction status
- `user_id`, `entity_id` - References
- `amount`, `total_amount`, `currency` - Financial details
- `payment_gateway`, `gateway_transaction_id` - Payment info
- `metadata` - JSONB for additional data

#### Interactions
Comments, reviews, ratings:
- `id` - Primary key
- `interaction_type` - Type of interaction
- `user_id`, `entity_id` - References
- `content`, `rating` - Interaction data

#### Configurations
Platform settings:
- `id` - Primary key
- `key` - Unique configuration key
- `value` - JSONB configuration value
- `is_active` - Status flag

## API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT tokens
- `POST /api/v1/auth/refresh` - Refresh access token

#### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{id}` - Get user by ID
- `GET /api/v1/users` - List all users (admin only)

#### Entities
- `POST /api/v1/entities` - Create entity (admin only)
- `GET /api/v1/entities` - List entities (with filters)
- `GET /api/v1/entities/{id}` - Get entity details
- `PUT /api/v1/entities/{id}` - Update entity (admin only)
- `DELETE /api/v1/entities/{id}` - Delete entity (admin only)

#### Transactions
- `POST /api/v1/transactions` - Create transaction
- `GET /api/v1/transactions` - List transactions
- `GET /api/v1/transactions/{id}` - Get transaction details
- `PUT /api/v1/transactions/{id}` - Update transaction (admin only)

## Configuration System

FlexiBase uses a JSON-based configuration system to control platform behavior:

```json
{
  "platformType": "ecommerce",
  "platformName": "My Store",
  "activeModules": ["commerce", "reviews", "wishlist"],
  "theme": {
    "name": "modern-shop",
    "primaryColor": "#3B82F6",
    "layout": "grid"
  },
  "features": {
    "userRegistration": true,
    "guestCheckout": true,
    "multiCurrency": false,
    "socialLogin": true
  },
  "paymentGateways": ["stripe", "paypal"],
  "integrations": {
    "analytics": "google",
    "email": "sendgrid"
  }
}
```

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

### Code Quality

Backend (Python):
```bash
black app/
flake8 app/
mypy app/
```

Frontend (TypeScript):
```bash
npm run lint
npm run type-check
```

## Deployment

### Production Deployment

1. Update environment variables in `.env` files
2. Build and run with production compose file:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Run database migrations:
```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Environment Variables

See `.env.example` files in backend and frontend directories for all required environment variables.

## Security

- Passwords hashed with bcrypt
- JWT-based authentication with refresh tokens
- CSRF protection
- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy
- CORS configuration
- Rate limiting (configurable)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the documentation at `/docs`
- Review API documentation at http://localhost:8000/api/docs

## Roadmap

### Phase 1: Core Foundation ✅
- [x] Backend structure with FastAPI
- [x] Database models and migrations
- [x] Authentication system
- [x] Core API endpoints
- [x] Frontend structure with Next.js
- [x] Basic layout and routing

### Phase 2: E-commerce Module (In Progress)
- [ ] Product management
- [ ] Shopping cart
- [ ] Checkout flow
- [ ] Payment integration
- [ ] Order management

### Phase 3: Additional Modules
- [ ] Donation platform module
- [ ] Subscription service module
- [ ] Community features
- [ ] Impact tracking

### Phase 4: Advanced Features
- [ ] Admin dashboard
- [ ] Analytics integration
- [ ] Email notifications
- [ ] File uploads
- [ ] Search and filtering
- [ ] Multi-language support

## Acknowledgments

Built with modern, production-ready technologies:
- FastAPI for high-performance backend
- Next.js for optimal frontend performance
- PostgreSQL for data reliability
- Docker for easy deployment
