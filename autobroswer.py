from selenium import webdriver
import lms
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

driver = None


def create_new_browser(ip=None, test=False):
    global driver

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"--proxy-server={ip}")

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

        # driver = webdriver.Chrome(executable_path="drivers/chromedriver", options=chrome_options)

        if test:
            driver.get("http://c3pbchau-cr.lms.vnedu.vn/")
            content = driver.page_source
            driver.quit()

            return "E-Learning" in content
    except:
        return False


def login_to_lms(user, password):
    global driver
    driver.get(lms.get_url_login(user, password))

    time.sleep(2)


def get_course_data():
    global driver

    driver.get("http://c3pbchau-cr.lms.vnedu.vn/service/user/getListCourseWithTab?tab=1&filterCourse[key]="
               "&filterCourse[khoiId]=&filterCourse[monId]=&filterCourse[lopId]=http://c3pbchau-cr.lms."
               "vnedu.vn/service/user/getListCourseWithTab?tab=1&filterCourse[key]=&filterCourse[khoiId]="
               "&filterCourse[monId]=&filterCourse[lopId]=")

    time.sleep(1)

    return driver.execute_script('return document.getElementsByTagName("pre")[0].outerText;')


def view_courses_not_finished(ids):
    global driver

    for id in ids:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])

        url = f"http://c3pbchau-cr.lms.vnedu.vn/course/enjoin?id={id}"

        driver.get(url)

        if driver.current_url != url:
            e = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div/div[1]/div/div[4]/a")
            e.click()

            time.sleep(3)
            driver.get(url)

        time.sleep(3)

        ids = []

        for x in driver.find_elements_by_xpath(
                f'//*[contains(@class, "tracking-content-title item_hoclieu_title item_hoclieu_title_")]'):
            ids.append(x.get_attribute("id"))

        t = 0

        for id_course in ids:
            course = driver.find_element_by_xpath(f'//*[@id="{id_course}"]')
            command = course.get_attribute("onclick")

            driver.execute_script(command.replace("$(event.target)", f"$('[id={id_course}]')") + ";")
            time.sleep(5)

            found = False

            # if have next button
            try:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="course_lesson_iframe"]')))
                except:
                    pass

                found = True

                e = driver.find_element_by_xpath('//*[@id="next"]')
                m = driver.find_element_by_xpath('//*[@id="app-pdf"]/div[1]/div/div/div[2]/label/span').text[0]

                for _ in range(int(m)):
                    e.click()
                    time.sleep(3)

                driver.switch_to.default_content()
            except:
                if found:
                    driver.switch_to.default_content()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(3)
# except:
#     print("Có lỗi xảy ra")
#     pass


def cancel():
    global driver
    driver.quit()
    time.sleep(5)
