from __future__ import print_function
from builtins import input
import lib.wicked as WC
import lib.database as DB
import lib.openhub as OH
import lib.copyright as CP
import lib.source as SR
#import lib.github as GH
import lib.unique as UN
import lib.pip as PP
import os


# noinspection PyInterpreter,PyInterpreter
def _ouput_pre_formating():
        # open input package list
        with open('input_package_list.csv') as file:
                orig_packages = file.readlines()

                      
        # copy to remaining package list
        with open('final_output/remaining_list.csv','w') as file:
                for package in orig_packages:
                        file.write(package)

        # create Final_license_list.csv file
        with open('final_output/Final_license_list.csv','w') as file:
                file.write("Package name | Modified package name | License | Source of License Information | Comments | Copyright Links/References \n")
                pass

def _run_without_copyright():

        # generate wicked output
        WC.get_wicked_data_before_src()
        print("\nWicked output generated")

        # generate database output
        CP.run_db_module()

        DB.get_database_data()
        print("\nDatabase output generated")

        # generate openhub output
        OH.get_openhub_data()
        print("\nOpenhub output generated")

        print(" License List generated!")
       


def _run_with_copyright(remove_image):
        

        # generate wicked output for src_packages
        WC.get_wicked_data_before_src()
        print("\nWicked output generated before src ")

        # verify remaining list with ubuntu.com 
        # verify with src 
        dict_packages = SR.verfiy_package_names()
        nosrc_packages = []
        src_packages = []
        for key, value in dict_packages.items():
                if value!="":
                        src_packages.append(value) # name fetched through ubuntu.com
                else:
                        nosrc_packages.append(key) # original name

                                                
        # remove original packages from the list as they are already checked.
        for package in nosrc_packages:
                del dict_packages[package]
                        

        # generate wicked output for src_packages
        WC.get_wicked_data_after_src(dict_packages, src_packages, nosrc_packages)
        print("\nWicked output generated after src ")

        # generate database output
        DB.get_database_data()
        print("\nDatabase output generated")

        # generate copyright output
        fetch_licence = "sh License-Automation/fetch_license.sh %s" % (remove_image)
        CP.get_copyright_data(fetch_licence)
        print("\nCopyright output generated")

        # generate openhub output
        OH.get_openhub_data()
        print("\nOpenhub output generated")

        print(" License List generated!")

        

def merge_python_and_pip_output():

        PP.merge_python_output()

        with open('npm_license_list.csv') as file:
                lines = file.readlines()

        with open('final_output/Final_license_list.csv','a+') as file:
                for line in lines:
                        file.write(line)

        if os.path.exists('rbase_license_list.csv'):
                with open('rbase_license_list.csv') as file:
                        lines = file.readlines()

                with open('final_output/Final_license_list.csv','a+') as file:
                        for line in lines:
                                if "Package" not in line:
                                        file.write(line.split('"')[1] + " | | " + line.split('"')[3] + " r_command | NA | NA \n")

        #print("Merged rbase output")

        with open('gem_license_list.csv') as file:
                lines = file.readlines()

        with open('final_output/Final_license_list.csv','a+') as file:
                for line in lines:
                        file.write(line)

        #print("Merged ruby gem output")

                
                                                                
