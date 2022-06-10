#!/bin/bash
free | cut -c 1-80 | sed -e '3d' 
while true; do
	free | cut -c 1-80 | sed -e '1d' -e '3d'
	sleep 5
done
