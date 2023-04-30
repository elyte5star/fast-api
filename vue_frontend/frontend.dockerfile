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


# Set working directory to nginx asset directory
WORKDIR /usr/share/nginx/html

COPY ./frontend/nginx.conf /etc/nginx/templates/nginx.conf.template


COPY --from=build-stage /vue-ui/dist /usr/share/nginx/html

EXPOSE 8080

ENTRYPOINT ["nginx", "-g", "daemon off;"]