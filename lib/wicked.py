import requests
import json
import os

def get_wicked_data_before_src():
        
        with open('final_output/remaining_list.csv') as file:
                packages = [package.strip() for package in file.readlines()]
                                
        # write all the packages in a csv file for wicked input
        with open('wicked_input.csv','w') as file:
                for package in packages:
                        file.write(package + "\n")
        
        url = 'https://wicked-pedigree-service.w3ibm.mybluemix.net/api/pedigree/check/file'
        files = {'file': open('wicked_input.csv', 'rb')}

        try:
                r = requests.post(url, files=files)
        except Exception as e:
                print ("Connection to Wicked failed! Check system proxy settings.")
                #print e
                exit()
                
        try:
                file = open("file.json", "w")
                file.write(r.text)
                file.close()
                print ("wicked response received!")
        except:
                print ("Error while writing wicked response to file!")
                exit()

        try:
                r.connection.close()
        except Exception as e:
                #print e
                exit()
        
        # This file contains wicked response
        jsonFile = open('file.json', 'r')
        jsonData = json.load(jsonFile)
        jsonFile.close()


        # print(type(jsonData))
        # return dictionary with key as package_name and value as the entire line to be written in Final_license_list.csv file
        package_names = _extract_licenses(jsonData)
        with open('final_output/Final_license_list.csv','a') as file:
                for key, value in package_names.items():
                        file.write( key + " | ")
                        file.write( value + '\n' )
                        packages.remove(key)
                
        _update_remaining_list( {}, packages)

        os.remove('file.json')
                
                
                
def get_wicked_data_after_src(dict_packages, src_packages, nosrc_packages):

        src_packages = set(src_packages)
        with open('wicked_input.csv','w') as file:
                for package in src_packages:
                        file.write(package + '\n')

        # write all the src packages in a csv file for wicked input
        with open('wicked_input.csv','a') as file:
                for package in nosrc_packages:
                        file.write(package + '\n')
        
        url = 'https://wicked-pedigree-service.w3ibm.mybluemix.net/api/pedigree/check/file'
        files = {'file': open('wicked_input.csv', 'rb')}

        try:
                r = requests.post(url, files=files)
        except Exception as e:
                print ("Connection to Wicked failed! Check system proxy settings.")
                #print e
                exit()
                
        try:
                file = open("file.json", "w")
                file.write(r.text)
                file.close()
                print ("wicked response received!")
        except:
                print ("Error while writing wicked response to file!")
                exit()

        try:
                r.connection.close()
        except Exception as e:
                #print e
                exit()
        
        # This file contains wicked response
        jsonFile = open('file.json', 'r')
        jsonData = json.load(jsonFile)
        jsonFile.close()
        
        # return dictionary with key as package_name and value as the entire line to be written in Final_license_list.csv file
        package_names = _extract_licenses(jsonData)

        # update the package_names to original names
        dict_packages = _update_orignal_names(package_names, dict_packages)
        
        _update_remaining_list(dict_packages, nosrc_packages)

        os.remove('file.json')


def _extract_licenses(values):
        package_names = {}
        for i, item in enumerate(values):
                #print(i, item, type(item))
                for key, value in item.items():
                        if(key=='possiblyRelatedPackages') and value!=[]:                                               
                                for p in item['possiblyRelatedPackages']:
                                        line = ""
                                        #package_names.append(p['awsomName'].lower())
                                        #line = line + p['awsomName']
                                        line = line + ' | ' + p['license']
                                        line = line + ' | ' + "WICC4D"
                                        if p['pedigreeReviewed']:
                                                line = line + ' | ' + 'NA'
                                        else:
                                                line = line + ' | ' + 'NA'
                                        line = line + ' | ' + 'NA'
                                        package_names[p['awsomName'].lower()] = line
                                        break
                        

        return package_names


def _update_orignal_names(package_names, dict_packages):

        remove_keys = []
        with open('final_output/Final_license_list.csv','a') as file:
                for key, value in dict_packages.items():
                                                
                        if value in package_names.keys():
                                file.write( key + " | " + value )
                                file.write( package_names[value] + '\n' )
                                remove_keys.append(key)

        # remove the packages for which licenses  have been found after source name change
        for key in remove_keys:
                del dict_packages[key]
        
        return dict_packages
                        
                
                


        
def _update_remaining_list(dict_packages, nosrc_packages):


        with open('final_output/remaining_list.csv', 'w') as file:
                for value in dict_packages.keys():
                        file.write(value.lower()+'\n')
                for value in nosrc_packages:
                        file.write(value.lower()+'\n')
                        
                        


        


