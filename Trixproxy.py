import random
from concurrent.futures import ThreadPoolExecutor
from pyfiglet import Figlet
from termcolor import colored

def generate_proxy(ip_range, port_range, proxy_type):
    ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))
    port = random.randint(port_range[0], port_range[1])
    proxy = f"{ip_address}:{port}"
    return proxy

def generate_proxies(num_proxies, proxy_type, num_threads):
    proxies = []

    # Define IP and port ranges based on proxy type
    ip_range = (0, 255)
    port_range = (1024, 65535)

    # Use ThreadPoolExecutor for concurrent proxy generation
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(generate_proxy, ip_range, port_range, proxy_type) for _ in range(num_proxies)]
        proxies = [future.result() for future in futures]

    # Save proxies to a file
    filename = f"proxies_{proxy_type}.txt"
    with open(filename, 'w') as file:
        for proxy in proxies:
            file.write(f"{proxy}\n")

    print(f"{num_proxies} {proxy_type} proxies generated and saved in {filename}.")
    print("Proxy generation complete.")

    return proxies, filename

def display_proxy_options():
    print("Proxy Types:")
    print("1 = HTTP")
    print("2 = HTTPS")
    print("3 = SOCKS4")
    print("4 = SOCKS5")
    print("00 = Back")

def print_banner():
    f = Figlet(font='block')
    banner_text = f.renderText('Trix Proxies')
    colorful_banner = colored(banner_text, 'cyan')
    print(colorful_banner)

def main():
    print_banner()

    num_proxies = int(input("Enter the number of proxies to generate: "))

    while True:
        display_proxy_options()
        choice = input("Enter the number for the type of proxy: ")

        if choice == "00":
            print("Going back.")
            return
        elif choice in {"1", "2", "3", "4"}:
            proxy_type = {'1': 'HTTP', '2': 'HTTPS', '3': 'SOCKS4', '4': 'SOCKS5'}[choice]
        else:
            print("Invalid choice. Please select a valid option.")
            continue

        num_threads = int(input("Enter the number of threads for concurrent proxy generation: "))

        proxies, filename = generate_proxies(num_proxies, proxy_type, num_threads)

if __name__ == "__main__":
    main()
