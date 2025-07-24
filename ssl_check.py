import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse

websites = [
    "https://www.google.com",
    "https://arctiq.com.au",
    "https://expired.badssl.com",
]

def check_expairy(hostname, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname,port), timeout = 5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                certificate = ssock.getpeercert()
                expairy_str = certificate['notAfter']
                expairy_date = datetime.strptime(expairy_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (expairy_date - datetime.utcnow()).days
                
                print(f"[{hostname}] SSL certificate expaires on {expairy_date}. ({days_left} days left)")
                if days_left <= 14:
                    print(f"ALERT: SSL certificate for {hostname} expaires in {days_left} days!")

    except Exception as e:
        print(f"Error! Check {hostname}: {e}")
    
for site in websites:
    parsed_url = urlparse(site)
    hostname = parsed_url.hostname
    check_expairy(hostname)
