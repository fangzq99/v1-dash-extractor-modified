# This script adds Company List.csv, Robot List.csv and Worksite List.csv to the "..\\downloaded CSV" folder for testing purposes

import shutil

shutil.copy2(r'C:\Users\intern10\Desktop\projects\v1-dash-extractor\scripts\troubleshooting files\auRobotListREFERENCE\Company List.csv',r'C:\Users\intern10\Desktop\projects\v1-dash-extractor\downloaded CSV\Company List.csv')
shutil.copy2(r'C:\Users\intern10\Desktop\projects\v1-dash-extractor\scripts\troubleshooting files\auRobotListREFERENCE\Robot List.csv',r'C:\Users\intern10\Desktop\projects\v1-dash-extractor\downloaded CSV\Robot List.csv')
shutil.copy2(r'C:\Users\intern10\Desktop\projects\v1-dash-extractor\scripts\troubleshooting files\auRobotListREFERENCE\Worksite List.csv',r'C:\Users\intern10\Desktop\projects\v1-dash-extractor\downloaded CSV\Worksite List.csv')
print('Raw AU csv added!')