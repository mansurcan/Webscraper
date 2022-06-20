import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import os
import urllib
import socket
import ssl
import pandas as pd
import A_Const

class Amazon:
    
    def __init__(self):
        '''Initializing webscaraper...'''
        print("Initializing webscraper...")
        
        website = "https://www.amazon.co.uk/"
        opt = webdriver.ChromeOptions()
        opt.headless = True
        opt.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
        self.driver.get(website)
        self.driver.set_page_load_timeout(10)
        self.driver.implicitly_wait(10)
        
    def _accept_cookies(self):   
        '''Accepts cookies...'''     
        print("Accepting cookies...")
        
        xpath_accept_cookies = "//input[@type='submit' and @id='sp-cc-accept']"
        accept_button = self.driver.find_element(By.XPATH, xpath_accept_cookies)
        accept_button.click()
        time.sleep(2)

    
    def _search(self):        
        '''Searching for the product in the Amazon website.'''
        print("Searching for the product...")
        
        search_term = "iPhone 13"
        search_input = self.driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']")
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)

        accept_button = self.driver.find_element(By.XPATH, "//span[text()='Apple']")
        accept_button.click()
        
    def _download_images(self):
        '''Downloads images from the Amazon website.'''
        print("Downloading images...")
        
        img = self.driver.find_elements(by=By.XPATH, value="//img[@class='s-image']")
        print(len(img))

        src = [i.get_attribute('src') for i in img]
        print(len(src))
        
        image_path = os.getcwd()
        image_path = os.path.join(image_path, 'iphone_images')
        if not os.path.exists(image_path):
            os.mkdir(image_path)
            print(image_path)
     
        count = 1
        for i in src:
            try:   
                urllib.request.urlretrieve(i, os.path.join(image_path, 'image' + str(count) + '.jpg'))
                count += 1
            except Exception as e:
                print(e)
        amz.scrape_data()
        
    def scrape_data(self):
        '''
        It scrapes the data from the website:
        - uuid, sku, number of stars, number of reviews, image links, product links.
        '''
        print("Scraping the data...")
        
        iphone_results = []

        for i in range(5):
            time.sleep(10)
                        
            sku = self.driver.find_elements(by=By.XPATH, value="//span[contains(@class,'a-size-medium a-color-base a-text-normal')]")
            asin = self.driver.find_elements(by=By.XPATH, value="//div[contains(@class, 's-result-item s-asin')]")
            reviews = self.driver.find_elements(by=By.XPATH, value="//div[@class='a-row a-size-small']/span[2]")
            image_link = self.driver.find_elements(by=By.XPATH, value="//img[@class='s-image']")
            product_link = self.driver.find_elements(by=By.XPATH, value="//a[@class='a-link-normal s-no-outline']")
            prices = self.driver.find_elements(by=By.XPATH, value="//span[contains(@class,'price-whole')]")
            
            price = [p.text for p in prices]
            
            if not None in [sku, asin, price, reviews, image_link, product_link]:
                try:
                    for i in range(len(sku)):    
                                        
                        uuidFour = str(uuid.uuid4()) 
                               
                        data = {'uuid': uuidFour,
                                'sku': sku[i].text, 
                                'asin': asin[i].get_attribute('data-asin'), 
                                'price': price[i],
                                'reviews': reviews[i].text, 
                                'image_link': image_link[i].get_attribute('src'), 
                                'product_link': product_link[i].get_attribute('href')}

                        iphone_results.append(data)
                        
                    next = self.driver.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
                    next.click()
                    time.sleep(10)              
                    
                    df_data = pd.DataFrame(iphone_results, columns=['uuid',
                                                                    'sku', 
                                                                    'asin', 
                                                                    'price',
                                                                    'reviews', 
                                                                    'image_link', 
                                                                    'product_link'])
                            
                    df_data.to_excel('Iphone_Results.xlsx', index=False)
                    df_data.to_json('Iphone_Results.json', orient='records')
                    
                    amz._download_images()
                    
                except Exception as e:
                    print(e)
                    continue
            
            print(df_data)
                
if __name__ == "__main__":  
    
    '''Main function...'''
    
    amz = Amazon()
    amz._accept_cookies()  
    amz._search()
    amz._download_images()
    amz.scrape_data()

    amz.driver.close()
    amz.driver.quit()