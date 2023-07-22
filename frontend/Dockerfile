# base image
FROM node:18

# install chrome for protractor tests
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -yq google-chrome-stable

# set working directory
WORKDIR /usr/src/fronted

# add `/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/fronted/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/fronted/package.json
RUN npm install

# add app
COPY . /usr/src/fronted
