'''
Scrapes a website and sends content to an email address every few hours
 
Used for monitoring Atlantic hurricanes

Usage: 
python scraper.py -e <RECIPIENT_EMAIL>


2020 © Ty Feng

'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import pause
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--email", required=True, help = "email address to send alerts to")
args = vars(ap.parse_args())
EMAIL = args["email"]

options = Options()
options.headless = True # using Chrome without opening its GUI display
options.add_argument("--window-size=1920,1200")
DRIVER_PATH="./chromedriver" # where you put your chromdriver

os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0' # set to Eastern time
time.tzset()

timeout = 32        # number of times of iteration
wait_interval = 3   # hours before the next iteration
wait_bool = False   # boolean variable to control 3 hours of waiting time between each email alert
while timeout > 0:
    if wait_bool == False:
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get("https://www.nhc.noaa.gov/gtwo.php")
        outlook_text = driver.find_element_by_xpath('//html/body/div[5]/div/div[3]/div/pre').get_attribute('innerHTML')
        driver.get('https://www.nhc.noaa.gov/refresh/graphics_at4+shtml/1.shtml')
        storm_name = driver.find_element_by_xpath('//html/body/div[5]/div/h2').get_attribute('innerText')
        current_time = time.strftime('%X %x %Z')
        struct_time = time.strptime(current_time, "%X %x %Z")
        struct_time_2 = (struct_time[0], struct_time[1], struct_time[2], struct_time[3]+wait_interval, struct_time[4], struct_time[5], struct_time[6], struct_time[7], struct_time[8])
        make_time = time.mktime(struct_time_2)
        localtime = time.localtime(make_time)
        next_time = time.strftime("%X %x %Z", localtime)
        
        f = open("mail.html", "w")
        f.write("<p>Hi, </p> \n<p>Here is the {} update for {} from <b><a href='https://www.nhc.noaa.gov/gtwo.php?basin=atlc&fdays=5'>NOAA</a></b>.</p>\n <p>The next update will be sent at {}. </p> \n <pre> {} </pre> \n".format(time.strftime('%I %p'), storm_name, next_time, outlook_text))
        f.close()
        
        os.system("wget -O storm.png https://www.nhc.noaa.gov/storm_graphics/AT09/refresh/AL092020_5day_cone_no_line_and_wind+png/storm.png")
        os.system("wget -O message.png https://www.nhc.noaa.gov/storm_graphics/AT09/refresh/AL092020_key_messages+png/messages.png")
        time.sleep(1)
        os.system("mutt -e 'set content_type=text/html crypt_use_gpgme=no' -a storm.png -a message.png -s '{} Update: {}' -c {} < mail.html".format(storm_name, current_time, EMAIL))
        print("Email update sent to: {} at {}. \n".format(EMAIL, current_time))
        driver.quit()
        wait_bool = True
        timeout = timeout - 1
        continue
    
    else:
        pause.hours(wait_interval)
        wait_bool = False
        continue
    
