# FREEWARE REQUEST AUTOMATION

EPA ORD Office of Science Information Management

2021-09-08

This script uses selenium to automatically file software requests for you.

--> CURRENTLY ONLY ORD MACHINES ARE SUPPORTED <--

Please let me know if you need EISD machine support added

To use it:

* You will need selenium installed as well as chromedriver.
* You will need to edit `freeware_auto_script.py` and change it to match your configuration (supervisor's name, etc)
* You will need a file that looks like this saved as `applications.txt`:
    ```
    homebrew # Homebrew allows convinence installation and updates of software. Without this utility it would be difficult if not impossible to keep my software up to date. It avoids admin rights and installs software in a user-writable location /opt/homebrew/
    git # This freeware allows version control of software.
    sqlite # sqlite.org I need sqlite because it is used in many pieces of ORD scientific software and is very useful in scripts.
    ```
How to use it:
`python3 freeware_auto_script.py applications.txt`

Your lan id and password will be promoted

License:
Usage of the works is permitted provided that this instrument is retained with the works,
so that any entity that uses the works is notified of this instrument. DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.
