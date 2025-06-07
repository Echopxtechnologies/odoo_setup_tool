# 🚀 Odoo 18 Auto Setup Tool

This script helps you automate the complete installation and setup of **Odoo 18** on Ubuntu systems, including PostgreSQL configuration, password setup, dependency installation, and user creation.

---

## ✅ Features

- Installs Odoo 18 from the official nightly repository
- Installs and configures PostgreSQL (sets passwords, creates roles)
- Handles required Python and system dependencies
- Installs `wkhtmltopdf (0.12.6.1)` for PDF report support
- Installs and sets up Nginx
- Automatically creates an Odoo with DB access
- Configures `odoo.conf` file securely
- Handles PostgreSQL authentication (`peer/md5`) switching

---

## 📦 Requirements

- Ubuntu 22.04+
- `sudo` privileges
- Python 3.8+

---

## 📥 Installation

```bash
git clone https://github.com/Echopxtechnologies/odoo_setup_tool.git
```
```bash
python3 odoo_setup_tool/odoo.py
```
---
# ☝️ During execution, the script will prompt you to:

- Set a master password for the PostgreSQL postgres user

- Set a password for the Odoo PostgreSQL user (odoo)

#### These credentials will be used to configure both PostgreSQL and the odoo.conf file.
