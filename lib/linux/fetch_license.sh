#!/bin/bash

clean_app_image=$1

#cleanup()
#{
#	remove_image=$1
#	
#	if [ -f build_container_output ]
#	then
#		base_container=`cat /tmp/build_container_output | grep base_container | cut -d":" -f2`
#		app_container=`cat /tmp/build_container_output | grep app_container | cut -d":" -f2`
#		app_image=`cat /tmp/build_container_output | grep app_image | cut -d":" -f2`
#		docker rm -f $base_container $app_container
#		if [ "$remove_image" = "yes" ]
#		then
#			docker rmi $app_image
#		fi
#	fi
#	rm -rf build_container_output
#}


#Fetch from ubuntu copyright file

cd ~/License-Automation
tr -d '\r' < remaining_list > list
if [ -s list ]
then
	app_container=`cat build_container_output | grep app_container | cut -d":" -f2 | sed 's/ //g'`
	echo $app_container
	docker cp analyze_vm.sh $app_container:/
	docker cp script.sh $app_container:/
	docker cp list $app_container:/
	docker exec $app_container /analyze_vm.sh
	docker cp $app_container:/ubuntu_packages.csv .
	sh output_format.sh
else
	cleanup
	exit
fi


#cleanup $clean_app_image
