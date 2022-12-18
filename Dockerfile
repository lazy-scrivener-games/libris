FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y python3-pip
RUN apt install -y libpangocairo-1.0-0
RUN pip install libris

CMD bash
