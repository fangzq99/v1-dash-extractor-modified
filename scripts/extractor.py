# This script is to extract data from v1 dashboard
from itertools import count
import os
from pathlib import Path
import sys
from time import sleep
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import *
# from IPython.display import display # Comment out this module if it causes errors
import read_CSV
from constants import REGIONS, DEFAULT_TIMEOOUT
from send2trash import send2trash


# INITIALIZE PROGRAM ENVIRONMENT
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    app_path = os.path.dirname(sys.executable)
    exec_path = sys.executable
    
    execution_method = 'executable'
    
    # ./extractor-resources
    main_folder_path = Path(os.path.join(app_path,'extractor-resources'))
    # ./extractor-resources/downloaded CSV
    downloaded_csv_path = Path(os.path.join(main_folder_path,'downloaded CSV'))
    # ./extractor-resources/downloaded CSV/final CSV
    final_csv_path = Path(os.path.join(downloaded_csv_path,'final CSV'))
    # ./extractor-resources/downloaded CSV/final CSVs uncombined
    final_csv_uncombined_path = Path(os.path.join(downloaded_csv_path,'final CSVs uncombined'))
    # ./extractor-resources/downloaded CSV/sorted CSV
    sorted_csv_path = Path(os.path.join(downloaded_csv_path,'sorted CSV'))
    # ./extractor-resources/downloaded CSV/unsorted CSV
    unsorted_csv_path = Path(os.path.join(downloaded_csv_path,'unsorted CSV'))
    
    if os.path.exists(main_folder_path):
        print('Base resources directory exists\n')
    else:
        print('No base resources directory found, now creating one with all its sub directory\n')
        os.makedirs(final_csv_path)
        os.makedirs(final_csv_uncombined_path)
        os.makedirs(sorted_csv_path)
        os.makedirs(unsorted_csv_path)
        
    if not os.path.exists(sorted_csv_path):
        print('sorted CSV directory do not exist, creating one now')
        os.makedirs(sorted_csv_path)
    if not os.path.exists(final_csv_uncombined_path):
        print('final CSVs uncombined directory do not exist, creating one now')
        os.makedirs(final_csv_uncombined_path)
    if not os.path.exists(final_csv_path):
        print('final CSV directory do not exist, creating one now')
        os.makedirs(final_csv_path)
    if not os.path.exists(downloaded_csv_path):
        print('downloaded CSV directory do not exist, creating one now')
        os.makedirs(downloaded_csv_path)
    if not os.path.exists(unsorted_csv_path):
        print('unsorted CSV directory do not exist, creating one now')
        os.makedirs(unsorted_csv_path)
    prefs = {'download.default_directory' : str(downloaded_csv_path)}
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
    # exec_path = "extractor.py"
    
    execution_method = 'script'
    
    # ./extractor-resources
    main_folder_path = Path(os.path.join(app_path,'extractor-resources'))
    # ./extractor-resources/downloaded CSV
    downloaded_csv_path = Path(os.path.join(main_folder_path,'downloaded CSV'))
    # ./extractor-resources/downloaded CSV/final CSV
    final_csv_path = Path(os.path.join(downloaded_csv_path,'final CSV'))
    # ./extractor-resources/downloaded CSV/final CSVs uncombined
    final_csv_uncombined_path = Path(os.path.join(downloaded_csv_path,'final CSVs uncombined'))
    # ./extractor-resources/downloaded CSV/sorted CSV
    sorted_csv_path = Path(os.path.join(downloaded_csv_path,'sorted CSV'))
    # ./extractor-resources/downloaded CSV/unsorted CSV
    unsorted_csv_path = Path(os.path.join(downloaded_csv_path,'unsorted CSV'))
    
    if os.path.exists(main_folder_path):
        print('Base resources directory exists\n')
    else:
        print('No base resources directory found, now creating one with all its sub directory\n')
        os.makedirs(final_csv_path)
        os.makedirs(final_csv_uncombined_path)
        os.makedirs(sorted_csv_path)
        os.makedirs(unsorted_csv_path)
        
    if not os.path.exists(sorted_csv_path):
        print('sorted CSV directory do not exist, creating one now')
        os.makedirs(sorted_csv_path)
    if not os.path.exists(final_csv_uncombined_path):
        print('final CSVs uncombined directory do not exist, creating one now')
        os.makedirs(final_csv_uncombined_path)
    if not os.path.exists(final_csv_path):
        print('final CSV directory do not exist, creating one now')
        os.makedirs(final_csv_path)
    if not os.path.exists(downloaded_csv_path):
        print('downloaded CSV directory do not exist, creating one now')
        os.makedirs(downloaded_csv_path)
    if not os.path.exists(unsorted_csv_path):
        print('unsorted CSV directory do not exist, creating one now')
        os.makedirs(unsorted_csv_path)
    prefs = {'download.default_directory' : str(downloaded_csv_path)}
    


