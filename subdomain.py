import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def resolve_subdomain(subdomain, domain):
    try: 
        full_domain = f"{subdomain}.{domain}"
        ip = socket.gethostbyname(full_domain)
        return full_domain, ip
    except socket.gaierror:
        return None

def load_wordlist(filepath):
    try:
        with open(filepath, "r") as file:
            return [line.strip() for line in file if [line.strip()]]
    except FileNotFoundError:
        print(f"ERROR: Wordlist file '{filepath}' is not correct.")
        exit(1)

def enumerate_subdomain(domain, wordlist, threads=10):
    subdomains = []
    print(f"Starting subdomain enumeration on {domain} ")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(resolve_subdomain, sub, domain) for sub in wordlist]
        for future in futures:
            result = future.result()
            if result:
                subdomains.append(result)
    return subdomains

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration")
    parser.add_argument("domain", help="Target Domain -> ex: google.com")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to subdomain")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    args = parser.parse_args()
    
    wordlist = load_wordlist(args.wordlist)
    
    results = enumerate_subdomain(args.domain, wordlist, args.threads)
    
    print("\nDiscovered Subdomains: ")
    for subdomain, ip in results:
        print(f"{subdomain}, -> {ip}")
        
if __name__ == "__main__":
    main()