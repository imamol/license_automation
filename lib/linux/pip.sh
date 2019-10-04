if [ -s /python_package_list.csv ]
then

        lines=`cat /python_package_list.csv`
        for line in $lines
        do
                license=`pip show $line | grep License:`
                echo $license

                if [ -z "$license" ]
                then
                        echo "NONE" >> /licenses
                else
                        license=`echo $license | sed  's/License: //g'`
                        echo $license >> /licenses

                fi
        done

        paste -d","  /python_package_list.csv /licenses  > /python_license_list.csv
else
	mv /python_package_list.csv /python_license_list.csv
fi