# NOTE: Do not delete this in the event the updateOkayButton part in companies_list function fail
# Very buggy update notification's ok button
def updateButtonClick():
    sleep(DEFAULT_TIMEOOUT)
    newUpdatesVisible = WebDriverWait(driver, DEFAULT_TIMEOOUT).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[3]/div/span/div/div/div/div[1]')))
    updateOkayButton = WebDriverWait(driver, DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/span/div/div/div/span[2]/button'))).click()


def clear_csv(paths=list(), use_custom_paths=False, raw=False, sorted=False, unsorted=False, final_uncombined=False, final=False, region=None):
    pattern = "*.csv"
    if use_custom_paths:
        for path in paths:
            os.chdir(path)
            if raw:
                try:
                    for filename in os.listdir(downloaded_csv_path):
                        if filename.endswith('.csv'):
                            if region != None:
                                print(region+"'s "+filename + " " +"will be removed")
                                # os.remove(filename)
                                send2trash(filename)
                            else:
                                print(filename + " " +"will be removed")
                                # os.remove(filename)
                                send2trash(filename)
                except:
                    print('Error while clearing raw CSVs')
            if sorted:
                try:
                    for filename in os.listdir(sorted_csv_path):
                        if filename.endswith('.csv'):
                            print(filename + " " +"will be removed")
                            # os.remove(filename)           
                            send2trash(filename) 
                except:
                    print('Error while clearing sorted CSVs')
            if unsorted:
                try:
                    for filename in os.listdir(unsorted_csv_path):
                        if filename.endswith('.csv'):
                            print(filename + " " +"will be removed")
                            # os.remove(filename)
                            send2trash(filename)
                except:
                    print('Error while clearing unsorted CSVs')
            if final_uncombined:
                try:
                    for filename in os.listdir(final_csv_uncombined_path):
                        if filename.endswith('.csv'):
                            print(filename + " " +"will be removed")
                            # os.remove(filename)  
                            send2trash(filename)   
                except:
                    print('Error while clearing final_uncombined CSVs')
            if final:
                try:
                    for filename in os.listdir(final_csv_path):
                        if filename.endswith('.csv'):
                            print(filename + " " +"will be removed")
                            # os.remove(filename)          
                            send2trash(filename)
                except:
                    print('Error while clearing final CSVs')
        print("Finish clearing the CSVs")
    else:
        if raw:
            try:
                os.chdir(downloaded_csv_path)
                for filename in os.listdir(downloaded_csv_path):
                    if filename.endswith('.csv'):
                        if region != None:
                            print(region+"'s "+filename + " " +"will be removed")
                            # os.remove(filename)
                            send2trash(filename)
                        else:
                            print(filename + " " +"will be removed")
                            # os.remove(filename)
                            send2trash(filename)
            except:
                print('Error while clearing raw CSVs')
                print(traceback.format_exc())
        if sorted:
            try:
                os.chdir(sorted_csv_path)
                for filename in os.listdir(sorted_csv_path):
                    if filename.endswith('.csv'):
                        print(filename + " " +"will be removed")
                        # os.remove(filename)           
                        send2trash(filename) 
            except:
                print('Error while clearing sorted CSVs')
                print(traceback.format_exc())
        if unsorted:
            try:
                os.chdir(unsorted_csv_path)
                for filename in os.listdir(unsorted_csv_path):
                    if filename.endswith('.csv'):
                        print(filename + " " +"will be removed")
                        # os.remove(filename)
                        send2trash(filename)
            except:
                print('Error while clearing unsorted CSVs')
                print(traceback.format_exc())
        if final_uncombined:
            try:
                os.chdir(final_csv_uncombined_path)
                for filename in os.listdir(final_csv_uncombined_path):
                    if filename.endswith('.csv'):
                        print(filename + " " +"will be removed")
                        # os.remove(filename)  
                        send2trash(filename)   
            except:
                print('Error while clearing final_uncombined CSVs')
                print(traceback.format_exc())
        if final:
            try:
                os.chdir(final_csv_path)
                for filename in os.listdir(final_csv_path):
                    if filename.endswith('.csv'):
                        print(filename + " " +"will be removed")
                        # os.remove(filename)          
                        send2trash(filename)
            except:
                print('Error while clearing final CSVs')
                print(traceback.format_exc())
        print("Finish clearing the CSVs")


# Obtain companies list CSV
def companies_list(current_region):
    try:
        temp=None
        while temp is None:
            try:    # This chunk of code was hacked together and is a mess, but the script still works so i did not refactor it
                updateOkayButton = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/span/div/div/div/span[2]/button')))
                updateOkayButton.click()
                try:
                    confirmUpdateSuccess = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/section/section/main/div/div/div/div/div[1]/div[3]/div/div/div/div[1]'))) # Retry login every DEFAULT_TIMEOOUT seconds
                    # print('Managed to click update button successfully!')
                    print(current_region+" log in success!")
                    break
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:   
                    print('Will retry clicking again...')
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except TimeoutException:
                print('Seems like the update button is gone for some reason...script will continue as per normal')
                temp = 1
                pass
            except NoSuchElementException:
                print('where?')
            except:
                print('Error occured while trying to log in...')
                # driver.quit()
                raise Exception('Restarting script')

        # Menu page select companies list
        try: 
            companyList = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#root > section > aside > div > ul > li:nth-child(2)'))).click()
            sleep(1)
            viewCompanies = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/aside/div/ul/li[1]/ul/li[1]/a'))).click()
            sleep(1)
        except NoSuchElementException:
            print("Cannot click view companies list...")
            raise Exception("Cannot click view companies list...")
        

        # Scroll to bottom to find the view list dropdown menu and click it
        companies1000 = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div/div/table/tfoot/tr/td/div/div[2]/div")))
        actions.move_to_element(companies1000).perform()
        companies1000.click()

        # Click 1000 for the drop down menu
        list1000 = driver.find_element(By.CSS_SELECTOR,'#menu- > div.MuiPaper-root.MuiMenu-paper.MuiPopover-paper.MuiPaper-elevation8.MuiPaper-rounded > ul > li:nth-child(7)').click()

        # Scroll up and click the download icon
        try:
            downloadIcon = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/section/main/div/div[2]/div/div/div/div/div/div[1]/div[4]/div/div/span[2]/button')))
            actions.move_to_element(downloadIcon).perform()
            downloadIcon.click()
        except NoSuchElementException:
            print("Cannot click on the download icon/Cannot scroll to the download icon!\nExiting script...")
            raise Exception("Cannot click on the download icon/Cannot scroll to the download icon!\nExiting script...")

        # Click the "Export as CSV" button
        try:
            exportCompanyListCSV = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'Export as CSV')]"))).click()
            print("Successfully downloaded " + current_region + " Companies List!")
        except NoSuchElementException:
            print("Failed to download CSV...")
            raise Exception("Failed to download CSV...")
    except KeyboardInterrupt:
        raise KeyboardInterrupt
        

