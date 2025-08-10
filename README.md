# FastAPI + React Fullstack Template

This repository provides a production-ready template for building fullstack applications using FastAPI (Python) for the backend and React (TypeScript) for the frontend. It includes Docker support, Traefik integration, and a modern development workflow.

## Features

- FastAPI backend (Python)
- React frontend (TypeScript, Vite, TailwindCSS)
- Dockerized development and deployment
- Traefik reverse proxy configuration
- Pre-configured testing and linting
- Example API and frontend integration

## Project Structure

```
backend/      # FastAPI backend code
frontend/     # React frontend code
docker-compose.yml, etc. # Docker and Traefik configs
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js (for frontend development)

### Development

1. Clone the repository:
   ```sh
   git clone https://github.com/mandjevant/FastAPIReactTemplate.git
   cd FastAPIReactTemplate
   ```
2. Start the stack with Docker Compose:
   ```sh
   docker-compose up --build
   ```
3. Access the frontend at `http://localhost:5173` and the backend at `http://localhost:8000`.

### Running Tests

- **Backend:**
  ```sh
  cd backend
  pytest
  ```
- **Frontend:**
  ```sh
  cd frontend
  npm test
  ```

## Customization

- Modify backend APIs in `backend/app/api/`
- Update frontend components in `frontend/src/`

## License

MIT
