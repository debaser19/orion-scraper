from selenium import webdriver
import creds
import time
import pandas as pd


def scrape_resellers():
    driver.get(base_url)

    # log in using the form
    driver.find_element_by_xpath('//*[@id="user_login"]').send_keys(creds.creds['username'])
    driver.find_element_by_xpath('//*[@id="user_password"]').send_keys(creds.creds['password'])
    driver.find_element_by_xpath('//*[@id="new_user"]/div[3]/div/input').click()

    # ask for MFA code and enter it to log in
    mfa_code = input("Please enter the MFA code: ")
    driver.find_element_by_xpath('//*[@id="code"]').send_keys(mfa_code)
    driver.find_element_by_xpath('/html/body/main/div/section/div[2]/div/form/div[3]/div/input').click()

    # select the reseller dropdown and grab all li elements
    driver.find_element_by_xpath('/html/body/header/nav/div/div[2]/ul/li[1]/a').click()
    time.sleep(2)
    reseller_ul = driver.find_element_by_xpath('//*[@id="dropdown"]/div[1]/ul')
    reseller_elements = reseller_ul.find_elements_by_tag_name('a')
    reseller_list = []

    # loop through reseller list and store the href and text of 'a' elements in list of dicts
    for reseller in reseller_elements:
        reseller_dict = {
            'reseller_href': reseller.get_attribute('href')[:-6]+'instances',
            'reseller_name': reseller.text
        }
        reseller_list.append(reseller_dict)

    return reseller_list


def scrape_instances(resellers_list):
    instances_list = []
    # loop through each reseller in the list and grab details for all instances
    for reseller in resellers_list:
        temp_list = []  # temp list to hold list of instance dicts for current reseller
        print(f'Navigating to {reseller["reseller_href"]}...')
        driver.get(reseller['reseller_href'])
        time.sleep(1)
        try:
            instances_table = driver.find_element_by_xpath('/html/body/main/div/div[2]/div/table/tbody')
            instance_rows = instances_table.find_elements_by_tag_name('tr')
            for row in instance_rows:
                instance_columns = row.find_elements_by_class_name('cell-contents')
                instance_dict = {   # create a dict to store the current instance details
                    'reseller_name': reseller['reseller_name'],
                    'instance_name': instance_columns[0].text,
                    'instance_region': instance_columns[1].text,
                    'instance_source': instance_columns[2].text,
                    'instance_memory': instance_columns[3].text,
                    'instance_public_ip': instance_columns[4].text,
                    'instance_tier': instance_columns[5].text,
                    'instance_state': instance_columns[6].text
                }
                print(instance_dict)
                # append the current instance dict to the temp reseller list
                temp_list.append(instance_dict)
            # append the temp reseller list to the master list of lists
            instances_list.append(temp_list)
            print(f'Found {len(temp_list)} instance(s) for {reseller["reseller_name"]}...\n')
        except Exception as e:
            print(f'\nCouldn\'t find any instances for {reseller["reseller_name"]}: {e}')

    # convert list of list of dicts to dataframe
    instances_df = pd.DataFrame([r for d in instances_list for r in d])
    print(instances_df)

    # export dataframe to excel file
    instances_df.to_excel('Orion_Instances.xlsx', sheet_name='Instances', index=False)


if __name__ == '__main__':
    # define urls and driver
    base_url = 'https://3cx.iaas.cloudcopartner.com/'
    driver_path = 'driver/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)

    scrape_instances(scrape_resellers())
