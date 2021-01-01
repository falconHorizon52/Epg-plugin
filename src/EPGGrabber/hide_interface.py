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

        self["key_red"] = Button(_("Hide"))
        
        super(HideProv, self).__init__(*args,**kwargs)
                
        self.update()
        
        self["setupActions"] = ActionMap(["EpgColorActions",'EpgMenuActions','EpgWizardActions','EpgShortcutActions'],
        {
            "red": self.keyRed,
            "cancel": self.close,
            "down": self.down,
            "up": self.up,
            
        }, -1)
        
        
        self["epgTitle"] = Label(_('Press Red Button to hide/show Provider'))
     
    def init(self):
        list = []
        self.installList=[]
  
        rows = self.epg_db.get_rows('select * from epg_prov order by title')
        
        table = rows.fetchall()
        
        for i in range(len(table)):
            list.append((table[i][1],i,table[i][0]))
        
        self.provList=list 
       
    def onWindowShow(self):
        self.onShown.remove(self.onWindowShow)
        self.new_version = Ver
        
        self.setTitle("EPG GRABBER BY ZIKO V %s" % Ver)
        
        self["key_red"].show()
        self["key_green"].hide()
        self.iniMenu()
        
    def go(self):pass    
        
    def keyRed(self):
        index = self['config'].getSelectionIndex()
        bouquet = self.provList[index][2]
        rows = self.epg_db.get_rows('select is_visible from epg_prov where bouquet = "{}"'.format(bouquet))
        status = 1 if rows.fetchone()[0] == 0 else 0
        self.epg_db.execute_commande('update epg_prov set is_visible = "{}" where bouquet = "{}"'.format(status,bouquet))
        self.update()
    
    def update(self):
        index = self['config'].getSelectionIndex()
        bouquet = self.provList[index][2]
        rows = self.epg_db.get_rows('select is_visible from epg_prov where bouquet = "{}"'.format(bouquet))
        status = "Show" if rows.fetchone()[0] == 0 else "Hide"
        self["key_red"].setText(status)