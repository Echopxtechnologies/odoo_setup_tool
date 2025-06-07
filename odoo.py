import os
import subprocess
import sys
import tempfile
import stat
import shutil
import time 

# Function to kill existing apt processes

def error(message):
    print(f"Error: {message}")
    sys.exit(1)

def run_command(command, shell=False, capture_output=False):
    try:
        result = subprocess.run(command, check=True, text=True, shell=shell, capture_output=capture_output)
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        error(f"Command failed: {e}")

class OdooInstaller:

    def install(self):
        print("** Installing Odoo 18... **")

        commands = [
            # Add Odoo GPG key
            
            ("** Add Odoo GPG key **", "wget -O - https://nightly.odoo.com/odoo.key | sudo gpg --dearmor -o /usr/share/keyrings/odoo-archive-keyring.gpg", True),
            
            # Add Odoo repo
            ("** Add Odoo repository **", "echo 'deb [signed-by=/usr/share/keyrings/odoo-archive-keyring.gpg] https://nightly.odoo.com/18.0/nightly/deb/ ./' | sudo tee /etc/apt/sources.list.d/odoo.list", True),
            
            # System update and Odoo install
            ("Updating the server","sudo apt update && apt upgrade -y",True),
            ("** Install Odoo **", ["sudo", "apt", "install", "-y", "odoo"], False),

            # Python & required dependencies
            ("** Install dependencies **", [
                "sudo", "apt", "install", "-y",
                "python3-pip", "python3-dev", "build-essential", "wget", "git", "python3-venv",
                "libxslt-dev", "libzip-dev", "libldap2-dev", "libsasl2-dev", "python3-setuptools",
                "node-less", "libjpeg-dev", "zlib1g-dev", "libpq-dev", "libxml2-dev", "libssl-dev",
                "libffi-dev", "libmysqlclient-dev", "libjpeg8-dev", "liblcms2-dev", "libblas-dev",
                "libatlas-base-dev", "npm", "curl", "xz-utils", "ca-certificates", "sudo", "nano",
                "libxrender1", "libfontconfig1", "libjpeg62", "libxtst6", "fontconfig", "xfonts-75dpi",
                "xfonts-base", "libpng16-16", "software-properties-common"
            ], False),
            ("** Clean APT cache **", ["sudo", "apt", "clean"], False),

            # wkhtmltopdf setup
            ("** Remove old wkhtmltopdf **", ["sudo", "apt-get", "remove", "--purge", "wkhtmltopdf", "-y"], False),
            ("** Remove wkhtmltopdf binaries **", "sudo rm -rf /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf /usr/share/man/man1/wkhtmltopdf.1.gz", True),
            ("** Autoremove **", ["sudo", "apt", "autoremove", "-y"], False),
            ("** Add PPA **", ["sudo", "add-apt-repository", "-y", "ppa:linuxuprising/libpng12"], False),
            ("** APT update again **", ["sudo", "apt", "update"], False),
            ("** Download wkhtmltopdf .deb **", "wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb", True),
            ("** Install wkhtmltopdf .deb **", ["sudo", "dpkg", "-i", "wkhtmltox_0.12.6.1-3.jammy_amd64.deb"], False),
            ("** Fix broken install **", ["sudo", "apt-get", "-f", "install", "-y"], False),
            ("** Link wkhtmltopdf **", "sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf", True),
            ("** Link wkhtmltoimage **", "sudo ln -s /usr/local/bin/wkhtmltoimage /usr/bin/wkhtmltoimage", True),

            # install nginx
            ("** Installing Nginx... **",["apt","install","nginx","-y"] ,False),

            # Create odoo user and folder
            ("** Create Odoo user **", ["sudo", "adduser", "--system", "--group", "odoo"], False),
            ("** Create /opt/odoo **", "sudo mkdir /opt/odoo", True),
            ("** Change ownership of /opt/odooo **", "sudo chown -R odoo:odoo /opt/odoo", True),
            ("** Clone from git **","git clone --depth 1 --branch 18.0 https://www.github.com/odoo/odoo /opt/odoo",True),
        ]

        for desc, cmd, shell in commands:
            try:
                print(f"{desc} ...")
                run_command(cmd, shell=shell)
                print(f"---> Success: {desc}...........................................[OK]")
            except Exception as e:
                print(f"---> Failed: {desc} — {e}")

        # Confirm installations
        try:
            version = run_command(["odoo", "--version"], capture_output=True)
            wkhtmltopdf_v = run_command(["wkhtmltopdf", "--version"], capture_output=True)
            print(f"==>  Odoo Version: {version}")
            print(f"==>  wkhtmltopdf Version: {wkhtmltopdf_v}")
        except Exception as e:
            print(f"==>  Version check failed: {e}")


    def restart_odoo(self):
        try:
            subprocess.run(["sudo", "systemctl", "restart", "odoo"], check=True)
        except Exception as e:
            print(f"Unable to restart odoo : {e}")

    def change_file_permis(self):
        os.chmod("/etc/odoo/odoo.conf", 0o640)
        subprocess.run(["sudo", "chown", "odoo:odoo", "/etc/odoo/odoo.conf"], check=True)


