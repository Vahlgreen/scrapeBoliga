import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import os
from selenium.common.exceptions import StaleElementReferenceException



def run_scraping(start_page,end_page):
    driver = webdriver.Chrome(ChromeDriverManager().install())


    driver.get("https://www.boliga.dk/salg/resultater?searchTab=1&page=1&sort=date-d&salesDateMin=2004&salesDateMax=2022&saleType=1")
    time.sleep(5)
    driver.find_element(By.XPATH,"//button[@id='declineButton']").click()
    next_button_xpath = "/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/div/div/app-pagination/div/div[4]/a"
    time.sleep(0.5)
    #print(driver.page_source)
    #print(driver.current_url)


    #if os.path.exists("alle_salg.csv"):
    #    os.remove("alle_salg.csv")
    #start_page = 490 #810
    #num_pages = 1000
    if start_page>0:
        for i in range(start_page):
            driver.find_element(By.XPATH, next_button_xpath).click()

    #alle_salg nåede til side 810
    with open("alle_salg_auto.csv",'a') as f:
        for j in range(start_page,end_page):
            time_start = time.time()
            for i in range(1,51):

                #pris
                while True:
                    try:
                        price = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[2]/span").text
                        break
                    except StaleElementReferenceException:
                        print("Element was not found")
                price = price[:-4]#remove units

                #adresse
                while True:
                    try:
                        adress = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[1]/a").text
                        break
                    except StaleElementReferenceException:
                        print("Element was not found")
                adress = adress.replace("\n"," ").replace(",","")
                zip_code = re.search("\d{4}.*",adress).group()
                street = adress.replace(f" {zip_code}","")

                #dato
                while True:
                    try:
                        sold_date = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[3]/div/span[1]").text
                        break
                    except StaleElementReferenceException:
                        print("Element was not found")

                #byggår
                while True:
                    try:
                        build_year = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[6]/span").text
                        break
                    except StaleElementReferenceException:
                        print("Element was not found")
                #kvm
                while True:
                    try:
                        sqm = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[1]").text
                        break
                    except StaleElementReferenceException:
                        print("Element was not found")

                sqm = sqm[:-2]

                #kvm pris
                #kvm
                while True:
                    try:
                        price_sqm = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[2]").text
                        break
                    except StaleElementReferenceException:
                        print("Element was not found")
                price_sqm = price_sqm[:-6]

                f.write(f"{street},{zip_code},{price},{sold_date},{sqm},{price_sqm},{build_year}\n")
            time_end = time.time()
            if j%10==0:
                print(f"Processing page {j} took: {(time_end - time_start)} seconds")
            driver.find_element(By.XPATH, next_button_xpath).click()
            time.sleep(0.4)

    return True


intervals = [i*200 for i in range(115)]

for i in range(len(intervals)):
    run_scraping(intervals[i],intervals[i+1])
