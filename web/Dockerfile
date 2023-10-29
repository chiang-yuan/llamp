FROM node:16-slim

ENV NODE_ENV=production

EXPOSE 5984

WORKDIR /srv/app

COPY package*.json .

RUN npm install --production=false

COPY . .

RUN chown -R node /srv/app

RUN npm run build

CMD ["npm", "run", "serve"]