# AI Learning Platform

A production-grade modular learning platform with AI-enhanced features for personalized learning experiences, incorporating adaptive assessments, content generation, analytics, and more.

## Technology Stack

- **Frontend**: Next.js (TypeScript), Tailwind CSS, React Query
- **Backend**: Python (FastAPI, Langchain, Langgraph)
- **Database**: Supabase (PostgreSQL)
- **AI**: Langchain, Langgraph, Google's free LLM model
- **Caching**: Redis
- **Monitoring**: Prometheus
- **Deployment**: GitHub Actions, Docker, Nginx, Vercel

## Features

- **Personalized Learning**: AI-generated learning paths tailored to individual learning styles
- **Adaptive Assessments**: Dynamically adjust difficulty based on user performance
- **Content Generation**: AI-assisted content creation for instructors
- **Analytics**: Comprehensive analytics for tracking user progress and engagement
- **Notifications**: Real-time notifications for course updates and achievements
- **Search**: Advanced search functionality for courses and content
- **User Preferences**: Customizable learning styles, UI preferences, and notification settings
- **Monitoring**: Performance metrics and error tracking

## Project Structure

```
.
├── frontend/                # Next.js frontend application
│   ├── app/                 # Next.js app router
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utility functions
│   ├── styles/              # Global styles
│   └── public/              # Static assets
│
├── backend/                 # FastAPI backend application
│   ├── app/                 # Application code
│   │   ├── api/             # API endpoints
│   │   ├── core/            # Core functionality
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── tests/               # Test suite
│   └── main.py              # Application entry point
│
├── docs/                    # Documentation
│   ├── database/            # Database schema
│   └── assets/              # Documentation assets
│
├── .github/                 # GitHub configuration
│   └── workflows/           # GitHub Actions workflows
│
├── docker-compose.yml       # Docker Compose configuration
├── .env.example             # Example environment variables
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+
- Python 3.11+
- Supabase account

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-learning-platform.git
   cd ai-learning-platform
   ```

2. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your Supabase credentials and other configuration.

4. Start the development environment:
   ```bash
   docker-compose up -d
   ```

5. Access the applications:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/v1/docs

## Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing

### Frontend

```bash
cd frontend
npm test
```

### Backend

```bash
cd backend
pytest
```

## Deployment

The application is configured for deployment using GitHub Actions:

- Frontend: Vercel
- Backend: Docker container (deploy to your preferred cloud provider)
- Database: Supabase

## Contributing

1. Create a feature branch: `git checkout -b feat/your-feature-name`
2. Commit your changes: `git commit -m "feat: add some feature"`
3. Push to the branch: `git push origin feat/your-feature-name`
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.