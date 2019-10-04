#!/bin/bash

remove_image=$1
password=$2

cd License-Automation
if [ -f build_container_output ]
then
	
	base_container=`cat build_container_output | grep base_container | cut -d":" -f2`
    app_container=`cat build_container_output | grep app_container | cut -d":" -f2`
    app_image=`cat build_container_output | grep app_image | cut -d":" -f2`
	#echo $base_container 
	#echo $app_container
	#echo $app_image
    echo $password | sudo -S docker rm -f $base_container $app_container
	if [ "$remove_image" = "yes" ]
	then
        	docker rmi $app_image
	fi
fi
rm -rf build_container_output
