gem_list=`cat gem_list.csv`
for gem in $gem_list
do
        license=`gem spec $gem license | head -n1 | cut -d " " -f2-`
		if [ -z "$license" ]
        then
                echo "$gem" >> /gem_remaining_list.csv
        else
			echo "$gem | | $license| gem_command | NA| NA" >> /gem_license_list.csv
		fi
done

if [ -f gem_license_list.csv ]
then
            echo ""
else
            touch /gem_license_list.csv
fi

if [ -f gem_remaining_list.csv ]
then
            echo ""
else
            touch /gem_remaining_list.csv
fi