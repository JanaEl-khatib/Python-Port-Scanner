# Used to create connections and interact with ports
import socket
# Used to run multiple scans at the same time
import threading

# Lock to prevent threads from printing over each other at the same time
print_lock = threading.Lock()

def scan_port(target_ip, port):
    try:
        # Create a socket object (IPv4, stream-based)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # 1-second timeout

        # Try connection to the port
        result = sock.connect_ex((target_ip, port)) # 0 = success

        # Using the lock so only one thread prints at a time
        with print_lock:
            if result == 0:
                print(f"[+] Port {port} is OPEN on {target_ip}")
            else:
                print(f"[-] Port {port} is CLOSED on {target_ip}")
        # Closes the socket
        sock.close()

    except socket.error:
        # If the socket fails to connect
        with print_lock:
            print(f"[!] Couldn't connect to {target_ip}")

# Function to prompt the user and run the scan
def run_scanner():
    # Asks the user for the IP or hostname
    target = input("Enter the IP address or hostname to scan: ")

    # Convert hostname to IP address
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Scanning host: {target_ip}")
    except socket.gaierror:
        print("Hostname could not be resolved.")
        return
    
    # List to keep track of all the threads
    threads = []
    
    # Define ports to scan and loops through them
    for port in range(1, 1025): # Common ports
        # Create a new thread to scan each port
        thread = threading.Thread(target=scan_port, args=(target_ip, port))
        # Keep track of the thread
        threads.append(thread)
        # Start scanning
        thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    run_scanner()