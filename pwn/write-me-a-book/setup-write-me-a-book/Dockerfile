FROM pwn.red/jail

# copy / from <some image> to /srv
COPY --from=ubuntu / /srv

COPY ./chall /srv/app/run
COPY ./lib /srv/app/lib
COPY ./flag /srv/flag
RUN chmod +x /srv/app/run

EXPOSE 5000
