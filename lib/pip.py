import json
import requests
import bs4



def get_license(package):
        package = package.lower()

        r = requests.get('https://pypi.org/project/'+package)

        soup = bs4.BeautifulSoup(r.text, features="html.parser")

        for link in soup.find_all('p'):
                text = link.get_text()
                #print(text)
                if "License:" in text:
                        text = text.replace('License: ','')
                        #print (text)
                        #text = text.replace(',',' | ')
                        return text

def merge_python_output():

        with open('python_license_list.csv') as file:
                lines = file.readlines()
                #print (lines)

        with open('DistroName') as file:
                name = file.read().strip()
                if name == 'centos' or name=='fedora':
                        file_name = 'final_output/remaining_list.csv'
                else:
                        file_name = 'input_package_list.csv'
                        
        for line in lines:
                if "---" in line:
                        continue

                package_name, license_name = line.split(',')[0].strip() , line.split(',')[1].strip()



                with open('final_output/Final_license_list.csv','a+') as file:
                        with open(file_name,'a') as rfile:
                                if license_name in ["NONE", "UNKNOWN"]:
                                        #print(package_name, license_name)
                                        try:
                                                license_name = get_license(package_name)
                                                file.write(package_name + " | | " + license_name + "|pypi.org | NA| NA\n")
                                        except:
                                                rfile.write(package_name +"\n")
                                else:
                                        file.write(package_name + " | | " + license_name + "| pip_command | NA| NA\n")

         
