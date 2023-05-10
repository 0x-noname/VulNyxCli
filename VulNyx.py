#!/usr/bin/python3
from prettytable import PrettyTable
from bs4 import BeautifulSoup
import requests, os
import argparse

def c_screen_unix():
    os.system('clear')

def c_screen_windows():
    os.system('cls')

def c_screen():

    if os.name == 'posix':
        c_screen_unix()

    elif os.name == 'nt':
        c_screen_windows()
        
c_screen()

color_header = '\033[1;37m'
color_reset = '\033[0m'
print(color_header + """
 _    __      ___   __              __  ___           __    _
| |  / /_  __/ / | / /_  ___  __   /  |/  /___ ______/ /_  (_)___  ___  _____
| | / / / / / /  |/ / / / / |/_/  / /|_/ / __ `/ ___/ __ \/ / __ \/ _ \/ ___/
| |/ / /_/ / / /|  / /_/ />  <   / /  / / /_/ / /__/ / / / / / / /  __(__  )
|___/\__,_/_/_/ |_/\__, /_/|_|  /_/  /_/\__,_/\___/_/ /_/_/_/ /_/\___/____/
                  /____/  
""" + color_reset)

def colorize_level(level):
    colors = {'easy': '\033[1;32m', 'medium': '\033[1;33m', 'hard': '\033[1;31m'}
    return f"{colors.get(level.lower(), '')}{level}\033[0m"

def colorize_header(header):
    return "\033[1;37m{}\033[0m".format(header)

def show_machines(level=None):
    url = "https://vulnyx.com/"
    result = requests.get(url)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    machine_rows = soup.find('table').find_all('tr')[1:]
    table = PrettyTable()
    table.field_names = [
        "\033[1;31mVMName\033[0m",
        "\033[1;31mLevel\033[0m",
        "\033[1;31mCreator\033[0m",
        "\033[1;31mDownload\033[0m"]
    for row in machine_rows:
        vname = row.find('td', class_="vm-name").find('span').get_text()
        machine_level = row.find('td', class_="level").find('span').get_text()
        if level is None or level.lower() == machine_level.lower():
            creator_box = row.find('td', class_="creator")
            creator_link = creator_box.find('a')
            creator_span = creator_box.find('span')
            creator = creator_link.get_text() if creator_link else creator_span.get_text() if creator_span else "Unknown"
            download_link = row.find('td', class_="url").find('a')['href']
            table.add_row([
                f"\033[1;37m{vname}\033[0m",
                colorize_level(machine_level),
                f"\033[1;37m{creator}\033[0m",
                f"\033[0;37m{download_link}\033[0m"])

    print(table)

def main():
    parser = argparse.ArgumentParser(usage='%(prog)s [--help] [--easy] [--medium] [--hard] [--all] [--info]')
    parser.add_argument('--easy', action='store_true', help='show only easy machines')
    parser.add_argument('--medium', action='store_true', help='show only medium machines')
    parser.add_argument('--hard', action='store_true', help='show only hard machines')
    parser.add_argument('--all', action='store_true', help='show all machines')
    parser.add_argument('--info', action='store_true', help='show info')
    args = parser.parse_args()

    if args.info:
        print("""
    Tool created for the VulNyx community!

    VulNyx Web:   https://vulnyx.com/
    VulNyx Tool:  https://github.com/0x-noname/VulNyxCli
        """)
    elif any([args.easy, args.medium, args.hard, args.all]):
        if args.easy:
            show_machines(level='easy')
        if args.medium:
            show_machines(level='medium')
        if args.hard:
            show_machines(level='hard')
        if args.all:
            show_machines()
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()

