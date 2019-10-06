Dashboard App that turns a raspberry pi and a tv into a useful application

I have this running on a raspberry pi zero at home

# Quick Start to Run on your own machine without a PI:
1. `clone repo`
2. `pip install -r requirements.txt`
3. copy sample-settings.yml to settings.yml
4. edit settings.yml as needed
5. `python screen.py`

# Setting up on a PI
TBD

# Todo:
 - Setup instructions in readme on installing on a pi (zero/p1 and p2+) diff arm architectures!
 - YAML configuration 
     - Allow more display resolutions
     - Landscape vs portrait orientation
     - ~~YAML layout~~
 - Cache folders
     - Global
     - Plugin Specific
     - Plugin Instance Specific
     - cache the weather icons instead of re-downloading them each time
     - Download free fonts from internet and store in local cache instead of hardcoded fonts
 - Un-splash plugin
     - Listen to anchor directives
     - Download higher res images and resize as needed
 - Global config for theme-ing
 - Extend graphing engine used in crypto to be more generic
 - Rotating display based on time (10 secs dashboard, 10 secs price graph)
 - ~~Move all images downloads to temp files that cleanup after themselves~~
 - ~~Change to a plugin based system, register now plugins, only load config when needed~~
 
 
# Ideas:
 - Download and sync images from google drive/dropbox/i-cloud folder and scan/rotate them  
 - Reduce the bar to get up and running
    - Prebuilt raspbian image
    - WYSIWYG config editor? pygame drag and drop?

 


  
  