FROM pwn.red/jail
COPY --from=ubuntu / /srv

ADD ./flag.txt /srv/app/flag.txt
ADD ./chall /srv/app/run

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run