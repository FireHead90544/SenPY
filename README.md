<div align="center">
  <img
    style="width: 165px; height: 165px"
    src="https://i.ibb.co/J5NvHGb/Logo.png"
    title="SenPY"
    alt="SenPY"
  />
  <h3>SenPY</h3>
  <p>
    A highly efficient anime downloader written in Python, integrated with Aria2.
  </p>
  <a href="https://github.com/FireHead90544/SenPY/releases"> <strong>· Download Executable Release ·</strong></a>
</div>
<hr>

## About SenPY

**SenPY** is a python script that allows you to download animes in your preferred quality. It allows you to download all episodes of an anime as a whole or any specific episode or episode range. It scrapes [gogoanime](https://gogoanime.so/) and fetches the anime data from there. SenPY uses [aria2](https://github.com/aria2/aria2) as an external downloader which boosts up the download speed drastically and comes with several other epic features. It also allows you to customize your "Anime Downloads" folder and downloads animes to that particular folder only.
<hr>

## Index of Contents
- [About](#about-senpy)
- [Installation](#installation)
- [Setup](#setup)
- [Screenshots](#screenshots)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Versioning](#versioning)
- [How it works in a nutshell](#a-bit-about-how-it-works)
- [Contribution](#contribution)
- [License](#license)
- [Homies](#homies)
<hr>

**I will probably be adding an installation/usage video (windows) soon, or if you want to please do and generate a pr, would be gladly accepted.**

## Installation

The installation is pretty easy.
1. Head over to the [Releases](https://github.com/FireHead90544/SenPY/releases) section and download the latest release for your operating system. Now refer to the [setup section](#setup).
2. Head over to the [aria2's releases](https://github.com/aria2/aria2/releases) and download the latest release for your system. Linux/Mac users can run `sudo apt install aria2 -y` and `brew install aria2` respectively.

**[Non-Techy users need not to think about this]** If you don't want to download the release and want to build the application on your own (or if you think this is a virus because your dumb antivirus marked it as false positive). You need to download python on your system first, clone the repository, switch to the project's root directory, install the requirements present in the `requirements.txt` and run the below command from the project root directory.
<details>
  <summary>Read this if you are somewhat experienced with pyinstaller</summary>
   If you know what you are doing, you can replace <b>--onefile</b> flag with <b>--onedir</b> since it is preferred over <b>--onefile</b> because of performance reasons as <b>--onefile</b> generated applications unpacks everything in a temp directory everytime when run. And linux/mac/android users can replace the "win" in --hidden-import with their os alternative in the below build command as "linux", "macosx", and "android" respectively.
</details>

```console
pyinstaller --noconfirm --console --onefile --name SenPY --icon icon.ico --hidden-import plyer.platforms.win.notification --add-data="icon.ico:." main.py
```
Now, open the `dist` folder and get your executable from there.
<hr>

## Setup

1. Extract the `aria2`'s folder you just downloaded. Copy the path to it's executable (In windows, the executable has an extension '.exe'), (Linux users can run `which aria2c` and copy that path)
2. Run the SenPY's application for the first time, it will create a config file at `$HOME/.senpy/config.json` (You can edit it manually if want to or just move onto next step)
3. Select the `Update Config File` option, update your gogoanime-registered email and password (you can use the below credentials too, but it's better to use your own since these ones can be invalidated probably). In the `aria2's executable path input`, enter the path to aria2's executable you just copied and in the `downloads folder input`, enter the path to the folder (make sure to create one already) where you want your animes to be downloaded. You can also set the maximum concurrent downloads and some other stuffs.

**Config File Location** (Not meant for general public): `$HOME/.senpy/config.json` (Global Location), `Project Root/config.json` (Local Location). Local Location takes priority over Global Location.

**Dummy Credentials**: (Please don't be a retarded kid and do not change the password or anything, just use your own credentials instead)
| Name | Value |
|:--:|:--:|
| EMAIL | wihay47579@aregods.com |
| PASSWORD | NeverGonnaGiveYouUp |
<hr>

## Example Setup (Windows)

Let's say I downloaded and extracted the aria2 release in `C:\Users\user\Downloads\aria2`, then the path to the executable becomes `C:\Users\user\Downloads\aria2\aria2c.exe`. I will now update this path in config file.

## Screenshots

<div align="center">
  <img src="https://user-images.githubusercontent.com/55452780/184005609-eea73142-8802-43f1-ad79-3d0d99e6d75d.png"
  title="BitAnime in action" alt="SenPY Screenshot">
</div>
<hr>

## Dependencies

**SenPY** has some internal and some external dependencies.

**Internal Dependency** represents *python libraries/modules* the application relies on.<br>
**External Dependency** represents *any other program* the application relies on.

|  Internal Dependency  |  Function  |
|:--:|:--:|
|  InquirerPy  | Taking all the cool looking inputs |
|  colorama  |  Beautifying the output text  |
|  plyer  |  Sending notifications on supported devices  |
|  io  |  Just for StringIO lol  |
|  subprocess  |  Interacting with aria2 and system shell  |
|  json  |  Parsing JSON  |
|  time  |  Sleeping/Calculating time taken for several processes  |
|  sys  |  Interacting with system buffer/temp directory  |
|  re  |  Regexing of course  |
|  os  |  Clearing the console and some other stuffs  |
|  requests  |  The most important dependency, fetching requests  |
|  bs4  |  Parsing the html data  |
|  pathlib  |  Interacting with system paths  |
|  logging  |  Logging everything using a logger  |

|  External Dependency  |  Function  |
|:--:|:--:|
|  aria2  |  Downloading the animes  |

Clone the repository, `cd` into the respective directory and run the below command in terminal
```console
pip install -r requirements.txt
```
to install all the internal dependencies that doesn't comes inbuilt with python.

Go to [aria2 releases](https://github.com/aria2/aria2/releases) and download the latest release and unpack the archive, and update the path to the aria2 executable in program's `config.json` to install the external dependency.
<hr>

## Usage

Refer to the [Installation](#installation) section and complete the installation first. Then just run the program and select the inputs as asked :)
<hr>

## Versioning

The project follows the following versioning convention.

v`MAJOR`.`MINOR`.`PATCH`
|  Type  |  Details  |
|:--:|:--:|
|  MAJOR  |  Includes rewrites, logic change, compatibility updates  |
|  MINOR  |  Includes library updates, major bug updates  |
|  PATCH  |  Includes minor updates, bug fixes, patches, etc |

<hr>

## A Bit About How It Works

This project fakes a browser request. Firstly, it fetches the cookies for the session using a user's email and password. Then it uses that cookies to create a session, then uses that session to fetch everything. On the anime episode's page, while being logged in (sesion's cookies) scrapes the download links to the episode. Makes a `HEAD` request to that link to get the direct download link and make sure that the link actually works. Rest stores all the links for the episodes selected and parses it to `aria2` and downloads them to the downloads folder assigned in the `config.json`. There is also a `senpy.log` file generated in the project root alongside the executable, which contains the logs, which can be used for debugging purposes.
<hr>

## Contribution

Yes, my code can be incomplete and might contains bugs, if you find any bug, [create an issue](https://github.com/FireHead90544/SenPY/issues). If you want to contribute to the code, please fork the repository, do your edits in your forked repository, fetch the upstreamand and create a pull request. If the contribution is good, I'll merge it with this repository. Please don't create any shit PRs (like grammatical fixes/typo(s) in README), instead create an issue for that.
<hr>

## License

The project is licensed under [GNU GPL v3](https://github.com/FireHead90544/SenPY/blob/main/LICENSE). Just read the license yourself, I won't spoonfeed the terms and conditions here xD
<hr>

## Homies

A huge thanks to the below projects for being one of the inspirations for this project.

- [sh1nobuu](https://github.com/sh1nobuu)'s  -   [BitAnime](https://github.com/sh1nobuu/BitAnime)
- [Arctic4161](https://github.com/Arctic4161)'s  -   [GoGo Downloader](https://github.com/Arctic4161/BitAnime)
- [justfoolingaround](https://github.com/justfoolingaround)'s  -   [animdl](https://github.com/justfoolingaround/animdl)
<hr>

## Back To Top
[Click here to go back to the top of page](#index-of-contents)
