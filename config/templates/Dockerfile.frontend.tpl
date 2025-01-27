# Use an official Node.js runtime as the base image
FROM node:20.14.0-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY frontend/package*.json ./

# Install project dependencies
RUN npm install

RUN echo pwd && ls -la && sleep 5

# Copy the entire files and subdirectories from frontend folder to the working directory
COPY frontend/ .

# SHOW ALL THE WORKING DIRECTORY FILES AND WAIT 60 SECONDS
RUN echo pwd && ls -la && sleep 5

# Build the React Vite project
RUN npm run build

# Expose the desired port
EXPOSE (FRONTEND_PORT)

# Define the command to run the project
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "(FRONTEND_PORT)"]