def print_banner():
    print("  ______   _______    ______    ______          ____   _______   ________  __    __  _______       ________  ______    ______   __       ")  
    print(" /      \ /       \  /      \  /      \      /      \ /        |/        |/  |  /  |/       \     /        |/      \  /      \ /  |      ")
    print("/$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |    /$$$$$$  |$$$$$$$$/ $$$$$$$$/ $$ |  $$ |$$$$$$$  |    $$$$$$$$//$$$$$$  |/$$$$$$  |$$ |      ")
    print("$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |    $$ \__$$/ $$ |__       $$ |   $$ |  $$ |$$ |__$$ |       $$ |  $$ |  $$ |$$ |  $$ |$$ |      ")
    print("$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |    $$      \ $$    |      $$ |   $$ |  $$ |$$    $$/        $$ |  $$ |  $$ |$$ |  $$ |$$ |      ")
    print("$$ \__$$ |$$ |__$$ |$$ \__$$ |$$ \__$$ |    /  \__$$ |$$ |_____    $$ |   $$ \__$$ |$$ |             $$ |  $$ \__$$ |$$ \__$$ |$$ |_____ ")
    print("$$    $$/ $$    $$/ $$    $$/ $$    $$/     $$    $$/ $$       |   $$ |   $$    $$/ $$ |             $$ |  $$    $$/ $$    $$/ $$       |")
    print(" $$$$$$/  $$$$$$$/   $$$$$$/   $$$$$$/       $$$$$$/  $$$$$$$$/    $$/     $$$$$$/  $$/              $$/    $$$$$$/   $$$$$$/  $$$$$$$$/ ")
    print("\n\n\n")



