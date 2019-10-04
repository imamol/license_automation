#! /bin/sh
#
#**********************************************************************
#
# Licensed Materials-Property of IBM
#
# (C)Copyright IBM Corp 2018
#
# All rights reserved
#
# US Government Users Restricted Rights:
# Use, duplication, or disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp
#
#**********************************************************************

#----------------------------------------------------------------------
#   ContainerCreatePackageList.sh
#
#   create the .csv file from a running Docker container
#
#   @author..: David B. Kumhyr
#   Date.....: 10Apr18
#   VCS......: git
#   @version : 1.0
#
#------------------------------------------------------------------------
#
#   Changes:
#
#     10Apr18 - DBK: First version.
#
#
#---------------------------------------------------------------------

Usage() {
   local base=${0##*/}
   cat << EOF
Usage: ${base} ./ContainerCreatePackageList.sh containerID outfile
   containerID = Running Docker container ID  e.g. "hhhhhhhhhhhh" - You can obtain by running "Docker PS"
   outfile = comma separated value (.csv) file listing all components of the Docker container

   Builds an input file for WICKED Pedigree Service API /pedigree/check/file/{filetype}
   Upload a file to pedigree check all the listed packages at once.
   wicked-pedigree-service.w3ibm.mybluemix.net/api
EOF
    return 0;
}

#[ $# -ne 3 ] && {
#    Usage
#    exit 0
#}

if [ "$1" = "--help" -o "$1" = "-h" ]; then
	Usage
	exit 0
fi

containerID=$1
outfile=$2
pip_outfile=$3
npm_outfile=$4
r_outfile=$5
base_image=$6
password=$7
gem_outfile=$8


echo $base_image

echo "ContainerID is -> " $containerID
echo "    Outfile is -> " $outfile

# figure out the flavour of the Linux OS in the container
# we handle only Alpine/CentOS/RH/Ubuntu
# NTD err handle
DistroInfo="DistroInfo"
#echo $DistroInfo
osVer=""

echo $password | echo $password | sudo -S -S docker exec $containerID cat /etc/os-release > $DistroInfo
echo $DistroInfo
# expected return
# NAME="Alpine Linux"
# *ID=alpine
# *VERSION_ID=3.7.0
# PRETTY_NAME="Alpine Linux v3.7"
# HOME_URL="http://alpinelinux.org"
#  BUG_REPORT_URL="http://bugs.alpinelinux.org"

# Find the ID in verfile
# ATTN: since "ID=" is the key in front of both pieces of info I want to
# if i search for ID= it returns
# "alpine
# 3.7.0"
# So I need to get them separately and concatenate them to the outfile

grep -e ^ID= $DistroInfo > DistroName
sed -n 's/.*ID=//p' DistroName > CleanDistroName
# Have to add removing " because some people add them to some distro info files
sed -i -e 's/\"//g' CleanDistroName
DistroName=$(cat CleanDistroName)

sed -n 's/.*_ID=//p' $DistroInfo > DistroVersion
# Have to add removing " because some people add them to some distro info files
sed -i -e 's/\"//g' DistroVersion

DistroVer=$(cat DistroVersion)
Distro=$DistroName,$DistroVer
# nuke any prior outfile with the initial seek for packages
# find all the "From" statements in the Docker output
#grep From $infile > $outfile
# fianlly write the OS and version to the outfile
echo $Distro > $outfile
# nuke the tmpfiles
rm DistroName
rm DistroVersion
rm CleanDistroName

echo $DistroName > DistroName

#case for the $Distro
case $DistroName in

	# Alpine distro case
	"alpine") echo  "alpine linux"
		# pull the list of installed packages
        #docker exec $containerID apk info -vv | sort >> $outfile
        echo $password | echo $password | sudo -S docker exec $containerID apk info  > apkName
        paste apkName >> $outfile
        rm apkName
        
		echo $password | echo $password | sudo -S docker exec $containerID apk update
        echo $password | sudo -S docker exec $containerID apk add curl
        echo $password | sudo -S docker exec $containerID curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        echo $password | sudo -S docker exec $containerID python get-pip.py
        echo $password | sudo -S docker exec $containerID pip list | awk '{print $1}' >> $pip_outfile
        echo $password | sudo -S docker exec $containerID npm list --depth=1 --parseable |  awk -F "/" '{print $NF}' | sort -u > $npm_outfile
		echo $password | sudo -S docker exec $containerID gem list | awk '{print $1}' >> $gem_outfile
        exit 0
        ;;

	# rhel distro case
	"rhel") echo "Red Hat - rhel"
        echo $password | sudo -S docker exec $containerID rpm -qa --qf "%{NAME}\n" > qaName
        echo $password | sudo -S docker exec $containerID rpm -qa --qf "%{LICENSE}\n" > qaLicense
		paste -d"| " qaName qaLicense | awk -F'|' '{print $1, " | | ", $2, " | distro | NA | NA "}'  >> $outfile
        rm qaName
        rm qaLicense
		
		echo $password | sudo -S docker exec $containerID microdnf -h
		var=`echo $password | sudo -S docker exec $containerID echo $?`
		
		if [ $var==0 ];
		then
			# microdnf case
			echo $password | sudo -S docker exec $containerID microdnf install -y curl
			echo $password | sudo -S docker exec $containerID curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py
			echo $password | sudo -S docker exec $containerID python2 /get-pip.py
			echo $password | sudo -S docker exec $containerID pip list | awk '{print $1}' >> $pip_outfile
        else
			# yum case
			echo $password | sudo -S docker exec $containerID yum install -y curl
			echo $password | sudo -S docker exec $containerID curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py
			echo $password | sudo -S docker exec $containerID python2 /get-pip.py
			echo $password | sudo -S docker exec $containerID pip list | awk '{print $1}' >> $pip_outfile		
		fi
		
		echo $password | sudo -S docker exec $containerID npm list --depth=1 --parseable |  awk -F "/" '{print $NF}' | sort -u > $npm_outfile
		echo $password | sudo -S docker exec $containerID gem list | awk '{print $1}' >> $gem_outfile
        exit 0
        ;;
		
	# CentOS distro case
	"centos") echo "centos linux"
        echo $password | sudo -S docker exec $containerID rpm -qa --qf "%{NAME}\n" > qaName
        echo $password | sudo -S docker exec $containerID rpm -qa --qf "%{LICENSE}\n" > qaLicense
		paste -d"| " qaName qaLicense | awk -F'|' '{print $1, " | | ", $2, " | distro | NA | NA "}'  >> $outfile
        rm qaName
        rm qaLicense
        
		echo $password | sudo -S docker exec $containerID yum check-update
        echo $password | sudo -S docker exec $containerID yum  install -y curl
        echo $password | sudo -S docker exec $containerID curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py
        echo $password | sudo -S docker exec $containerID python /get-pip.py
        echo $password | sudo -S docker exec $containerID pip list | awk '{print $1}' >> $pip_outfile
        echo $password | sudo -S docker exec $containerID npm list --depth=1 --parseable |  awk -F "/" '{print $NF}' | sort -u > $npm_outfile
		echo $password | sudo -S docker exec $containerID gem list | awk '{print $1}' >> $gem_outfile
        exit 0
        ;;

	# fedora distro case
	"fedora") echo "Fedora linux"
        echo $password | sudo -S docker exec $containerID rpm -qa --qf "%{NAME}\n" > rhName
        echo $password | sudo -S docker exec $containerID rpm -qa --qf "%{LICENSE}\n" > rhLicense
        paste -d"| " qaName qaLicense | awk -F'|' '{print $1, " | | ", $2, " | distro | NA | NA "}'  >> $outfile
        rm rhLicense
        
		echo $password | sudo -S docker exec $containerID yum check-update
        echo $password | sudo -S docker exec $containerID yum install -y curl
        echo $password | sudo -S docker exec $containerID curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py
        echo $password | sudo -S docker exec $containerID python /get-pip.py
        echo $password | sudo -S docker exec $containerID pip list | awk '{print $1}' >> $pip_outfile
        echo $password | sudo -S docker exec $containerID npm list --depth=1 --parseable |  awk -F "/" '{print $NF}' | sort -u > $npm_outfile
		echo $password | sudo -S docker exec $containerID gem list | awk '{print $1}' >> $gem_outfile
        exit 0
        ;;

	# debian distro case
	"debian") echo "Debian linux"
        # docker exec $containerID dpkg --get-selections | grep -v "deinstall" | cut -f1 > ubName
        echo $password | sudo -S docker exec $containerID dpkg --get-selections | cut -f1 > ubName
        #docker exec $containerID dpkg-query -W -f='${version}\n' > ubVersion
        # remove the spurious ":ppc64el" from the package names
        #sed -i -e 's/-.*//' ubVersion
        #sed -i -e 's/+.*//' ubVersion
        sed -i -e 's/\:ppc64el//g' ubName
	sed -i -e 's/\:amd64//g' ubName
        paste ubName >> $outfile
        rm ubName
        #rm ubVersion

        if [ "$base_image" = "ppc64le/r-base" ]
		then
			echo $passowrd | sudo -S docker exec $containerID R -e 'installed.packages(fields = "License")[,c(1,10)]' >> $r_outfile
		else
			echo $password | sudo -S docker exec $containerID apt-get update
				echo $password | sudo -S docker exec $containerID apt-get install -y curl
				echo $password | sudo -S docker exec $containerID curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py
				echo $password | sudo -S docker exec $containerID python /get-pip.py
				echo $password | sudo -S docker exec $containerID pip list | awk '{print $1}' >> $pip_outfile
				echo $password | sudo -S docker exec $containerID npm list --depth=1 --parseable |  awk -F "/" '{print $NF}' | sort -u > $npm_outfile
				echo $password | sudo -S docker exec $containerID gem list | awk '{print $1}' >> $gem_outfile
		fi
        exit 0
        ;;

	# ubuntu distro case
	"ubuntu") echo "Ubuntu linux"
        # docker exec $containerID dpkg --get-selections | grep -v "deinstall" | cut -f1 > ubName
        echo $password | sudo -S docker exec $containerID dpkg --get-selections | cut -f1 > ubName
        #docker exec $containerID dpkg-query -W -f='${version}\n' > ubVersion
        # remove the spurious ":ppc64el" from the package names
        #sed -i -e 's/-.*//' ubVersion
        #sed -i -e 's/+.*//' ubVersion
        sed -i -e 's/\:ppc64el//g' ubName
 	sed -i -e 's/\:amd64//g' ubName
        paste ubName >> $outfile
        rm ubName

       
	echo $password | sudo -S docker exec $containerID apt-get update
        echo $password | sudo -S docker exec $containerID apt-get install -y curl
        echo $password | sudo -S docker exec $containerID curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py
        echo $password | sudo -S docker exec $containerID python /get-pip.py
        echo $password | sudo -S docker exec $containerID pip list | awk '{print $1}' >> $pip_outfile
        echo $password | sudo -S docker exec $containerID npm list --depth=1 --parseable |  awk -F "/" '{print $NF}' | sort -u > $npm_outfile
		echo $password | sudo -S docker exec $containerID gem list | awk '{print $1}' >> $gem_outfile
        exit 0
        ;;

	*) echo "Unknown linux"
        echo "Distro unknown to this script"
        exit -1
        ;;

esac

# create a tempfile
#TmpOut=$(mktemp tmpfile18SSC.XXXXXXXXXX) || { echo "Failed to create temp file"; exit -1; }

# Pour the changes back into the proper file
#cp $TmpOut $outfile

# DBK NTD - for some reason the sed adds a -e suffix and so the rm doesn't work?
#rm $TmpOut
