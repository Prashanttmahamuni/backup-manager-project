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
