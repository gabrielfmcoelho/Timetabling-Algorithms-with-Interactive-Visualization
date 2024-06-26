# env var main project name
PROJECT_NAME = template-api
MODE = dev
PORT = 8080

setup-env:
	@echo "Setting up environment..."
	cp ./src/Dockerfile.$(MODE) ./Dockerfile
	@echo "PROJECT_NAME=$(PROJECT_NAME)" > .env
	@echo "MODE=$(MODE)" >> .env
	@echo "PORT=$(PORT)" >> .env

build:
	docker build -t $(PROJECT_NAME)-$(MODE)-i ./src

run:
	docker run --rm --name $(PROJECT_NAME)-$(MODE)-c -p $(PORT):$(PORT) $(PROJECT_NAME)-$(MODE)-i

start-clean-api: setup-env build run

start-api: build run

stop-api:
	docker stop $(PROJECT_NAME)-$(MODE)-c

clean:
	docker rmi $(PROJECT_NAME)-$(MODE)-i
	rm -f .env Dockerfile
