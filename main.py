import contextlib
from difflib import SequenceMatcher
from senpy import GogoClient
from InquirerPy import prompt  # pip install InquirerPy
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
from colorama import Fore, init  # pip install colorama
from senpy import __version__
from plyer import notification  # pip install plyer
from pathlib import Path
from io import StringIO
import subprocess
import time
import sys
import re

init(autoreset=True)
client = GogoClient()


def header() -> None:
    """Prints the header of the application. Took a long time to style not gonna lie xD"""
    client.utils.clear()
    print(f"""
    \t\t{Fore.WHITE} _____           {Fore.LIGHTBLUE_EX}________   __
    \t\t{Fore.WHITE}/  ___|          {Fore.LIGHTBLUE_EX}| ___ \ \ / /
    \t\t{Fore.WHITE}\ `--. {Fore.GREEN} ___ {Fore.RED}_ __ {Fore.LIGHTBLUE_EX}| |_/ /\ V / 
    \t\t{Fore.WHITE} `--. \{Fore.GREEN}/ _ \{Fore.RED} '_ \{Fore.YELLOW}|  __/  \ /  
    \t\t{Fore.WHITE}/\__/ /{Fore.GREEN}  __/{Fore.RED} | | {Fore.YELLOW}| |     | |  
    \t\t{Fore.WHITE}\____/ {Fore.GREEN}\___|{Fore.RED}_| |_{Fore.YELLOW}\_|     \_/ {Fore.WHITE}v{__version__}  

\t      {Fore.GREEN}Developers: {Fore.WHITE}FireHead90544 {Fore.RED}& {Fore.YELLOW}Arctic4161
{Fore.YELLOW} _____________________________________________________________                             
{Fore.BLUE} _____  ___  _____   {Fore.CYAN}___ _____ _ __  __   ___________ ________ 
{Fore.BLUE} |__||\ |||\/||___   {Fore.CYAN}|  \|  || | ||\ ||   |  ||__||  \|___|__/ 
{Fore.BLUE} |  || \|||  ||___   {Fore.CYAN}|__/|__||_|_|| \||___|__||  ||__/|___|  \ 
{Fore.YELLOW} _____________________________________________________________
                                                                
    """)


def home():
    """
    The home-something of this application, all the cool stuff happens here.
    """
    header()
    questions = [
        {
            "type": "list",
            "name": "action",
            "message": "Select an action: ",
            "choices": [
                Choice(download_anime, name="Download an Anime"),
                Choice(batch_download_anime, name="Batch Download Anime"),
                Choice(update_configs, name="Update Config File"),
                Choice(sys.exit, name="Exit")
            ]
        }
    ]
    result = prompt(questions=questions, style=client.config.stylesheet)
    result['action']()


def update_configs():
    header()
    questions = [
        {
            "type": "list",
            "name": "action",
            "message": "Select an action: ",
            "choices": [
                Choice(update_email, name="Enter Email Address"),
                Choice(update_pass, name="Update Password"),
                Choice(update_download_directory, name="Downloads Directory"),
                Choice(update_aria_file_path, name="Aria2 Path"),
                Choice(batch_download, name="Set Batch download Option?"),
                Choice(mal_username, name="Set MAL username"),
                Choice(mal_status, name="Set MAL download status"),
                Choice(dub_sub, name="Set MAL Dub or Sub for batch download"),
                Choice(batch_qual, name="Set Quality for batch download"),
                Choice(update_max_concurrent_downloads, name="Max Concurrent Downloads"),
                Choice(write_file, name="Write to File"),
                Choice(home, name="Back")
            ]
        }
    ]
    answers = prompt(questions=questions, style=client.config.stylesheet)
    answers['action']()


def update_email() -> None:
    """
    Updates the config file and it's contents in a cool way, sheeeeeeeeesh :)
    """
    header()
    print(f"{Fore.GREEN}>>> Update Email... Current Email: {Fore.WHITE}{client.config.loaded_config['EMAIL']}")
    questions = [
        {
            "type": "input",
            "message": "Enter your gogoanime-registered email:",
            "name": 'EMAIL',
            "validate": lambda result: bool(re.match(
                r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$",
                result)),
            "invalid_message": "Invalid email address."}]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['EMAIL'] = results['EMAIL']
    update_configs()


def update_pass():
    header()
    print(f"{Fore.GREEN}>>> Update Password...")
    questions = [
        {
            "type": "password",
            "message": "Enter the password associated with the email:",
            "name": "PASSWORD",
            "transformer": lambda _: "[hidden]",
            "validate": lambda result: len(result) > 0,
            "invalid_message": "Input cannot be empty."
        }]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['PASSWORD'] = results['PASSWORD']
    update_configs()


