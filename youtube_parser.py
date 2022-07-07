import requests
from decimal import Decimal
from bs4 import BeautifulSoup

def parseSoup(soup):
    string = str(soup).split("subscriberCountText")
    subs = string[len(string)-1].split('"')[8].split(' ')
    final_number = 0
    if subs[1][0:3] == 'тыс':
        final_number = str(Decimal(subs[0].replace(',', '.')) * 1000).split('.')[0]
    elif subs[1][0:3] == 'мил':
        final_number = str(Decimal(subs[0].replace(',', '.')) * 1000000).split('.')[0]
    else:
        final_number = str(Decimal(subs[0])).split('.')[0]
    return final_number

def getNumberOfSubscribers(id):
    urls = ["https://www.youtube.com/c/MrMaxLife","https://www.youtube.com/user/PewDiePie","https://www.youtube.com/user/toplesofficial","https://www.youtube.com/user/MrLololoshka"]
    main_response = requests.get(url=urls[id])
    main_soup = BeautifulSoup(main_response.text, "html.parser")
    print(parseSoup(main_soup))
    return parseSoup(main_soup)
