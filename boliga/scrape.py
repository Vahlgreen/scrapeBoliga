import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import os
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.boliga.dk/salg/resultater?searchTab=1&page=1&sort=date-d&salesDateMin=2004&salesDateMax=2022&saleType=1")
time.sleep(3)
driver.find_element(By.XPATH,"//button[@id='declineButton']").click()
next_button_xpath = "/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/div/div/app-pagination/div/div[4]/a"
time.sleep(0.5)
#print(driver.page_source)
#print(driver.current_url)


if os.path.exists("alle_salg.csv"):
    os.remove("alle_salg.csv")

num_pages = 50


with open("alle_salg.csv",'a') as f:
    for j in range(1,num_pages):
        time_start = time.time()
        for i in range(1,51):

            #pris
            price = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[2]/span").text
            price = price[:-4]#remove units

            #adresse
            adress = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[1]/a").text
            adress = adress.replace("\n"," ").replace(",","")
            zip_code = re.search("\d{4}.*",adress).group()
            street = adress.replace(f" {zip_code}","")

            #dato
            sold_date = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[3]/div/span[1]").text
            #byggår
            build_year = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[6]/span").text
            #kvm
            sqm = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[1]").text
            sqm = sqm[:-2]
            #kvm pris
            price_sqm = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[2]").text
            price_sqm = price_sqm[:-6]

            f.write(f"{street},{zip_code},{price},{sold_date},{sqm},{price_sqm},{build_year}\n")
        time_end = time.time()
        print(f"Time passed: {(time_end - time_start)}")
        driver.find_element(By.XPATH, next_button_xpath).click()
        time.sleep(0.4)


#from selenium import webdriver
#browser exposes an executable file
#Through Selenium test we will invoke the executable file which will then #invoke actual browser
#driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
# to maximize the browser window
#driver.maximize_window()
#get method to launch the URL
#driver.get("https://www.tutorialspoint.com/index.htm")
#to refresh the browser
#driver.refresh()
#to close the browser
#driver.close()