def update_download_directory():
    header()
    print(
        f"{Fore.GREEN}>>> Update Download Directory... Current path: {Fore.WHITE}{client.config.loaded_config['DOWNLOADS_DIR']}")
    questions = [
        {
            "type": "filepath",
            "message": "Enter the path to the anime downloads directory:",
            "validate": PathValidator(is_dir=True, message="Input is not a directory"),
            "name": "downloads_dir",
            "only_directories": True,
        }]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['DOWNLOADS_DIR'] = results['downloads_dir']
    update_configs()


def update_aria_file_path():
    header()
    print(
        f"{Fore.GREEN}>>> Update Aria2 Binary Path... Current path: {Fore.WHITE}{client.config.loaded_config['ARIA_2_PATH']}")
    questions = [
        {
            "type": "filepath",
            "message": "Enter the path to aria2's executable:",
            "name": "aria_2_path",
            "validate": PathValidator(is_file=True, message="Input is not a file"),
            "only_files": True,
        }]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['ARIA_2_PATH'] = results['aria_2_path']
    update_configs()


def batch_download():
    header()
    print(
        f"{Fore.GREEN}>>> Do you want to use MAL or Anitaku bookmarks to batch download?")
    questions = [
        {
            "type": "confirm",
            "name": "batch_dl_mal",
            "message": "Y to use an MAL file to batch download, N will "
                       "set it to use Anitaku bookmarks.",
            "default": True
        }]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['BATCH_DOWNLOAD_MAL'] = results['batch_dl_mal']
    if results['batch_dl_mal'] is True:
        if 'MAL_USERNAME' not in client.config.config_updates:
            mal_username()
    else:
        update_configs()


def mal_username():
    header()
    print(f"{Fore.GREEN}>>> Enter MAL username")
    questions = [
        {
            "type": "input",
            "message": "Enter your username",
            "name": "MAL_USERNAME",
            "validate": lambda result: len(result) > 0,
            "invalid_message": "Input cannot be empty."
        }]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['MAL_USERNAME'] = results['MAL_USERNAME']
    if 'status' not in client.config.config_updates:
        mal_status()
    else:
        update_configs()


def mal_status():
    header()
    print(f"{Fore.GREEN}>>> Select MAL status to download")
    header()
    questions = [
        {
            "type": "list",
            "name": "status",
            "message": "Select a MAL status ",
            "choices": [
                Choice("Currently Watching", name="Currently Watching"),
                Choice("Completed", name="Completed"),
                Choice("On Hold", name="On Hold"),
                Choice("Dropped", name="Dropped"),
                Choice("Plan to Watch", name="Plan to Watch"),
                Choice("All Animes", name="All Animes")
            ]
        }
    ]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['STATUS'] = results['status']
    if 'dub' not in client.config.config_updates:
        dub_sub()
    else:
        update_configs()


def dub_sub():
    header()
    print(f"{Fore.GREEN}>>> Select Dub or Sub to batch download")
    header()
    questions = [
        {
            "type": "list",
            "name": "dub",
            "message": "Select dub or sub to batch download",
            "choices": [
                Choice("Dub", name="Dub"),
                Choice("Sub", name="Sub"),
            ]
        }
    ]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['DUB'] = results['dub']
    update_configs()


def batch_qual():
    header()
    print(f"{Fore.GREEN}>>> Select Quality for batch download")
    header()
    questions = [
        {
            "type": "list",
            "name": "QUALITY",
            "message": "Select quality for batch download",
            "choices": [Choice(360, name="360p"), Choice(480, name="480p"), Choice(720, name="720p"),
                        Choice(1080, name="1080p")]
        }
    ]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['QUALITY'] = results['QUALITY']
    update_configs()


def update_max_concurrent_downloads():
    header()
    print(
        f"{Fore.GREEN}>>> Update Max Concurrent Downloads... Currently: {Fore.WHITE}"
        f"{client.config.loaded_config['MAX_CONCURRENT_DOWNLOADS']}")
    questions = [
        {
            "type": "number",
            "message": "Enter the max concurrent downloads allowed:",
            "name": "max_concurrent_downloads",
            "min_allowed": 1,
            "default": client.config.max_concurrent_downloads,
            "max_allowed": 16,  # Choose higher on your on risk man :skull:
            "validate": lambda result: result.isdigit(),
            "invalid_message": "Input must be an integer and cannot be empty."
        }]
    results = prompt(questions=questions, style=client.config.stylesheet)
    client.config.config_updates['MAX_CONCURRENT_DOWNLOADS'] = results['max_concurrent_downloads']
    update_configs()


