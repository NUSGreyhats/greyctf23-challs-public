# greyctf pwn jail
## Based on https://github.com/redpwn/jail
# Rudimentary per-connection python runner based on the Pwn Dockerfile template

FROM python:3 AS src

RUN apt-get update
RUN apt-get -y install python3-pip
RUN /usr/bin/python3 -m pip install --no-cache-dir pycryptodome

# This is the actual container that runs
FROM redpwn/jail:latest

ENV JAIL_TIME 300

# Copy the entire python filesystem from src to here
COPY --from=src / /srv/
COPY ./main.py /srv/app/run
EXPOSE 5000
RUN chmod +x /srv/app/run
