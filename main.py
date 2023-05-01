import random
import time
from pyhtmlreport import Report
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
report = Report()
driver: WebDriver = webdriver.Chrome()
report.setup(
    report_folder=r'Reports',
    module_name='Device',
    release_name='Test V1',
    selenium_driver=driver
    )
driver.get('http://127.0.0.1:8000/')
# Test Case 1
try:
    report.write_step(
        'Go to Loading Page',
        status=report.status.Start,
        test_number=1
        )
    assert (driver.title == "WELCOME TO LET'S TALK")
    report.write_step(
        'Landing Page loaded Successfully.',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Landing Page loaded Successfully.',
        status=report.status.Fail,
        screenshot=True)
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
    )

# Test Case 2
try:
    report.write_step(
        'Signup for a user',
        status=report.status.Start,
        test_number=2
        )
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/a[2]').click()
    time.sleep(1)
    driver.find_element(By.NAME, 'first_name').send_keys('Nuzhat')
    time.sleep(1)
    driver.find_element(By.NAME, 'last_name').send_keys('Zeba')
    time.sleep(1)
    driver.find_element(By.NAME, 'email').send_keys('nuzhatzeba@gmail.com')
    time.sleep(1)
    driver.find_element(By.NAME, 'password').send_keys('Nuzhat@#123')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="div_id_gender"]/div/div[2]/label').click()
    time.sleep(1)
    driver.find_element(By.NAME, 'Date_Of_Birth').send_keys('08,12,1999') # .send_keys('08/12/1999')
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/form/div[1]/input').click()
    time.sleep(1)
    assert (driver.title == 'Login PAGE')
    report.write_step(
        'Successfully Signup ',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to Signup',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )
# Test Case 3
try:
    report.write_step(
        'Login for a user',
        status=report.status.Start,
        test_number=3
        )
    driver.find_element(By.NAME, 'email').send_keys('nuzhatzeba@gmail.com')
    time.sleep(1)
    driver.find_element(By.NAME, 'password').send_keys('Nuzhat@#123')
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/form/div[3]/input').click()
    assert (driver.title == "Welcome to Let's Talk homepage")
    report.write_step(
        'Successfully login ',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to login',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,

        screenshot=True
        )
# Test Case 4
try:
    report.write_step(
        'Going to Profile Page',
        status=report.status.Start,
        test_number=4
    )
    driver.find_element(By.XPATH,'/html/body/div/div[1]/ul/li[4]/a').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div/form/div[2]/input').click()
    time.sleep(1)
    assert (driver.title == 'Welcome to Profile Page')
    report.write_step(
        'Successfully Showed Profile',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to Show Profile',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )

# Test Case 5

try:
    report.write_step(
        'Updating Bio',
        status=report.status.Start,
        test_number=5
    )
    # driver.findElement(By.NAME,'about_info').click().send_keys('Hello 🤗 My name is NUZHAT ZEBA.') # " I am a Student, currently studying at the University of Asia Pacific in the Computer Science and Engineering Department. I am an enthusiastic, self-motivated, responsible and hard working person. I am able to work well both in a team environment as well as using my own initiative. I am able to work well under pressure and adhere to strict deadlines. I am a person who is very interested in movies and dramas 🍿. I also love traveling🌴. Life is short, and the world is wide. Going everywhere is on my list. Reading books📚 and mandala arts 🖼️ are my escape from the monotones of life.")
    driver.findElement(By.id('exampleFormControlTextarea2')).click().send_keys('Hello 🤗 My name is NUZHAT ZEBA.')  # " I am a Student, currently studying at the University of Asia Pacific in the Computer Science and Engineering Department. I am an enthusiastic, self-motivated, responsible and hard working person. I am able to work well both in a team environment as well as using my own initiative. I am able to work well under pressure and adhere to strict deadlines. I am a person who is very interested in movies and dramas 🍿. I also love traveling🌴. Life is short, and the world is wide. Going everywhere is on my list. Reading books📚 and mandala arts 🖼️ are my escape from the monotones of life.")
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div/form/div[2]/input').click()
    time.sleep(1)
    assert (driver.title == 'Welcome to Profile Page')
    report.write_step(
        'Successfully changed about info or Bio',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to change or edit bio',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )

# # Test Case 6
try:
    report.write_step(

        'Go to Update Password Page',
        status=report.status.Start,
        test_number=6
        )
    driver.find_element(By.XPATH,'/html/body/section/div/div/div[1]/div/div/form/a[1]').click()
    driver.find_element(By.NAME, 'password').send_keys('Nuzhat@#123')
    time.sleep(1)
    driver.find_element(By.NAME, 'new_password').send_keys('Nuzhat12@#123')
    time.sleep(1)
    driver.find_element(By.NAME, 'confirm_password').send_keys('Nuzhat12@#123')
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/form/div[4]/input').click()
    time.sleep(1)
    assert (driver.title == 'Welcome to Profile Page')
    report.write_step(
        'Password Updated',
        status=report.status.Pass,
        screenshot=True
    )
except AssertionError:
    report.write_step(
        'Failed to update password',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )
# Test Case 7
try:
    report.write_step(
        'Back to Homepage',
        status=report.status.Start,
        test_number=7
        )
    driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[1]/form/a[2]').click()
    time.sleep(1)
    assert (driver.title == "Welcome to Let's Talk homepage")
    report.write_step(
        'Back to Homepage',
        status=report.status.Pass,
        screenshot=True

    )
except AssertionError:
    report.write_step(
        'Failed to Back to Homepage',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )
# Test Case 8
try:
    report.write_step(
        'Goto to Therapist BotChat Page',
        status=report.status.Start,
        test_number=8
        )
    driver.find_element(By.XPATH, '/html/body/div/div[1]/ul/li[2]/a').click()
    time.sleep(1)
    assert (driver.title == 'Welcome to Therapist BotChat Page')
    time.sleep(1)
    report.write_step(
        'Therapist BotChat Page Loaded',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to Load Therapist BotChat Page page',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )

# Test Case 9
try:
    report.write_step(
        'Send Message To Therapist Bot',
        status=report.status.Start,
        test_number=9
        )
    driver.find_element(By.NAME, 'message').click().send_keys('Hello, What is your name?')
    time.sleep(1)
    driver.find_element(By.XPATH,'/html/body/div/div/form/div/div/input').click()
    time.sleep(1)
    assert (driver.title == 'Welcome to Therapist BotChat Page')
    report.write_step(
        'Send Message Successful',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to Send Message',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )
# Test Case 10
try:
    report.write_step(
        'Back To HomePage',

        status=report.status.Start,
        test_number=10
        )
    driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[3]/div[1]/form/a').click()
    time.sleep(2)
    assert (driver.title == "Welcome to Let's Talk homepage")
    report.write_step(
        'Back to Homepage.',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to Back to Homepage',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )

# Test Case 11
try:
    report.write_step(
        'Diary Page',
        status=report.status.Start,
        test_number=11
        )
    driver.find_element(By.XPATH, '/html/body/div/div[1]/ul/li[3]/a').click()
    time.sleep(2)
    assert (driver.title == 'Dairy Page')
    report.write_step(
        'Successfully showed diary',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to show diary',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )
# Test Case 12
try:
    report.write_step(
        'Add Notes to Diary',
        status=report.status.Start,
        test_number=10
        )

    driver.find_element(By.NAME, 'title').send_keys('New Story')
    time.sleep(1)
    driver.find_element(By.NAME, 'notes').click().send_keys('Memory... is the diary that we all carry about with us.')
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/section/div/div[2]/div[1]/div/div/form/div[2]/input').click()
    time.sleep(1)
    assert (driver.title == 'Dairy Page')
    report.write_step(
        'Notes successfully added.',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to add notes',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
    )
# Test Case 13
try:
    report.write_step(
        'Back To HomePage',

        status=report.status.Start,
        test_number=13
        )
    driver.find_element(By.XPATH, '/html/body/section/div/div[2]/div[1]/div/div/form/a').click()
    time.sleep(2)
    assert (driver.title == "Welcome to Let's Talk homepage")
    report.write_step(
        'Back to Homepage.',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to Back to Homepage',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )
# Test Case 14
try:
    report.write_step(
        'Logout User',
        status=report.status.Start,
        test_number=14
        )
    driver.find_element(By.XPATH, '/html/body/div/div[1]/ul/li[5]/a').click()
    time.sleep(2)
    assert (driver.title == "WELCOME TO LET'S TALK")
    report.write_step(
        'User has been logged out.',
        status=report.status.Pass,
        screenshot=True
        )
except AssertionError:
    report.write_step(
        'Failed to Logout',
        status=report.status.Fail,
        screenshot=True
        )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
        )
finally:
    report.generate_report()
    driver.quit()