def write_file():
    header()
    print(f"{Fore.GREEN}>>> Write to Config File?...")
    questions = [
        {
            "type": "confirm",
            "name": "proceed",
            "message": "Are you sure you want to update the config file?",
            "default": True
        }]
    write_file.results = prompt(questions=questions, style=client.config.stylesheet)
    if write_file.results['proceed']:
        client.config.write_config(client.config.config_updates)
        client.config.config_updates = {}
        print(f"{Fore.GREEN}>>> Config file updated successfully.")
        client.utils.sleep(3)
    home()


def do_pre_checks() -> None:
    """
    Just checks to make sure the dependencies are present in the device
    and everything's okay, and prevents the program for running until everything's ok.
    """
    # Checking the aria2 installation
    try:
        old = sys.stdout
        sys.stdout = StringIO()
        subprocess.call([client.config.aria_2_path])
        sys.stdout = old
    except Exception:
        client.config.logger.critical("Aria2 is not found, update the config file, if required.")
        print(
            f"{Fore.RED}>>> Aria2 Not found, please install it and try again or Update it's path in config file, "
            f"if haven't.")
        client.utils.sleep(5)
        header()

    # Checking if the downloads directory exists
    try:
        if not client.config.downloads_dir.exists():
            print(f"{Fore.RED}>>> Downloads directory does not exists, please create it, or update the config file.")
            client.config.logger.critical(
                "Downloads directory does not exists, please create it, or update the config file.")
            client.utils.sleep(5)
            header()
    except Exception as e:
        client.config.logger.critical(f"Downloads directory does not exists, an error occured, Error: {e}")
        sys.exit()


