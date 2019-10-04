from __future__ import print_function
from builtins import input
import paramiko
import getpass
import os

_hostname = ''
_username = ''
_password = ''
_ssh = ''

def login_to_vm():
    global _hostname
    global _username
    global _password
    global _ssh

    _hostname = input('Enter host IP address: ')
    _username = input('Enter username: ')
    _password = getpass.getpass("Enter Password : ")

    try:
        _ssh = paramiko.SSHClient()
        _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh.connect(_hostname,username=_username,password=_password)
        print("Connected to %s" % (_hostname))



    except paramiko.AuthenticationException:
        print("Failed to connect to %s due to wrong username/password" % (_hostname))
        exit(1)
    except Exception as e:
        print(e.message)



def cleanup_containers(run_cleanup):
    try:
        stdin, stdout, stderr = _ssh.exec_command("echo " + _password + "| sudo -S " + run_cleanup + " " + _password)
        stdout.channel.recv_exit_status()
    except Exception as e:
        print("Error while running cleanup!")
        #print(e.message)



def run_build_container(build_container):
    try:
        print("Building Docker image and containers...")
        stdin, stdout, stderr = _ssh.exec_command("echo " + _password + "| sudo -S " + build_container + " " + _password)
        status=stdout.channel.recv_exit_status()
        if ( status == 10 ):
            print("Error during Application image creation! Check Dockerfile.")

    except Exception as e:
        cleanup_containers()
        #print(e.message)




def copy_initial_files_to_vm():
    try:
        sftp = _ssh.open_sftp()

        try:
            sftp.mkdir('License-Automation')
        except:
            pass

        sftp.put('lib/linux/build_containers.sh','License-Automation/build_containers.sh')
        sftp.put('lib/linux/ContainerCreatePackageList.sh', 'License-Automation/ContainerCreatePackageList.sh')
        sftp.put('lib/linux/cleanup.sh', 'License-Automation/cleanup.sh')
        sftp.put('lib/linux/analyze_vm.sh','License-Automation/analyze_vm.sh')
        sftp.put('lib/linux/script.sh', 'License-Automation/script.sh')
        sftp.put('lib/linux/fetch_license.sh', 'License-Automation/fetch_license.sh')
        sftp.put('lib/linux/output_format.sh', 'License-Automation/output_format.sh')
        sftp.put('lib/linux/pip.sh', 'License-Automation/pip.sh')
        sftp.put('lib/linux/npm.sh', 'License-Automation/npm.sh')
        sftp.put('lib/linux/gem.sh', 'License-Automation/gem.sh')
        sftp.put('lib/linux/gem.sh', 'License-Automation/gem.sh')
        sftp.put('lib/DB_license_sheet.csv', 'License-Automation/DB_license_sheet.csv')
        sftp.close()
    except Exception as e:
        print(e)
        print("Error while copying build_containers.sh to linux machine!")



def copy_input_package_list_to_windows():
    try:
        sftp = _ssh.open_sftp()
        sftp.get('License-Automation/input_package_list.csv','input_package_list.csv')
        sftp.close()
        print("Successfully copied input_package_list.csv!")
    except:
        print("input_package_list.csv not found at the user specified location.")


def copy_python_license_list_to_windows():
    try:
        sftp = _ssh.open_sftp()
        sftp.get('License-Automation/python_license_list.csv','python_license_list.csv')
        sftp.close()
        print("Successfully copied python_license_list.csv!")
    except:
        print("python_license_list.csv not found at the user specified location.")


def copy_npm_license_list_to_windows():
    try:
        sftp = _ssh.open_sftp()
        sftp.get('License-Automation/npm_license_list.csv','npm_license_list.csv')
        sftp.close()
        print("Successfully copied npm_license_list.csv!")
    except:
        print("npm_license_list.csv not found at the user specified location.")

def copy_gem_license_list_to_windows():
    try:
        sftp = _ssh.open_sftp()
        sftp.get('License-Automation/gem_license_list.csv','gem_license_list.csv')
        sftp.get('License-Automation/gem_remaining_list.csv','gem_remaining_list.csv')
        sftp.close()
        print("Successfully copied gem_license_list.csv!")
    except:
        print("gem_license_list.csv not found at the user specified location.")


