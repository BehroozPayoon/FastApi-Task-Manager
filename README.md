## Task Manager

The project developed by the help of Docker, Traefik and Postgresql. You can find a running version on: https://auth.payoon.dev

1. The first step is to build the docker image using the Dockerfile => `Docker build -t task-manager:latest .`
2. For production use `docker-compose.yml` and for development use `docker-compose.local.yml` for example => `docker-compose -f docker-compose.local.yml up -d`
3. After the project is running you can test the it using => `docker-compose -f docker-compose.local.yml exec app pytest`
