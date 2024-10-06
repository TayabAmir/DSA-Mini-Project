from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="C:/chromedriver-win64[1]/chromedriver-win64/chromedriver.exe")
options = webdriver.ChromeOptions()
# options.add_argument("headless")
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service=service, options=options)

url = "http://result.biselahore.com/"
driver.get(url)

def search_result(rollno):
    try:
        inter_id, roll_no_id, type_id, year_id, search_button_id = 'rdlistCourse_1', 'txtFormNo', 'ddlExamType', 'ddlExamYear', 'Button1'
        
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, inter_id)))
        driver.find_element(By.CSS_SELECTOR, f'label[for="{inter_id}"]').click()

        driver.find_element(By.ID, roll_no_id).clear()
        driver.find_element(By.ID, roll_no_id).send_keys(str(rollno))

        Select(driver.find_element(By.ID, type_id)).select_by_value('2') 
        Select(driver.find_element(By.ID, year_id)).select_by_value('2023')
        driver.find_element(By.ID, search_button_id).click()

        driver.implicitly_wait(5)
    except Exception as e:
        print(f"Error during search for roll number {rollno}: {e}")
        return False 

    return True

def scrape_data(rollno):
    try:
        status = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[3]/td[3]').text
        if status == "ABSENT":
            return None

        name = driver.find_element(By.XPATH, '//*[@id="Name"]').text
        cnic = driver.find_element(By.XPATH, '//*[@id="lblBFARM"]').text
        urdu = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[3]/td[8]').text
        english = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[4]/td[8]').text
        islamiat = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[5]/td[8]').text
        pak_study = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[6]/td[8]').text
        physics = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[7]/td[8]').text
        chemistry = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[8]/td[8]').text
        mathematics = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[9]/td[8]').text
        total = driver.find_element(By.XPATH, '//*[@id="GridStudentData"]/tbody/tr[11]/td[2]').text

        
        def process_subject_marks(subject, part1Xpath, part2Xpath):
            if subject == "AB" or not subject.isdigit():
                part1 = driver.find_element(By.XPATH, part1Xpath).text
                part1 = 0 if part1 == "AB" or part1 == "--" else int(part1)
                part2 = driver.find_element(By.XPATH, part2Xpath).text
                part2 = 0 if part2 == "AB" or part2 == "--" else int(part2)
                return part1 + part2
            else:
                return int(subject)

        urdu = process_subject_marks(urdu, '//*[@id="GridStudentData"]/tbody/tr[3]/td[5]', '//*[@id="GridStudentData"]/tbody/tr[3]/td[6]')
        english = process_subject_marks(english, '//*[@id="GridStudentData"]/tbody/tr[4]/td[5]', '//*[@id="GridStudentData"]/tbody/tr[4]/td[6]')
        islamiat = process_subject_marks(islamiat, '//*[@id="GridStudentData"]/tbody/tr[5]/td[5]', '//*[@id="GridStudentData"]/tbody/tr[5]/td[5]')
        pak_study = process_subject_marks(pak_study, '//*[@id="GridStudentData"]/tbody/tr[6]/td[6]', '//*[@id="GridStudentData"]/tbody/tr[6]/td[6]')

        def process_practical_marks(subject, part1Xpath, part2Xpath, practical_xpath):
            if subject == "AB" or not subject.isdigit():
                part1 = driver.find_element(By.XPATH, part1Xpath).text
                part1 = 0 if part1 == "AB" or part1 == "--" else int(part1)
                part2 = driver.find_element(By.XPATH, part2Xpath).text
                part2 = 0 if part2 == "AB" or part2 == "--" else int(part2)
                practical = driver.find_element(By.XPATH, practical_xpath).text
                practical = 0 if practical == "AB" or practical == "--" else int(practical)
                return part1 + part2 + practical
            else:
                return int(subject)

        physics = process_practical_marks(physics, '//*[@id="GridStudentData"]/tbody/tr[7]/td[5]', '//*[@id="GridStudentData"]/tbody/tr[7]/td[6]', '//*[@id="GridStudentData"]/tbody/tr[7]/td[7]')
        chemistry = process_practical_marks(chemistry, '//*[@id="GridStudentData"]/tbody/tr[8]/td[5]', '//*[@id="GridStudentData"]/tbody/tr[8]/td[6]', '//*[@id="GridStudentData"]/tbody/tr[8]/td[7]')
        mathematics = process_practical_marks(mathematics, '//*[@id="GridStudentData"]/tbody/tr[9]/td[5]', '//*[@id="GridStudentData"]/tbody/tr[9]/td[6]', '//*[@id="GridStudentData"]/tbody/tr[9]/td[7]')

        total_split = total.split(' ')
        if total_split[-2].isdigit():
            total = int(total_split[-2])
        else:
            total = urdu + english + islamiat + pak_study + physics + chemistry + mathematics

        return [rollno, name, cnic, urdu, english, islamiat, pak_study, physics, chemistry, mathematics, total]

    except Exception as e:
        print(f"Error extracting data for roll number {rollno}: {e}")
        return None

if __name__ == "__main__":
    search_result(421412)