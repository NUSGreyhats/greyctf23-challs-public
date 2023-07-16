FROM pwn.red/jail

# copy / from <some image> to /srv
COPY --from=ubuntu / /srv

COPY ./chall /srv/app/run
COPY ./books /srv/app/books
COPY ./lib /srv/app/lib
RUN chmod +x /srv/app/run

EXPOSE 5000
