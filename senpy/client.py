import re

import requests

from .config import GogoConfig
from .utils import GogoUtils
from bs4 import BeautifulSoup
import time


class GogoClient:
    """The GogoAnimeClient which interacts with the servers
    and its endpoints and does some highly intellectual stuffs
    which makes anime available to you, without you caring 
    about doing stuffs manually.
    """
    def __init__(self) -> None:
        self.url_ajax = None
        self.config = GogoConfig()
        self.utils = GogoUtils()
        self.session = self.config.session

    def anime_search(self, query: str) -> list:
        """Searches for anime with given query.

        Args:
            query (str): The query to search for.

        Returns:
            anime_list (list(dict)): The list of animes found.
        """
        start = time.perf_counter()
        search_url = f"{self.config.CURRENT_URL}/search.html?keyword={query}"
        soup = BeautifulSoup(self.session.get(search_url).content, 'html.parser')
        animes = soup.select("#wrapper_bg > section > section.content_left > div > div.last_episodes > ul > li")
        anime_list = []
        for anime in animes:
            try:
                anime_list.append({"name": anime.find("p", {"class": "name"}).a.getText().strip(), 
                    "id": anime.find("p", {"class": "name"}).a["href"].strip().split("/")[-1].replace("/", ""), 
                    "released": anime.find("p", {"class": "released"}).getText().strip().split("Released:")[1].strip(), 
                    "image": anime.div.a.img["src"]
                })
            except Exception as e:
                self.config.logger.error(f"An error occured while searching for animes | {e}")

        self.config.logger.info(f"({round(time.perf_counter() - start, 2)}s) Fetched animes with query: \"{query}\", Found \"{len(anime_list)}\" results.")
        return anime_list

    def get_all_episode_numbers(self, animeid: str) -> list:
        """Returns all the episodes of the anime (including bonus episodes like 17.5, 13.5, etc.).

        Args:
            animeid (str): The id of anime whose all episodes to fetch.

        Returns:
            eps (list): The list of all available episodes of the anime.
        """
        start = time.perf_counter()
        soup = BeautifulSoup(self.session.get(f"{self.config.CURRENT_URL}/category/{animeid}").content, 'html.parser')
        # Arigato Zai-Kun (https://github.com/FireHead90544/SenPY/issues/10#issue-1955506329)
        anime_id = soup.find("input", {"id": "movie_id"})['value']
        last = int(list(soup.select("#episode_page")[0])[-2].a['ep_end'])
        url = soup.find("meta", property="og:image")
        self.url_ajax = url["content"].split("/")[2]
        soup = BeautifulSoup(self.session.get(f"https://ajax.{self.url_ajax}/ajax/load-list-episode?ep_start=0&ep_end={last}&id={anime_id}").content, 'html.parser')
        all_eps = [eval(ep['href'].strip().split("-episode-")[1].replace("-", ".")) for ep in soup.select("ul#episode_related > li > a")]
        all_eps.sort()

        self.config.logger.info(f"({round(time.perf_counter() - start, 2)}s) Fetched all episodes for anime id: \"{animeid}\"")
        return all_eps

    def get_episode_pages_links(self, animeid: str, eps: list) -> list:
        """Returns the list to the episode pages of anime with given id.

        Args:
            animeid (str): The id of anime whose episode links to fetch.
            eps (list(Union[int, float])): The list of episode numbers to fetch.

        Returns:
            links (list): The list containing links to the episode pages of anime.
        """
        start = time.perf_counter()
        soup = BeautifulSoup(self.session.get(f"{self.config.CURRENT_URL}/category/{animeid}").content, 'html.parser')
        anime_id = soup.find("input", {"id": "movie_id"})['value']
        soup = BeautifulSoup(self.session.get(f"https://ajax.{self.url_ajax}/ajax/load-list-episode?ep_start={min(eps)}"
                                              f"&ep_end={max(eps)}&id={anime_id}").content, 'html.parser')
        links = [f"{self.config.CURRENT_URL}{ep['href'].strip()}" for ep in soup.select("ul#episode_related > li > a")
                 if eval(ep['href'].split('-episode-')[1].replace('-', '.')) in eps][::-1]

        self.config.logger.info(f"({round(time.perf_counter() - start, 2)}s) Fetched episodes' links for anime id: "
                                f"\"{animeid}\"")
        return links

    def get_episode_quality_download_links(self, url: str) -> dict:
        """Returns the download links to the various qualities available for the episode.

        Args:
            url (str): The url to episode of the anime.

        Returns:
            links (dict): Dictionary containing quality:link pairs.
        """
        start = time.perf_counter()
        soup = BeautifulSoup(self.session.get(url).content, 'html.parser')
        links = {}
        qualities_container = soup.select("#wrapper_bg > section > section.content_left > div > div.anime_video_body "
                                          "> div.list_dowload > div > a")
        if not qualities_container:
            self.config.logger.error(f"Unable to retrieve links for the url \"{url}\"")
            return links

        for link in qualities_container:
            try:
                redirected = self.session.get(link["href"], allow_redirects=False)
                links[f"{link.getText().strip().split('x')[1]}p"] = redirected.headers['location'].strip()
            except KeyError as e:
                self.config.logger.error(f"Unable to retrieve link for {link.getText().strip().split('x')[1]}p "
                                         f"quality for this episode")
        links = {k: v for k, v in links.items() if v} # Filter out empty links

        self.config.logger.info(f"({round(time.perf_counter() - start, 2)}s) Fetched links for qualities available "
                                f"for episode #{url.split('-')[-1].replace('/', '')}")
        return links

    def get_show_from_bookmark(self):
        anime_dic = {}
        soup = BeautifulSoup(self.session.get(f"{self.config.CURRENT_URL}/user/bookmark").content, 'html.parser')
        table = soup.find("div", attrs={"class": "article_bookmark"})
        splitTableLines = table.text.split("Remove")
        for rows in splitTableLines:
            fullRow = " ".join(rows.split())
            if "Anime name" in fullRow:
                fullRow = fullRow.replace("Anime name Latest", "")
                splitRow = fullRow.split("Latest")
            elif fullRow == "Status":
                break
            else:
                fullRow = fullRow.replace("Status ", "")
                splitRow = fullRow.split("Latest")
            animeName = splitRow[0].strip().encode("ascii", "ignore").decode()
            animeName = re.sub("[^A-Za-z\d ]+", "", animeName)
            anime_dic[animeName] = None

        return anime_dic

