FROM ubuntu:20.04

# Invariants
ARG PORT=10000
ARG USERNAME=user
ENV USERNAME ${USERNAME}
RUN useradd -m $USERNAME
RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Challenge files
ADD chal /home/$USERNAME/
RUN chown root:root /home/$USERNAME
RUN chmod 444 /home/$USERNAME/*
RUN chmod +x /home/$USERNAME/monkeytype
EXPOSE $PORT

ENV TERM xterm
ENV COLUMNS 37
ENV LINES 10

CMD socat TCP-LISTEN:10000,reuseaddr,fork EXEC:/home/user/monkeytype

