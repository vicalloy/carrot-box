FROM       python:3.8
MAINTAINER vicalloy "https://github.com/vicalloy"

RUN apt-get update && apt-get install -y \
		npm \
		pkg-config \
	  --no-install-recommends && \
		rm -rf /var/lib/apt/lists/* && \
		npm install -g yarn

RUN pip install --upgrade pip setuptools pipenv

RUN mkdir /app
WORKDIR /app

COPY ./ ./
RUN pipenv install -d --skip-lock --system
RUN make init

EXPOSE 9000
CMD ["make", "run"]
