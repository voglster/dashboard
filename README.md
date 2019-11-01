Dashboard App that turns a raspberry pi and a tv into a useful application

Looking for help? or want to talk to me? [Discord](https://discord.gg/RCNq2ap)

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
cp sample-settings.yml settings.yml
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

# Settings.yml
each module has its own settings and the entire dashboard is saved in settings.yml
```YAML
qboard:
  timezone: "US/Central"  # optional any pytz timezone specification for local time
  debug: True # optional, displays commit hash in bottom left and bounding boxes for modules
  preferred_resolution: 1920x1080 # optional, if running not on a pi, defines the window size
  theme: # optional, override font sizes/colors
    font_weights:
      large: 115
      medium: 80
      small: 60
      extra_small: 35
      tiny: 18
    primary_color: white # can be named color, hex color #FFFFFF, or comma separated RGB 255,255,255
  - name: "clock"
    id: "clock1"
    position: #all modules should support positioning like this if they can be positioned
      anchor_point: "topright" # which part of modules box should be the attached
      anchor_to:
        id: "screen" # the id of the module you anchor this module to OR screen for whole screen
        point: "topright" # which part of target you want to put your anchor point to
      offset: 0,0 # how much to offset from anchor point in pixels (x, y)
```

#### Anchor Points
These are just the pygame rect names but pretty self explanatory, options:
 - topleft
 - bottomleft
 - topright
 - bottomright
 - midtop
 - midleft
 - midbottom
 - midright
 - center


# Todo:
While I try and keep this up to date,
The most up to date todo can be found here [Trello Board](https://trello.com/b/f9JI6Dz7/qboard)
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

 


  
  