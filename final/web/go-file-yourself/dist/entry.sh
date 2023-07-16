#!/bin/sh

clamd

clamonacc
while [ $? -ne 0 ]; do 
    clamonacc
done

su appuser -c "/app" -s /bin/sh