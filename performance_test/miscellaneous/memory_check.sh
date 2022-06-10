#!/bin/bash
while true; do
	sed -n '1,3p' /proc/meminfo; cat /proc/meminfo | grep Slab; date
	sleep 5
done
