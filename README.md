# Script guide

<br></br>

## Links
[robotlist google sheet link](https://docs.google.com/spreadsheets/d/1wSNBCjC6I3twhZVhVms0_wFmmLdCzZ8RfLsMjE_xqxU/edit#gid=1221195598)

<br></br>

## Before you start
* All the relevant scripts are located in the "..\V1-DASH-EXTRACTOR\scripts" folder
    * The extractor.py script will import constants.py and readCSV.py
    * The main script is extractor.py
* The only constants you need to modify to get the script working
    * Default path (your system path leading to the /V1-DASH-EXTRACTOR folder)
    * All region sites (currently there are four regions sites, to add more regions simply modify the regions in the constantsly.py file)
    * Username
    * Password
    * Timeout seconds (this determines how long the script will wait at certain steps before it shuts down, because sometimes the website is laggy and it may take a few minutes for the page to display)
* The script need to be manually ran
    * Alternatively, you can use Windows Task Scheduler to run the executable version made by pyinstaller on a daily basis but I do no have admin access so I did not test it out
    * Or some script running website can be used which will execute the script daily
* The script supports region adding, meaning if theres a new region called Oceania you will only have to modify the regions related constants in constants.py

<br></br>

## **Script Operation**
1. extractor.py will first get the list of Company List.csv, Robot List.csv and Worksite List.csv from the V1 dashboard site for all the regions listed inside constants.py using the companies_list(), robots_list() and worksites_list() function. These 3 functions are grouped into the main_script() function (This operation is done in extractor.py).
2. After that, it will process all of them by joining the all CSVs for each region and put them into the "..\final CSV uncombined" folder using the process_region_CSV() function (This operation is done completely in the read_CSV.py).
3. After obtaining all uncombined CSVs for all regions located in the "..\final CSV uncombined" folder, a merge function called merge_CSV() inside read_CSV.py will execute to combine all regions' CSV into one single CSV by appending them one after another (This operation is done in the read_CSV.py).
4. After merging into one finalized csv, it will be moved to "..\downloaded CSV\final CSV" folder (This operation is done in read_CSV.py)
5. The export_CSV_to_GS() function inside readCSV.py will then upload the files to the google sheet. The client_secret.json inside "..\V1-DASH-EXTRACTOR\miscellaneous" folder will be responsible for linking to the google sheet used. If different Google account is used, the .json file will be different. For specifics on how to be used with different accounts, refer to Instructions.md Section 12

<br></br>

## **To build an executable(exe) version of the script**
* Ignore extractor.spec and build folder inside "..\V1-DASH-EXTRACTOR\scripts" folder. These files are used to added when running pyinstaller, th


ey are not crucial to using the executable version of the script. Only dist folder is important.
* To build your own executable, first install pyinstaller using
    ```python
    pip install pyinstaller
    ```
* Then change your directory in your code editor's terminal to where the extractor.py script is. Type in
    ```python
    pyinstaller extractor.py
    ```
* This will build a 'build' and 'dist' folder. Inside these folders contain an exe version of the script. Simply move them to the desktop for ease of execution.
* Quick build command
    ```python
    pyinstaller 
    ```


<br></br>

## To quickly install all the packages required for this script:
- Change directory to the folder where requirements.txt is (which is in ../V1-DASH-EXTRACTOR in this case)
- Run:
  ```python
  # Install all required packages from requirements.txt
  py -m pip install -r requirements.txt
  ```