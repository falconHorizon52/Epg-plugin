from Plugins.Extensions.EPGGrabber.interface import EPGGrabber , Ver
from Screens.Screen import Screen
from Components.config import (config, 
        getConfigListEntry, 
        ConfigSubsection, 
        ConfigYesNo, 
        configfile, 
        ConfigSelection)

from Components.Button import Button
from Components.Label import Label
from Components.ActionMap import ActionMap


class HideProv(EPGGrabber):
    
    def __init__(self,*args,**kwargs):
        super(HideProv, self).__init__(*args,**kwargs)
        
        self["setupActions"] = ActionMap(["EpgColorActions",'EpgMenuActions','EpgWizardActions','EpgShortcutActions'],
        {
            "red": self.keyRed,
            "cancel": self.close,
        }, -1)
        
        
        self["epgTitle"] = Label(_('Press red to hide provider'))
        
    def onWindowShow(self):
        self.onShown.remove(self.onWindowShow)
        self.new_version = Ver
        if config.plugins.EpgPlugin.update.value:
            self.checkupdates()
        self.setTitle("EPG GRABBER BY ZIKO V %s" % Ver)
        
        self["key_red"].show()
        self["key_green"].hide()
        self.iniMenu()
        
        
    def keyRed(self):
        self.close(None)
    
    def go(self):pass    
    