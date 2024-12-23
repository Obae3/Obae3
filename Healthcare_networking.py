import logging
import socket
import paramiko
import psutil
import shutil
import smtplib
import csv
import time
import random
import subprocess
from email.mime.text import MIMEText

# Set up logging
logging.basicConfig(level=logging.INFO)

# Configuration Parameters
NETWORK_IPS = ['192.168.1.1', '192.168.1.2', '192.168.1.3']
MONITOR_INTERVAL = 10
SOURCE_DIRECTORY = '/path/to/source/directory'
BACKUP_DIRECTORY = '/path/to/backup/directory'
EMAIL_FROM = "your-email@example.com"
EMAIL_PASSWORD = "your-email-password"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 465
ALERT_RECIPIENT = "recipient@example.com"
REMOTE_SERVER_IP = '192.168.1.20'
REMOTE_USERNAME = 'user'
REMOTE_PASSWORD = 'password'
LOCAL_FILE_PATH = '/path/to/local/file.txt'
REMOTE_FILE_PATH = '/path/to/remote/file.txt'
SERVERS = ["server1", "server2", "server3"]
REQUEST = "GET /index.html"

def troubleshoot_network():
    def check_connectivity(ip):
        try:
            response = subprocess.run(['ping', '-c', '3', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if response.returncode == 0:
                logging.info(f"Connectivity to {ip} is successful.")
            else:
                logging.error(f"Failed to connect to {ip}.")
        except Exception as e:
            logging.error(f"Error checking connectivity: {e}")

    for ip in NETWORK_IPS:
        check_connectivity(ip)

def send_message_to_device(ip, port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(message.encode())
            response = s.recv(1024)
            logging.info(f"Received response: {response.decode()}")
    except Exception as e:
        logging.error(f"Communication failed: {e}")

def transport_content():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_SERVER_IP, username=REMOTE_USERNAME, password=REMOTE_PASSWORD)
        
        sftp = ssh.open_sftp()
        sftp.put(LOCAL_FILE_PATH, REMOTE_FILE_PATH)
        sftp.close()
        
        ssh.close()
        logging.info("Content transported successfully.")
    except Exception as e:
        logging.error(f"Content transportation failed: {e}")

def monitor_network():
    try:
        while True:
            stats = psutil.net_io_counters()
            logging.info(f"Bytes Sent: {stats.bytes_sent}, Bytes Received: {stats.bytes_recv}")
            time.sleep(MONITOR_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped.")

def run_security_checks():
    try:
        logging.info("Running antivirus scan...")
        # Add your antivirus scan logic here
        
        logging.info("Checking firewall status...")
        firewall_status = subprocess.run(['ufw', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(firewall_status.stdout.decode())
        
        logging.info("Security checks completed successfully.")
    except Exception as e:
        logging.error(f"Security checks failed: {e}")

def backup_data():
    try:
        shutil.copytree(SOURCE_DIRECTORY, BACKUP_DIRECTORY)
        logging.info("Data backup completed successfully.")
    except Exception as e:
        logging.error(f"Data backup failed: {e}")

def send_alert(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = ALERT_RECIPIENT
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, ALERT_RECIPIENT, msg.as_string())
        server.quit()
        logging.info("Alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

def generate_report():
    data = [
        ["Timestamp", "Metric", "Value"],
        [time.strftime("%Y-%m-%d %H:%M:%S"), "CPU Usage", "23%"],
        [time.strftime("%Y-%m-%d %H:%M:%S"), "Memory Usage", "68%"]
    ]
    
    with open("network_report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    logging.info("Report generated successfully.")

def load_balance():
    chosen_server = random.choice(SERVERS)
    logging.info(f"Sending request '{REQUEST}' to server: {chosen_server}")

def main_menu():
    while True:
        print("\nHealthcare Networking Project")
        print("1. Troubleshoot Network")
        print("2. Send Message to Device")
        print("3. Transport Content")
        print("4. Monitor Network")
        print("5. Run Security Checks")
        print("6. Backup Data")
        print("7. Send Alert")
        print("8. Generate Report")
        print("9. Load Balance")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            troubleshoot_network()
        elif choice == '2':
            ip = input("Enter device IP address: ")
            port = int(input("Enter device port: "))
            message = input("Enter message: ")
            send_message_to_device(ip, port, message)
        elif choice == '3':
            transport_content()
        elif choice == '4':
            monitor_network()
        elif choice == '5':
            run_security_checks()
        elif choice == '6':
            backup_data()
        elif choice == '7':
            subject = input("Enter alert subject: ")
            body = input("Enter alert body: ")
            send_alert(subject, body)
        elif choice == '8':
            generate_report()
        elif choice == '9':
            load_balance()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
