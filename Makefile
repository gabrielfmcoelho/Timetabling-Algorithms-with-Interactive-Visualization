# Main Environment Variables
PROJECT_NAME ?= timetabling-interactive-visualization
MODE ?= dev

API_PORT ?= 8083
FRONTEND_PORT ?= 3000
API_VERSION ?= 0.1.0
FRONTEND_VERSION ?= 0.1.0

CORS_ALLOW_ORIGINS ?= "localhost:3000,localhost:8083,192.168.15.15:8083"
CORS_ALLOW_CREDENTIALS ?= true
CORS_ALLOW_METHODS ?= "*"
CORS_ALLOW_HEADERS ?= "*"


setup-env:
	bash config/scripts/setup_env.sh $(PROJECT_NAME) $(MODE) $(API_PORT) $(FRONTEND_PORT) $(API_VERSION) $(FRONTEND_VERSION) $(CORS_ALLOW_ORIGINS) $(CORS_ALLOW_CREDENTIALS) $(CORS_ALLOW_METHODS) $(CORS_ALLOW_HEADERS)

clean-env:
	rm -f .env Dockerfile docker-compose.yml

# ---------------------------------------------------------------------
# Whole Service (API + DB) with Docker Compose
service-build:
	docker compose build

service-run-debug:
	docker compose up --remove-orphans

service-run:
	docker compose up -d --remove-orphans

service-init: setup-env service-build service-run

service-init-debug: setup-env service-build service-run-debug

service-stop:
	docker compose down

service-clean: service-stop clean-env

# ---------------------------------------------------------------------
# Independent Services
# ------------------------------------------
# API
api-build:
	docker build -t $(PROJECT_NAME)-api-$(MODE)-i -f Dockerfile.api .

api-run:
	docker run --rm --name $(PROJECT_NAME)-api-$(MODE)-c -p $(API_PORT):$(API_PORT) --volume ./api/src/logs/history:/app/logs/history --network $(PROJECT_NAME)-network $(PROJECT_NAME)-api-$(MODE)-i

api-rebuild: api-build api-run

api-init: setup-env api-rebuild

api-stop:
	docker stop $(PROJECT_NAME)-api-$(MODE)-c

api-clean:
	docker rmi $(PROJECT_NAME)-api-$(MODE)-i

api-clean-env: api-stop api-clean clean-env
# ------------------------------------------
# FRONTEND
frontend-build:
	docker build -t $(PROJECT_NAME)-frontend-$(MODE)-i -f Dockerfile.frontend .

frontend-run:
	docker run --rm --name $(PROJECT_NAME)-frontend-$(MODE)-c -p $(FRONTEND_PORT):$(FRONTEND_PORT) --network $(PROJECT_NAME)-network $(PROJECT_NAME)-frontend-$(MODE)-i

frontend-rebuild: frontend-build frontend-run

frontend-init: setup-env frontend-rebuild

frontend-stop:
	docker stop $(PROJECT_NAME)-frontend-$(MODE)-c

frontend-clean:
	docker rmi $(PROJECT_NAME)-frontend-$(MODE)-i

frontend-clean-env: frontend-stop frontend-clean clean-env