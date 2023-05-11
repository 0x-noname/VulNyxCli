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

#
white = '\033[1;37m'
red = "\033[1;31m"
reset = '\033[0m'


print(white + """
                         _    __      __                    ________    ____
                        | |  / /_  __/ /___  __  ___  __   / ____/ /   /  _/
                        | | / / / / / / __ \/ / / / |/_/  / /   / /    / /  
                        | |/ / /_/ / / / / / /_/ />  <   / /___/ /____/ /   
                        |___/\__,_/_/_/ /_/\__, /_/|_|   \____/_____/___/   
                                          /____/                            
""" + reset)
print(white + "                                         Author" + reset + "  :", red + "0x-noname" + reset)
print(white + "                                         Version" + reset + " :" , red +  "1.1\n" + reset)

def colorize_level(level):
    colors = {'easy': '\033[1;32m', 'medium': '\033[1;33m', 'hard': '\033[1;31m'}
    return f"{colors.get(level.lower(), '')}{level}\033[0m"

def colorize_header(header):
    return "\033[1;37m{}\033[0m".format(header)

def show_machines(level=None, show_writeups=False, show_download=True):
    url = "https://vulnyx.com/"
    result = requests.get(url)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    machine_rows = soup.find('table').find_all('tr')[1:]
    table = PrettyTable()
    if show_writeups:
        table.field_names = [
            "\033[1;31mVMName\033[0m",
            "\033[1;31mLevel\033[0m",
            "\033[1;31mCreator\033[0m",
            "\033[1;31mWriteups\033[0m"]
    else:
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
            if show_writeups:
                writeups_column = row.find('td', class_="writeups")
                writeup_links = writeups_column.find_all('a')
                writeup_links = [f"\033[0;37m{link.get('href')}\033[0m" for link in writeup_links]
                writeup_links = '\n'.join(writeup_links) if writeup_links else "Nothing..."
                table.add_row([
                    f"\033[1;37m{vname}\033[0m",
                    colorize_level(machine_level),
                    f"\033[1;37m{creator}\033[0m",
                    f"\033[1;37m{writeup_links}\033[0m"])
            elif show_download:
                download_link = row.find('td', class_="url").find('a')['href']
                table.add_row([
                    f"\033[1;37m{vname}\033[0m",
                    colorize_level(machine_level),
                    f"\033[1;37m{creator}\033[0m",
                    f"\033[0;37m{download_link}\033[0m"])
    print(table)
    
def main():
    parser = argparse.ArgumentParser(usage='%(prog)s [--help] [--easy] [--medium] [--hard] [--all] [--write] [--info]')
    parser.add_argument('--easy', action='store_true', help='show only easy machines')
    parser.add_argument('--medium', action='store_true', help='show only medium machines')
    parser.add_argument('--hard', action='store_true', help='show only hard machines')
    parser.add_argument('--all', action='store_true', help='show all machines')
    parser.add_argument('--write', action='store_true', help='show writeups')
    parser.add_argument('--info', action='store_true', help='show tool information')
    args = parser.parse_args()


    if args.info:
        print("                        Tool created for the VulNyx community!\n")
        print(white + "                        VulNyx Web" + reset + "  :", red + "https://vulnyx.github.io/" + reset)
        print(white + "                        VulNyx Tool" + reset + " :", red + "https://github.com/0x-noname/VulNyxCli\n\n" + reset)
       
    elif args.write:
        show_machines(show_writeups=True)
    elif any([args.easy, args.medium, args.hard, args.all]):
        if args.easy:
            show_machines(level='easy', show_download=not args.all)
        if args.medium:
            show_machines(level='medium', show_download=not args.all)
        if args.hard:
            show_machines(level='hard', show_download=not args.all)
        if args.all:
            show_machines(show_download=True)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
