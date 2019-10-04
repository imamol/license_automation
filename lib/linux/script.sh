#!/bin/bash

COPYRIGHT_FILE=$1
# Remove copyright lines
sed '/^Copyright:/,/^\License:/{/^Copyright:/!{/^\License:/!d}}'   ${COPYRIGHT_FILE}  > temp1
cat temp1 | grep -v Copyright > temp2
# Fetch Files and licenses
sed -n '/^Files:/,/^License:/p' temp2 > temp3
awk 'NR==FNR{if (/^Files:|^License:/) hit=NR; next} {print} FNR==hit{exit}'  temp3 temp3

# Remove whitespace from License line
# e.g. License: BSD (clause)  --->  License: BSD(clause)
sed -i  '/License:/ {s/ //g}; s/License:/License: /g' temp3


printf  "\nFinal output....................... \n"

# Combine all the files for same license.
awk '
  $1=="License:"{
     a[$2]=a[$2](a[$2]?",":"")f;
     f="";
     next
  }
  $1=="Files:"{
     $1=$2
  }
  {
     f=f (f?",":"")$1
  }
  END{
    for(i in a)
      printf "%s(%s)\n",i,a[i]
  }'  temp3 > outputFile.txt 


# For some packages, we are getting 100+ files for particular license ,which is difficult to hold in one line. 
# So adding below line to keep maximum 5 files per license.
# If file count exceeds limit of 5, then script will add a message saying "More than 5 files , to view all the files 
# of this license please check copyright file of that package".
cat outputFile.txt  | sed 's/,/)"More_than_5_Files_for_this_license"Line_cutter/5' | sed 's/Line_cutter.*//'  > temp4
cat temp4 |  tr '\n' ', '  > final_output.txt
rm temp1  temp2 temp3 temp4 
