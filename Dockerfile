FROM       python:3.8
MAINTAINER vicalloy "https://github.com/vicalloy"

RUN apt-get update && apt-get install -y \
		npm \
		pkg-config \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN npm install -g bower
RUN pip install --upgrade pip setuptools
#RUN ln -s /usr/bin/nodejs /usr/bin/node

WORKDIR /opt
#RUN git clone https://github.com/vicalloy/carrot-box
COPY . /opt/carrot-box
WORKDIR /opt/carrot-box
RUN make init

EXPOSE 9000
CMD ["make", "run"]
