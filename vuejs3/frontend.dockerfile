# build stage
FROM node:lts-alpine as build-stage

# Set working directory
WORKDIR /vue-ui

# Copy the package.json and install dependencies
COPY ./frontend/package*.json ./
RUN npm install

# Copy rest of the files
COPY ./frontend .

# Build the project
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /vue-ui/dist /usr/share/nginx/html

COPY --from=build-stage /vue-ui/nginx.conf /etc/nginx/templates/nginx.conf.template

EXPOSE 8000

CMD ["nginx", "-g", "daemon off;"]