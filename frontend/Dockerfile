# Use official Node.js image as base
FROM node:20

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first for better caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build the Angular app
RUN npm run build

# Expose Angular dev server port
EXPOSE 4200

# Start the Angular application
CMD ["npm", "start"]
