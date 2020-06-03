#!/bin/sh

if [ $# != 3 ]
then
  echo "Usage: "$0" <listen_addr> <listen_port> <nus_server_addr>"
  exit 1
fi

python -m dnslib.intercept -a $1 -p $2 -i "nus.c.shop.nintendowifi.net IN A "$3
