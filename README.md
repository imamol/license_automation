**Note:**\
Works for packages installed using _standard package manager_ of the following Distros :
1) Ubuntu
2) Debian
3) CentOS
4) Fedora
5) Alpine


**Linux Requirements:**

- ppc64le Ubuntu VM with docker running

**Windows Requirements:**

- Install required python packages through following command on cmd: \
	pip install paramiko requests beautifulsoup4 future

**Configuration:**

- On Windows machine which has access to wicked swagger APIs, download and extract the .zip file.
	- (Wicked swagger API url - https://wicked-pedigree-service.w3ibm.mybluemix.net/api-docs/ )
- Check the ssh connection from windows machine to ubuntu VM.

**Steps to run the automation:**

- Run the "script.py" file on windows machine.
- The aplication will prompt for 3 options to generate licenses.
	1) Container id's
	2) Dockerfile link
	3) input_package_list.csv\
The first 2 options will generate the input_package_list.csv file from the container, whereas the 3rd option will take input from the input_package_list.csv file in the same folder as the script.py file.
- Next, the application will ask for VM details. Provide the details of Ubuntu VM as some part of the automation will run on this VM (Non-root users of the VM will require sudo access).
- Once the application has finished executing, it will prompt the user to exit.

**Final Output:**

- The final output of the automation will be available under the final_output folder on windows machine.
	- Final_license_list.csv contains the license information for all the packages.
	- remaining_list.csv contains the list packages for which the automation could not retrive the license information. For these packages we need to gather the license information manually.
- input_package_list.csv contains the list of all the packages for which the automation tries to retrive the license informatio and will be in the same folder as script.py file.
- The .csv files can be opened using excel and then saved as .xlxs for further use. 
