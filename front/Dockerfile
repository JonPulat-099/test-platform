
FROM node:12.22.12
WORKDIR /app
ADD ./package.json .
ADD ./package-lock.json .
RUN npm ci
RUN npm run build

COPY . /app/
