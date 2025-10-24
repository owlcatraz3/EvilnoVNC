#!/bin/bash
# Get the pid of the websocket connection from a source (if reverse proxy is used to direct victim to the malicious webpage), then kill the connection. Edit the source IP address as needed.
pid=$(sudo docker exec evilnovnc sudo ss -tunp | grep 192.168.100.22 | awk -F'pid=' '{print $2}' | awk -F',' '{print $1}')

sudo docker exec evilnovnc sudo kill $pid
