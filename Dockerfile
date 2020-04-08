FROM       python:3.8
MAINTAINER vicalloy "https://github.com/vicalloy"

RUN apt-get update && apt-get install -y \
		npm \
		pkg-config \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN npm install -g bower
RUN pip install --upgrade pip setuptools

WORKDIR /opt
COPY . /opt/carrot-box
WORKDIR /opt/carrot-box
RUN make init-docker

EXPOSE 9000
CMD ["make", "run"]
