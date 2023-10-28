FROM node:16-slim

EXPOSE 5984

WORKDIR /srv/app

COPY package*.json .

RUN npm install --production=false

COPY . .

RUN chown -R node /srv/app

RUN usermod -u 99580 node && \ 
    groupmod -g 99580 node 

RUN npm run build

CMD ["npm", "run", "serve"]
