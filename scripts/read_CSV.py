import datetime
import glob
import pathlib
import sys
import traceback
import pandas as pd
import numpy as np
import os
import shutil
import constants as cst
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from extractor import downloaded_csv_path, final_csv_path, final_csv_uncombined_path, main_folder_path, sorted_csv_path, unsorted_csv_path, app_path

final_filename = str
current_date = datetime.datetime.now()


def process_region_CSV(region):
    try:
        os.chdir(downloaded_csv_path)
        
        # Data preparation for Robot List
        pd.read_csv('Robot List.csv').drop('Robot Picture', axis=1).drop('Status', axis=1).drop('Last Online',axis=1).to_csv('unsorted_'+region+'RobotList.csv',index=False)
        pd.read_csv('unsorted_'+region+'RobotList.csv').sort_values(by=["Serial No"],ascending=True).to_csv('sorted_'+region+'RobotList.csv',index=False)
        read_sorted_RobotList = pd.read_csv('sorted_'+region+'RobotList.csv')

        # Data preparation for Company List
        pd.read_csv('Company List.csv').drop('Company Logo', axis=1).drop('Website', axis=1).drop('Email',axis=1).drop('Remarks',axis=1).to_csv('unsorted_'+region+'CompanyList.csv',index=False)
        read_unsorted_CompanyList = pd.read_csv('unsorted_'+region+'CompanyList.csv')

        # Data preparation for Worksite List
        pd.read_csv('Worksite List.csv').drop('Worksite Picture', axis=1).to_csv('unsorted_'+region+'WorksiteList.csv',index=False)
        read_unsorted_WorksiteList = pd.read_csv('unsorted_'+region+'WorksiteList.csv')

        # Move unsorted list to a new folder
        shutil.move(Path(str(downloaded_csv_path)+"/unsorted_"+region+"RobotList.csv"), Path(str(unsorted_csv_path)+"/unsorted_"+region+"RobotList.csv"))
        shutil.move(Path(str(downloaded_csv_path)+"/unsorted_"+region+"CompanyList.csv"), Path(str(unsorted_csv_path)+"/unsorted_"+region+"CompanyList.csv"))
        shutil.move(Path(str(downloaded_csv_path)+"/unsorted_"+region+"WorksiteList.csv"), Path(str(unsorted_csv_path)+"/unsorted_"+region+"WorksiteList.csv"))
        shutil.move(Path(str(downloaded_csv_path)+"/sorted_"+region+"RobotList.csv"), Path(str(sorted_csv_path)+"/sorted_"+region+"RobotList.csv"))

        # Combine data
        combine_RLandCL_old = pd.merge(read_sorted_RobotList, read_unsorted_CompanyList, left_on='Company Name', right_on='Company Name', how='left', suffixes=('','__unsorted'))
        combine_RLandCL = combine_RLandCL_old.drop(combine_RLandCL_old.filter(regex='__unsorted').columns, axis=1)
        combine_RLandCLandWL = pd.merge(combine_RLandCL, read_unsorted_WorksiteList, left_on='Worksite', right_on='Worksite Name', how='left', suffixes=('','__unsorted'))

        # Add region column
        combine_RLandCLandWL['Region'] = region

        # Final CSV uncombinedclean up move final to a new folder
        temp_filename = str("finalized_"+region+"_list")+str(" ")+str(current_date.day)+str("-")+str(current_date.month)+str("-")+str(current_date.year)
        finalized_list = combine_RLandCLandWL.drop(['Worksite Name','Operating Company','Street Address','Address Line 2','Unique Number'], axis=1).to_csv(str(temp_filename+'.csv'),index=False)
        shutil.move(Path(str(downloaded_csv_path)+'/'+str(temp_filename+'.csv')), Path(str(final_csv_uncombined_path)+'/'+str(temp_filename+'.csv')))

        # Display final CSV uncombined
        os.chdir(final_csv_uncombined_path)
        read_finalized_list = pd.read_csv(str(temp_filename+'.csv'))
        print(region+' final list created!')
    except:
        print("Error! Unable to process "+region+"'s CSV! Refer to process_region_CSV function for debugging!")
        print(traceback.format_exc())
        raise Exception("process_region_CSV function error!")


def merge_CSV():
    # find all csv files in the folder
    # use glob pattern matching -> extension = 'csv'
    # save result in list -> all_filenames
    try:
        os.chdir(final_csv_uncombined_path)
        extension = 'csv'
        all_uncombined_finalCSVs = [i for i in glob.glob('*.{}'.format(extension))]

        # Combine all files in the list
        final_csv = pd.concat([pd.read_csv(f) for f in all_uncombined_finalCSVs ])

        # Export to csv
        temp_filename = str("finalized_list")+str(" ")+str(current_date.day)+str("-")+str(current_date.month)+str("-")+str(current_date.year)
        final_csv.to_csv(str(temp_filename + '.csv'),index=False)
        final_filename = (temp_filename + ".csv")
        
        # Move to final_csv to final CSV folder
        shutil.move(Path(str(final_csv_uncombined_path)+'/'+final_filename), Path(str(final_csv_path)+'/'+final_filename))
    except:
        print("merge_CSV function error!")
        raise Exception("merge_CSV function error!")
    return final_filename


def export_CSV_to_GS(client_secrets_path):
    try:
        # Change to wherever you stored your client_secret.json 
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        os.chdir(Path(app_path))
        # credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        # credentials = ServiceAccountCredentials.from_json_keyfile_name(resource_path('client_secret.json'), scope)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secrets_path, scope)
        client = gspread.authorize(credentials)

        spreadsheet = client.open('robotlist')

        final_filename = merge_CSV()

        os.chdir(final_csv_path)
        with open(final_filename, 'rb') as file_obj:
            content = file_obj.read()
            client.import_csv(spreadsheet.id, data=content)
    except:
        print("export_CSV_to_GS function error!")
        raise Exception("export_CSV_to_GS function error!")

if __name__ == "__name__":
    pass

