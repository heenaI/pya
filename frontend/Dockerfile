# Use official Node.js image as base
FROM node:20 AS build-stage  

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first for better caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build the Angular app
RUN npm run build --dev

# Use Nginx to serve the Angular app
FROM nginx:alpine AS runtime

# Copy built Angular files from the build stage
COPY --from=build-stage /app/dist/ai-task-optimizer /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]