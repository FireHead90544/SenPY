import os
import time

class GogoUtils:
    """Some utilities used by the application."""
    def __init__(self) -> None:
        pass

    def string_to_sequence(self, ep_str: str) -> list:
        """Parses and returns a sequence of episodes from a string containing episode numbers.

        Args:
            ep_str (str): The string containing episode numbers. (e.g, "1-7, 8, 10, 11 , 13 , 15, 15, 15-19, 18.5, 19.5, 20")

        Returns:
            ep_num list[Union[int, float]]: The list containg the parsed and sorted episode numbers. (e.g, [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 15, 16, 17, 18, 18.5 19, 19.5, 20])
        """
        final = []
        temp = list(ep_str.split(","))
        for i in temp:
            if "-" in i: # Handles episode in between ranges (list(int))
                lower, upper = list(i.split("-"))
                final.extend(range(int(lower), int(upper)+1))
            else: # Handles, extra/bonus episodes (floats) and normal episodes (ints)
                try:
                    final.append(int(i))
                except ValueError:
                    final.append(float(i))

        return sorted(list(set(final)))

    def fix_episode_download_names(self, ep_list: list) -> list:
        """The downloaded episodes with the original link would have crappy shizzy names
        This changes the name of the downloaded episode before actually downloading it
        directly in the link, so that after download a proper naming convention is followed.

        Args:
            ep_list (list): The final list containing links to episodes.

        Returns:
            named_downloads (list): A list to download episodes but with proper names.
        """
        named_downloads = []
        for link in ep_list:
            prefix, name = link.split("&title=")
            name = f"EP.{name.split('-episode-')[1].replace('-', '.')}"
            named_downloads.append(f"{prefix}&title={name}")
        
        return named_downloads

    def clear(self) -> None:
        """Clears the shiz in the terminal :)"""
        os.system("cls" if os.name == "nt" else "clear")

    def sleep(self, seconds: int) -> None:
        """Sleeps for the specified number of seconds.

        Args:
            seconds (int): The number of seconds to sleep for.
        """
        time.sleep(seconds)

    def convert_seconds_to_time(self, rawseconds: int) -> str:
        """
        Converts seconds to human readable representation.

        Args:
            rawseconds (int): The number of seconds to convert.
        
        Returns:
            str: The human readable representation of the time.
        """
        days = rawseconds // 86400
        hours = (rawseconds - days * 86400) // 3600
        minutes = (rawseconds - days * 86400 - hours * 3600) // 60
        seconds = rawseconds - days * 86400 - hours * 3600 - minutes * 60

        return (
            ("{0} day{1}, ".format(days, "s" if days != 1 else "") if days else "")
            + (
                "{0} hour{1}, ".format(hours, "s" if hours != 1 else "")
                if hours
                else ""
            )
            + (
                "{0} minute{1}, ".format(minutes, "s" if minutes != 1 else "")
                if minutes
                else ""
            )
            + (
                "{0} second{1}, ".format(seconds, "s" if seconds != 1 else "")
                if seconds
                else ""
            )[:-2]
        )