FROM pwn.red/jail
COPY --from=ubuntu / /srv
RUN mkdir -p /srv/app/lib #&& ln -s /bin/sh /srv/app/run
ADD ./flag.txt /srv/app/flag.txt
ADD ./lib /srv/app/lib
ADD ./chall /srv/app/run

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run
RUN chmod +x /srv/app/lib/ld-linux-x86-64.so.2


