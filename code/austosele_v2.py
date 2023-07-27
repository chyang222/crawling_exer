import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui
import os
import time
import random
from tqdm import tqdm

num = 19

df = pd.read_json("C:\\Users\\user\\Downloads\\node_info2_19_202207.json")

df = df.T
df = df.reset_index()
df.rename(columns = {'idx' : 'LINK_ID'}, inplace = True)
df = df.round(6)
df = df.astype({'x':'str', 'y': 'str'})
df['coor'] = df[['y', 'x']].apply(', '.join, axis=1)
df = df.astype({'LINK_ID':'int64'})
df = df.sort_values(by=["LINK_ID"], ascending=[True]) 

ind = []
address = []

#----------------------------------------------------------------------------------------------------------------------------------------------------------------


try:
   os.mkdir("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final".format(str(num)))  
   for i in df.LINK_ID.unique():
     os.mkdir("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}".format(str(num), str(i)))  
except:
   pass

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
def locate(*args):
   answer = []
   
   icon = pyautogui.locateOnScreen('C:\\Users\\user\\Desktop\\icon\\icon3.PNG', confidence=0.5)
   pyautogui.moveTo(icon)
   icon2 = pyautogui.locateOnScreen('C:\\Users\\user\\Desktop\\icon\\icon4.PNG', confidence=0.5)
   pyautogui.moveTo(icon2)
   icon3 = pyautogui.locateOnScreen('C:\\Users\\user\\Desktop\\icon\\icon5.PNG', confidence=0.5)
   pyautogui.moveTo(icon3)

   if icon == None and icon2 == None and icon3 == None:
        while icon == None and icon2 == None and icon3 == None :
            pyautogui.moveTo(1230,720)
            pyautogui.dragTo(1400, 720, 0.3, button='left')
            time.sleep(0.5)
            icon = pyautogui.locateOnScreen('C:\\Users\\user\\Desktop\\icon\\icon3.PNG', confidence=0.5)
            icon2 = pyautogui.locateOnScreen('C:\\Users\\user\\Desktop\\icon\\icon4.PNG', confidence=0.5)
            icon3 = pyautogui.locateOnScreen('C:\\Users\\user\\Desktop\\icon\\icon5.PNG', confidence=0.5)
            
        answer.append(icon)
        answer.append(icon2)
        answer.append(icon3)

    # 도로의 정확한 사진으로서 맞추기

   for i in answer:
      if i != None:
        return i

#----------------------------------------------------------------------------------------------------------------------------------------------------------------

def craw_tsafer0(i):
   xy = df.coor.iloc[i]

   try:
      element = WebDriverWait(driver,
                               10).until(
         EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
      ) #입력창이 뜰 때까지 대기
   finally:
      pass   
   
   time.sleep(1.5) 
   search_box = driver.find_element(By.CLASS_NAME, "input_search")
   search_box.send_keys(xy)
   search_box.send_keys(Keys.ENTER) 
   time.sleep(1) 

   try:
      element = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/div[2]/div[1]/maps-controller/dynamic-content-outlet[1]/control-widget/control-top-widget-holder/div/control-layer-group/control-panorama"))
      ) 
   finally:
      pass

   road_view = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/div[2]/div[1]/maps-controller/dynamic-content-outlet[1]/control-widget/control-top-widget-holder/div/control-layer-group/control-panorama")

   if i == 0:
      road_view.click() #거리뷰 클릭
      add_text = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div[2]/div/div[3]/div[2]/div/fusion-marker/div/div[2]/div[2]/div/strong')
      address.append(add_text.text)
   
   else:
      try:
         add_text = driver.find_element(By.XPATH,'/html/body/div[3]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/fusion-marker/div/div[2]/div[2]/div/strong')
         address.append(add_text.text)
      except:
         address.append(xy)

   time.sleep(2) 
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\일반지도.png".format(str(num), str(df.LINK_ID.iloc[i])),  region=(1000,200,1200,1200))
   # 여기까지 일반지도 스크린샷


   try:
      element = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/div[2]/div[1]/maps-controller/dynamic-content-outlet[1]/control-widget/control-top-widget-holder/control-carto-map-widget-holder/div/control-carto-map-satellite"))
      ) 
   finally:
      pass

   satellite_button = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/div[2]/div[1]/maps-controller/dynamic-content-outlet[1]/control-widget/control-top-widget-holder/control-carto-map-widget-holder/div/control-carto-map-satellite")
   satellite_button.click()
   time.sleep(2) 
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\위성지도.png".format(str(num), str(df.LINK_ID.iloc[i])),region=(1000,200,1200,1200))
   ## 여기까지 위성지도 스크린샷


   try:
      pyautogui.moveTo(1325,740)
      pyautogui.click()
      driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/fusion-marker/div/div[2]/div[2]/div/strong')
   except:
      pyautogui.moveTo(1325+55,740+55)
      pyautogui.click()

   time.sleep(1) 
   
   if i == 0:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/panorama-onboarding/div/button"))
            ) 
        finally:
            pass
        popup_button = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/panorama-onboarding/div/button")
        popup_button.click()
        #팝업창 삭제

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/panorama-location-info/button"))
            ) 
        finally:
            pass
        around_location = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/panorama-location-info/button")
        around_location.click()
        #주변장소 접기

   pyautogui.moveTo(1500,700)
   for count2 in range(5):
       time.sleep(0.25)
       pyautogui.scroll(500)
    

   icon = locate()
   if locate() != None:
        pyautogui.moveTo(icon)
        pyautogui.dragTo(650, 725, 1, button='left')

   pyautogui.moveTo(1500,700)

   for count in range(5):
      pyautogui.scroll(-500)
      time.sleep(0.25)
    # 도로의 정확한 사진으로서 맞추기

   time.sleep(1) 
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\로드뷰1.png".format(str(num), str(df.LINK_ID.iloc[i])),region=(400,150,1600,1000))
   ## 여기까지 로드뷰1 스크린샷


   try:
      element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/div[2]/panorama-compass/div/button[3]"))
      ) 
   finally:
      pass

   right = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/div[2]/panorama-compass/div/button[3]")
   
   for count in range(4):
      right.click()
      time.sleep(0.2)

   time.sleep(1)
   
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\로드뷰2.png".format(str(num), str(df.LINK_ID.iloc[i])),region=(400,150,1600,1000))
   ## 여기까지 로드뷰2 스크린샷

   try:
      element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/button"))
      ) 
   finally:
      pass

   final_but = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/button")
   final_but.click()
   time.sleep(0.5)
   #처음 화면으로 돌리기