# Obtain robots list CSV
def robots_list(current_region):
    try:
        # Menu page select robots list
        try: 
            robotList = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#root > section > aside > div > ul > li:nth-child(4) > div.ant-menu-submenu-title'))).click()
            sleep(1)
            viewRobots = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="robots$Menu"]/li[1]/a'))).click()
            sleep(1)
        except NoSuchElementException:
            print("Cannot click view robots list...")
            raise Exception("Cannot click view robots list...")

        # Scroll to bottom to find the view list dropdown menu and click it
        companies1000 = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div/div/table/tfoot/tr/td/div/div[2]/div')))
        actions.move_to_element(companies1000).perform()
        companies1000.click()

        # Click 1000 for the drop down menu
        list1000 = driver.find_element(By.CSS_SELECTOR,'#menu- > div.MuiPaper-root.MuiMenu-paper.MuiPopover-paper.MuiPaper-elevation8.MuiPaper-rounded > ul > li:nth-child(7)').click()

        # Scroll up and click the download icon
        try:
            downloadIcon = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/section/main/div/div[2]/div/div/div/div/div/div[1]/div[4]/div/div/span[2]/button')))
            actions.move_to_element(downloadIcon).perform()
            downloadIcon.click()
        except NoSuchElementException:
            print('Cannot click on the download icon/Cannot scroll to the download icon!Exiting script...')
            raise Exception("Cannot click on the download icon/Cannot scroll to the download icon!Exiting script...")

        # Click the "Export as CSV" button
        try:
            exportCompanyListCSV = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div.MuiPopover-root > div.MuiPaper-root.MuiMenu-paper.MuiPopover-paper.MuiPaper-elevation8.MuiPaper-rounded > ul > li'))).click()
            print("Successfully downloaded " + current_region + " Robots List!")    
        except NoSuchElementException:
            print("Failed to download CSV!Exiting script...")
            raise Exception("Failed to download CSV!Exiting script...")
    except KeyboardInterrupt:
        raise KeyboardInterrupt
        

