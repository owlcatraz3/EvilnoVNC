#!/bin/bash

pid=$(sudo docker exec evilnovnc sudo ss -tunp | grep 192.168.100.22 | awk -F'pid=' '{print $2}' | awk -F',' '{print $1}')

sudo docker exec evilnovnc sudo kill $pid
