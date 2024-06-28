import requests
from colorama import Fore
from requests import Session
from bs4 import BeautifulSoup
from .errors import InvalidCredentialsError
import json
from pathlib import Path
import logging
import time


class GogoConfig:
    """A configuration class for GoGoAnime, 
    which will be used to log in and get the required cookies for downloads,
    the csrf token and the current gogoanime url, and
    managing the config file.
    """

    def __init__(self) -> None:
        """Initializes the configuration object which handles the configuration
        for the application.
        """
        self.logger = logging.getLogger(__name__)
        self.setup_logger()
        self.config_path = self.get_config_path()
        self.session = Session()
        self.MAIN_URL = "https://raw.githubusercontent.com/FireHead90544/SenPY/main/CURRENT_URL.txt"  # GitHub action will auto update this with the current domain
        self.CURRENT_URL = ""
        self.get_current_url()
        self.cookies = {}
        self.config_updates = {}
        self.stylesheet = {"questionmark": "#16C60C bold", "answermark": "#e0af68", "answer": "#E5E512",
                           "input": "#98c379", "question": "#E74856 bold", "answered_question": "",
                           "instruction": "#a9b1d6", "long_instruction": "#a9b1d6", "pointer": "#3A96DD",
                           "checkbox": "#9ece6a", "separator": "", "skipped": "#48444c", "validator": "",
                           "marker": "#9ece6a", "fuzzy_prompt": "#bb9af7", "fuzzy_info": "#a9b1d6",
                           "fuzzy_border": "#343740", "fuzzy_match": "#bb9af7", "spinner_pattern": "#9ece6a",
                           "spinner_text": ""}
        try:
            self.loaded_config = json.load(open(self.config_path))
            self.email = self.loaded_config['EMAIL']
            self.password = self.loaded_config['PASSWORD']
            self.downloads_dir = Path(self.loaded_config['DOWNLOADS_DIR'])
            self.aria_2_path = Path(self.loaded_config['ARIA_2_PATH'])
            self.batch_dl_mal = self.loaded_config['BATCH_DOWNLOAD_MAL']
            self.batch_mal_username = self.loaded_config['MAL_USERNAME']
            self.batch_mal_status = self.loaded_config['STATUS']
            self.batch_mal_dub = self.loaded_config['DUB']
            self.batch_quality = self.loaded_config['QUALITY']
            self.max_concurrent_downloads = int(self.loaded_config['MAX_CONCURRENT_DOWNLOADS'])
        except KeyError as e:
            print(
                f"{Fore.RED}>>> Config file incorrect! Update Config file Immediately, Error: {e}{Fore.RED} <<<")
            time.sleep(15)

    def setup_logger(self) -> None:
        """Sets up the logger's configurations. General public need not to bother about it.
        The logger file location is the root directory of the application.
        """
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("[ %(asctime)s ] -  %(name)s | %(levelname)s | - %(message)s")
        file_handler = logging.FileHandler(Path.cwd() / "senpy.log", mode="w")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_config_path(self) -> Path:
        """Returns the path to the config file.
        Local Path ($CWD/config.json) takes greater precedence than Global Path ($HOME/.senpy/config.json)
        If none exists, Global Path is created, but you need to update the config keys yourself.

        Returns:
            config_path (Path): The path to the config file.
        """
        start = time.perf_counter()
        global_config = Path.home() / ".senpy" / "config.json"
        local_config = Path.cwd().parent / "config.json"
        if not local_config.exists():
            if not global_config.exists():
                self.logger.info(f"No config file found, creating one at \"{global_config.resolve()}\"")
                global_config.parent.mkdir(parents=True, exist_ok=True)
                global_config.touch()
                with open(global_config, "w") as f:
                    json.dump({"EMAIL": "wihay47579@aregods.com",
                               "PASSWORD": "NeverGonnaGiveYouUp",
                               "DOWNLOADS_DIR": r"ENTER DOWNLOAD LOCATION (Windows: Drive:\Folder, Linux: "
                                                "/path/to/folder)",
                               "ARIA_2_PATH": "ENTER THE PATH TO ARIA2's EXECUTABLE",
                               "BATCH_DOWNLOAD_MAL": "True",
                               "STATUS": "Plan to Watch",
                               "DUB": "Dub",
                               "QUALITY": 1080,
                               "MAX_CONCURRENT_DOWNLOADS": 6}, f, indent=2, sort_keys=True)
                    self.logger.warning("Make sure to update your config file before trying to download anything.")
            self.config_path = global_config
        else:
            self.config_path = local_config

        self.logger.info(
            f"({round(time.perf_counter() - start, 2)}s) Config file found at \"{self.config_path.resolve()}\"")

        return self.config_path

    def get_cookies(self) -> dict:
        """Returns the cookies for session which will be later used.
        
        Returns:
            cookies (dict): The cookies for the session.
        """
        start = time.perf_counter()
        self.session.post(
            f"{self.CURRENT_URL}/login.html",
            data={
                "email": self.email,
                "password": self.password,
                "_csrf": self.get_csrf_token(),
            }, allow_redirects=True
        )
        self.cookies["gogoanime"] = self.session.cookies.get("gogoanime")
        self.cookies["auth"] = self.session.cookies.get("auth")

        if not self.cookies["auth"]:
            self.logger.critical("Invalid credentials. Please check your credentials.")
            raise InvalidCredentialsError(
                f"Invalid Credentials Provided, Please Correct Them !!! Config File at \"{self.config_path.resolve()}\"")

        self.logger.info(f"({round(time.perf_counter() - start, 2)}s) Successfully fetched cookies for the session.")
        return self.cookies

    def get_current_url(self) -> str:
        """Returns the current gogoanime url with the current domain.
        Fetches it from the main url that keeps itself updated using a github action, i.e, 
        https://raw.githubusercontent.com/FireHead90544/SenPY/main/CURRENT_URL.txt

        Returns:
            current_url (str): The URL of the current gogoanime domain.
        """
        self.CURRENT_URL = self.session.get(self.MAIN_URL).text.split("\n")[0]
        return self.CURRENT_URL

    def get_csrf_token(self) -> str:
        """Returns the CSRF token for logging in.
        Fetches it from the login endpoint using GET request.

        Returns:
            csrf_token (str): The CSRF token for login.
        """
        return BeautifulSoup(
            self.session.get(f"{self.CURRENT_URL}/login.html").content,
            "html.parser",
        ).select("meta[name='csrf-token']")[0]["content"]

    def write_config(self, new: dict) -> None:
        """Updates the config file with the new configuration.
        Also updates the current loaded configuration.

        Args:
            new (dict): The configuration changes to be updated.
        """
        self.loaded_config.update(new)
        with open(self.config_path, "w") as f:
            json.dump(self.loaded_config, f, indent=4, sort_keys=True)
        self.refresh_config()

    def refresh_config(self) -> None:
        """Refreshes the config variables from the loaded config.
        """
        self.email = self.loaded_config['EMAIL']
        self.password = self.loaded_config['PASSWORD']
        self.downloads_dir = Path(self.loaded_config['DOWNLOADS_DIR'])
        self.aria_2_path = Path(self.loaded_config['ARIA_2_PATH'])
        self.batch_dl_mal = self.loaded_config['BATCH_DOWNLOAD_MAL']
        self.batch_mal_username = self.loaded_config['MAL_USERNAME']
        self.batch_mal_status = self.loaded_config['STATUS']
        self.batch_mal_dub = self.loaded_config['DUB']
        self.batch_quality = self.loaded_config['QUALITY']
        self.max_concurrent_downloads = int(self.loaded_config['MAX_CONCURRENT_DOWNLOADS'])
