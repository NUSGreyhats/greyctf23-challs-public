FROM riscv64/debian:sid
RUN apt update
RUN apt install -y socat
COPY ./easypwn ./easypwn
COPY ./flag.txt ./flag.txt
CMD ["socat", "-d", "-d", "TCP-LISTEN:10533,reuseaddr,fork,su=daemon", "EXEC:'timeout -s SIGKILL 60s ./easypwn',stderr"]
