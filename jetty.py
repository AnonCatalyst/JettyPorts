import socket
import asyncio
import concurrent.futures
from tqdm import tqdm
from colorama import Fore, Style
from pprint import pprint
import random
from urllib.parse import urlparse

SUCCESS_EMOJI = "✅"
WARNING_EMOJI = "⚠️"
ERROR_EMOJI = "❌"

def scan_port(target, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except socket.error:
                    service = "Unknown"
                return port, service
    except socket.error:
        pass
    return None

async def scan_port_async(target, port, progress_bar, timeout=1):
    try:
        result = await asyncio.to_thread(scan_port, target, port, timeout)
        if result:
            print(f"{Fore.GREEN}{SUCCESS_EMOJI} Port {result[0]} is open. Service: {result[1]}{Style.RESET_ALL}")
            return result
        return None
    except KeyboardInterrupt:
        raise KeyboardInterrupt

async def port_scan_async(target, start_port=1, end_port=65535, timeout=1):
    open_ports = []
    progress_bar = tqdm(total=end_port - start_port + 1, desc=f"{Fore.WHITE}Scanning Ports{Style.RESET_ALL}", unit="port")
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        loop = asyncio.get_event_loop()
        for port in range(start_port, end_port + 1):
            task = loop.create_task(scan_port_async(target, port, progress_bar, timeout))
            task.add_done_callback(lambda future: progress_bar.update(1))
            tasks.append(task)
        try:
            for future in asyncio.as_completed(tasks):
                result = await future
                if result:
                    open_ports.append(result)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}{WARNING_EMOJI} Scan stopped by user.{Style.RESET_ALL}")
            raise KeyboardInterrupt
        finally:
            progress_bar.close()
    return open_ports

def parse_target(target):
    if "://" not in target:
        target = "http://" + target
    parsed_url = urlparse(target)
    return parsed_url.netloc

if __name__ == "__main__":
    print(f"\n{Fore.WHITE}🔍 Welcome to JettyPorts! 🔍{Style.RESET_ALL}")
    target_input = input(f"{Fore.WHITE}Enter the target IP address, hostname, or domain: {Style.RESET_ALL}")

    target = parse_target(target_input)

    try:
        open_ports = asyncio.run(port_scan_async(target))
    except KeyboardInterrupt:
        raise KeyboardInterrupt

    print(f"{Fore.CYAN}══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🎉 Scan complete. Open ports: 🎉{Style.RESET_ALL}")
    if open_ports:
        print(f" {Fore.GREEN}🎉 Open ports found: 🎉{Style.RESET_ALL}")
        pprint(open_ports, indent=4, width=40)
        print(f"{Fore.GREEN}🎉 Total open ports found: {len(open_ports)} 🎉{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{ERROR_EMOJI} No open ports found on the target.{Style.RESET_ALL}")
