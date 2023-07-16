FROM riscv64/debian:sid
RUN apt update
RUN apt install -y socat
COPY ./ropv ./ropv
COPY ./flag.txt ./flag.txt
CMD ["socat", "-d", "-d", "TCP-LISTEN:12335,reuseaddr,fork,su=daemon", "EXEC:'timeout -s SIGKILL 60s ./ropv',stderr"]
