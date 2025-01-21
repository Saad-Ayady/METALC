import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from colorama import Fore, Style, init
import sys
import argparse
import os


user_agent_string = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0"
headers: dict[str, str] = {'User-Agent': user_agent_string}
init()
bold_text = Style.BRIGHT
res_bold_text = Style.RESET_ALL
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
panel = (f"""{bold_text}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡟⠀⠀⠀⣠⢠⣤⣤⣤⣤⣤⣤⣤⣤⣄⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡄⢠⣤⣤⣤⣤⢠⣤⣤⣤⣤⠀⠀⠀⠀⠀⣤⣤⣤⣤⠀⠀⠀⠀⢠⣤⣤⣤⣄⠀⠀⠀⠀⣀⣠⣤⣤⣀⡀⠀⠀⢾⣿⣿⣿⡟⠷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠋⣹⣿⡟⠀⢀⣤⣾⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⡷⠂⢹⣿⣿⣿⣿⡄⠀⠙⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠁⠀⣸⣿⣿⣧⣴⣿⣿⣿⣿⢸⣿⣿⣿⣟⣛⣛⣛⣛⡟⠛⠛⣿⣿⣿⣿⠛⠛⠛⢁⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠈⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⢰⣿⣿⣿⣿⡿⠿⠿⡿⠋⠀⠀⢸⣿⣿⡽⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⢈⣿⣿⣿⣿⠀⠀⢀⣾⣿⣿⣋⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⠟⣿⣿⢻⣿⣿⣿⣿⢸⣿⣿⣿⠿⠿⠿⠿⠿⡇⠀⢈⣿⣿⣿⣿⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⢠⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⢿⣿⣿⣿⣧⣄⣀⣀⣼⣦⣄⠀⢸⣿⣿⣿⡿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⡏⠀⠸⠃⣼⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⢨⣿⣿⣿⣿⠀⣼⣿⣿⣿⡿⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠖⣿⣿⣿⡆⠀⠹⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⡟⠀⠀⠀⠀⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡅⠀⠨⣿⣿⣿⣿⣼⣿⣿⣿⡿⠁⢸⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠙⠻⢿⣿⣿⣿⡿⠟⠋⠁⠀⣿⣿⣿⣧⠀⠀⢻⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⡿⠀⠀⠀⠀⢰⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⠀⠀⠀⢿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⠁⠀⠀⠀⠀⢸⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⡇⠀⠀⠀⢿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⠇⠀⠀⠀⠀⢀⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⠀⠀⠀⠘⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  {red}[Coded BY] : {blue}Said Ayady ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⠀⠀⠀⠀⠀⠀   ⠀⠘⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡟⠀⠀⣀⠔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        {red}[FOLLOW ME IN INSTAGRAM] :⠀{blue}Saad__dy⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀   ⠀⠀⠀⠑⢦⣀⠀⠀⠹⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡟⣀⣴⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠷⣦⣄⠹⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣰⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣆⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣦⠀⠀⠀
⠀⠀⣴⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣦⠀⠀
⠀⣼⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣧⠀
⠜⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳
    {res_bold_text}""")
def check_is_run(url, cookies=None) -> None:
    try :
        re = requests.get(url=url, headers=headers, cookies=cookies)
        return 1
    except:
        return 0

def read_file_lines(file_path):
    lines = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                lines.append(line.strip())
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    return lines

def creat_urls_to_bred_fors(url, wordList) :
    if not "FUZZINTHISPARTPLZ" in url :
        return 0
    arr = read_file_lines(wordList)
    uarr = []
    for i in arr :
        newURL = url.replace("FUZZINTHISPARTPLZ", i)
        uarr.append(newURL)
    return uarr

def brud_fors(url: str, wordList: str, cookies=None):
    urls = creat_urls_to_bred_fors(url=url, wordList=wordList)
    if not urls:
        return {}
    dec_url = {}      
    for i in urls:
        try:
            re = requests.get(url=i, headers=headers, cookies=cookies)
            dec_url[i] = re.status_code
        except Exception as e:
            continue
    return dec_url

def print_Work(url, word, isSave, filename, cookies=None):
    links = brud_fors(url, word, cookies=cookies)
    if isSave:
        try:
            with open(filename, 'w') as file:
                for li, sc in links.items():
                    file.write(f"{li} [{sc}]\n")
        except Exception as e:
            print(f"Error saving to file: {e}")
    else:
        # If isSave is False, just print the links
        for li, sc in links.items():
            print(f"{li} [{sc}]")


