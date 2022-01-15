from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.service import Service
import re
from datetime import datetime
import csv
import pprint

browser = Service("chromedriver.exe")
op = webdriver.ChromeOptions()
op.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"

driver = webdriver.Chrome(service=browser, chrome_options=op)
##
keywords_justjoin_url={
    "devops_aws": "https://justjoin.it/?q=DevOps@category;AWS@skill",
    "sre_aws" : "https://justjoin.it/?q=AWS@skill;sre@keyword",
    "aws_entry_job" : "https://justjoin.it/?q=junior@keyword;AWS@skill",
    }
offers_urls=[]
name=""
email=""
message= "
CV_pdf=""

##header = ['site', 'date', 'success', 'url']
state_of_jj=[]

def load_urls_from_keywords(keywords):
    ## find all offers with keywords from  keywords_justjoin_url
    ## execution, just provide variable to def ()
    ## results are added to offers_urls
    driver.get(keywords)
    assert "Just" in driver.title
    htmlentire = driver.page_source
    for i in range(len(htmlentire.split())):
        temp=htmlentire.split()[i]
        if "offer" in temp:
            ##regex  \boffers\/\S(.*n?)(?=") returning results that starts with word offers and ends with "
            if "company_logos" not in temp:
                if re.search (r'\boffers\/\S(.*n?)(?=")',  htmlentire.split()[i]) :
                    offers_urls.append(re.search (r'\boffers\/\S(.*n?)(?=")',  htmlentire.split()[i]).group() )

    assert "No results found." not in driver.page_source





def enter_site_fillUp_data_to_apply(urls):

    driver.get(urls)
    try:
        driver.find_element_by_name('name').send_keys(name)
        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('message').send_keys(message)
    except:
        success="non standard application"

    try:
        driver.find_element_by_xpath("//*[@id='offer-apply-container']/form/div[1]/div[4]/div/div[2]/input").send_keys(CV_pdf)
    except NoSuchElementException:
        pass

    ## element is assigned with xpath, then the js is executed and the element can be clicked!

    ##here we have check box processing data in future recrutiments
    try:
        ## not every company have check box for future recruitments

        element = driver.find_element_by_xpath('//*[@id="offer-apply-container"]/form/div[2]/div/div/label/span[1]/span[1]/input')
        driver.execute_script("arguments[0].click();", element)
    except NoSuchElementException:
        pass

    try:

        # here we have APPLY button
        element = driver.find_element_by_xpath('//*[@id="offer-apply-container"]/form/div[3]/div[1]/button/span[2]')
        driver.execute_script("arguments[0].click();", element)
    except NoSuchElementException:
        pass



    try:
        ### check if application was succesfuly done
        time.sleep(5)
        element = driver.find_element_by_xpath('//*[@id="offer-apply-container"]/div[2]/div/img')
        success=element.is_displayed()



    except NoSuchElementException:
        success="brak elementu"
    date_of_applying = datetime.now()
    state_of_jj.append(["justojoin", date_of_applying,success, urls ])


def check_job_applications(url_check):
    ## gonna make a small check to not to spam dudes with my app
    with open("justjoin.csv") as j_app:
        for lines in j_app.readlines():
            print(lines)
            print(url_check)
            if url_check in lines:
                print(j_app.read())
                print("znalazlo link z oferta")
                ## True here means that i already applied for this job app. and am waiting for results, hope they will great.
                return True

    print("fales")
    ## False here means that the url was not saved in job applications csv, so I did not apply to this job yet
    return False


#enter_site_fillUp_data_to_apply("https://justjoin.it/offers/klient-just-join-it-junior-devops-engineer")
for key in keywords_justjoin_url:
    offers_urls.append(load_urls_from_keywords(keywords_justjoin_url[key]))

for urls in offers_urls:
    if urls is not None:
        print("test_urlow")
        print(urls)
        if not check_job_applications(urls):
            print("https://justjoin.it/" + urls)
            enter_site_fillUp_data_to_apply("https://justjoin.it/" + urls)## poprawic aby od razu byl przesylany pelny adres

pprint.pprint(state_of_jj)
with open('justjoin.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for line in state_of_jj:
        # write the state of aplications
        writer.writerow(line)



driver.close()


