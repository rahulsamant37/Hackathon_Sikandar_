# Commit Structure

This document outlines the commit structure for the AI Learning Platform project. We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification to maintain a clear and structured commit history.

## Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries
- **ci**: Changes to CI configuration files and scripts

## Commit Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **type**: One of the commit types listed above
- **scope** (optional): The part of the codebase affected by the change
- **subject**: A short description of the change
- **body** (optional): A more detailed description of the change
- **footer** (optional): Information about breaking changes or references to issues

## Example Commits

Here's a list of example commits for the AI Learning Platform project:

### Initial Setup

```
feat(project): initial project setup

- Set up Next.js frontend
- Set up FastAPI backend
- Configure Docker and Docker Compose
- Add basic authentication
```

### Backend Features

```
feat(backend): add user authentication service

- Implement JWT authentication
- Add user registration and login endpoints
- Create password reset functionality
- Add email verification
```

```
feat(backend): implement course management

- Add course creation and update endpoints
- Implement module management
- Add content creation endpoints
- Create enrollment functionality
```

```
feat(backend): add AI-powered learning paths

- Implement learning path generation service
- Create personalized recommendation engine
- Add learning style analysis
- Integrate with LangChain for AI capabilities
```

```
feat(backend): implement adaptive assessments

- Create adaptive quiz generation
- Add difficulty adjustment based on performance
- Implement personalized feedback
- Add progress tracking
```

```
feat(backend): add analytics service

- Implement user activity tracking
- Create content engagement metrics
- Add course performance analytics
- Implement retention analysis
```

```
feat(backend): add notification system

- Create in-app notification service
- Implement email notifications
- Add notification preferences
- Create notification API endpoints
```

```
feat(backend): implement search functionality

- Add course search
- Implement content search
- Create combined search endpoint
- Add caching for search results
```

```
feat(backend): add user preferences

- Implement learning style preferences
- Add UI preferences
- Create notification preferences
- Add API endpoints for preferences
```

```
feat(backend): add monitoring and logging

- Implement Prometheus metrics
- Add structured logging
- Create health check endpoints
- Add performance monitoring
```

### Frontend Features

```
feat(frontend): implement authentication UI

- Create login and registration pages
- Add password reset flow
- Implement protected routes
- Add authentication context
```

```
feat(frontend): create course browsing and enrollment

- Implement course listing page
- Add course detail page
- Create enrollment functionality
- Add my courses page
```

```
feat(frontend): add learning interface

- Create content viewer
- Implement quiz interface
- Add progress tracking
- Create learning path visualization
```

```
feat(frontend): implement instructor dashboard

- Add course creation interface
- Create content management
- Implement student progress tracking
- Add analytics dashboard
```

```
feat(frontend): add user profile and preferences

- Create profile page
- Implement preferences UI
- Add notification settings
- Create learning style questionnaire
```

```
feat(frontend): implement search functionality

- Add search bar component
- Create search results page
- Implement filtering and sorting
- Add search history
```

### Infrastructure

```
chore(infra): set up CI/CD pipeline

- Configure GitHub Actions
- Add Docker build and push
- Implement automated testing
- Create deployment workflow
```

```
chore(infra): add monitoring and observability

- Set up Prometheus
- Configure logging
- Add health checks
- Implement error tracking
```

```
chore(infra): improve caching and performance

- Add Redis caching
- Implement database indexing
- Optimize API responses
- Add rate limiting
```

### Documentation

```
docs(project): add comprehensive documentation

- Update README
- Create API documentation
- Add development guidelines
- Document deployment process
```

```
docs(api): add OpenAPI documentation

- Add endpoint descriptions
- Document request/response schemas
- Add authentication details
- Create example requests
```

## Branching Strategy

We use a feature branch workflow:

1. Create a feature branch from `develop`: `git checkout -b feat/feature-name`
2. Make changes and commit using conventional commits
3. Push the branch and create a pull request to `develop`
4. After review and approval, merge the pull request
5. Periodically merge `develop` into `main` for releases

## Release Process

1. Merge `develop` into `main`
2. Tag the release: `git tag -a v1.0.0 -m "Release v1.0.0"`
3. Push the tag: `git push origin v1.0.0`
4. The CI/CD pipeline will automatically deploy the release