def main():

        
        dirname = os.getcwd()
        if not os.path.exists("final_output"):
                os.makedirs("final_output") 
        
        path = ""


        print( " 1. Container ID's")
        print( " 2. Dockerfile path")
        print( " 3. input_package_list.csv")
        ch = int(input(" -->  "))
        
        
        if ch == 3:
                generate_package_list = 'no'
                remove_image='no'

                _ouput_pre_formating()
                _run_without_copyright()        
                
                
        elif ch == 2:
                generate_package_list = 'yes'
                path = input("Enter absolute path to Dockerfile parent directory : ")
                remove_image = input("Do you want to delete docker image? [Y/N] : ")
                remove_image = remove_image.lower()

                if remove_image in {'y', 'yes'}:
                        remove_image='yes'
                elif remove_image in {'n', 'no'}:
                        remove_image='no'
                else:
                        print("Invalid Input! Docker image will not be deleted by default.")
                        remove_image='no'

                build_container = "sh License-Automation/build_containers.sh %s" % (path)
                
                CP.login_to_vm()
                CP.copy_initial_files_to_vm()
                CP.run_build_container(build_container)
                CP.copy_input_package_list_to_windows()
                CP.copy_image_name_to_windows()

                _ouput_pre_formating()
                
                if os.path.exists('DistroName'):
                        with open('DistroName') as file:
                                name = file.read().strip()
                
                #print(name)
                # copy npm and pip output to windows
                CP.copy_python_license_list_to_windows()
                CP.copy_npm_license_list_to_windows()
                CP.copy_gem_license_list_to_windows()

                if name=='debian':
                        CP.copy_rbase_license_list_to_windows()
                        
                if name=='centos' or name=='fedora' or name=='rhel':
                        CP.copy_final_license_list_to_windows()
                        with open('final_output/remaining_list.csv','w') as file:
                                pass

                        merge_python_and_pip_output()
                        
                elif name=='alpine':
                        _run_without_copyright()
                        merge_python_and_pip_output()
                        
                elif name=='ubuntu' or name=='debian':
                        _run_with_copyright(remove_image)
                        merge_python_and_pip_output()
                
                
                else:
                        print('container distro error '+name+"\n")
                        exit()

                os.remove('DistroName')
                
                run_cleanup = "sh License-Automation/cleanup.sh %s" % (remove_image)
                CP.cleanup_containers(run_cleanup)

                #CP.delete_files_from_linux()    
                        
        elif ch == 1:
                base_container_id = input("Enter base container id: ")
                application_container_id = input("Enter application container id: ")

                print(" Base image? ")
                print(" 1. Centos / Fedora / Rhel")
                print(" 2. Ubuntu / Debian")
                print(" 3. Alpine ")
                base_image_choice = int(input(" --->  "))

                if base_image_choice not in [1,2,3]:
                        print(" Base image not supported")
                        exit(1)


                # centos/fedora base image case
                elif base_image_choice == 1:
                        #base_container_id = 'd76e18c9034b'
                        #application_container_id = 'dd0cc0487c6a'
                        
                        build_container = "sh License-Automation/build_containers.sh %s %s" % (base_container_id, application_container_id)
                        CP.login_to_vm()
                        CP.copy_initial_files_to_vm()
                        CP.run_build_container(build_container)
                        CP.copy_input_package_list_to_windows()
                        CP.copy_final_license_list_to_windows()
                        CP.copy_image_name_to_windows()
                                                
                        # copy npm and pip output to windows
                        CP.copy_python_license_list_to_windows()
                        CP.copy_npm_license_list_to_windows()
                        CP.copy_gem_license_list_to_windows()
                        merge_python_and_pip_output()


                        print(" License List generated!")
                        CP.delete_files_from_linux()


                # ubuntu base image case
                elif base_image_choice == 2:
                        #base_container_id = 'b309ad7b15f4'
                        #application_container_id = '185e13f2f3e2'

                        build_container = "sh License-Automation/build_containers.sh %s %s" % (base_container_id, application_container_id)
                        generate_package_list = 'yes'
                        remove_image = 'no'

                        CP.login_to_vm()
                        CP.copy_initial_files_to_vm()
                        CP.run_build_container(build_container)
                        CP.copy_input_package_list_to_windows()
                        CP.copy_image_name_to_windows()
                                                
                        # copy npm and pip output to windows
                        CP.copy_python_license_list_to_windows()
                        CP.copy_npm_license_list_to_windows()
                        CP.copy_rbase_license_list_to_windows()
                        CP.copy_gem_license_list_to_windows()


                        _ouput_pre_formating()

                        _run_with_copyright(remove_image)

                        merge_python_and_pip_output()

                        CP.delete_files_from_linux()


                # alpine base image case:
                elif base_image_choice == 3:
                        #base_container_id = '2eed7246b5f9'
                        #application_container_id = '88672d07deda'

                        build_container = "sh License-Automation/build_containers.sh %s %s" % (base_container_id, application_container_id)
                        generate_package_list = 'yes'
                        remove_image = 'no'

                        CP.login_to_vm()
                        CP.copy_initial_files_to_vm()
                        CP.run_build_container(build_container)
                        CP.copy_input_package_list_to_windows()
                        CP.copy_image_name_to_windows()
                                                
                        # copy npm and pip output to windows
                        CP.copy_python_license_list_to_windows()
                        CP.copy_npm_license_list_to_windows()
                        CP.copy_gem_license_list_to_windows()


                        _ouput_pre_formating()
                        _run_without_copyright()

                        merge_python_and_pip_output()


                        CP.delete_files_from_linux()

                
        else:
                print(" Invalid choice.. Aborting")
                exit()


        
                

if __name__ == '__main__':
        main()
