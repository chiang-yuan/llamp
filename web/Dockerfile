FROM node:16-slim

# EXPOSE 5984

# WORKDIR /srv/app

# COPY package*.json .

# # RUN npm install --production=false

# RUN npm install --production=false

# COPY . .

# # RUN chown -R node /srv/app

# RUN npm run build

# CMD ["npm", "run", "serve"]

# Create and set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the frontend application source code into the container
COPY . .

RUN chown -R 99580:0 /app

RUN usermod -u 99580 node && \ 
    groupmod -g 99580 node 

# Build the frontend application (replace 'npm run build' with your build command if needed)
RUN npm run build

# Expose the port your frontend application will run on (if necessary)
EXPOSE 80

# Define the command to start the web server (adjust as needed)
CMD ["npm", "run", "serve"]
