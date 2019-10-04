


def get_database_data():
        with open('License-Automation/remaining_pkgs') as file:
                rem_packages = [line.strip() for line in file.readlines()]

        with open('License-Automation/DB_license_sheet.csv', 'r') as file:
                lines = [line.strip().split('|') for line in file.readlines()]

                with open('License-Automation/Final_license_list.csv', 'a') as o_file:
                        for line in lines:
                                if line[0].strip() in rem_packages:
                                        rem_packages.remove(line[0].strip())
                                        o_file.write(line[0] + ' | | ')
                                        for each in line[1:]:
                                                o_file.write(each + ' | ')
                                        # o_file.write('Database\n')

        with open('License-Automation/remaining_pkgs', 'w') as file:
                for package in rem_packages:
                        file.write(package + '\n')

if __name__ == '__main__':
        get_database_data()



"""
Database module checks if package from remaining_list is present in license_db
and removes it from the list if found.
"""
"""
import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def get_database_data():
    with open('final_output/remaining_list.csv') as file:
        rem_packages = [line.strip() for line in file.readlines()]

    conn = create_connection('/lib/license.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM license")
        rows = cursor.fetchall()
        lines = [row.strip().split('|') for row in rows]

        with open("final_output/Final_license_list.csv", 'a') as final_file:
            for line in lines:
                if line[0].strip() in rem_packages:
                    rem_packages.remove(line[0].strip())
                    final_file.write(line[0] + ' | | ')
                    for each in line[1:]:
                        final_file.write(each + ' | ')

    with open('final_output/remaining_list.csv', 'w') as remaining_file:
        for package in rem_packages:
            remaining_file.write(package + '\n') 
            
"""
