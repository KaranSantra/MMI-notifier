import schedule
import time
from datetime import datetime
import pytz
import os

def job():
    # Replace this line with the command to run your Python script
    os.system('python mmi-extractor-notifier')  # Replace 'notify.py' with your actual script

# Get the timezone for India
india_tz = pytz.timezone('Asia/Kolkata')

# Schedule the job every weekday at 9:35 AM IST
schedule.every().monday.at("09:35").do(job)
schedule.every().tuesday.at("09:35").do(job)
schedule.every().wednesday.at("09:35").do(job)
schedule.every().thursday.at("09:35").do(job)
schedule.every().friday.at("09:35").do(job)

print("Scheduler started. The script will run at 9:35 AM IST every weekday.")

while True:
    now = datetime.now(india_tz)
    schedule.run_pending()
    time.sleep(60)  # Check every minute