import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
from scrapy import Selector
import os
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

import pandas as pd

kommuner = pd.read_csv("komuner_DK.csv",header = None,names=["kom"])
kommuner["kom"] = kommuner["kom"].replace("Allerød","Alleroed")
start_urls = []
for index, row in kommuner.iterrows():
    start_urls.append(f"https://www.boligsiden.dk/salgspris/solgt/alle/1?periode.from=1992-01-01&periode.to=2022-12-31&salgstype=auction&displaytab=mergedtab&by={str(row['kom']).lower()}")

driver_options = webdriver.ChromeOptions()
driver_options.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=driver_options)

#"https://www.boligsiden.dk/salgspris/solgt/alle/1?periode.from=1992-01-01&periode.to=2022-12-31&salgstype=auction&displaytab=mergedtab&by=odense"

for index,url in enumerate(start_urls):
    driver.get(url)
    print(kommuner.iloc[index]["kom"])
    next_button_selector = f"//*[@id='page-salesprice-result']/div/div/div[2]/div/div[2]/div[2]/a"

    decline_cookies_selector = "#onetrust-close-btn-container > button"
    if index == 0:
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, decline_cookies_selector).click()
    time.sleep(2)

    selenium_response_text = driver.page_source
    new_selector = Selector(text=selenium_response_text)

    sidetal = new_selector.css("#page-salesprice-result > div > div > div:nth-child(3) > div.pager.pager--list.pager--propertySale.pager--bottom > div > div.pagenumber > span:nth-child(2)::text").get()
    sidetal = int(str(sidetal).split(" ")[-1])
    #sidetal = 2
    filename = "test.csv"
    with open(filename, 'a') as f:
        for i in range(1,sidetal+1):
            for j in range(1,31):
                selenium_response_text = driver.page_source
                page_selector = Selector(text=selenium_response_text)
                street = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__info.ci__info--address > div.row-2.text-truncate > a::text").get()
                #street = new_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child(27) > div.ci__info.ci__info--address > div.row-2.text-truncate > a::text").get()
                city_and_zip = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__info.ci__info--address > div.row-3 > span::text").get()

                if city_and_zip is not None:
                    zip = re.search("\d{4}",city_and_zip).group()
                    city = city_and_zip.replace(zip,"")


                #Første række:Auktion eller Fri handel selector
                auktion_bool = False
                trade_bool = False
                trade_price = 0
                auktion_price = 0
                trade_index = 1
                #while not auktion_bool and not trade_bool:
                while True:
                    try:
                        trade = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(1) > span::text").get()

                        if not auktion_bool and trade == "Auktion":
                            auktion_bool=True
                            auktion_price = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(3)::text").get()
                            auktion_date = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(2)::text").get()

                        if not trade_bool and trade == "Fri handel":
                            trade_bool = True
                            trade_price = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(3)::text").get()
                            trade_date = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(2)::text").get()

                        if (trade_bool and auktion_bool) or trade_index>10:
                            break
                        trade_index = trade_index + 1
                    except Exception:
                        print("exception occured")
                        break

                if street is None or city_and_zip is None or city is None or zip is None or auktion_price is None or auktion_date is None or trade_price is None or trade_date is None:
                    continue
                #print(f"række {j}: {street.strip()}, {city_and_zip.strip()}, {auktion_price},{auktion_date}, {trade_price},{trade_date}\n")
                f.write(f"{street.strip()};{city.strip()};{zip.strip()};{auktion_price};{auktion_date};{trade_price};{trade_date}\n")

            click_succes = False
            while not click_succes:
                try:
                    driver.find_element(By.XPATH, next_button_selector).click()
                    click_succes = True
                except NoSuchElementException:
                    print("NoSuchElementException")

                driver.get(url.replace(f"alle/{i}",f"alle/{i+1}"))
            time.sleep(1)