# Use the official Node.js image as the base image
FROM node:20 AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of your application code
COPY . .

# Build the React app for production
RUN npm run build

COPY /image /app/dist/image

# Use Nginx to serve the app
FROM nginx:alpine
# Copy the built files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
