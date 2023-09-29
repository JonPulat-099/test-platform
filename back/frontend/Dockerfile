FROM node:12-alpine

WORKDIR /var/www

RUN node --version
RUN npm --version
# RUN npm i -g --silent pm2
COPY package*.json ./


RUN npm install && npm cache clean --force
COPY  . .
# RUN npm run generate
