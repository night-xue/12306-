from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
def get_ticket(from_station,to_station,date):
    option = webdriver.EdgeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option("detach", True)


    driver = webdriver.Edge(executable_path='./edge driver', options=option)

    driver.maximize_window()

    driver.get('https://kyfw.12306.cn/otn/resources/login.html')

    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    driver.execute_script(script)

    userName_tag = driver.find_element(By.ID,'J-userName')
    password_tag = driver.find_element(By.ID,'J-password')
    userName_tag.send_keys('18835986243')
    password_tag.send_keys('xqj011118')

    btn = driver.find_element(By.ID,'J-login')
    btn.click()
    sleep(2)

    span = driver.find_element(By.ID,'nc_1_n1z')
    action = ActionChains(driver)
    action.click_and_hold(span)
    for i in range(10):
        action.move_by_offset(35, 0).perform()
        sleep(0.1)
    action.release()

    # driver.implicitly_wait(10)
    # time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,'.btn-primary').click()

    driver.find_element(By.CSS_SELECTOR,'#link_for_ticket').click()

    driver.find_element(By.CSS_SELECTOR,'#qd_closeDefaultWarningWindowDialog_id').click()

    driver.find_element(By.ID,'wf').click()

    driver.find_element(By.CSS_SELECTOR,'#fromStationText').click()
    driver.find_element(By.CSS_SELECTOR,'#fromStationText').clear()
    driver.find_element(By.CSS_SELECTOR,'#fromStationText').send_keys(from_station)
    driver.find_element(By.CSS_SELECTOR,'#fromStationText').send_keys(Keys.ENTER)

    driver.find_element(By.CSS_SELECTOR,'#toStationText').click()
    driver.find_element(By.CSS_SELECTOR,'#toStationText').clear()
    driver.find_element(By.CSS_SELECTOR,'#toStationText').send_keys(to_station)
    driver.find_element(By.CSS_SELECTOR,'#toStationText').send_keys(Keys.ENTER)

    driver.find_element(By.CSS_SELECTOR,'#train_date').click()
    driver.find_element(By.CSS_SELECTOR,'#train_date').clear()
    driver.find_element(By.CSS_SELECTOR,'#train_date').send_keys(date)
    driver.find_element(By.CSS_SELECTOR,'#train_date').send_keys(Keys.ENTER)

    driver.find_element(By.ID,'query_ticket').click()

    # 预定
    # driver.find_element(By.CSS_SELECTOR,'#ticket_27000D25670A_01_05 > td.no-br > a').click()
    # driver.find_element(By.CSS_SELECTOR,'#normalPassenger_0').click()
    # driver.find_element(By.CSS_SELECTOR,'#dialog_xsertcj_ok').click()