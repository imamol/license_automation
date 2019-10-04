#!/bin/bash


WORK_DIR=`dirname $0`
COPYRIGHTS_DIR=${WORK_DIR}/copyrights
REPORTS_DIR=${WORK_DIR}/reports


###################################################################
# analyze_ubuntupacks
#
#
# Description:
#     This function retrieve the information about the Ubuntu 
#     packages.
#
###################################################################
analyze_ubuntupacks()
{
    # PACKAGES=`dpkg --get-selections | awk '{print $1}'`
    PACKAGES=`cat list`
    UBUNTU_REPORT_CSV=ubuntu_packages.csv
    COPYRIGHT_FILE=""
    VERSION=""
    LICENSE_TYPE=""

    rm -f ${UBUNTU_REPORT_CSV}
    rm -rf ${COPYRIGHTS_DIR}
    touch ${UBUNTU_REPORT_CSV}
    echo "#Package	Version	   Repository	Licenses_type	Is_GPL   Comments" >> ${UBUNTU_REPORT_CSV}
    for dep in ${PACKAGES}
    do
        if [ "echo ${dep} | grep ':ppc64el'" ]
        then
            dep=`echo ${dep} | cut -d ':' -f 1`
        fi
        COPYRIGHT_FILE=`dpkg -L $dep | grep copyright`
        if [ $? != 0 ]
        then
            LICENSE_TYPE="_NA_"
            IS_GPL="Others"
        else
            LICENSE_TYPE=""
            mkdir -p ${COPYRIGHTS_DIR}/$dep
            cp ${COPYRIGHT_FILE} ${COPYRIGHTS_DIR}/$dep
    
            LICENSES=`grep "License:" ${COPYRIGHT_FILE} | sed -e 's/License: //g' | sed -e 's/License://g'`
            if [ "${LICENSES}" != "" ]
            then
                while read -r licLines; do
                    if [ "${LICENSE_TYPE}" = "" ]
                    then
                        LICENSE_TYPE=$licLines
                    else
                        echo ${LICENSE_TYPE} | grep "$licLines" > /dev/null
                        if [ $? -eq 1 ]
                        then
                            LICENSE_TYPE=$licLines,${LICENSE_TYPE}
                        fi 
                    fi
                done <<< "${LICENSES}"
            fi
            if [ "${LICENSE_TYPE}" = "" ]
            then
                LICENSE_TYPE="_NA_"
            fi
            echo $LICENSE_TYPE | grep "GPL" > /dev/null
            if [ $? -eq 0 ]
            then
                IS_GPL="GPL"
            else
                grep "GPL" ${COPYRIGHT_FILE} > /dev/null
                if [ $? -eq 0 ]
                then
                    IS_GPL="GPL"
                else
                    IS_GPL="Others"
                fi 
            fi
        fi
        
        VERSION=`dpkg -s $dep | egrep "^Version:" | cut -f 2 -d " "`
        if [ ! -z "$COPYRIGHT_FILE" ]
		then 
			  bash script.sh "$COPYRIGHT_FILE"    
			  Comments=`cat final_output.txt`	
		fi
     
        echo "$dep | | $LICENSE_TYPE | Copyright_File     |  $Comments |  NA " >> ${UBUNTU_REPORT_CSV}
        # egrep -lRI "^Filename: .*/${dep}_[^/]+.deb" /var/lib/apt/lists/ | grep -q 'restricted' && echo "$dep	$VERSION	restricted	$LICENSE_TYPE	$IS_GPL  $Comments " >> ${UBUNTU_REPORT_CSV}
        # egrep -lRI "^Filename: .*/${dep}_[^/]+.deb" /var/lib/apt/lists/ | grep -q 'main' && echo "$dep	$VERSION	main	$LICENSE_TYPE	$IS_GPL  $Comments " >> ${UBUNTU_REPORT_CSV}
        # egrep -lRI "^Filename: .*/${dep}_[^/]+.deb" /var/lib/apt/lists/ | grep -q 'multiverse' && echo "$dep	$VERSION	multiverse	 $IS_GPL  $Comments " >> ${UBUNTU_REPORT_CSV} 
        # egrep -lRI "^Filename: .*/${dep}_[^/]+.deb" /var/lib/apt/lists/ | grep -q 'universe' && echo "$dep	$VERSION	universe	$LICENSE_TYPE	$IS_GPL  $Comments " >> ${UBUNTU_REPORT_CSV}
    done
#    echo "Successfully fetched the licenses from copyright file"
}

# echo "\n Successfully fetched the license from copyright"
###################################################################
# Main block
###################################################################
analyze_ubuntupacks
