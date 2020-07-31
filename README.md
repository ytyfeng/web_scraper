# Web Scraper

## Scrapes a website using Selenium and sends results (text and images) to user's email every few hours

### Used for monitoring hurricanes and automating sending hurricane alerts to email

To use:  
1. Download [Chrome Driver](https://chromedriver.chromium.org/).  
2. Download Chrome that is supported by the Chrome Driver.  
3. Put Chrome binaries in a local directory and link them to the system through `.bashrc`. Specifically, add something like this to the `.bashrc` file in root directory:
` export PATH="$HOME/chrome-linux:$PATH" `  
4. Specify Chrome Driver path in the `scraper.py` file:  
` DRIVER_PATH='./chromedriver'  # if it is in the same directory as scraper.py `  
5. Run `scraper.py` as a background process detached from shell:
` nohup python scraper.py -e <RECIPIENT_EMAIL> &`