def cearling_all_links(url, cookies=None):
    urls = []
    try:
        re = requests.get(url=url, headers=headers, cookies=cookies)
        re.raise_for_status()  # Ensure we handle unsuccessful responses
        soup = BeautifulSoup(re.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href') 
            if href: 
                full_url = urljoin(url, href)
                urls.append(full_url)
        for link in soup.find_all('link'):
            href = link.get('href') 
            if href: 
                full_url = urljoin(url, href)
                urls.append(full_url)
    except requests.exceptions.RequestException as e:
        pass
    return urls

def get_js_links(url, cookies=None):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        js_links = []
        for script in soup.find_all('script', src=True):
            js_url = script.get('src')
            full_js_url = urljoin(url, js_url)
            js_links.append(full_js_url)
        return js_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

def unaq(lines) :
    if not lines:
        return []

    result = [lines[0]]  # Always include the first line
    for i in range(1, len(lines)):
        if lines[i] != lines[i - 1]:
            result.append(lines[i])

    return result

def fulter_link(url, cookies=None) :
    url = cearling_all_links(url, cookies=cookies)
    urls= []
    c = []
    for i in url:
        urli = cearling_all_links(i, cookies=cookies)
        urls.append(urli)
    for j in urls :
        for x in j :
            c.append(x)
    return unaq(c)

def extract_links_from_js(js_url, cookies=None):
    try:
        response = requests.get(js_url, cookies=cookies)
        response.raise_for_status() 
        js_content = response.text
        url_pattern = r'https?://[^\s\'"()<>]+'
        extracted_links = re.findall(url_pattern, js_content)
        unique_links = list(set(extracted_links))
        return unique_links
    except requests.exceptions.RequestException as e:
        return []
    except Exception as e:
        return []

def allJs(url, cookies=None) :
    jsLink = get_js_links(url, cookies=cookies)
    all_re = []
    for js in jsLink :
        c = extract_links_from_js(js, cookies=cookies)
        for cs in c :
            all_re.append(cs)
    return all_re

# print("[Crawlink HMTL link]")
# x = fulter_link("https://myaccount.google.com/?pli=1")
# for xs in x :
#     print(xs)
# print("[Crawlink JS link]")
# j = allJs("https://myaccount.google.com/?pli=1")
# for xs in j :
#     print(xs)
# print("[Crawlink brud_fors link]")
# print_Work("https://myaccount.google.com/FUZZINTHISPARTPLZ",".word.txt")

# color_text("red", "said")

def save_links_to_file(links, filename):
    try:
        with open(filename, 'a') as file:
            for link in links:
                file.write(link + '\n')
        print(f"{bold_text}{green}[Links saved to {filename}]{res_bold_text}")
    except Exception as e:
        print(f"{red}{bold_text}Error saving to file: {e}{res_bold_text}")


def help_func():
    print(f"""{bold_text}
    Usage:
      -u  or --url   <URL>          Specify the URL for testing.
      -b  or --bread                 Call the brute force function.
      -w  or --word  <wordlist>      Specify the path to the wordlist.
      -o  or --output <FileSaving>   Output file to save links.
      -c  or --cook <Cookies>        Specify cookies for the crawling process.
      -h  or --help                  Show this help message.
    {res_bold_text}""")

def main():
    parser = argparse.ArgumentParser(description="Script to handle URL testing with Crawling")
    
    # Arguments
    parser.add_argument('-u', '--url', type=str, help='URL to test')
    parser.add_argument('-b', '--bread', action='store_true', help='Call brute force function')
    parser.add_argument('-w', '--word', type=str, help='Path to wordlist for brute force')
    parser.add_argument('-o', '--output', type=str, help='Output file to save links')
    parser.add_argument('-c', '--cook', type=str, help='Cookies for the crawling process')
    args = parser.parse_args()
    cookies = None
    if args.cook:
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in args.cook.split(';')}
    
    if args.url:
        url = args.url
        if check_is_run(url, cookies) != 1 :
            print(f"{red}{bold_text}[URL NOT WORKING]{res_bold_text}")
            os.exit(1)
        print(panel)
        print(f"\n{bold_text}{yellow}[{red}Crawling HMTL link{yellow}]{res_bold_text}")
        print(f"{blue}{bold_text}--------------------{res_bold_text}")
        x = fulter_link(url, cookies)
        if args.output:
            save_links_to_file(x, args.output)
        for xs in x :
            print(xs)
        print(f"\n{bold_text}{yellow}[{red}Crawling JS link{yellow}]{res_bold_text}")
        print(f"{blue}{bold_text}--------------------{res_bold_text}")
        j = allJs(url, cookies)
        if args.output:
            save_links_to_file(j, args.output)
        for xs in j :
            print(xs)
    
    if args.bread:
        if args.word :
            if os.path.exists(args.word):
                word_list = args.word
            else :
                print(f"{bold_text}{red}Ur WordList Not Fond i Use MY word list{res_bold_text}")
                word_list = "src/.word.txt"
        else :
            word_list = "src/.word.txt"
        print(f"\n{bold_text}{yellow}[{red}Crawling brud_fors link{yellow}]{res_bold_text}")
        print(f"{bold_text}{blue}---------------------------{res_bold_text}")
        if args.output:
            print_Work(f"{url}FUZZINTHISPARTPLZ",word_list, True, args.output, cookies)
        else :
            print_Work(f"{url}FUZZINTHISPARTPLZ",word_list, False, "blablaHH", cookies)

    if args.url is None and args.bread is False and args.word is None:
        help_func()

if __name__ == '__main__':
    try :
        main()
    except KeyboardInterrupt:
        print(f"{bold_text}{blue}GOOD BAY BRO (-_-).{res_bold_text}")
        exit(0)
