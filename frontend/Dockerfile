FROM node:alpine

WORKDIR /app
RUN npm i -g @angular/cli \
    && npm install angular-http-server -g

ADD /frontend/package.json package.json
RUN npm install --silent
ADD /frontend .
RUN ng build --prod
EXPOSE 8080

CMD npm run prod