# 🗄️ Automated Backup and Rotation Script with Google Drive Integration

## 📌 Overview  

This project provides a fully automated shell/Python script to manage backups for a GitHub-hosted project. It creates timestamped `.zip` archives of your codebase, organizes them into a structured directory, integrates with Google Drive using `rclone`, implements a rotational backup strategy (daily, weekly, monthly), and sends a webhook notification upon successful backup.
    
---  

## ⚙️ Features

- Backup project directory into timestamped `.zip` files    
- Store backups in `~/backups/ProjectName/YYYY/MM/DD/`
- Upload backups to Google Drive using `rclone`
- Retain last X daily, weekly (Sunday), and monthly backups
- Delete older backups automatically based on retention policy
- Log all operations to `backup.log`
- Send a POST `cURL` notification on successful backup
- Configurable via script arguments or `.env/config.json`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/backup-script.git
cd backup-script
```
### 2. Install rclone (Recommended)
```bash
curl https://rclone.org/install.sh | sudo bash
```
### 3. Configure Google Drive with rclone
```bash
rclone config
```
Follow the prompts to authenticate and create a remote named remote.

## 🧾 Script Usage
Shell Script
```bash
./backup_script.sh --project-dir /path/to/project \
                   --project-name MyProject \
                   --gdrive-folder BackupFolderName \
                   --daily 7 --weekly 4 --monthly 3 \
                   --notify-url https://webhook.site/your-unique-url
```

Python Script
```bash
python3 backup.py --project-dir /path/to/project \
                  --project-name MyProject \
                  --gdrive-folder BackupFolderName \
                  --daily 7 --weekly 4 --monthly 3 \
                  --notify-url https://webhook.site/your-unique-url
```

### Optional Flags
- --no-notify : Disable webhook notification
- --config config.json : Load settings from config file

## 🗂️ Configuration File (Optional)
.env or config.json
```json
{
  "project_dir": "/path/to/project",
  "project_name": "MyProject",
  "gdrive_folder": "BackupFolderName",
  "daily_retention": 7,
  "weekly_retention": 4,
  "monthly_retention": 3,
  "notify_url": "https://webhook.site/your-unique-url",
  "notify_enabled": true
}
```
## 📅 Scheduling with Crontab
To run the backup daily at midnight:
```bash
crontab -e
```
Add:
```bash
0 0 * * * /path/to/backup_script.sh --project-dir /path/to/project --project-name MyProject --gdrive-folder BackupFolderName --daily 7 --weekly 4 --monthly 3 --notify-url https://webhook.site/your-unique-url
```
## 📤 Sample Webhook Payload
```json
{
  "project": "MyProject",
  "date": "20251111_181900",
  "test": "BackupSuccessful"
```
## 📁 Expected Output
- Backup file: MyProject_20251111_181900.zip
- Stored at: ~/backups/MyProject/2025/11/11/
- Log entry in backup.log:

```Code
[2025-11-11 18:19:00] Backup created: MyProject_20251111_181900.zip
[2025-11-11 18:19:10] Uploaded to Google Drive: BackupFolderName
[2025-11-11 18:19:15] Notification sent to webhook
[2025-11-11 18:19:20] Deleted 2 old daily backups
```
## 🔐 Security Considerations
- Ensure .env or config.json is excluded from version control (.gitignore)

- Use secure tokens for webhook URLs

- Limit Google Drive access via rclone to specific folders

- Validate deletion logic to avoid accidental data loss

## 🧠 Contribution & Support
- Feel free to fork, improve, and submit pull requests. For issues or feature requests, open a GitHub issue.
















