import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
from urllib.parse import urlparse


# Set up a session with retries
def get_session_with_retries(retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


session = get_session_with_retries()


# Sanitize the domain input
def sanitize_domain(domain):
    parsed = urlparse(domain)
    return parsed.netloc or parsed.path


# Fetch URLs from the Wayback Machine
def fetch_urls_from_wayback(domain):
    print("[*] Fetching URLs from Wayback Machine...")
    urls = []
    page = 0
    while True:
        wayback_url = (
            f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&collapse=urlkey&page={page}"
        )
        try:
            response = session.get(wayback_url, timeout=20)  # Increased timeout
            response.raise_for_status()
            data = response.json()

            if len(data) <= 1:  # No more data
                break

            page_urls = [row[1] for row in data[1:]]  # Extract URLs from JSON
            urls.extend(page_urls)
            print(f"[+] Fetched {len(page_urls)} URLs from page {page}...")
            page += 1
        except requests.exceptions.Timeout:
            print(f"[!] Timeout fetching Wayback Machine page {page}. Retrying...")
            continue
        except requests.exceptions.RequestException as e:
            print(f"[!] Error fetching from Wayback Machine on page {page}: {e}")
            break
    return urls


# Fetch URLs from Common Crawl
def fetch_urls_from_commoncrawl(domain):
    print("[*] Fetching URLs from Common Crawl...")
    urls = []
    cc_indexes = [
        "CC-MAIN-2023-10-index",
        "CC-MAIN-2023-06-index",
        "CC-MAIN-2023-02-index",
    ]

    for index in cc_indexes:
        cc_url = f"https://index.commoncrawl.org/{index}?url={domain}/*&output=json"
        try:
            response = session.get(cc_url, timeout=15)
            response.raise_for_status()
            data = response.json()

            index_urls = [row["url"] for row in data]
            urls.extend(index_urls)
            print(f"[+] Fetched {len(index_urls)} URLs from {index}...")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"[!] No data in index {index} for domain {domain}.")
            else:
                print(f"[!] HTTP error for index {index}: {e}")
        except requests.exceptions.Timeout:
            print(f"[!] Timeout for index {index}. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"[!] Error fetching from Common Crawl index {index}: {e}")
    return urls


# Save results to a file
def save_to_file(urls, filename="urls.txt"):
    try:
        with open(filename, "w") as file:
            for url in urls:
                file.write(url + "\n")
        print(f"[*] Results saved successfully to {filename}.")
    except Exception as e:
        print(f"[!] Error saving to file: {e}")


# Main function
def main():
    domain = input("Enter the domain (e.g., example.com): ").strip()
    sanitized_domain = sanitize_domain(domain)
    print(f"[+] Sanitized domain: {sanitized_domain}")

    all_urls = []

    # Fetch from Wayback Machine
    wayback_urls = fetch_urls_from_wayback(sanitized_domain)
    all_urls.extend(wayback_urls)

    # Fetch from Common Crawl
    commoncrawl_urls = fetch_urls_from_commoncrawl(sanitized_domain)
    all_urls.extend(commoncrawl_urls)

    # Remove duplicates
    all_urls = list(set(all_urls))

    if all_urls:
        print(f"[+] Total unique URLs found: {len(all_urls)}")
        save_to_file(all_urls)
    else:
        print("[!] No URLs found. Try another domain or check API availability.")


if __name__ == "__main__":
    main()