# Postgres related class
class PostgresSetup:

    def __init__(self, postgres_password, odoo_password):
        self.postgres_password = postgres_password
        self.odoo_password = odoo_password
        self.PG_HBA_PATH = "/etc/postgresql/14/main/pg_hba.conf"

    def _replace_auth_method(self, to_method="md5"):
        new_lines = []
        with open(self.PG_HBA_PATH, "r") as file:
            for line in file:
                parts = line.split()
                # Only replace if this is a 'local' line for 'odoo' or 'postgres'
                if (
                    len(parts) >= 5
                    and parts[0] == "local"
                    and parts[2] in ["odoo", "postgres"]
                    and parts[-1] != to_method  # Only change if not already correct
                ):
                    # Replace method (last part) with to_method
                    new_line = " ".join(parts[:-1]) + f" {to_method}\n"
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
        # Write back
        with open(self.PG_HBA_PATH, "w") as file:
            file.writelines(new_lines)



    def _restart_postgresql(self):
        subprocess.run(["sudo", "systemctl", "restart", "postgresql"], check=True)

    def _run_sql_as_postgres(self, sql):
        subprocess.run(['sudo', '-u', 'postgres', 'psql', '-c', sql], check=True)

    def _run_sql_file_as_postgres(self, sql_content):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write(sql_content)
            tmp_file_path = tmp_file.name

        # Set read permissions so 'postgres' can access it
        os.chmod(tmp_file_path, 0o644)

        subprocess.run(['sudo', '-u', 'postgres', 'psql', '-f', tmp_file_path], check=True)

        os.remove(tmp_file_path)

    def add_odoo_auth_line(self):
        entry = "local   all             odoo                                    md5\n"
        with open(self.PG_HBA_PATH, "r") as file:
            lines = file.readlines()
        
        if entry not in lines:
            lines.insert(93, entry)  # Add at the top (or choose another spot)
            with open(self.PG_HBA_PATH, "w") as file:
                file.writelines(lines)
            print("** Added md5 auth line for odoo user. **")
        else:
            print("** md5 auth line for odoo user already exists. **")



    def rewrite_config(self):
        config = f"""[options]
        ; This is the password that allows database operations:
        admin_passwd = {self.postgres_password}
        db_host = localhost
        db_port = 5432
        db_user = odoo
        db_password = {self.odoo_password}
        addons_path = /usr/lib/python3/dist-packages/odoo/addons
        default_productivity_apps = True
        """
        os.makedirs("/etc/odoo", exist_ok=True)

        with open("/etc/odoo/odoo.conf", "w") as f:
            f.write(config)

    def setup(self):
        print("** Switching to peer authentication... **")
        self._replace_auth_method(to_method="peer")

        self._restart_postgresql()

        print("** Setting postgres password...")
        self._run_sql_as_postgres(f"ALTER USER postgres WITH PASSWORD '{self.postgres_password}';")

        print("** Creating and configuring Odoo user...")
        sql_script = f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'odoo') THEN
                    CREATE ROLE odoo WITH LOGIN PASSWORD '{self.odoo_password}';
                ELSE
                    ALTER ROLE odoo WITH PASSWORD E'{self.odoo_password}';
                END IF;
                    ALTER ROLE odoo WITH CREATEDB CREATEROLE LOGIN;
            END
            $$;
            """

        try:
            self._run_sql_file_as_postgres(sql_script)
        except subprocess.CalledProcessError as e:
            print(" Failed to apply SQL script:", e)
            sys.exit(1)

        print("** Writing to odoo.conf... **")
        self.rewrite_config()

        print("** Reverting back to md5 authentication... **")
        self._replace_auth_method(to_method="md5")
        self.add_odoo_auth_line()
        self._restart_postgresql()

        print("** PostgreSQL setup completed successfully. **")

class tools_files:
    def __init__(self,php_version):
        self.php_version = php_version
    def install_permission(self):
        cmds = [
            #description , command , shell
                ("Installing PHP FPM", f"sudo apt install php{self.php_version}-common php{self.php_version}-fpm php{self.php_version}-pgsql php{self.php_version}-curl php{self.php_version}-mbstring php{self.php_version}-xml php{self.php_version}-gd php{self.php_version}-cli php{self.php_version}-mysql php{self.php_version}-bcmath php{self.php_version}-zip -y", True),
                ("Starting PHP-FPM", f"sudo systemctl start php{self.php_version}-fpm", True),
                ("Enable PHP-FPM", f"sudo systemctl enable php{self.php_version}-fpm", True),
                ("Create a Port.txt file","sudo touch /var/www/port.txt",True),
                ("Create a env.json file","sudo touch /var/www/env.json",True),
                ("Change the fiel permission of env.json","sudo chown -R www-data:www-data /var/www/env.json",True),
                ("Change Ownership of Port.txt","sudo chown -R www-data:www-data /var/www/port.txt",True),
                ("Change the file permission of Port.txt","sudo chmod 644 /var/www/port.txt",True),
                ("Write a default port number in port.txt","echo '8070' | sudo tee /var/www/port.txt",True),
                ("Installing software-properties","sudo apt install software-properties-common -y",True),
                ("Adding the repository","sudo add-apt-repository universe -y",True),
                ("Restart PHP-FPM",f"sudo systemctl restart php{self.php_version}-fpm", True),
                ("Install Certbot ","sudo apt install certbot python3-certbot-nginx -y",True),
                ("Create a Parent Directory to store the file ","sudo mkdir /var/www/instance",True),
                ("Create a Directory inside","sudo mkdir /var/www/instance/htdocs",True),
                ("Change the file permission of Directory","sudo chown -R www-data:www-data /var/www/instance" ,True),
                ("Clone the file from git.....","git clone https://github.com/Echopxtechnologies/instance_manager.git /var/www/instance/htdocs",True),
                ("Change the ownership of tool ","sudo chown -R www-data:www-data /var/www/instance/htdocs/web_instance_tool.py",True),
                
        ]

        for desc ,cmd, shell in cmds:
            try:
                print(f"==>{desc}")
                run_command(cmd,shell=shell)
                print(f"==> Success {desc}.................................[OK] \n") 
            except Exception as e:
                print(f"==> Error in {desc}: {e}")

class Install:
    def Webmin(self):
        print("Installing Webmin!....")
        cmds = [
            # (description, command, shell)
            ("Adding Webmin GPG key", "wget -q -O- http://www.webmin.com/jcameron-key.asc | sudo gpg --dearmor -o /usr/share/keyrings/webmin.gpg", True),
            ("Adding Repository", "sudo sh -c 'echo \"deb [signed-by=/usr/share/keyrings/webmin.gpg] http://download.webmin.com/download/repository sarge contrib\" > /etc/apt/sources.list.d/webmin.list'", True),
            ("Updating...", "sudo apt update", True),
            ("Installing Webmin", "sudo apt install -y webmin", True),
            ("Enabling Firewall", "sudo ufw allow 10000/tcp", True),
        ]

        for desc, cmd, shell in cmds:
            try:
                print(f"==> {desc}")
                result = subprocess.run(cmd, shell=shell, check=True, text=True, capture_output=True)
                print(f"==> Success: {desc}.................................[OK]\n")
            except subprocess.CalledProcessError as e:
                print(f"==> Error in {desc}: {e.stderr}")
                exit(1)  # Exit if any critical step fails

class write_data_file:
    # First call this function write_env 
    # 2nd call this function create_nginx_config 
    # 3rd call this fucntion append_nginx_config
    
    def __init__(self,domain,master_password,bearer_token):
        self.domain = domain
        self.master_password = master_password
        self.bearer_token = bearer_token
        self.env_path = "/var/www/env.json"
        self.nginx_path = "/etc/nginx/sites-available"
        self.nginx_file = f"{self.nginx_path}/erpinstall.{self.domain}"

    def create_nginx_config(self):
        try:
            php_version = "8.1"
            content = f"""
        server {{
            listen 80;
            server_name erpinstall.{self.domain};

            root /var/www/instance/htdocs;
            index index.php index.html index.htm;

            location ~ \.(txt|py|save|json)$ {{
                deny all;
                return 403;
            }}

            location ~ /\. {{
                deny all;
                return 403;
            }}

            location / {{
                try_files $uri $uri/ =404;
            }}

            location ~ \.php$ {{
                include snippets/fastcgi-php.conf;
                fastcgi_pass unix:/run/php/php{php_version}-fpm.sock;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;

                fastcgi_connect_timeout 1800s;
                fastcgi_send_timeout 1800s;
                fastcgi_read_timeout 1800s;
                send_timeout 1800s;
            }}
        }}
            """

            subprocess.run(f"sudo touch {self.nginx_file}",shell=True)

            with open(self.nginx_file,'w') as f:
                f.write(content)
            print("HTTP NGINX Config written successfully.")
        except:
            print("Error creating nginx config file")

    def write_env(self):
        try:
            env = f"""
            {{
            "master_password": "{self.master_password}",
            "host": "localhost",
            "db_name":"instance_db",
            "database": "postgres",
            "user": "postgres",
            "bearer_token": "{self.bearer_token}",
            "admin_password" : "{self.master_password}"
            }}
            """
            with open(self.env_path,'w') as f:
                f.write(env)
        except Exception as e:
            print(f"Error writing env file: {e}")

    def sim_link(self):
        try:
            subprocess.run(f"sudo ln -s {self.nginx_file} /etc/nginx/sites-enabled/",shell=True)
        except Exception as e:
            print(f"Error when creating a sim link: {e}")
    
    def run_certbot(self):
        try:
            certbot_cmd = f"sudo certbot --nginx -d erpinstall.{self.domain} --non-interactive --agree-tos -m echopx@gmail.com"
            subprocess.run(certbot_cmd, shell=True, check=True)
            print("Certbot SSL installed successfully.")
        except Exception as e:
            print(f"Error running certbot: {e}")

class database_setup:
    def __init__(self, db_name):
        self.db_name = db_name

    def database_exists(self):
            result = subprocess.run(f"sudo -u postgres psql -tAc \"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'\"", shell=True, capture_output=True, text=True)
            return result.stdout.strip() == '1'
    
    def create_database(self):
        try:

            print(f"Creating database {self.db_name}...")

            if not self.database_exists():
                subprocess.run(f"sudo -u postgres createdb {self.db_name}", shell=True, check=True)
                print(f"Database {self.db_name} created successfully.")
            else:
                print(f"Database {self.db_name} already exists.")

            self.apply_schema()
            print(" Schema applied successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error Creating database: {e}")


    def apply_schema(self):
        schema = f"""
        SET client_encoding = 'UTF8';
        SET TIME ZONE 'UTC';

        CREATE TABLE session (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            login_token VARCHAR(256) NOT NULL UNIQUE,
            login_time TIMESTAMP NOT NULL,
            ip VARCHAR(20) NOT NULL,
            user_agent VARCHAR(256) NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(256) NOT NULL UNIQUE,
            password VARCHAR(256) NOT NULL
        );
        CREATE TABLE instances (
            id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            instance_name character varying(100) NOT NULL,
            db_name character varying(100) NOT NULL,
            db_user character varying(100) NOT NULL,
            db_password character varying(100) NOT NULL,
            domain character varying(255) NOT NULL,
            port integer NOT NULL
        );
        """

        # write to safer folder
        tmpfile_path = f"/var/tmp/{self.db_name}_schema.sql"
        with open(tmpfile_path, "w") as tmpfile:
            tmpfile.write(schema)

        try:
            subprocess.run(f"sudo -u postgres psql -d {self.db_name} -f {tmpfile_path}", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error applying schema: {e}")

        os.remove(tmpfile_path)



def add_permission():
    # Path constants
        SUDOERS_FILE = "/etc/sudoers"
        TEMP_FILE = "/etc/sudoers.tmp"
        BACKUP_FILE = "/etc/sudoers.backup"

        # Your custom sudoers content
        append_content = """\
