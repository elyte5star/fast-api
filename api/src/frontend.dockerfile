
# build stage
FROM node:lts-alpine as build-stage

# make the 'app' folder the current working directory
WORKDIR /app

COPY /resources/frontend/package*.json ./

RUN npm install
# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY ./resources/frontend .

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]