# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DOTSTAFF_USERNAME = os.getenv("DOTSTAFF_USERNAME")
DOTSTAFF_PASSWORD = os.getenv("DOTSTAFF_PASSWORD")

EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DOTSTAFF_URL = "https://my.dotstaff.com/VendorPostingList.aspx?navigationID=MV%7c1025"

OUTPUT_TXT_PATH = "output/dotstaff_jobs.txt"

CHROME_DRIVER_PATH = r"C:\Users\atharva wagholikar\Desktop\dotstaff\chromedriver-win64\chromedriver.exe"