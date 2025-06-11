# 🚀 Odoo 18 Auto Setup Tool

This Python script automates the **complete installation and configuration of Odoo 18** on Ubuntu-based systems. It also optionally sets up Webmin and an ERP Instance Manager Tool with domain binding and SSL.

---

## ✅ Features

- ✅ Interactive prompt to install:
  - Odoo 14–18 (with repository auto-setup)
  - Webmin panel (optional)
  - ERP Instance Manager Tool (optional)
- ✅ Installs and configures PostgreSQL (sets passwords, creates roles)
- ✅ Securely configures `odoo.conf` with credentials and paths
- ✅ Installs all required Python & system dependencies
- ✅ Installs `wkhtmltopdf 0.12.6.1` for PDF report generation
- ✅ Installs and sets up **Nginx** as a web server
- ✅ Sets file & user permissions (Odoo, www-data)
- ✅ Creates and configures ERP installer UI at `https://erpinstall.<your-domain>`
- ✅ Issues free SSL certificates with **Certbot**
- ✅ Appends fine-tuned sudo permissions for automation

---

## 📦 Requirements

- Ubuntu 22.04 or later
- Python 3.8+
- Root or `sudo` access

---

## 📥 Installation Steps

```bash
git clone https://github.com/Echopxtechnologies/odoo_setup_tool.git
python3 odoo_setup_tool/odoo.py
```
---
# ☝️ During execution, the script will prompt you to:

- ✅ Choose whether to install:
  - Odoo
  - Webmin
  - ERP Installer Tool

- 🧩 Select the Odoo version to install (supports 14 to 18)

- 🔐 Set a master password for the PostgreSQL `postgres` user

- 🔐 Set a password for the PostgreSQL `odoo` user

- ⚠️ Confirm reinstallation if Odoo is already installed

- 🌐 Provide your domain name (e.g., `example.com`)  
  _(used to create the subdomain `erpinstall.example.com`)_

- 🔑 Enter a bearer token (optional) for ERP Installer access

These inputs are used to configure PostgreSQL users, Odoo settings, ERP installer tools, and NGINX with SSL.
---
