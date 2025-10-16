import os
import json
import zipfile
from datetime import datetime

# Load configuration file
with open("config.json") as f:
    config = json.load(f)

# Extract configuration details
project_name = config["project_name"]                
project_dir = config["project_dir"]                   
backup_root = config["backup_root"] 

# Create timestamp for naming
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_filename = f"{project_name}_{timestamp}.zip"

# Create structured folder path for backup
year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")
day = datetime.now().strftime("%d")

backup_path = os.path.join(backup_root, project_name, year, month, day)
os.makedirs(backup_path, exist_ok=True)

# Full backup zip path
zip_filepath = os.path.join(backup_path, zip_filename)

# Function to create ZIP archive of the project
def zip_project(src_dir, dest_zip):
    print(f"📦 Creating ZIP archive from {src_dir} ...")
    with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(src_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, src_dir)
                zipf.write(abs_path, rel_path)
    print(f"✅ ZIP file created successfully: {dest_zip}")

# Run backup
zip_project(project_dir, zip_filepath)

import subprocess

gdrive_remote = config["gdrive_remote"]
gdrive_folder = config["gdrive_folder"]

def upload_to_gdrive(local_path, remote_name, remote_folder):
    try:
        result = subprocess.run(
            ["rclone", "copy", local_path, f"{remote_name}:{remote_folder}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Upload to Google Drive successful.")
            return True
        else:
            print("❌ Upload failed:", result.stderr)
            return False
    except Exception as e:
        print("❌ Upload error:", str(e))
        return False

upload_success = upload_to_gdrive(zip_filepath, gdrive_remote, gdrive_folder)

import shutil

retention = config["retention"]

def list_backups(base_path):
    backups = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".zip") and project_name in file:
                full_path = os.path.join(root, file)
                try:
                    timestamp_str = file.replace(f"{project_name}_", "").replace(".zip", "")
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    backups.append((timestamp, full_path))
                except ValueError:
                    continue
    return sorted(backups, key=lambda x: x[0], reverse=True)

def apply_retention(backups):
    daily, weekly, monthly = [], [], []
    for ts, path in backups:
        if ts.weekday() == 6:  # Sunday
            weekly.append((ts, path))
        if ts.day == 1:
            monthly.append((ts, path))
        daily.append((ts, path))

    deleted = []

    # Apply daily retention
    for b in daily[retention["daily"]:]:
        os.remove(b[1])
        deleted.append(b[1])

    # Apply weekly retention
    for b in weekly[retention["weekly"]:]:
        if os.path.exists(b[1]):
            os.remove(b[1])
            deleted.append(b[1])

    # Apply monthly retention
    for b in monthly[retention["monthly"]:]:
        if os.path.exists(b[1]):
            os.remove(b[1])
            deleted.append(b[1])

    return deleted

all_backups = list_backups(os.path.join(backup_root, project_name))
deleted_files = apply_retention(all_backups)
print(f"🧹 Deleted {len(deleted_files)} old backups.")
print("\n✅ Backup process completed successfully!")
print(f"Backup stored at: {zip_filepath}")

import logging
import requests

# Setup logging
log_file = "backup.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Log details
logging.info(f"Backup created: {zip_filename}")
logging.info(f"Upload status: {'Success' if upload_success else 'Failed'}")
if deleted_files:
    logging.info(f"Deleted backups: {', '.join(deleted_files)}")

# Send notification if enabled
if config.get("notify", True) and upload_success:
    payload = {
        "project": project_name,
        "date": timestamp,
        "test": "BackupSuccessful"
    }
    try:
        response = requests.post(config["webhook_url"], json=payload)
        if response.status_code == 200:
            print("📣 Notification sent successfully.")
            logging.info("Notification sent.")
        else:
            print("⚠️ Notification failed.")
            logging.warning("Notification failed.")
    except Exception as e:
        print("⚠️ Notification error:", str(e))
        logging.error(f"Notification error: {str(e)}")
