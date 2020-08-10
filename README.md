# Cu-Register: Course Registration Tool
`cu-register` finds when a course becomes open and automatically registers you for it. It interfaces Clemson University's Banner System 
bu can be modified to work at other universities. 
<p align="center">
  <img src="https://github.com/aru-py/cu-register/blob/master/demo.gif" width=80%></img>
</p>

## Features
* Support for **multiple courses**
* Logs you in and performs **2-factor authentication**
* Runs in the background with **headless mode**
* Sends **push notifications** to your phone

## Requirements
* `Python 3.7+`
* `Google Chrome`

## Usage
1. Open your terminal and run `git clone https://github.com/aru-py/cu-register`
2. `cd cu-register && pip3 install -r requirements.txt `
3. Get a copy of [chrome webdriver](https://chromedriver.chromium.org/), extract it, and place it in your `$PATH`
4. Finally, run the script with it `cd src/ && python driver.py`
5. If a browser opens, the program is running.

## Settings
* **Change Scan Frequency:** By default, scans are performed every ten seconds, but this can configured under *global settings* in `driver.py` 
* **Enable Headless Mode:** In `driver.py`, Change `HEADLESS_MODE = False` to `HEADLESS_MODE = True` 
* **Enable Push Notifications:** Create a [IFTTT recipe](https://ifttt.com/) that uses *webhooks* and *push notifications* and add the webhook endpoitn to `data/ifttt.key`

## License
This software is released under the **MIT License** and is free to use and distribute. Contributions are greatly appreciated.
