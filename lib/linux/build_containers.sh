#!/bin/bash

if [ "$#" -eq 0 ]
then
        echo "Check arguments to the script!"
        exit 10
fi

cleanup()
{
	rm -rf build_output base_outfile app_outfile
	if [ "$#" -ne 0 ]
	then
		rm -rf build_container_output 
	fi
}

cleanup 1

if [ "$#" -eq 2 ]
then
	dockerfile_path=$1
	password=$2

	base_image=`grep FROM $dockerfile_path/Dockerfile | tail -1 | awk '{print $2}'`

	echo "Base Image : $base_image"

	echo $password | sudo -S docker build $dockerfile_path > build_output

	application_image_id=`grep -i "Successfully built" build_output | cut -d" " -f3`

	echo "Application Image ID : $application_image_id"
	if [ -z $application_image_id ]
	then
		exit 10
	fi

	base_container_id=`echo $password | sudo -S docker run -d -it $base_image /bin/sh`

	application_container_id=`echo $password | sudo -S docker run -d -it $application_image_id /bin/sh`

	echo "Base Image Container : $base_container_id \nApplication Image Container : $application_container_id"
fi

if [ "$#" -eq 3 ]
then
	base_container_id=$1
	application_container_id=$2
	password=$3
fi

cd License-Automation/
sh ContainerCreatePackageList.sh $base_container_id base_outfile base_pip base_npm base_r $base_image $password base_gem #> /dev/null
sh ContainerCreatePackageList.sh $application_container_id app_outfile app_pip app_npm app_r $base_image $password app_gem #> /dev/null

DistroName=`cat DistroName`

echo $DistroName

if  [ "$DistroName" = "centos" ] || [ "$DistroName" = "fedora" ]
then
	echo "centos/fedora case"
	grep -F -x -v -f base_outfile app_outfile > Final_license_list.csv
	sed -i '1iPackage name | Modified package name | License | Source of License Information | Comments | Copyright Links/References ' Final_license_list.csv
	cut -d "," -f 1 Final_license_list.csv > input_package_list.csv
	
	sed -i -e 1,3d base_pip
    sed -i -e 1,3d app_pip
    grep -F -x -v -f base_pip app_pip > python_package_list.csv
    grep -F -x -v -f base_npm app_npm > npm_package_list.csv
	grep -F -x -v -f base_gem app_gem > gem_list.csv

	echo $password | sudo -S docker cp python_package_list.csv $application_container_id:/
	echo $password | sudo -S docker cp pip.sh $application_container_id:/
	echo $password | sudo -S docker exec $application_container_id sh /pip.sh
	echo $password | sudo -S docker cp $application_container_id:/python_license_list.csv .
			
    echo $password | sudo -S docker cp npm_package_list.csv $application_container_id:/
	echo $password | sudo -S docker cp npm.sh $application_container_id:/
	echo $password | sudo -S docker exec $application_container_id sh /npm.sh
	echo $password | sudo -S docker cp $application_container_id:/npm_license_list.csv .

	echo $password | sudo -S docker cp gem_list.csv $application_container_id:/
	echo $password | sudo -S docker cp gem.sh $application_container_id:/
	echo $password | sudo -S docker exec $application_container_id /gem.sh
	echo $password | sudo -S docker cp $application_container_id:/gem_license_list.csv .
	echo $password | sudo -S docker cp $application_container_id:/gem_remaining_list.csv .
elif [ "$DistroName" = "rhel" ]
then
	echo "rhel case"
	grep -F -x -v -f base_outfile app_outfile > Final_license_list.csv
	sed -i '1iPackage name | Modified package name | License | Source of License Information | Comments | Copyright Links/References ' Final_license_list.csv
	cut -d "," -f 1 Final_license_list.csv > input_package_list.csv
else
	echo "ubuntu / alpine case"
	#cut -d "," -f 1 base_outfile > /tmp/base
	#cut -d "," -f 1 app_outfile > /tmp/app

	grep -F -x -v -f base_outfile app_outfile > input_package_list.csv
	
	if [ "$base_image" = "ppc64le/r-base" ]
	then
		 grep -F -x -v -f base_r app_r > rbase_license_list.csv
	
	else
		sed -i -e 1,3d base_pip
    		sed -i -e 1,3d app_pip
    		grep -F -x -v -f base_pip app_pip > python_package_list.csv
    		grep -F -x -v -f base_npm app_npm > npm_package_list.csv
			grep -F -x -v -f base_gem app_gem > gem_list.csv

			echo $password | sudo -S docker cp python_package_list.csv $application_container_id:/
			echo $password | sudo -S docker cp python_package_list.csv $application_container_id:/
			echo $password | sudo -S docker cp pip.sh $application_container_id:/
			echo $password | sudo -S docker exec $application_container_id sh /pip.sh
			echo $password | sudo -S docker cp $application_container_id:/python_license_list.csv .
			
    		echo $password | sudo -S docker cp npm_package_list.csv $application_container_id:/
			echo $password | sudo -S docker cp npm.sh $application_container_id:/
			echo $password | sudo -S docker exec $application_container_id sh /npm.sh
			echo $password | sudo -S docker cp $application_container_id:/npm_license_list.csv .
			echo $password | sudo -S docker cp gem_list.csv $application_container_id:/

			echo $password | sudo -S docker cp gem_list.csv $application_container_id:/
			echo $password | sudo -S docker cp gem.sh $application_container_id:/
			echo $password | sudo -S docker exec $application_container_id sh /gem.sh
			echo $password | sudo -S docker cp $application_container_id:/gem_license_list.csv .
			echo $password | sudo -S docker cp $application_container_id:/gem_remaining_list.csv .
	fi
fi

cleanup 

echo "base_container:$base_container_id \napp_container:$application_container_id \napp_image:$application_image_id" > build_container_output
