ios_ui_config_file = "/home/bsobhani/git/bsstudio-xf/23id2/ios_gui.ui"

def update_gui():
    #import os
    #os.system("git -C /opt/bsstudio/bsstudio-xf pull")
    #os.system("git -C /home2/xf21id1/git/bsstudio pull")
    #os.system("git -C /home2/xf21id1/git/bsstudio-xf pull")
	pass

def ios_gui(filename=ios_ui_config_file):
    # Note: install it in the developer mode with the following command before
    # it's packaged with conda
    #   $ cd /home2/xf21id1/git/bsstudio/
    #   $ pip install -e .
    import os
    #os.environ["BSSTUDIO_LOG_FILE_NAME"] = "/var/log/bsstudio/bsstudio.log"
    import sys
    sys.path.append("/home/bsobhani/code/bsstudio/")
    import bsstudio
    bsstudio.load(filename)
