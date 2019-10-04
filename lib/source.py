import requests
from bs4 import BeautifulSoup

def verfiy_package_names():
        with open('final_output/remaining_list.csv') as file:
                orig_packages = file.readlines()

        bad_count = 0
        good_count = 0
        count = 0
        dict_packages = {}
        for package in orig_packages:
                package = package.strip()
                        
                        
                r = requests.get('https://packages.ubuntu.com/xenial/'+package)
                if ( r.status_code > 400):
                        bad_count+=1
                        dict_packages[package] = ""
                        #print("miss hit")
                else:   
                        good_count+=1
                        #print("hit")
                        src_name = _get_package_name(r)
                        if package == src_name:
                                count+=1
                        dict_packages[package] = src_name
        #print(" Packages: %d" % len(lines))
        #print(" Hit count: %d" % good_count)
        #print(" Miss count: %d" % bad_count)
        #print(" Correct  count: %d" % count)

        return dict_packages
        

def _get_package_name(page):

        soup = BeautifulSoup(page.text, 'html.parser')
        text = soup.find_all('p')[0].get_text()
        #print(text)
        name = _find_between(text, 'Download Source Package', ':').strip()
        #print(name)
        return name
        
def _find_between(s, first, last):
        try:
                start = s.index(first) + len(first)
                end = s.index(last, start)
                return s[start:end]
        except ValueError:
                return ""

