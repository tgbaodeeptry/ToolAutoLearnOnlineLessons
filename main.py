from selenium import webdriver 
import hashlib, time 
from selenium.webdriver.common.keys import Keys

# Request open file: Course.studyLesson('5eaa8934e0c3fhoi04','3', $("ul").find(`[data-course-moudule-id="5e7c24ae826166hq"]`))
# Load course: http://c3pbchau-cr.lms.vnedu.vn/course/enjoin?id=5eb20885206a7h7g04 - listCourses.id

username = input("Username: ")
password = input("Password: ")
# username = "TranGiaBao_c3pbchau.cr"
# password = "Bao270304*@"

url_login = "http://c3pbchau-cr.lms.vnedu.vn/service/security/login?redirect_url=&email=" + username + "&password=" + hashlib.md5(password.encode()).hexdigest() 
url_get_courses = "http://c3pbchau-cr.lms.vnedu.vn/service/user/getListCourseWithTab?tab=1&filterCourse[key]=&filterCourse[khoiId]=&filterCourse[monId]=&filterCourse[lopId]=http://c3pbchau-cr.lms.vnedu.vn/service/user/getListCourseWithTab?tab=1&filterCourse[key]=&filterCourse[khoiId]=&filterCourse[monId]=&filterCourse[lopId]="

# # login = requests.get(url_login)
# print(login.json())

# if login.json()["success"]:
    # courses_request = requests.get(url_get_courses, cookies=login.cookies)
    
    # courses = courses_request.json()

    # if courses["success"]:
        # list_courses = courses["data"]["listCourse"]
        
        # for detail in list_courses:
            # id_course = detail["id"]
            
            # enjoin_request = requests.get(f"http://c3pbchau-cr.lms.vnedu.vn/course/enjoin?id={id_course}", cookies=login.cookies)

            # page = enjoin_request.text

            # all_match_click = re.findall(r'onclick="Course.studyLesson.*', page)

            # for x in all_match_click:
                # print(x) 

driver = webdriver.Chrome(executable_path="/home/administrator/Documents/Project/Python/ToolAutoViewLessons/drivers/chromedriver")
driver.maximize_window()

driver.get(url_login)
driver.get("http://c3pbchau-cr.lms.vnedu.vn/user/dashboard")
element = driver.find_elements_by_xpath(f'//*[contains(@href, "/course/detail")]')

for e in element:
    id = e.get_attribute("href")[46:64]
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get(f"http://c3pbchau-cr.lms.vnedu.vn/course/enjoin?id={id}")
    
    time.sleep(1)

    for course in driver.find_elements_by_xpath(f'//*[contains(@class, "tracking-content-title item_hoclieu_title item_hoclieu_title_")]'):
        command = course.get_attribute("onclick")
        id_course = course.get_attribute('id') 
        
        
        driver.execute_script(command.replace("$(event.target)", f"$('[id={id_course}]')") + ";")
        
        time.sleep(3)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(1)

driver.quit()
