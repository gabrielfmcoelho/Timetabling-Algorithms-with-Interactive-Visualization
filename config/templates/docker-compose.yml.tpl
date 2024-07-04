services:
  api:
    build: 
      context: .
      dockerfile: Dockerfile.api
    container_name: (PROJECT_NAME)-api-c
    volumes:
      - ./api/src/logs/history:/app/logs/history
    networks:
      - (PROJECT_NAME)-network
    ports:
      - "(API_PORT):(API_PORT)"
  
  frontend:
    build: 
      context: .
      dockerfile: Dockerfile.frontend
    container_name: (PROJECT_NAME)-frontend-c
    networks:
      - (PROJECT_NAME)-network
    ports:
      - "(FRONTEND_PORT):(FRONTEND_PORT)"

networks:
  (PROJECT_NAME)-network:
    name: (PROJECT_NAME)-network
    driver: bridge