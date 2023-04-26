# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

RUN rm /etc/nginx/conf.d/default.conf

COPY ./frontend/nginx.conf /etc/nginx

# Set working directory to nginx asset directory
WORKDIR /usr/share/nginx/html

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