def copy_rbase_license_list_to_windows():
    try:
        sftp = _ssh.open_sftp()
        sftp.get('License-Automation/rbase_license_list.csv','rbase_license_list.csv')
        sftp.close()
        print("Successfully copied rbase_license_list.csv!")
    except:
        print("rbase_license_list.csv not found at the user specified location.")

def copy_final_license_list_to_windows():
    try:
        sftp = _ssh.open_sftp()
        sftp.get('License-Automation/Final_license_list.csv','final_output/Final_license_list.csv')
        sftp.close()
        print("Successfully copied Final_license_list.csv!")

    except:
        print("Final_license_list.csv not found at the user specified location.")


def copy_image_name_to_windows():
    try:
        sftp = _ssh.open_sftp()
        sftp.get('License-Automation/DistroName','DistroName')
        sftp.close()
        print("Successfully copied DistroName!")
    except:
        print("DistroName not found at the user specified location.")


# license fetching starts here


def get_copyright_data(fetch_licence):
    with open('final_output/remaining_list.csv') as file:
        lines = file.readlines()
    if len(lines) == 0:
        return
    _copy_remaining_list_to_vm()
    try:
        stdin, stdout, stderr = _ssh.exec_command("chmod +x License-Automation/analyze_vm.sh")
        stdin, stdout, stderr = _ssh.exec_command(fetch_licence)
        status=stdout.channel.recv_exit_status()
        if ( status == 10 ):
            print("Error during fetching licenses from copyright file..")
            exit()
    except Exception as e:
        cleanup_containers()
        #print(e.message)


    _copy_output_to_windows()
    _merge_with_original_file()
       


def _copy_remaining_list_to_vm():
    try:
        sftp = _ssh.open_sftp()

        sftp.put('final_output/remaining_list.csv','License-Automation/remaining_list')
        sftp.close()
    except Exception as e:
        print(e)
        print("Error while copying remaining_list.csv to linux machine!")



def _copy_output_to_windows():     
    try:
        sftp = _ssh.open_sftp()

        sftp.get('License-Automation/remaining_pkgs','final_output/remaining_list.csv')
        sftp.get('License-Automation/ubuntu_packages.csv','final_output/copyright_output.csv')
        sftp.close()
    except Exception as e:
        print(e)
        print("Error in copying copyright output to windows")



def _merge_with_original_file():
    with open('final_output/copyright_output.csv') as file:
        lines = file.readlines()

    with open('final_output/Final_license_list.csv','a') as file:
        with open('lib/DB_license_sheet.csv','a') as db_file:
            for line in lines:
                #line = line.replace('|',',')
                file.write(line)
                #db_file.write(line)

    os.remove('final_output/copyright_output.csv')

def delete_files_from_linux():
    try:
        stdin, stdout, stderr = _ssh.exec_command('rm -r License-Automation')
        status=stdout.channel.recv_exit_status()
        if ( status == 10 ):
            print("Error during deleting folder in Linux")

    except Exception as e:
        print(e)

def copy_db_module_files_to_vm():
        try:
                sftp = _ssh.open_sftp()
                sftp.put('final_output/Final_license_list.csv', 'License-Automation/Final_license_list.csv')
                sftp.put('lib/database.py', 'database.py')
                sftp.close()
                print("Successfully copied input_package_list.csv!")
        except:
                print("Error in copying db_module_files to vm")

def copy_db_module_files_to_windows():
    try:
        sftp = _ssh.open_sftp()

        sftp.get('License-Automation/remaining_pkgs', 'final_output/remaining_list.csv')
        sftp.get('License-Automation/Final_license_list.csv', 'final_output/Final_license_list.csv')
        sftp.close()
    except Exception as e:
        print(e)
        print("Error in copying db_module_files to windows")

def run_db_module():
        copy_db_module_files_to_vm()

        try:
                stdin, stdout, stderr = _ssh.exec_command('python License-Automation/database.py')
                status = stdout.channel.recv_exit_status()
                if (status == 10):
                        print("Error during database module")

        except Exception as e:
                print(e)

        copy_db_module_files_to_windows()
