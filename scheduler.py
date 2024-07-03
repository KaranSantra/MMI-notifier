import schedule
import time
import subprocess
import pandas as pd
from datetime import datetime

def run_secondary_script():
    try:
        result = subprocess.run(['python', './test2.py'], capture_output=True, text=True)
        value1, value2 = result.stdout.strip().split()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        weekday = now.strftime("%A")

        df = pd.DataFrame([[date, weekday, value1, value2]], columns=['Date', 'Weekday', 'Value1', 'Value2'])
        try:
            existing_df = pd.read_excel('stock_data.xlsx')
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_excel('stock_data.xlsx', index=False)
    except Exception as e:
        print(f"Error running script or writing to file: {e}")

schedule.every().monday.at("09:15").do(run_secondary_script)
schedule.every().tuesday.at("09:15").do(run_secondary_script)
schedule.every().wednesday.at("09:15").do(run_secondary_script)
schedule.every().thursday.at("09:15").do(run_secondary_script)
schedule.every().friday.at("09:15").do(run_secondary_script)

def time_until_next_run():
    next_run = min(job.next_run for job in schedule.jobs)
    return (next_run - datetime.now()).total_seconds()

while True:
    schedule.run_pending()
    sleep_duration = time_until_next_run()
    time.sleep(sleep_duration)