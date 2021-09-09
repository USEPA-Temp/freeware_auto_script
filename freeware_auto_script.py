""" FREEWARE REQUEST AUTOMATION
EPA ORD Office of Science Information Management
2021-09-08

This script uses selenium to automatically file software requests for you.

--> CURRENTLY ONLY ORD MACHINES ARE SUPPORTED <--
Please let me know if you need EISD machine support added

To use it:
* You will need selenium installed as as as chromedriver.
* You will need to edit this file and change it to match your configuration
* You will need a file that looks like this:
    homebrew # Homebrew allows convinence installation and updates of software. Without this utility it would be difficult if not impossible to keep my software up to date. It avoids admin rights and installs software in a user-writable location /opt/homebrew/
    git # This freeware allows version control of software.
    sqlite # sqlite.org I need sqlite because it is used in many pieces of ORD scientific software and is very useful in scripts.

How to use it:
* python3 freeware_auto_script.py applications.txt

Your lan id and password will be promoted

License:
Usage of the works is permitted provided that this instrument is retained with the works,
so that any entity that uses the works is notified of this instrument. DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.
"""
import os
import sys
import time
import subprocess

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

assert sys.version_info >= (3, 7), "Must use Python 3.7+ due or change the below to ordereddict"
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        exit(1)
USERNAME = os.environ.get('USERNAME') or input("LAN ID: ")
PASSWORD = os.environ.get('PASSWORD') or input('LAN PASSWORD: ')
ORD_MACHINE = input("This tool only supports ORD machines right now. EISD is not supported Ok?: ")

SUPERVISOR_EMAIL = "last.first@epa.gov"
data = {
    "Email Required Field": "your.email@epa.gov",
    "Phone": "5551234567",
    "Site Required Field": "COR",
    "Office Required Field": "OSIM",
    "System Name Required Field": f"{os.environ.get('COMPUTERNAME') or subprocess.check_output('hostname').decode().split('.', 1)[0]}",
    "Supervisor, Enter a name or email address...": SUPERVISOR_EMAIL,
    "Direct Supervisor Email Required Field": SUPERVISOR_EMAIL,
    "Software Required Field": "",
    "Justification Required Field": "",
    "Operating System Required Field": "",  # Put Apple Mac OS
}


def supervisor(field, wait, *_):
    time.sleep(1)
    field.send_keys(Keys.RETURN)
    time.sleep(1)
    wait.until(presence_of_element_located((By.CSS_SELECTOR, f"li[title*={SUPERVISOR_EMAIL[:4]}]")))
    field.send_keys(Keys.RETURN)


def software_name_field(field, wait, software_name, software_justification):
    field.send_keys(software_name + Keys.RETURN)


def software_justification_field(field, wait, software_name, software_justification):
    field.send_keys(software_justification + Keys.RETURN)


extra_steps = {
    "Supervisor, Enter a name or email address...": supervisor,
    "Software Required Field": software_name_field,
    "Justification Required Field": software_justification_field,
}


def main(software_name, software_justification):
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 10)
        driver.get(f"https://{USERNAME}:{PASSWORD}@ordsecurity.epa.gov/resources/Lists/FreewareShareware/NewForm.aspx")
        for title, value in data.items():
            field = driver.find_element_by_css_selector(f"[title*='{title}'")
            field.send_keys(value + Keys.RETURN)
            if title in extra_steps:
                extra_steps[title](field, wait, software_name, software_justification)

        for field in driver.find_elements_by_css_selector("[value='Save']"):
            try:
                field.click()
            except ElementNotInteractableException:
                pass
        wait.until(presence_of_element_located((By.ID, "DeltaPlaceHolderUtilityContent")))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            for line in f:
                if "#" not in line:
                    continue
                s, d = [_.strip() for _ in line.split("#", 1)]
                main(s, d)
