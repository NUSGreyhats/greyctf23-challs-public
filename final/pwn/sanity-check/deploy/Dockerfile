FROM ubuntu:22.04

RUN apt-get update \
        && apt-get install -y qemu-system-x86 xinetd

RUN useradd --create-home --shell /bin/bash ctf

WORKDIR /home/ctf

COPY ./initramfs.cpio.gz /home/ctf
COPY ./run.sh /home/ctf
COPY ./bzImage /home/ctf
COPY ./pow /home/ctf
COPY ./setup.py /home/ctf
COPY ./service.conf /service.conf

RUN chmod +x run.sh
RUN chmod +x pow
RUN chmod +x setup.py

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

CMD ["/usr/sbin/xinetd", "-dontfork", "-f", "/service.conf"]
