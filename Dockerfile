# BUILDING VUE
FROM node AS building-stage

WORKDIR /app

COPY /frontend/package*.json /app

RUN npm install --unsafe-perm

COPY /frontend /app/

RUN npm run build

# PRODUCTION IMAGE
FROM python:3.12-slim as production-stage

COPY /backend/requirements.txt .
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y nginx && apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV production

COPY /backend/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=building-stage /app/dist /var/www/html

WORKDIR /app
COPY /backend/src /app

EXPOSE 80
EXPOSE 502

CMD ["sh", "-c", "nginx -g 'daemon off;' & python main.py"]