#!/bin/sh

RECIPIENT="root"

/usr/bin/mail -s "Virus detected: ${CLAM_VIRUSEVENT_VIRUSNAME}" ${RECIPIENT} <<EOF
A virus has been detected in the file ${CLAM_VIRUSEVENT_FILENAME}

This message was generated by ClamAV
EOF