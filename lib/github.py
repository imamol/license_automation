from __future__ import print_function
from builtins import input
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import getpass
import sys
import github3


def _get_sha(username, password, url):

        
        r = requests.get(url,auth=HTTPBasicAuth(username, password))

        print(r.text)
        if r.status_code < 400:
                data = json.loads(r.text)
                return data['sha']
                print("Creds validated..")
        else:
                print("Error in accessing github api to uplod file..")
                exit()


def upload_file():

        username = input("Github username: ")
        password = getpass.getpass("Github passsword: ")
        url = "https://api.github.ibm.com/repos/abhople/LicenseAutomation/contents/lib/DB_license_sheet.csv"
        
        sha = _get_sha(username, password, url)
        
        with open('lib/DB_license_sheet.csv') as file:
                lines = file.read()

        PY3 = sys.version_info[0] >= 3

        if PY3:
                lines = lines.encode()  
                file_data = base64.b64encode(lines)
                file_data = file_data.decode()
        else:
                file_data = base64.b64encode(lines)
                
        data = json.dumps({'message':'uploading new db', 'content':file_data, 'sha':sha})

        r = requests.put(url,data, auth=HTTPBasicAuth(username, password))

        if r.status_code < 400:
                print("DB_license_sheet.csv uploaded on github")
        else:
                print("Error in accessing github api to upload file..")
                exit()


def create_and_upload_file(username, password, repo, file_name):
        
        gh = github3.login(username=username, password=password)

        repository = gh.repository('junawaneshivani', 'build-scripts')


        with open(file_name, 'rb') as fd:
                contents = fd.read()
        try :
                repository.create_file(
                        path=repo,
                        message='Added generated License File ',
                        content=contents,
                )
        except Exception as e:
                print (e)
                return False

        return True
