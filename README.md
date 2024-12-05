# Kaya


## Getting Started

### Prerequisites
- Python 3.10.15
- Docker
- PostgreSQL database [https://neon.tech/]

### Installation & Running
1. Clone the repository
2. Set up environment variables (Copy .env.example to .env and set the variables)
    - `DATABASE_URL` will be provided
3. Build the Docker image
```bash
docker build -t usekaya:latest .
```
4. Run the Docker container
```bash
docker run --name kaya-container -p 8000:8000 --env-file .env usekaya:latest
```

