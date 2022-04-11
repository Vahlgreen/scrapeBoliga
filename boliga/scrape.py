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

## Read and clean data
kommuner = pd.read_csv("data_files/komuner_DK.csv", header = None, names=["kom"])
kommuner["kom"] = kommuner["kom"].replace("Vesthimmerlands","Vesthimmerland")
kommuner= kommuner.iloc[93:98]["kom"].reset_index(drop=True)
kommuner = kommuner.to_frame()

#append all starturls
start_urls = []
for index, row in kommuner.iterrows():
    start_urls.append(f"https://www.boligsiden.dk/salgspris/solgt/alle/1?periode.from=1992-01-01&periode.to=2022-12-31&salgstype=auction&displaytab=mergedtab&kommune={str(row['kom']).lower()}")

#initiate browser
driver_options = webdriver.ChromeOptions()
driver_options.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=driver_options)
#driver = webdriver.Chrome(ChromeDriverManager().install())

#scrape all urls
for index,url in enumerate(start_urls):
    driver.get(url)
    kommune = kommuner.iloc[index]["kom"]
    print(f"{index}, {kommune}, {url}")

    decline_cookies_selector = "#onetrust-close-btn-container > button"
    if index == 0:
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, decline_cookies_selector).click()
    time.sleep(2)

    selenium_response_text = driver.page_source
    new_selector = Selector(text=selenium_response_text)

    pagenum = new_selector.css("#page-salesprice-result > div > div > div:nth-child(3) > div.pager.pager--list.pager--propertySale.pager--bottom > div > div.pagenumber > span:nth-child(2)::text").get()
    pagenum = int(str(pagenum).split(" ")[-1])

    filename = "data_files/test.csv"
    with open(filename, 'a') as f:
        for i in range(1, pagenum):
            for j in range(1,31):
                selenium_response_text = driver.page_source
                page_selector = Selector(text=selenium_response_text)
                street = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__info.ci__info--address > div.row-2.text-truncate > a::text").get()
                city_and_zip = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__info.ci__info--address > div.row-3 > span::text").get()
                sqm = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child(1) > td.area::text").get()


                if city_and_zip is not None:
                    if re.search("\d{4}",city_and_zip) is not None:
                        zip = re.search("\d{4}",city_and_zip).group()
                    city = kommune

                #Første række:Auktion eller Fri handel selector
                auction_bool = False
                trade_bool = False
                trade_price = 0
                auction_price = 0
                trade_index = 1
                while True:
                    try:
                        trade = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(1) > span::text").get()

                        if not auction_bool and trade == "Auktion":
                            auction_bool=True
                            auction_price = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(3)::text").get()
                            auction_date = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(2)::text").get()

                        if not trade_bool and trade == "Fri handel":
                            trade_bool = True
                            trade_price = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(3)::text").get()
                            trade_date = page_selector.css(f"#page-salesprice-result > div > div > div:nth-child(3) > div.row > div:nth-child({j}) > div.ci__kf.ci__kf--1 > table > tbody > tr:nth-child({trade_index}) > td:nth-child(2)::text").get()

                        if (trade_bool and auction_bool) or trade_index>10:
                            break
                        trade_index = trade_index + 1
                    except Exception:
                        print("exception occured")
                        break

                if street is None or city_and_zip is None or city is None or zip is None or auction_price is None or auction_date is None or trade_price is None or trade_date is None:
                    continue
                f.write(f"{street.strip()};{city.strip()};{zip.strip()};{auction_price};{auction_date};{trade_price};{trade_date};{sqm}\n")

            if i == 1:
                next_button_selector = f"//*[@id='page-salesprice-result']/div/div/div[2]/div/div[2]/div[2]/a"
            else:
                next_button_selector = "//*[@id='page-salesprice-result']/div/div/div[2]/div/div[2]/div[2]/a[2]"
            click_succes = False
            while not click_succes:
                try:
                    driver.find_element(By.XPATH, next_button_selector).click()
                    click_succes = True
                except NoSuchElementException:
                    print("NoSuchElementException")

            #print(f"{driver.current_url}, {i}")

            #driver.get(url.replace(f"alle/{i}",f"alle/{i+1}"))

            time.sleep(1)