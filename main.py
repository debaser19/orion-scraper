from selenium import webdriver
import creds
import time


def scrape_orion():
    # define urls and driver
    sandbox_org = 'ac5406a1-f390-471b-91b4-aed55ac97a79'
    instances_url = 'https://3cx.iaas.cloudcopartner.com/organization/'
    driver_path = 'driver/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(f'{instances_url}{sandbox_org}/instances')

    # log in using the form
    # TODO: need to get the actual creds and update in creds.py
    driver.find_element_by_xpath('//*[@id="user_login"]').send_keys(creds.creds['username'])
    driver.find_element_by_xpath('//*[@id="user_password"]').send_keys(creds.creds['password'])
    driver.find_element_by_xpath('//*[@id="new_user"]/div[3]/div/input').click()
    time.sleep(10)


if __name__ == '__main__':
    scrape_orion()