# Obtain worksites list CSV
def worksites_list(current_region):
    try:
        # Menu page select view worksites
        try: 
            worksiteList = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/aside/div/ul/li[5]/div'))).click()
            sleep(1)
            viewWorksites = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="worksite_managements$Menu"]/li[1]'))).click()
            sleep(1)
        except NoSuchElementException:
            print('Cannot click view worksite management list!Exiting script...')
            raise Exception("Cannot click view worksite management list!Exiting script...")
        
        sleep(1)

        # Scroll to bottom to find the view list dropdown menu and click it
        worksites1000 = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div/div/table/tfoot/tr/td/div/div[2]/div')))
        actions.move_to_element(worksites1000).perform()
        worksites1000.click()

        # Click 1000 for the drop down menu
        list1000 = driver.find_element(By.CSS_SELECTOR,'#menu- > div.MuiPaper-root.MuiMenu-paper.MuiPopover-paper.MuiPaper-elevation8.MuiPaper-rounded > ul > li:nth-child(7)').click()

        # Scroll up and click the download icon
        try:
            downloadIcon = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/section/main/div/div[2]/div/div/div/div/div/div[1]/div[4]/div/div/span[2]/button')))
            actions.move_to_element(downloadIcon).perform()
            downloadIcon.click()
        except NoSuchElementException:
            print('Cannot click on the download icon/Cannot scroll to the download icon!Exiting script...')
            raise Exception("Cannot click on the download icon/Cannot scroll to the download icon!Exiting script...")

        # Click the "Export as CSV" button
        try:
            exportCompanyListCSV = WebDriverWait(driver,DEFAULT_TIMEOOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div.MuiPopover-root > div.MuiPaper-root.MuiMenu-paper.MuiPopover-paper.MuiPaper-elevation8.MuiPaper-rounded > ul > li'))).click()
            print("Successfully downloaded " + current_region + " Worksite List!")
        except NoSuchElementException:
            print("Failed to download CSV!Exiting script...")
            raise Exception("Failed to download CSV!Exiting script...")
    except KeyboardInterrupt:
        raise KeyboardInterrupt


# Main test
def main_script(current_region):
    try:
        companies_list(current_region)
        robots_list(current_region)
        worksites_list(current_region)   
    # Throw keyboard interrupt exception to the main loop.
    # The reason why there is no command like print performed here
    # is that any command here will be performed on top of the 
    # main loop's keyboard interrupt exception.
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    
    
def resource_path():
    if hasattr(sys, '_MEIPASS'):
        pre_bundled_data_path = os.path.join(sys._MEIPASS, 'client_secret.json')
        if os.path.exists(pre_bundled_data_path):
            print("Obtaining the client_secrets.json from the pre-bundled data")
            return pre_bundled_data_path
        else:
            print("Obtaining the client_secrets.json from the file in the folder together with the exe")
            return os.path.join(app_path, 'client_secret.json')
    else:
        print("Obtaining the client_secrets.json from the file in the folder")
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client_secret.json')


if __name__ == "__main__":
    tries_count = 0
    client_secrets_path = resource_path()
    print(f'The client secrets file is located at {client_secrets_path}')
    if execution_method == 'executable':
        print('\nThe program is running as an executable')
        print(f'The current location of the executable is: {app_path}\n')
    elif execution_method == 'script':
        print('\nThe program is running in a script')
        print(f'The current location of the script is: {app_path}\n')
            
    # Driver Settings: GUI mode 
    # DRIVER_PATH = Service(executable_path=r'C:\Users\intern10\Desktop\projects\v1-dash-extractor\miscellaneous\chromedriver\chromedriver.exe') # Work path
    # prefs = {'download.default_directory' : str(DEFAULT_PATH)+"\\v1-dash-extractor\\downloaded CSV"}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless=chrome')    # NOTE: Disable this if you wish to use the GUI mode
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--disable-notifications')    # Disables notifications...but never actually tested it oout
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    program_start_time = time.perf_counter()    # Calculate program run time
    
    os.chdir(downloaded_csv_path)  # Change directory to ../downloaded CSV

    while tries_count < 3:
        try:
            # Initializing webdriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
            # driver = webdriver.Chrome(service=DRIVER_PATH,options=chrome_options)  # DRIVER_PATH can be changed to other names
            print(f'The current browser is {driver.capabilities["browserName"]} and its version is {driver.capabilities["browserVersion"]} ')
            print(f'The current chromedriver version is {driver.capabilities["chrome"]["chromedriverVersion"].split(" ")[0]} \n')
            actions = ActionChains(driver)
            click = ActionChains(driver)
            driver.maximize_window()

            # Clearing folders to ensure clean start
            print('Clearing Raw, Sorted, Unsorted, finalUncombined CSVs:')
            clear_csv(sorted=True, final_uncombined=True, raw=True, unsorted=True)
            
            # Loop through all existing regions in the constants file to get each region's final list
            for region_count,region_name in enumerate(REGIONS):
                # Go to the region's website
                driver.get(REGIONS[region_name]['site'])
                
                # Enter the user's particulars for the specific region
                # Enter username
                username_input_box = WebDriverWait(driver, DEFAULT_TIMEOOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR,'[name="username"]')))
                username_input_box.send_keys(REGIONS[region_name]['account'])
                # Enter password
                password_input_box = driver.find_element(By.CSS_SELECTOR,'[name="password"]')
                password_input_box.send_keys(REGIONS[region_name]['password'])
                # Check the agree terms... checkbox
                agree_terms_checkbox = driver.find_element(By.CSS_SELECTOR,'[class="ant-checkbox-input"]')
                agree_terms_checkbox.click()
                # Click login button
                login_button = driver.find_element(By.CSS_SELECTOR,'[type="submit"]')
                login_button.click()
                
                # Main script
                main_script(region_name)
                print("Processing the " + region_name + " final lists now...")
                sleep(2)

                # Process the current region's CSV into one big CSV through common columns
                read_CSV.process_region_CSV(region_name)
                sleep(1)

                # Base CSV clearing
                print(region_name + "'s RAW CSVs will be cleared:")
                # file_operations.clear_raw_CSV(region=region_name, path=downloaded_csv_path)
                clear_csv(raw=True, region=region_name)
                sleep(2)
                
                print("\n")

            # Combine the four finalized region's CSVs
            print('\nMerging the four REGIONS CSV!')
            read_CSV.merge_CSV()
            sleep(1)

            # Upload to GS
            print('\nExporting the final CSV to GS now!')
            read_CSV.export_CSV_to_GS(client_secrets_path)
            sleep(1)

            # Delete sorted and unsorted CSV
            clear_csv(sorted=True, unsorted=True)

            # Print program execution time
            print("\nThe execution of this script took %s seconds" % (time.perf_counter() - program_start_time))

            # Terminate the script
            print('Script completed! Exiting now...')
            driver.quit()
            break
        
        # Catch keyboard interrupt like ctrl+c or ctrl+z before other general exceptions
        except KeyboardInterrupt:
            print("Keyboard interrupt detected! Driver will quit!")
            driver.quit()
            sys.exit()
            
        # Catch all other types of exception like NoSuchElementException etc..
        except:
            # Increase the try count by 1 each time the script throws an exception
            tries_count+=1
            if tries_count == 3:
                print('Script retried 3 times and something is wrong...disable headless and check the script!')
                driver.quit()
            if tries_count < 3:
                print('Rerunning the script...try number: '+str(tries_count))
        
        

