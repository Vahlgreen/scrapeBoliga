import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.boliga.dk/salg/resultater?searchTab=1&page=1&sort=date-d&salesDateMin=2004&salesDateMax=2022&saleType=1")
time.sleep(5)
driver.find_element(By.XPATH,"//button[@id='declineButton']").click()
#time.sleep(2)
next_button_xpath = "/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/div/div/app-pagination/div/div[4]/a"
#driver.find_element(By.XPATH,next_button_xpath).click()
time.sleep(0.5)
#print(driver.page_source)
#print(driver.current_url)

with open("alle_salg.csv",'a') as f:
    for j in range(1,5):
        for i in range(1,50):

            #pris
            print(driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[2]/span").text)
            price = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[2]/span").text
            #adresse
            print(driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[1]/a").text)
            adress = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[1]/a").text
            #dato
            print(driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[3]/div/span[1]").text)
            sold_date = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[3]/div/span[1]").text
            #byggår
            print(driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[6]/span").text)
            build_year = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[6]/span").text
            #kvm
            print(driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[1]").text)
            sqm = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[1]").text
            #kvm pris
            print(driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[2]").text)
            price_sqm = driver.find_element(By.XPATH,f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[4]/div/span[2]").text
            print("")
            f.write(f"{price},{sold_date},{sqm},{price_sqm},{build_year},{adress}\n")
        driver.find_element(By.XPATH, next_button_xpath).click()
        time.sleep(0.5)
while True:
    pass

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