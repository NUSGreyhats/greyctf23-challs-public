FROM pwn.red/jail
COPY --from=alpine / /srv

COPY ./arraystore2 /srv/app/run
COPY ./flag.txt /srv/app/flag.txt

ENV JAIL_MEM=64M JAIL_PORT=20002
