# General setup for Selenium script

# press ctrl+shift+v to launch MR file in VSC
# To run script, first open cmd and type:
```python
pip install webdriver-manager
pip install selenium
pip install pandas
pip install ipython
pip install oauth2client
pip install gspread
```

#####

## 1. Webdriver
### 1.1 *Deprecated way (GUI)*
#### 1.1.1 service
* DRIVER_PATH = r'C:\Users\intern10\Desktop\chromedriver_win32\chromedriver.exe'  # Either add r in front of the double quotation marks ot use doule slash(e.g. "C:\\Users...")
* driver = webdriver.Chrome(executable_path=DRIVER_PATH)  # Alternative way of declaring: driver = webdriver.Chrome(executable_path=r'C:\Users\intern10\Desktop\chromedriver_win32\chromedriver.exe')
#### 1.1.2 options
* * driver = webdriver.Chrome(...chrome_options=opts...)

### 1.2 *Updated way (GUI)*
#### 1.2.1 service
* driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=[options variable name])
#### 1.2.2 options
* driver = webdriver.Chrome(...options=opts...)

### 1.3 *Headless mode*
```python
DRIVER_PATH = Service(r'C:\Users\intern10\Desktop\chromedriver_win32\chromedriver.exe')  # Either add r in front of the double quotation marks ot use doule slash(e.g. "C:\\Users...")
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=DRIVER_PATH)  # Alternative way of declaring: driver = webdriver.Chrome(executable_path=r'C:\Users\intern10\Desktop\chromedriver_win32\chromedriver.exe')
driver.get('https://google.com')    # Similar to driver.navigate().to('https://google.com') 
```

### 1.4 *GUI mode*
```python
DRIVER_PATH = Service(r'C:\Users\intern10\Desktop\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(service=DRIVER_PATH)  # DRIVER_PATH can be changed to other names
driver.get('https://google.com')    # Similar to driver.navigate().to('https://google.com') 
```

### 1.5 *If chromedriver is not installed*
```python
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# instead of
driver = webdriver.Chrome(service=r'C:\Users\intern10\Desktop\chromedriver_win32\chromedriver.exe')
```


## 2. Testing (exceptions)
```python
from selenium.common.exceptions import (...)
```
1. ConnectionClosedException: This exception takes place when there is a disconnection in the driver.

2. ElementClickInterceptedException: The command could not be completed as the element receiving the events is concealing the element which was requested clicked.

3. ElementNotInteractableException: This Selenium exception is thrown when an element is presented in the DOM but it is impossible to interact with such element.

4. ElementNotSelectableException: This Selenium exception is thrown when an element is presented in the DOM but is unavailable for selection. Hence, it is impossible to interact with.

5. ElementNotVisibleException: This type of Selenium exception takes place when an existing element in DOM has a feature set as hidden. In this situation, elements are there, but you can not see and interact with the WebDriver.

6. ErrorHandler.UnknownServerException: Exception is used as a placeholder if the server returns an error without a stack trace.

7. ErrorInResponseException: This exception is thrown when a fault has occurred on the server-side. You can see it happens when interacting with the Firefox extension or the remote driver server.

8. ImeActivationFailedException: This exception occurs when IME engine activation has failed.

9. ImeNotAvailableException: This exception takes place when IME support is unavailable.

10. InsecureCertificateException: Navigation made the user agent to hit a certificate warning, which is caused by an invalid or expired TLS certificate.

11. InvalidArgumentException: This Selenium exception is thrown if an argument does not belong to the expected type.

12. InvalidCookieDomainException: This happens when you try to add a cookie under a different domain rather than the current URL.

13. InvalidCoordinatesException: This happens if the coordinates offered to an interacting operation are not valid.

14. InvalidElementStateException: This Selenium exception occurs if a command cannot be finished as the element is invalid.

15. InvalidSessionIdException: Takes place when the given session ID is not included in the list of active sessions, which means the session does not exist or is inactive either.

16. InvalidSwitchToTargetException: Happens if the frame or window target to be switched does not exist.

17. JavascriptException: This problem happens when executing JavaScript supplied by the user.

18. JsonException: Happens when you afford to get the session capabilities where the session is not created.

19. MoveTargetOutOfBoundsException: Takes place if the target provided to the ActionChains move() methodology is not valid. For example: out of the document.

20. NoAlertPresentException: Happens when you switch to no presented alert.

21. NoSuchAttributeException: Occurs when the attribute of the element could not be found.

22. NoSuchContextException: Happens in mobile device testing and is thrown by ContextAware.

23. NoSuchCookieException: This exception is thrown if there is no cookie matching with the given path name found amongst the associated cookies of the current browsing context’s active document.

