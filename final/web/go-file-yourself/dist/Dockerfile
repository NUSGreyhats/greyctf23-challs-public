#build stage
FROM golang:alpine AS builder
RUN apk add --no-cache git
WORKDIR /go/src/app
COPY . .
RUN go get -d -v ./...
RUN go build -o /go/bin/app -v ./...

#final stage
FROM debian:bullseye
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends clamav clamav-daemon clamdscan postfix mailutils ca-certificates -y
COPY --from=builder /go/bin/app /app
COPY entry.sh /entry.sh
RUN chmod 755 /entry.sh
RUN chmod 755 /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN mkdir /uploads
RUN chmod 755 /uploads
RUN chown appuser:appuser /uploads

RUN freshclam
RUN mkdir /var/run/clamav
RUN chown clamav:clamav /var/run/clamav
COPY mailvirus.sh /etc/clamav/virusevent.d/mailvirus
RUN chmod 755 /etc/clamav/virusevent.d/mailvirus
RUN echo "OnAccessIncludePath /uploads" >> /etc/clamav/clamd.conf
RUN echo "OnAccessExcludeUname clamav" >> /etc/clamav/clamd.conf
RUN echo "VirusEvent run-parts /etc/clamav/virusevent.d" >> /etc/clamav/clamd.conf

RUN apt-get install -y gcc
COPY flag /flag
RUN chmod 400 /flag
COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod 4755 /readflag
RUN rm /readflag.c

ENTRYPOINT [ "/entry.sh" ]
LABEL Name=gofileyourself Version=0.0.1
EXPOSE 3000
