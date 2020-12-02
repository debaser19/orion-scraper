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
    driver.find_element_by_xpath('//*[@id="user_login"]').send_keys(creds.creds['username'])
    driver.find_element_by_xpath('//*[@id="user_password"]').send_keys(creds.creds['password'])
    driver.find_element_by_xpath('//*[@id="new_user"]/div[3]/div/input').click()

    # ask for MFA code
    mfa_code = input("Please enter the MFA code: ")
    driver.find_element_by_xpath('//*[@id="code"]').send_keys(mfa_code)
    driver.find_element_by_xpath('/html/body/main/div/section/div[2]/div/form/div[3]/div/input').click()
    time.sleep(10)

    # select the reseller dropdown and grab all hrefs
    reseller_ul = driver.find_element_by_xpath('//*[@id="dropdown"]/div[1]/ul').click()


if __name__ == '__main__':
    scrape_orion()