24. NoSuchElementException: Happens if an element could not be found.

25. NoSuchFrameException: Takes place if frame target to be switch does not exist.

26. NoSuchWindowException: Occurs if window target to be switched does not exist.

27. NotFoundException: This exception is a subclass of WebDriverException. It happens when an element on the DOM does not exist.

28. RemoteDriverServerException: This Selenium exception is thrown when the server does not respond due to the problem that the capabilities described are not proper.

29. ScreenshotException: It is impossible to capture a screen.

30. ScriptTimeoutException: Thrown when executeAsyncScript takes more time than the given time limit to return the value.

31. SessionNotCreatedException: A new session could not be successfully created.

32. SessionNotFoundException: The WebDriver is performing the action right after you quit the browser.

33. StaleElementReferenceException: This Selenium exception happens if the web element is detached from the current DOM.

34. TimeoutException: Thrown when there is not enough time for a command to be completed.

35. UnableToCreateProfileException: You can open a browser with certain options using profiles, but sometimes a new version of the Selenium driver server or browser may not support the profiles.

36. UnableToSetCookieException: Occurs if a driver is unable to set a cookie.

37. UnexpectedAlertPresentException: This Selenium exception happens when there is the appearance of an unexpected alert.

38. UnexpectedTagNameException: Happens if a support class did not get a web element as expected.

39. UnhandledAlertException: It happens when there is an alert, but WebDriver is unable to perform Alert operation.

40. UnknownMethodException: Thrown when the requested command matches with a known URL but not matching with a methodology for that URL.

41. UnreachableBrowserException: This Selenium exception happens if the browser is unable to be opened or has crashed because of some reasons.

42. UnsupportedCommandException: Occurs when remote WebDriver does not send valid commands as expected.

43. WebDriverException: This takes place when the WebDriver is performing the action right after you close the browser.

## 3. CSS selector strategies
* **id** 
    * either: # OR id=
* **class** 
    * either: . OR class=
* **input** 
    * either: = OR input[...][...]
* **button**
    * button[...][...]

## 4. Scrolll into view
* **Method 1**
```python
companies1000 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div/div/table/tfoot/tr/td/div/div[2]/div")))
driver.execute_script("arguments[0].scrollIntoView(true);", companies1000)
```
* **Method 2**
```python
companies1000 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div/div/table/tfoot/tr/td/div/div[2]/div")))
actions = ActionChains(driver)
actions.move_to_element(companies1000).perform()
```
** Key thing to note: Must use explicit/implicit wait for finding elements if not the action will fail as the script cannot immediately identify where the element is

## 5.  Notifications
### 5.1 Alerts
* https://www.techbeamers.com/handle-alert-popup-selenium-python/
### 5.2 Notifications
```python
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
```
* https://stackoverflow.com/questions/41400934/handle-notifications-in-python-selenium-chrome-webdriver


## 6.   Rename file (python)
* https://pynative.com/python-rename-file/
* https://stackoverflow.com/questions/5218261/python-how-to-rename-a-text-file-with-datetime
```python

```


## 7.   Directories (python)
* https://realpython.com/working-with-files-in-python/
* https://stackoverflow.com/questions/8858008/how-to-move-a-file-in-python


## 8.   Filtering unnamed column methods
* https://www.datasciencelearner.com/drop-unnamed-column-pandas/#:~:text=An%20unnamed%20column%20in%20pandas,in%20analyzing%20the%20data%20efficiently.


## 9.   Drop columns with specific string in columns
```python
df = df.drop(df.filter(regex='Test').columns, axis=1)
```
* https://stackoverflow.com/questions/19071199/drop-columns-whose-name-contains-a-specific-string-from-pandas-dataframe


## 10.  Remove all rows containing specific text in the column
* https://www.geeksforgeeks.org/how-to-drop-rows-that-contain-a-specific-string-in-pandas/


## 11.  Combine CSVs/excels/(anything)/...
* https://github.com/ekapope/Combine-CSV-files-in-the-folder/blob/master/Combine_CSVs.py


## 12. Upload to Google Sheets
* https://medium.com/craftsmenltd/from-csv-to-google-sheet-using-python-ef097cb014f9
```python
# Change to wherever you stored your client_secret.json 
os.chdir(Path(str(cst.DEFAULT_PATH)+"\\V1-DASH-EXTRACTOR"))
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('robotlist')

os.chdir(cst.FINAL_CSV_PATH)
with open('finalized_list.csv', 'r') as file_obj:
    content = file_obj.read()
    client.import_csv(spreadsheet.id, data=content)
```


## 13.  Long Click
```python
actions.click_and_hold(updateOkayButton).perform()
sleep(2)
actions.release(updateOkayButton).perform()
```