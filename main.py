from bs4 import BeautifulSoup
import requests
import re
import urllib.parse
import os
from colorama import Fore, init
init(autoreset=True)


bracketColor = Fore.MAGENTA
numberColor = Fore.BLUE
resetColor = Fore.RESET

def get_magnet(url):
    anime_res =  requests.get(url)
    anime_bs = BeautifulSoup(anime_res.text, "html.parser")
    m_link = anime_bs.find_all('a', {'href': re.compile(r'magnet:\?xt=urn:btih:[a-zA-Z0-9]*')})
    return m_link[0]['href']

def take_input(text, min, max):
    while True:
        try:
            result = int(input(text))
            if result < int(min):
                print("Value too small.")
            elif result > int(max):
                print("Value too big.")
            else:
                break
        except ValueError:
            print("Invalid Input")
    return result

def main():
    query = input("Search Anime: ")
    if len(query.split(' ')) > 1:
        query = "+".join(query.split(" "))


    url = f"https://1337x.wtf/category-search/{query}/Anime/1/"
    res = requests.get(url)
    bs = BeautifulSoup(res.text, "html.parser")

    animes = bs.find_all('a', {'href': re.compile(r'torrent\/[0-9]{7}\/[a-zA-Z0-9?%-]*/')})
    if len(animes) > 10:
        animes = animes[:10]

    for index, anime in enumerate(animes):
        if index % 2 == 0:
            titleColor = Fore.YELLOW
        else:
            titleColor = Fore.WHITE

        print(f"{bracketColor}[{numberColor}{index}{bracketColor}]{resetColor} {titleColor}{anime.text}")

    anime_number = int(take_input(">>> ", 0, len(animes)))
    selected_anime_title = animes[anime_number].text
    selected_anime_link = animes[anime_number]['href']

    magnet_link = get_magnet(urllib.parse.urljoin("https://1337x.wtf/", selected_anime_link))

    print(magnet_link)
    os.system(f"peerflix -k {magnet_link}")

if __name__ == "__main__":
    main()
