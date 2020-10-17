# WebPlots
# WebPlots
__WebPlots__ can help anyone see and understand their data :chart_with_upwards_trend:
________________________________________________________________________________________
Upload, explore and analize your data using advanced charts and tabs

![Image](https://github.com/Kostr0min/WebPlots/blob/master/github_images/webplots_main.png)

## **Progress**

<img align="right" width="470" height="350" src="https://github.com/Kostr0min/WebPlots/blob/master/github_images/webplots_main_1.png">

:white_check_mark: Dash-form app   
:white_check_mark: Data loader   
:white_check_mark: Several charts :chart_with_upwards_trend::bar_chart::chart_with_downwards_trend:    
:white_check_mark: Descriptive statistics :clipboard:    
:white_check_mark: Selection by columns and data slice :hocho:   
:white_check_mark: Session keeper:guard: (collect all user settings and save in the database :open_file_folder:)  
:white_check_mark: Session loader   
:black_square_button: User authorization  
:black_square_button: More source (add users databases connection)  
:black_square_button: Statistical tests support  
:black_square_button: More charts  
:black_square_button: Tools for time-series 

## **Folder description**

 - webplots.py main app code with all callbacks
 - layout.py provide dash layout using get_layout() method
 - modules.py plotly graph modules
 - dbmodules.py database connection methods
 - tables.py functions for collect data for html.Table
 - exmpl.csv use this data to review WebPlots

## **Deploy with Docker**
<img align="right" width="300" height="300" src="https://github.com/Kostr0min/WebPlots/blob/master/github_images/webplots_dropout.png">

Requirements:
 - Docker
 - Docker-compose
 - uWSGI

Folder with webplots -> your_path  
Use terminal and go to your path -> cd /home/username/your_path  
Be sure that port for Docker app (Dockerfile -> EXPOSE: port) is free  
Build the container $docker-compose build  
And run application $docker-compose up  

Be aware that docker containers are configured with the local MySQL server in mind. If you want to use MySQL docker container uncomment code in docker-compose.yml and clear line 9: network_mode: "host" and configure Docker volume for data. (I advice to use mysql-connector-python instead of SQLAlchemy)

## **Testing**

Requirements:
 - Main tool for testing this app is the dash.testing
 - Selenium
 - Webdriver (for Chrome, Firefox, etc.)
 A few installation tips for ChromeDriver:
 First, you need to download the chromedriver file for Chromium (https://sites.google.com/a/chromium.org/chromedriver/home).
 Add this file to your PATH (like: export PATH="/home/user/driver_path/:$PATH"). And now type --webdriver Chrome parametr for pytest: $pytest --webdriver Chrome tests.py



## **Session keeper**

To save your configuration press the save button and copy your code.  
If you want to restore all settings just insert your code in whitespace in the top of load button and press this button.  

![Image](https://github.com/Kostr0min/WebPlots/blob/master/github_images/webplots_sessioncode.png)
