Dashboard App that turns a raspberry pi and a tv into a useful application

I have this running on a raspberry pi zero at home

# Quick Start to Run on your own machine without a PI:
1. `clone repo`
2. `pip install -r requirements.txt`
3. copy sample-settings.yml to settings.yml
4. edit settings.yml as needed
5. `python screen.py`

# Setting up on a PI
I have tested this on a PI Zero W

make sure you have python installed

`sudo apt install python3 python3-pip`

```bash
cd ~
git clone https://github.com/voglster/qboard.git
cd qboard
python3 -m venv .venv
source ./.venv/bin/activate
pip install -U -r requirements.txt
sudo -E python screen.py
```

Note: from what I can tell to write to the framebuffer you need root access, if there is a better way let me know!


# Auto starting screen.py on boot
```bash
sudo apt install supervisor
cd ~/.qboard/
sudo cp qboard.conf /etc/supervisor/conf.d/
sudo supervisorctl start qboard
```
logs can be found at: `/var/log/supervisord/`


# Todo:
 - Explain settings.yml in this file
 - Cache folders
     - Global
     - Plugin Specific
     - Plugin Instance Specific
     - Download free fonts from internet and store in local cache instead of hardcoded fonts
 - Extend graphing engine used in crypto to be more generic
 - Rotating display based on time (10 secs dashboard, 10 secs price graph)
 - ~~Un-splash plugin~~
     - ~~Listen to anchor directives~~
     - ~~Download higher res images and resize as needed~~
 - ~~Global config for theme-ing~~
 - ~~Move all images downloads to temp files that cleanup after themselves~~
 - ~~Change to a plugin based system, register now plugins, only load config when needed~~
 - ~~Setup instructions in readme on installing on a pi (zero/p1 and p2+) diff arm architectures!~~
 - ~~YAML configuration~~
     - ~~Allow more display resolutions~~
     - ~~Landscape vs portrait orientation~~
     - ~~YAML layout~~
 
 
# Ideas:
 - Download and sync images from google drive/dropbox/i-cloud folder and scan/rotate them  
 - Reduce the bar to get up and running
    - Prebuilt raspbian image
    - WYSIWYG config editor? pygame drag and drop?

 


  
  