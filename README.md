# okcscrape3
(**okc**upid **scrape**r in Python **3**)
## What it does
Scrape and log usernames and profile text content from the popular dating website OKCupid.

Here's what it captures:

<p align="center">
  <img src="https://i.imgur.com/Nq3xt7K.png">
</p>

## How to use it
okcscrape3 is a command line app, so install it, run it on the command line, and check out the help text like so:

<p align="center">
  <img src="https://i.imgur.com/MdRKSv7.gif">
</p>

### Detailed command overview
>```okcscrape3 <args>```

Calling okcscrape3 using only arguments and no subroutine will allow you to set internal configuration variables such as

```--base-url```

>```okcscrape3 <args> findusers <args>```
  
This is the ```findusers``` subroutine. Calling this will launch a Selenium Chromedriver instance and navigate to the OKC "browse profiles" page to scrape usernames. The usernames, along with the date they were gathered and a boolean flag indicating whether the profile associated with that username has been fetched yet, will be stored in a .csv in the ```data``` folder of the package installation directory. A cookies file is not required to use this subroutine.

## How to install it
Clone the repo or download + extract it, spin up a terminal/shell (I've only tested this on Windows), navigate to the top level 'okcscrape3' folder and use pip to install with the following command:
```
py -m pip install .
```
Or just however you access pip, which would essentially be:
```
<prefix to get to pip> pip install .
```
Here's an example of what that looks like:

<p align="center">
  <img src="https://i.imgur.com/8gOigL8.gif">
</p>

If the 'Scripts' folder of the Python 3 installation on which you just installed okcscrape3 is on your %PATH%, you can simply install the package and call the app by typing 'okcscrape3' in the command prompt.

I haven't comprehensively tested the installation process, so let me know if you run into issues.
