

package_list=`cat /npm_package_list.csv`

for package in $package_list
do
        license=`npm show $package license`

        echo "$package | | $license| npm_command | NA| NA" >> /npm_license_list.csv
done


if [ -f /npm_license_list.csv ]
then
	echo ""
else
	touch /npm_license_list.csv
fi