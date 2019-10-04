import requests
import xml.etree.ElementTree as ET

def get_openhub_data():

        with open('final_output/remaining_list.csv') as file:
                rem_packages = [ line.strip() for line in file.readlines()]

        #print(rem_packages)
        
        
        with open("final_output/Final_license_list.csv", 'a') as o_file:
                
                with open('final_output/remaining_list.csv','w') as file:
                        for package in rem_packages:
                                line = _get_data( package.strip() )
                                if line != package:
                                        o_file.write(line)
                                else:
                                        file.write(package+'\n')                        

        

def _get_data( package ):

        #print(package)
        url = "https://www.openhub.net/p/" + package + ".xml?api_key=704edce637a89135302910c178076ed209b0bfe92a4d6bbc294d5858c997e61a"
        try:
                r = requests.get(url)
                
        except Exception:
                print(" Try changing proxy setting.. Not able to access url..")
        
 

        if r.status_code>400:
                return package
        try:
                if "<status>" not in r.text:
                        return package
                #print(package)
                root = ET.fromstring(r.content)
                #root = tree.getroot()
                status = root.find('status').text

                license_info = ''
                
                for html_url in root.iter('html_url'):
                        url = html_url.text
                for lic in root.iter('license'):
                        license_info = lic.find('name').text
                if license_info != ''        :
                        line = package + '| | ' + license_info + '|openhub.net|NA|'+ url + '\n'
                        #print(line)
                        return line
                else:
                        return package
        except Exception as e:
                Wprint(e)
                return package

