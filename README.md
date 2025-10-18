# 🔄 Automated Backup and Rotation Script with Google Drive Integration

## 📦 Overview

This project provides a fully automated Python script to back up a specified GitHub project directory. It creates timestamped ZIP archives, stores them locally in a structured format, uploads them to Google Drive using `rclone`, applies a rotational backup strategy (daily, weekly, monthly), and sends a webhook notification upon successful backup. Logging and configuration support are included.

---

## 🎯 Objectives

- Back up a specified project directory  
- Organize and store backups in a timestamped format  
- Integrate with Google Drive using CLI tools  
- Implement a rotational backup strategy (daily, weekly, monthly)  
- Send a cURL request on successful backup  
- Log the process and support configuration  

---

## 🛠️ Requirements

### ✅ Python 3  
### ✅ rclone (for Google Drive integration)  
### ✅ Internet access (for webhook and Drive upload)  


