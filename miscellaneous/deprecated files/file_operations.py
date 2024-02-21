# DEPRECATED
# This script is to remove files inside the V1-DASH-EXTRACTOR folder
# Can be further customized according to needs
import fnmatch
import glob
import os
from pathlib import Path
import constants as cst
from send2trash import send2trash


def clear_raw_CSV(path, region=str):
    os.chdir(path)
    clean_start_list = ('Robot','Company','Worksite')
    try:
        for filename in os.listdir(path):
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
        print('clear_raw_CSV() error')


def clear_previous_raw_CSV(path):
    os.chdir(path)
    clean_start_list = ('Robot','Company','Worksite')
    try:
        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                print(filename + " " +"will be removed")
                # os.remove(filename)
                send2trash(filename)
    except:
        print('clear_previous_raw_CSV() error')


def clear_unsorted_CSV(path):
    os.chdir(path)
    try:
        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                print(filename + " " +"will be removed")
                # os.remove(filename)
                send2trash(filename)
    except:
        print('clear_unsorted_CSV() error')


def clear_sorted_CSV(path):
    os.chdir(path)
    try:
        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                print(filename + " " +"will be removed")
                # os.remove(filename)           
                send2trash(filename) 
    except:
        print('clear_sorted_CSV error')      


def clear_final_uncombined_CSV(path):
    os.chdir(path)
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            print(filename + " " +"will be removed")
            # os.remove(filename)  
            send2trash(filename)   


def clear_final_CSV(path):
    os.chdir(path)
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            print(filename + " " +"will be removed")
            # os.remove(filename)          
            send2trash(filename)


def full_clear_CSV(path):
    clear_previous_raw_CSV()
    clear_unsorted_CSV()
    clear_sorted_CSV()
    # clearTestingCSV()   
    clear_final_uncombined_CSV()


def absolute_clear_CSV():
    clear_raw_CSV()
    clear_unsorted_CSV()
    clear_sorted_CSV()
    # clearTestingCSV()   
    clear_final_uncombined_CSV()
    # clear_final_CSV() 


def custom_clear_CSV():
    # clear_raw_CSV()
    clear_unsorted_CSV()
    clear_sorted_CSV()
    # clearTestingCSV()   


if __name__ == "__main__":
    pass
    # clear_raw_CSV()
    # clear_unsorted_CSV()
    # clear_sorted_CSV()
    # # clearTestingCSV()
    # clear_final_uncombined_CSV()
    # full_clear_CSV()
    # custom_clear_CSV()
    # absolute_clear_CSV()