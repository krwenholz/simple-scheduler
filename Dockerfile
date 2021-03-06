FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1

EXPOSE 8080

RUN apt-get update
RUN apt-get install --yes npm nodejs
# Link nodejs to node so bower can find it
RUN update-alternatives --install /usr/bin/node nodejs /usr/bin/nodejs 100
RUN npm install
RUN node_modules/bower/bin/bower install --allow-root