# Custom sudoers entries for www-data and odoo

# Allow www-data to run specific commands without password
www-data ALL=(ALL) NOPASSWD: \
    /usr/bin/mkdir, \
    /usr/bin/chown, \
    /usr/bin/git, \
    /usr/bin/tee, \
    /usr/bin/systemctl, \
    /usr/bin/ln, \
    /usr/bin/certbot, \
    /usr/bin/nginx, \
    /bin/rm, \
    /bin/systemctl, \
    /usr/sbin/nginx, \
    /usr/bin/unlink

# More specific www-data file/dir permissions (for Odoo)
www-data ALL=(ALL) NOPASSWD: /usr/bin/mkdir /etc/odoo/
www-data ALL=(ALL) NOPASSWD: /usr/bin/tee /etc/odoo/*
www-data ALL=(ALL) NOPASSWD: /usr/bin/chown /etc/odoo/*
www-data ALL=(ALL) NOPASSWD: /usr/bin/chmod /etc/odoo/*
www-data ALL=(ALL) NOPASSWD: /usr/bin/rm /etc/odoo/*
www-data ALL=(ALL) NOPASSWD: /usr/bin/tee /etc/nginx/sites-available/*
www-data ALL=(ALL) NOPASSWD: /usr/bin/tee /etc/systemd/system/*.service
www-data ALL=(ALL) NOPASSWD: /usr/bin/tee /etc/odoo/*.conf
www-data ALL=(ALL) NOPASSWD: /usr/bin/tee /var/www/port.txt
www-data ALL=(ALL) NOPASSWD: /usr/bin/mkdir /etc/odoo
www-data ALL=(ALL) NOPASSWD: /usr/bin/mkdir -p /opt/odoo_*
www-data ALL=(ALL) NOPASSWD: /usr/bin/chown /opt/odoo_*
www-data ALL=(ALL) NOPASSWD: /usr/bin/chown /etc/odoo/*
www-data ALL=(ALL) NOPASSWD: /usr/bin/chmod 644 /etc/systemd/system/*.service
www-data ALL=(ALL) NOPASSWD: /usr/bin/chmod 755 /etc/odoo/*.conf
www-data ALL=(ALL) NOPASSWD: /usr/bin/certbot --nginx *
www-data ALL=(ALL) NOPASSWD: /usr/bin/systemctl daemon-reload
www-data ALL=(ALL) NOPASSWD: /usr/bin/systemctl enable odoo_*
www-data ALL=(ALL) NOPASSWD: /usr/bin/systemctl start odoo_*
www-data ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
www-data ALL=(ALL) NOPASSWD: /usr/bin/ln -s /etc/nginx/sites-available/* /etc/nginx/sites-enabled/
www-data ALL=(ALL) NOPASSWD: /bin/rm -rf /opt/odoo_*
www-data ALL=NOPASSWD: /bin/rm -rf /opt/odoo_*
www-data ALL=NOPASSWD: /usr/bin/rm /etc/systemd/system/*.service
www-data ALL=NOPASSWD: /usr/bin/rm /etc/nginx/sites-enabled/*
www-data ALL=NOPASSWD: /usr/bin/rm /etc/letsencrypt/live/*
www-data ALL=NOPASSWD: /usr/bin/unlink /etc/nginx/sites-enabled/*
www-data ALL=NOPASSWD: /usr/bin/rm /etc/nginx/sites-available/*

# Allow odoo user to run specific commands without password
odoo ALL=(ALL) NOPASSWD: /usr/bin/odoo
odoo ALL=(ALL) NOPASSWD: /bin/systemctl
odoo ALL=(ALL) NOPASSWD: /bin/mkdir
odoo ALL=(ALL) NOPASSWD: /bin/chown
odoo ALL=(ALL) NOPASSWD: /bin/chmod
odoo ALL=(ALL) NOPASSWD: /usr/sbin/nginx
odoo ALL=(ALL) NOPASSWD: /usr/bin/tee
odoo ALL=(ALL) NOPASSWD: /usr/bin/certbot
odoo ALL=(ALL) NOPASSWD: /usr/local/bin/odoo-service-manager
odoo ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx
odoo ALL=(ALL) NOPASSWD: /usr/sbin/nginx -t
odoo ALL=(ALL) NOPASSWD: /usr/bin/rm /etc/odoo/*
"""

        # Step 1: Backup
        shutil.copy(SUDOERS_FILE, BACKUP_FILE)
        print(f"Backup saved to {BACKUP_FILE}")

        # Step 2: Copy existing content and append new rules
        with open(SUDOERS_FILE, "r") as f:
            existing = f.read()

        with open(TEMP_FILE, "w") as f:
            f.write(existing.strip() + "\n\n" + append_content.strip() + "\n")

        # Step 3: Check syntax
        if os.system(f"visudo -c -f {TEMP_FILE}") == 0:
            shutil.copy(TEMP_FILE, SUDOERS_FILE)
            print(" Updated /etc/sudoers successfully.")
        else:
            print(" Syntax error in temporary sudoers file. Aborting.")

def main():
    print_banner()
    if os.path.exists("/etc/odoo/odoo.conf"):
        response = input("Odoo is already installed. Reinstall? (y/n): ")
        if response.lower() != 'y':
            sys.exit("Aborted.")

    installer = OdooInstaller()
    installer.install()
    print("-----------------------------------------------------------------------------------------------------------")
    print("\n")
    master_password = input("===> Please enter a new password for postgres database: ")
    odoo_password = input("===> Please enter a new password for odoo user: ")
    domain = input("===> Enter your domain (e.g., echopx.org). It will be used as erpinstall.<yourdomain>: ")
    bearer_token = input("====> Enter bearer token: ")
    print("\n")
    print("-----------------------------------------------------------------------------------------------------------")
    pg = PostgresSetup(master_password, odoo_password)
    pg.setup()
    installer.restart_odoo()
    installer.change_file_permis()
    php_version = "8.1"
    tools = tools_files(php_version)
    tools.install_permission()
    data = write_data_file(domain, master_password, bearer_token)
    data.write_env()
    data.create_nginx_config()
    data.sim_link()

    # TEST nginx
    os.system("sudo nginx -t && sudo systemctl restart nginx")

    # Run certbot
    data.run_certbot()

    db_name = "instance_db"
    db = database_setup(db_name)
    db.create_database()
    try:
        # Call the function
        add_permission()
        print("** Permission's added successfully **")
    except Exception as e:
        print(f"Error Unable to add the permission's snippet to the sudoers file: {e}")

    try:
        subprocess.run("sudo chmod +x /var/www/instance/htdocs/remove_instance.py",True)
    except Exception as e:
        print(f"Error Changing mod of remove_instance.py: {e}")
    try:
        installer = Install()
        installer.Webmin()
    except Exception as e:
        print(f"Error Unable to install webmin: {e}")
    
    print("**   Odoo user created with provided password. **")
    print("**   Odoo instance installed and PostgreSQL password set. **")
    print("\n")
    print(f"Now you can access your installer at: https://erpinstall.{domain}")
    print("\n")

if __name__ == "__main__":
    main()
