FROM node:12-alpine
RUN apk update && apk upgrade
RUN apk add bash

WORKDIR /var/www

RUN node --version
RUN npm --version
RUN npm i -g --silent pm2
COPY package*.json ./


RUN npm install && npm cache clean --force
COPY  . .
RUN npm run generate