#------------------------------------------------------------------------------------------------------------------------------------------------------------

def craw_tsafer1(i):
   xy = df.coor.iloc[i]

   try:
      element = WebDriverWait(driver,
                               10).until(
         EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
      ) #입력창이 뜰 때까지 대기
   finally:
      pass

   time.sleep(1.5) 
   search_box = driver.find_element(By.CLASS_NAME, "input_search")
   search_box.send_keys(xy)
   search_box.send_keys(Keys.ENTER) 
   time.sleep(1.5) 

   try:
      add_text = driver.find_element(By.XPATH,'/html/body/div[3]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/fusion-marker/div/div[2]/div[2]/div/strong')
      address.append(add_text.text)
   except:
      address.append(xy)

   time.sleep(2) 
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\위성지도.png".format(str(num), str(df.LINK_ID.iloc[i])),region=(1000,200,1200,1200))
   # 여기까지 위성지도 스크린샷
   
   try:
      element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/div[2]/div[1]/maps-controller/dynamic-content-outlet[1]/control-widget/control-top-widget-holder/control-carto-map-widget-holder/div/control-carto-map-normal/a"))
      ) 
   finally:
      pass


   common_button = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/div[2]/div[1]/maps-controller/dynamic-content-outlet[1]/control-widget/control-top-widget-holder/control-carto-map-widget-holder/div/control-carto-map-normal/a")
   common_button.click()
   

   time.sleep(3) 
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\일반지도.png".format(str(num), str(df.LINK_ID.iloc[i])),  region=(1000,200,1200,1200))
   # 여기까지 일반지도 스크린샷

   try:
      pyautogui.moveTo(1325,740)
      pyautogui.click()
      driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/fusion-marker/div/div[2]/div[2]/div/strong')

   except:
      pyautogui.moveTo(1325+55,740+55)
      pyautogui.click()

   pyautogui.moveTo(1500,700)

   for count2 in range(5):
       time.sleep(0.25)
       pyautogui.scroll(500)
    
   icon = locate()
   
   if locate() != None:
        pyautogui.moveTo(icon)
        pyautogui.dragTo(650, 725, 1, button='left')


   pyautogui.moveTo(1500,700)
   for count in range(5):
      time.sleep(0.25)
      pyautogui.scroll(-500)
    # 도로의 정확한 사진으로서 맞추기

   time.sleep(5) 
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\로드뷰1.png".format(str(num), str(df.LINK_ID.iloc[i])),region=(400,150,1600,1000))
   ## 여기까지 로드뷰1 스크린샷

   try:
      element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/div[2]/panorama-compass/div/button[3]"))
      ) 
   finally:
      pass

   right = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/div[2]/panorama-compass/div/button[3]")
   
   for count in range(4):
      right.click()
      time.sleep(0.3)

   time.sleep(1.3)
   
   pyautogui.screenshot("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}\\로드뷰2.png".format(str(num), str(df.LINK_ID.iloc[i])),region=(400,150,1600,1000))
   ## 여기까지 로드뷰2 스크린샷

   try:
      element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/button"))
      ) 
   finally:
      pass

   final_but = driver.find_element(By.XPATH, "/html/body/app/layout/div[3]/panorama-layout/div/button")
   final_but.click()
   time.sleep(1.5)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    driver = webdriver.Chrome(executable_path='C:\\Users\\User\\Desktop\\python\\chromedriver.exe')

    time.sleep(0.5)

    driver.maximize_window()
    driver.get("https://map.naver.com/v5/") 

    for i in tqdm(range(12, len(df))):
        print(str(df.LINK_ID.iloc[i]))
        ind.append(str(df.LINK_ID.iloc[i]))

        if i == 0 or i % 2 == 0:
            craw_tsafer0(i)

        else:
            craw_tsafer1(i)


    add_df = pd.DataFrame(address,  columns = ["주소"], index = ind)
    add_df.to_csv("C:\\Users\\User\\Desktop\\sele_test\\nodexy\\{}_node_final\\{}_address.csv".format(str(num), str(num)), encoding="euc-kr")