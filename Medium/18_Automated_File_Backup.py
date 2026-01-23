import os
import shutil
import datetime
import schedule
import time

source_dir = "/home/riteshbrahmachari/Pictures" # Example source
destination_dir = "/home/riteshbrahmachari/Backups" # Example dest

def copy_folder_to_directory(source, dest):
    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))
    
    try:
        shutil.copytree(source, dest_dir)
        print(f"Folder copied to: {dest_dir}")
    except FileExistsError:
        print(f"Backup already exists in: {dest_dir}")
    except Exception as e:
        print(f"Error: {e}")

def perform_backup():
    # In a real scenario, you'd probably want to make these inputs or config
    # For now, we stub with placeholders or ask user
    print("Performing daily backup...")
    # copy_folder_to_directory(source_dir, destination_dir) 
    print("Backup routine finished (Simulated).")

# schedule.every().day.at("10:30").do(perform_backup)
schedule.every(10).seconds.do(perform_backup) # For demo

print("Backup service started...")
while True:
    schedule.run_pending()
    time.sleep(1)
