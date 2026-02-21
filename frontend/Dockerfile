# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Accept build arguments for environment variables
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets to Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration if needed for SPA routing
# (We'll create a minimal default.conf to handle React Router fallback)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
