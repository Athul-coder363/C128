from tokenize import Intnumber
from urllib import request
from attr import attr
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/Incre/C127/chromedriver")
browser.get(START_URL)
time.sleep(10)
#add all the relevant columns
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data =  []
def scrape():
    
    for i in range(1,5):
        soup = BeautifulSoup(browser.page_source, "html.parser")

        #to check, the scrapping done page one by one
        current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
        if current_page_num < i:
            browser.find_element(By.XPATH, value='//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
                
        elif current_page_num > i:
            browser.find_element(By.XPATH, value='//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
                
        else:
            break

           
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            #add the href to the temp_list
            hyperlink_li_tag=li_tag[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print(planet_data[0])
    """with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)"""
scrape()
new_PlanetData = []
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
            td_tag = tr_tag.find_all("td")
            for td_tags in td_tag:
                try:
                    temp_list.append(td_tags.find_all("div", attrs = {"class": "value"})[0].content(0))
                except:
                    temp_list.append('')
        new_PlanetData.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
for index, data in enumerate(planet_data):
    scrape_more_data(data[5])
    print(f"scraping at{index+1} is completed")    
print(new_PlanetData[0:10])
final_planet_data = []
for index, data in enumerate(planet_data):
    new_planet_data_element = planet_data[index] 
    new_planet_data_element = [elem.replace("\n", "")for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)
with open("newTwo.csv","w") as f:
    csvWriter = csv.writer(f)
    csvWriter.writerow(headers)
    csvWriter.writerows(final_planet_data)
