import requests
from sqlite3 import connect
from paths import DB_PATH

class CreateDB:
    
    def create_tables(self):
        
        with connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS EPG_BOUQ (RELATED_NAME TEXT primary key , NAME TEXT , PATH TEXT , CHANNELS TEXT )')
            cur.execute('CREATE TABLE IF NOT EXISTS EPG_PROV (BOUQUET TEXT primary key , TITLE TEXT , DATE TEXT , IS_VISIBLE INTEGER DEFAULT 1 , RELATED_NAME text REFERENCES EPG_BOUQ(RELATED_NAME))')

    def insert_into_tables(self,data,providers):
        self.create_tables()
        with connect(DB_PATH) as conn:
            cur = conn.cursor()
            for bouq in data['bouquets']:
               cur.execute("INSERT INTO EPG_BOUQ(RELATED_NAME,NAME,PATH,CHANNELS) values (?,?,?,?)",(bouq["related_name"],bouq["name"],bouq["path"],str(bouq["channels"]),))
    
            for prov in providers['bouquets']:
               cur.execute("INSERT INTO EPG_PROV(BOUQUET,TITLE,DATE,RELATED_NAME) values (?,?,?,?)",(prov["bouquet"],prov["title"],prov["date"],prov["related_name"],))

    def get_data(self):
        bouq_data = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/develop/src/EPGGrabber/api/bouquets.json').json()
        prov_data = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/develop/src/EPGGrabber/api/providers.json').json()
        self.insert_into_tables(bouq_data,prov_data)
    
    def get_rows(self,custom_req=None):
        with connect(DB_PATH) as conn:
            cur = conn.cursor()
            
            if custom_req:
                rows = cur.execute(custom_req)
                
            else:
                rows = cur.execute("select * from epg_bouq inner join epg_prov on EPG_BOUQ.RELATED_NAME = EPG_PROV.RELATED_NAME")

            return rows
    
    def execute_commande(self,commande=None):
        if commande:
            with connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute(commande)