def download_using_aria2(links: list, anime_dir: str) -> None:
    """Downloads the episodes using external downloader aria2
    Since the default python downloader (using requests) is tooooo slow as compared to aria2
    and would require me to use my brain tooo much and handle several validations
    because some of you will surely try to break the program.
    Aria2 is wickedly fast and easy to use, read more about it on its docs.
    Communicates with aria2 using subprocess PIPE :)

    Args:
        links (list): The list of links of episodes to download.
    """
    start = time.perf_counter()
    download_dir = client.config.downloads_dir / anime_dir
    file = f"{str(client.config.aria_2_path.resolve())[:-10]}Failed_Download.log"
    cmd = [str(client.config.aria_2_path.resolve()),
           f"--max-concurrent-downloads={client.config.max_concurrent_downloads}", "-d", str(download_dir.resolve()),
           "-Z", "--save-session", file, "--auto-file-renaming=false"]
    cmd = subprocess.list2cmdline(cmd)
    cmd += " \"" + "\" \"".join(links) + "\""
    p = subprocess.Popen(cmd, shell=False, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        print(line.rstrip(), end="\r")
    p.communicate()
    with open(file, "r+") as file:
        lines = file.readlines()
        print(lines)  # TODO need to check file and if it contains anything resend to aria2 to retry download
    total_time = client.utils.convert_seconds_to_time(round(time.perf_counter() - start))
    header()
    client.config.logger.info(f"Downloaded {len(links)} episodes to \"{download_dir.resolve()}\" in {total_time}")
    print(
        f"{Fore.GREEN}>>> Download Completed in {total_time} {Fore.WHITE}| Downloaded {Fore.GREEN}{len(links)} episodes{Fore.WHITE} to {Fore.RED}\"{download_dir.resolve()}\" {Fore.GREEN}<<<")
    # Some pyinstaller config for --onefile option
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(".")
    app_icon = base_path / "icon.ico"
    try:
        notification.notify(title="SenPY | Download Completed",
                            message=f"Downloaded {len(links)} episode(s) to \"{str(download_dir.resolve())}\" in "
                                    f"{total_time}",
                            app_icon=str(app_icon.resolve()), timeout=10)
    except Exception as e:
        client.config.logger.error(
            f"Unable to send notification | Error: {e}")  # silently ignore if unable to show notification
    client.utils.sleep(10)


def search_anime_and_get_episode_pages_links() -> tuple:
    """
    Searches for an anime, gets its id, the number of episodes to download.
    And, proceeds to download them.
    """
    header()
    questions = [
        {
            "type": "input",
            "message": "Enter the name of Anime to search for:",
            "name": "anime_name",
            "validate": lambda result: len(result) > 0,
            "invalid_message": "Input cannot be empty."
        }
    ]
    result = prompt(questions=questions, style=client.config.stylesheet)
    results = client.anime_search(result['anime_name'])
    header()
    if len(results) != 0:
        return get_results(results)
    print(f"\n>>> {Fore.RED}No results found. {Fore.WHITE}Please try again with another query.")
    client.utils.sleep(3)
    search_anime_and_get_episode_pages_links()


def parse_anime_and_get_episode_pages_links() -> tuple:
    """
    parses anime from either MAL or bookmarks, gets its id, the number of episodes to download.
    And, proceeds to download them.
    """
    header()
    questions = [
        {
            "type": "input",
            "message": "Enter the name of Anime to search for:",
            "name": "anime_name",
            "validate": lambda result: len(result) > 0,
            "invalid_message": "Input cannot be empty."
        }
    ]
    result = prompt(questions=questions, style=client.config.stylesheet)
    results = client.anime_search(result['anime_name'])
    header()

    if len(results) != 0:
        return get_results(results)
    print(f"\n>>> {Fore.RED}No results found. {Fore.WHITE}Please try again with another query.")
    client.utils.sleep(3)
    search_anime_and_get_episode_pages_links()


def get_results(arg0):
    header()
    print(f"\n{Fore.GREEN}>>> {Fore.WHITE}Found {Fore.GREEN}{len(arg0)} {Fore.WHITE}results:")
    choices = [Choice(r['id'], name=f"{r['name']} [Released: {r['released']}]") for r in arg0]
    choicesback = [Choice(search_anime_and_get_episode_pages_links, name="Back")]
    questions = [
        {
            "type": "list",
            "name": "anime_id",
            "message": "Select the anime to download:",
            "choices": choices + choicesback
        }
    ]
    results = prompt(questions=questions, style=client.config.stylesheet)
    with contextlib.suppress(TypeError):
        results['anime_id']()
    anime_id = results['anime_id']
    all_eps = client.get_all_episode_numbers(anime_id)
    print("\n")
    questions = [
        {
            "type": "list",
            "name": "episodes",
            "message": "Select the episode(s) to download:",
            "choices": [
                Choice(
                    "all",
                    name=f"All Episodes ({len(all_eps)})",
                ),
                Choice("custom", name="Custom (Range, Numbers)"),
                Choice(get_results, name="Back")
            ],
        }
    ]
    result = prompt(questions=questions, style=client.config.stylesheet)
    with contextlib.suppress(Exception):
        result['episodes'](arg0)
    if result['episodes'] == "custom":
        header()
        print(
            f">>> {Fore.RED}IMPORTANT: {Fore.WHITE}Please make sure that the {Fore.GREEN}episode actually "
            f"exists{Fore.WHITE}, else you will get {Fore.RED}errors {Fore.WHITE}later.")
        eps = client.utils.string_to_sequence(prompt(questions=[{"type": "input",
                                                                 "message": "Enter the episode number/range to "
                                                                            "download [Can Include Bonus Episodes, "
                                                                            "e.g, 14.5] (e.g, 1-6, 6.5, 7, 10-12): ",
                                                                 "name": "episodes",
                                                                 "validate": lambda result: len(result) > 0,
                                                                 "invalid_message": "Input cannot be empty."}],
                                                     style=client.config.stylesheet)['episodes'])
    else:
        eps = all_eps

    anime_dir = anime_id.replace("-", " ").title()
    return client.get_episode_pages_links(anime_id, eps), anime_dir


def download_anime() -> None:
    """
    Searches the anime, selects it and does some highly intellectual stuff
    and downloads the anime to your machine.
    In short, searches anime, fetches its episodes and quality and downloads it.
    """
    if "auth" not in client.config.cookies:
        client.config.get_cookies()  # get cookies and use login information
    do_pre_checks()  # Makes sure everything's okay and program's ready to run.
    ep_pages_links, anime_dir = search_anime_and_get_episode_pages_links()
    header()
    questions = [
        {
            "type": "list",
            "name": "quality",
            "message": "Select the download quality of episodes:",
            "choices": [Choice(360, name="360p"), Choice(480, name="480p"), Choice(720, name="720p"),
                        Choice(1080, name="1080p")]
        }
    ]
    print(
        f"\n>>> {Fore.RED}IMPORTANT: {Fore.WHITE}Please note that in case the chosen quality is not found for any "
        f"episode, the next higher quality available will be downloaded. In case, that's not available, one previous "
        f"available quality will be chosen.")
    result = prompt(questions=questions, style=client.config.stylesheet)
    print(f"\n>>> {Fore.GREEN}Fetching Download Links...")
    fetch_downloads(ep_pages_links, result['quality'], anime_dir)
    home()


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def batch_results(key, value):
    if value is not None:
        value2 = "-".join(value.split())
        results = client.anime_search(value)
        for i in results:
            anime_id = i['id']
            if similar(value2, anime_id) > 0.7:
                return anime_id
        value = value.replace(" Dub", '')
        results = client.anime_search(value)
        for i in results:
            anime_id = i['id']
            if similar(value2, anime_id) > 0.7:
                return anime_id
        results = client.anime_search(key)
        key2 = "-".join(key.split())
        for i in results:
            anime_id = i['id']
            if similar(key2, anime_id) > 0.7:
                return anime_id
        key = key.replace(" Dub", '')
        key2 = "-".join(key.split())
        results = client.anime_search(key)
        for i in results:
            anime_id = i['id']
            if similar(key2, anime_id) > 0.7:
                return anime_id
    else:
        key2 = "-".join(key.split())
        results = client.anime_search(key)
        for i in results:
            anime_id = i['id']
            if similar(key2, anime_id) > 0.7:
                return anime_id
        key = key.replace(" Dub", '')
        key2 = "-".join(key.split())
        results = client.anime_search(key)
        for i in results:
            anime_id = i['id']
            if similar(key2, anime_id) > 0.7:
                return anime_id

    print(f"\n>>> {Fore.RED}No results found for {key}")
    client.config.logger.info(f"No results found for {key}")


def fetch_downloads(ep_pages_links, value, anime_dir):
    try:
        download_links = []
        for ep_link in ep_pages_links:
            quality_links = client.get_episode_quality_download_links(ep_link)
            qualities = [int(q.replace("p", "")) for q in
                         quality_links.keys()]  # Get the raw integers of the qualities available for easy comparision
            if f"{client.config.batch_quality}p" in quality_links:
                download_links.append(quality_links[f"{client.config.batch_quality}p"])
            elif f"{client.config.batch_quality}p" not in quality_links.keys():
                try:
                    quality = sorted([q for q in qualities if q > client.config.batch_quality])[
                        0]  # Get the next quality available
                    client.config.logger.warning(
                        f"{client.config.batch_quality}p quality not found, "
                        f"selected {quality}p instead for episode: {ep_link}.")
                except Exception:
                    quality = sorted([q for q in qualities if q < client.config.batch_quality])[
                        -1]  # Get the previous quality available
                    client.config.logger.warning(
                        f"{client.config.batch_quality}p quality not found, selected "
                        f"{quality}p instead for episode: {ep_link}.")
                download_links.append(quality_links[f"{quality}p"])
        download_links = client.utils.fix_episode_download_names(ep_list=download_links)
        client.config.logger.info(
            "Logging the download links for aria2 experiments or other purposes if required.")
        client.config.logger.info(download_links)
        print(
            f"\n>>> {Fore.GREEN}"
            f"Fetched Download Links. Starting Download in a few seconds. Please do not close the "
            f"window.")
        print(
            f"\n>>> {Fore.RED}"
            f"If you are an experienced aria2 user, download links have also been logged in the log "
            f"file, "
            f"you can do stuffs with them later.")
        print(f"\n>>> {Fore.GREEN}You can change the number of max concurrent downloads in config file.")
        client.utils.sleep(6)
        download_using_aria2(download_links, anime_dir)
        return

    except IndexError:
        print(f"\n>>> {Fore.RED}No results found for {value}")
        client.config.logger.info(f"No results found for {value}")
        return


def batch_download_anime() -> None:
    """
    Searches for the anime, selects it and does some highly intellectual stuff
    and downloads the anime to your machine.
    In short, searches anime, fetches its episodes and quality and downloads it.
    """
    if "auth" not in client.config.cookies:
        client.config.get_cookies()  # get cookies and use login information
    do_pre_checks()  # Makes sure everything's okay and program's ready to run.
    if client.config.batch_dl_mal is True:
        print(f"\n>>> {Fore.GREEN}Fetching anime list from MAL...")
        anime_dic = client.utils.parse_mal_json(client.config.batch_mal_username, client.config.batch_mal_dub,
                                                client.config.batch_mal_status)
    else:
        print(f"\n>>> {Fore.GREEN}Fetching shows from bookmarks...")
        anime_dic = client.get_show_from_bookmark()

    for key, value in anime_dic.items():
        anime_id = batch_results(key, value)
        if anime_id is not None:
            all_eps = client.get_all_episode_numbers(anime_id)
            anime_dir = anime_id.replace("-", " ").title()
            print(f"\n>>> {Fore.GREEN}Fetching Download Links for {anime_dir}")
            ep_pages_links = client.get_episode_pages_links(anime_id, all_eps)
            fetch_downloads(ep_pages_links, value, anime_dir)
    home()


if __name__ == "__main__":
    home()  # Start all the oogling-boogling here lol :)
