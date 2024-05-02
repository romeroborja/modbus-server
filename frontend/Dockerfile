# DEVELOPMENT
FROM node:lts-alpine as development-stage

WORKDIR /app

COPY package*.json /app

RUN npm install

COPY . /app/

CMD ["npm", "run", "serve"]

# BUILDING
FROM node AS building-stage

WORKDIR /app

COPY package*.json /app

RUN npm install --unsafe-perm

COPY . /app/

RUN npm run build

# PRODUCTION
FROM nginx as production-stage

COPY --from=building-stage /app/dist /usr/share/nginx/html

COPY nginx/nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
