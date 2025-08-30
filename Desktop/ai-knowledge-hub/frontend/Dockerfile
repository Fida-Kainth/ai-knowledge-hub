# ---------- Build stage ----------
    FROM node:20-alpine AS build
    WORKDIR /app
    
    # Install deps
    COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
    RUN \
      if [ -f package-lock.json ]; then npm ci; \
      elif [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile; \
      elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
      else npm i; fi
    
    # Copy source
    COPY . .
    
    # Build for production
    RUN npm run build
    
    # ---------- Runtime stage (NGINX) ----------
    FROM nginx:1.27-alpine AS runtime
    WORKDIR /usr/share/nginx/html
    
    # Remove default static content
    RUN rm -rf ./*
    
    # Copy built assets
    COPY --from=build /app/dist ./
    
    # Minimal SPA nginx config with history fallback to index.html
    # and basic gzip/brotli (if available) settings.
    RUN printf '%s\n' \
      'server {' \
      '  listen       80;' \
      '  server_name  _;' \
      '  root   /usr/share/nginx/html;' \
      '  index  index.html;' \
      '' \
      '  gzip on;' \
      '  gzip_types text/plain text/css application/json application/javascript application/octet-stream image/svg+xml;' \
      '  gzip_min_length 1024;' \
      '' \
      '  location / {' \
      '    try_files $uri $uri/ /index.html;' \
      '  }' \
      '' \
      '  # Cache static assets aggressively (fingerprinted by Vite).' \
      '  location ~* \.(?:js|css|woff2?|ttf|otf|eot|svg|png|jpg|jpeg|gif|webp)$ {' \
      '    expires 30d;' \
      '    access_log off;' \
      '    add_header Cache-Control "public, max-age=2592000, immutable";' \
      '    try_files $uri =404;' \
      '  }' \
      '}' \
      > /etc/nginx/conf.d/default.conf
    
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]
    