### Author : Vishnu BKM

### This script downloads the Cash Market Bhavcopy from Public data of NSE website
### The script downloads the bhavcopy for the date range provided
### Provide Date range input in the following variable
### Remember the error message does not mean that the file is not available, it could be due to trading holidays also

## Provide date range in the format of dd-mmm-yyyy
From_Date = '1-Jan-2023'
To_Date = '10-Jan-2025'

import os
import requests
import zipfile
from datetime import datetime, timedelta
import urllib.request as request

Today = datetime.today()
From = datetime.strptime(From_Date, '%d-%b-%Y')
To = datetime.strptime(To_Date, '%d-%b-%Y')

if (To > Today):
    To = Today

if (From > To):
    print ('Check the date range')
    exit()

# Create year folders if they don't exist
current_year = From.year
end_year = To.year

for year in range(current_year, end_year + 1):
    year_folder = str(year)
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

# File path base
Base_URL = "https://archives.nseindia.com/content/historical/EQUITIES/"
Base_URL_New = "https://nsearchives.nseindia.com/products/content/"

Download_Date = From

while (Download_Date <= To):

    Year = datetime.strftime(Download_Date, "%Y")
    Month = str.upper(datetime.strftime(Download_Date, "%b"))
    Date = datetime.strftime(Download_Date, "%d")
    Date_1 = datetime.strftime(Download_Date, "%d%m%Y")

    # old convention
    if (Download_Date < datetime(2024,7,8)):

        URL = Base_URL+Year+"/"+Month+"/cm"+Date+Month+Year+"bhav.csv.zip"
        Local_File_Name = ".\\"+Year+"\\cm"+Date+Month+Year+"bhav.csv.zip"

        #Fetch the file from URL
        try:

            # Download bhav zip file
            request.urlretrieve(URL, Local_File_Name)

            # Extract the zip content
            with zipfile.ZipFile(Local_File_Name, 'r') as zip_ref:
                zip_ref.extractall('.\\'+Year)

            # delete zip file
            os.remove(Local_File_Name)
            
            print ("CM Bhav for "+datetime.strftime(Download_Date, "%d-%b-%Y")+ " downloaded")

        except Exception:
            print ("*** CM Bhav for "+datetime.strftime(Download_Date, "%d-%b-%Y")+ " Unavailable")
    
    # new convention
    else:

        URL = Base_URL_New+"sec_bhavdata_full_"+Date_1+".csv"
        Local_File_Name = ".\\"+Year+"\\sec_bhavdata_full_"+Date_1+".csv"        

        #Fetch the file from URL
        try:

            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}                

            # Download bhav zip file
            Resp = requests.get (URL, timeout=3, headers=header)

            if Resp.status_code == 200 :

                with open (Local_File_Name, 'wb') as File:
                    File.write (Resp.content)

                print ("CM Bhav for "+datetime.strftime(Download_Date, "%d-%b-%Y")+ " downloaded")
            
            else :

                print ("*** CM Bhav for "+datetime.strftime(Download_Date, "%d-%b-%Y")+ " Unavailable")

        except Exception:
            print ("*** CM Bhav for "+datetime.strftime(Download_Date, "%d-%b-%Y")+ " Unavailable")
    
    Download_Date = Download_Date + timedelta(days=1)
