ARG image=python:3.11.6
FROM $image
RUN apt-get update -y \
 && apt-get install -y xxd \
 && pip install --upgrade pip
WORKDIR /src
ARG email=docker@build
ARG name=docker
RUN git config --global user.email "$email" \
 && git config --global user.name "$name"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["./run.sh"]
