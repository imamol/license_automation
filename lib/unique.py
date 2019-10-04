

def fetch_unique_licenses(file_name):

        with open(file_name) as file:
                lines = file.readlines()

        print( len(lines))
        license_list = []

        for line in lines:
                try:
                        package_name, license_info = line.split('|')[0].strip() , line.split('|')[1].strip().lower()
                except:
                        continue

                if license_info not in license_list:
                        license_list.append(license_info)



        print( len(license_list) )
        print( license_list)

        return license_list

        
#fetch_unique_licenses('../final_output/argparse-ppc64le.csv')
