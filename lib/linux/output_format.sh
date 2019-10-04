#!/bin/bash

cat list | cut -d ':' -f 1 > l1
mv l1 list
cat ubuntu_packages.csv | grep -v "_NA_" > t1
cat t1 > ubuntu_packages.csv
cat ubuntu_packages.csv | awk '{print $1}' > temp
sed -i '1d' temp  ubuntu_packages.csv
#cat ubuntu_packages.csv  >> ../Final_license_list
grep -vxf temp list  > remaining_pkgs
#echo -en '\n'  >> ../Final_license_list
mv temp license_found_from_copyright

rm -rf t1  copyrights  final_output.txt outputFile.txt 
