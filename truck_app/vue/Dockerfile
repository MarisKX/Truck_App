#client vue Dockerfile
FROM node:14.17.5 as build-stage
WORKDIR /vue
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build
EXPOSE 8080
CMD [ "npm", "run", "serve" ]