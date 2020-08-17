FROM node:alpine

WORKDIR /app
RUN npm i -g @angular/cli \
    && npm install angular-http-server -g

COPY /frontend/package.json package.json
RUN npm install --silent
COPY /frontend .
RUN ng build --prod
EXPOSE 8080

CMD npm run prod