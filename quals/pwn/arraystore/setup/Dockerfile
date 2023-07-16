FROM pwn.red/jail
COPY --from=ubuntu / /srv

COPY ./arraystore /srv/app/run
COPY ./flag.txt /srv/app/flag.txt

ENV JAIL_MEM=64M JAIL_PORT=10546