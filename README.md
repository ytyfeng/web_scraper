# Web Scraper & Automated Email Alert Program
## Scrapes a website using [Selenium](https://pypi.org/project/selenium/) and sends results (text and images) to user's email every few hours
*Used for monitoring hurricanes and automating sending hurricane alerts to email*


*To use*:  
1. Download [Chrome Driver](https://chromedriver.chromium.org/).  
2. Download Chrome that is supported by the Chrome Driver.  
3. Put Chrome binaries in a local directory and link them to the system through `.bashrc`. Specifically, add something like this to the `.bashrc` file in your root directory:
``` bash
export PATH="$HOME/chrome-linux:$PATH"
```  
4. Specify Chrome Driver path in the `scraper.py` file:  
``` python
DRIVER_PATH='./chromedriver'  # if it is in the same directory as scraper.py
```
5. Download and install [Selenium](https://pypi.org/project/selenium/) Python module:  
``` bash
pip install selenium
```
6. Make sure your linux system has `mutt` email client. Check by typing the following in your terminal to see if you have it.  
``` bash
mutt
```
7. Run `scraper.py` as a background process detached from shell:
``` bash
nohup python scraper.py -e <RECIPIENT_EMAIL> &
```

*Program overview*:
1. Using Chrome Driver, get a web page.
``` python
driver.get("https://www....")
```

2. Get xcode path for the desired content of the web page using your browser's developer tool (Mac: `option`+`command`+`i` keys).
Choose the element and copy its full xpath.
For example,
``` python
content = driver.find_element_by_xpath('//html/body/div[5]/div/h2')
```

To access the text content,
``` python
content.get_attribute('innerText')
# or
content.get_attribute('innerHTML')
```

3. Write the scraped content into an HTML file using Python's file module.  
4. Send the email using the `mutt` email client:
``` bash
mutt -e 'set content_type=text/html crypt_use_gpgme=no' -a <EMAIL_ATTACHMENTS> -s '<EMAIL_SUBJECT>' -c {} < mail.html".format(EMAIL)
```
5. To send email update every few hours, I'm using `pause` module:  
``` python
pause.hours(wait_interval)
```
