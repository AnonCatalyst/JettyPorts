# JettyPorts - Network Port Scanner

JettyPorts is a Python script designed to scan a target for open ports on a network. It utilizes asynchronous programming to improve scanning efficiency.

## Features

- **Asynchronous Port Scanning**: Utilizes asyncio to scan multiple ports concurrently, improving performance.
- **User-Friendly Interface**: Simple command-line interface with prompts for target input.
- **Keyboard Interrupt Handling**: Gracefully handles interruptions, allowing users to stop the scan if needed.
- **Port Identification**: Identifies services running on open ports when possible.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AnonCatalyst/JettyPorts
   ```

2. Install dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python3 jetty.py
   ```

2. Enter the target IP address, hostname, or domain when prompted.

3. Wait for the scan to complete.

4. View the results:
   - Open ports and corresponding services are displayed.
   - If no open ports are found, a message notifies the user.

## Customization

- **Timeout**: Adjust the timeout duration for port scanning by modifying the `timeout` parameter in the `port_scan_async` function.
- **Port Range**: Modify the `start_port` and `end_port` parameters in the `port_scan_async` function to specify a custom port range.
