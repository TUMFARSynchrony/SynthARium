#!/bin/bash

echo "Generating new self signed certificate using openssl."

echo "Please input the IP address (e.g. 127.0.0.1) the backend runs on:"
read backend
echo "Got: $backend"

openssl req -newkey rsa:4098 -x509 -nodes -keyout key.key -new -out cert.crt \
	-sha256 -days 712 -subj "//CN=localhost/CN=localhost" \
	-addext "subjectAltName=DNS.1:localhost,IP:127.0.0.1,IP:$backend"


if [ $? -ne 0 ];
then
	echo "Failed to generate certificate."
else 
	echo "------------------------------------------------------------"
	echo "You may have to manually open a connection to the backend in"
	echo "your browser and \"accept the risk\" to allow the frontend to"
	echo "access the backend when using a self signed certificate."
	echo "To do that, open http(s)://$backend:<backend port>"
	echo "------------------------------------------------------------"
	echo "Certificate finished"
fi

$SHELL
