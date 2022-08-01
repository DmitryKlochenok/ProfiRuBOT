# Открыть сайт
import time
import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.common.action_chains
import tutors_data

def load_tutor_data():
    global first_message
    global login
    global password
    global keywords


    tutor = input("Имя преподавателя: ")
    for k, v in tutors_data.tutors.items():
        if tutor == k:
          first_message = v[0]
          login = v[1]
          password = v[2]
          keywords = v[3]

#def close_banner():
    #banner_close = driver.find_element(By.XPATH, '//*[@id="content-content"]/div[1]/div/div[1]')
    #action.move_to_element_with_offset(banner_close, 0, 0)
    #action.click()
    #action.perform()

def run_search():
    while True:

        time.sleep(10)
        t = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        action = webdriver.common.action_chains.ActionChains(driver)

        driver.get("https://profi.ru/backoffice/n.php")
        login_place = driver.find_element(By.CSS_SELECTOR,
                                          "#content > div > div.WrapperStyles__ContentWrapper-y7txxx-2.fYTfEX > div > div.auth-container > div > div > form > div > div > div:nth-child(1) > label > span > input")
        login_place.send_keys(login)
        password_place = driver.find_element(By.CSS_SELECTOR, "input.login-form__input-password")
        password_place.send_keys(password)
        ui_button = driver.find_element(By.CSS_SELECTOR, "[type='button']")
        ui_button.click()
        time.sleep(10)

        #close_banner()

        # Цикл обновить страницу и найти анкету




        while t <= 30:

            try:
              time.sleep(3)
              driver.refresh()
            except:
                continue

            time.sleep(5)
            # Найти анкету и нажать
            anketa = driver.find_element(By.CSS_SELECTOR, '#content-content :nth-child(1)')
            #support = driver.find_element(By.XPATH, '//*[@id="layout-header__content"]/nav/a[5]/div')
            ord_time_1 = driver.find_element(By.CSS_SELECTOR, "#content-content :nth-child(1) > div > div > div :nth-child(2) :nth-child(2) > div :nth-child(2)")
            ord_time_2 = driver.find_element(By.CSS_SELECTOR, "#content-content :nth-child(1) > div > div > div > div :nth-child(2)")

            #for keyword in keywords:
                #if keyword in anketa.text:
                    #print("Сделано исключение")
                    #continue
            if ord_time_1.text == "1 минуту назад" or ord_time_1.text == "2 минуты назад" or ord_time_2.text == "1 минуту назад" or ord_time_2.text == "2 минуты назад":
                    action.move_to_element_with_offset(anketa, 1, 1)
                    #action.move_to_element_with_offset(support, 1, 250)
                    action.click().perform()
                    #action.perform()
            else:
                continue
            time.sleep(10)

            # Перейти в соседнюю вкладку
            p = driver.current_window_handle
            parent = driver.window_handles[0]
            try:
              chld = driver.window_handles[1]
            except:
                time.sleep(20)
                continue
            driver.switch_to.window(chld)

            # Нажать откликнуться, вставить шаблон, нажать откликнуться

            time.sleep(8)
            try:
                #response_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Поддержка"]')
                response_button = driver.find_element(By.CSS_SELECTOR, "div[class^='Tariffs__Button']")
                if "руб." in response_button.text:
                    print("Закончились бесплатные отклики")
                    quit()
                    break

                #action.move_to_element_with_offset(response_button, 1, 300)
                action.move_to_element_with_offset(response_button, 1, 1)
                action.click()
                action.perform()
                t += 1
            except:
                driver.close()
                driver.switch_to.window(parent)
                continue

            try:
                time.sleep(3)
                template = driver.find_element(By.CSS_SELECTOR, ".backoffice-common-textarea :first-child")
                template.send_keys(first_message)
                try:
                  send_message = driver.find_element(By.XPATH,"/html/body/div[5]/div/div/div[1]/div[2]/div/div[2]/a/div/div")
                  action = webdriver.common.action_chains.ActionChains(driver)
                  action.move_to_element_with_offset(send_message, 1, 1)
                  action.click()
                  action.perform()
                except:
                    send_message = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div[2]/div/div[2]/button/div/div")
                    action = webdriver.common.action_chains.ActionChains(driver)
                    action.move_to_element_with_offset(send_message, 1, 1)
                    action.click()
                    action.perform()
                action = webdriver.common.action_chains.ActionChains(driver)
                action.move_to_element_with_offset(send_message, 1, 1)
                action.click()
                action.perform()
                driver.close()

                # Вернуться на главную вкладку
                driver.switch_to.window(parent)
                continue
            except:
                driver.refresh()
                driver.close()
                driver.switch_to.window(parent)
                continue


        driver.quit()


def add_tutor():
    with open("tutors_data.py", "w") as file:
        print("Для редактирования данных удалить данные о преподавателе и добавить заново")
        inp_tutor = input("Имя преподавателя: ")
        while inp_tutor in tutors_data.tutors.keys():
            print("Имя уже занято, введите по-другому")
            inp_tutor = input("Имя преподавателя: ")
        inp_pnumber = input("Номер телефона преподавателя")
        inp_login = input("Введите логин: ")
        inp_pass = input("Введите пароль: ")
        inp_template = input("Введите текст отклика \n Для раставления абзацев использовать символ \ n (без пробела): ")
        inp_keywords = input("Исключить из поиска ключевые слова: ")

        tutors_data.tutors["inp_tutor"] = [inp_template, inp_login, inp_pass, inp_keywords, inp_pnumber]

def del_tutor():
    with open("tutors_data.py", "w") as file:
        del_tut = input("Имя преподавателя, которого надо удалить: ")
        del tutors_data.tutors["del_tut"]

#git test
def g():
    pass