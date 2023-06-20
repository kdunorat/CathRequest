import requests
from bs4 import BeautifulSoup


class CathRequest:
    def __init__(self, superfamily_id):
        self.superfamily_id = superfamily_id
        self.client = requests.session()
        
    def get_info(self):
        fam_set = set()
        url_1 = f"http://www.cathdb.info/version/latest/superfamily/{self.superfamily_id}/alignments" 
        r1 = self.client.get(url=url_1, timeout=50)
        
        # BS4
        soup = BeautifulSoup(r1.content, "html.parser")
        with open("arquivo.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
        all_a = soup.find_all('a')
        
        for a in all_a[17:]:
            if 'CATH News' in a.text:
                break
            path = a["href"]
            file_name = self.get_file_name(path, 2)
            fam_id = self.get_file_name(path, 1)
            fam_name = a.text
            if fam_name.isnumeric():
                continue
            elif fam_name == '':
                fam_name = 'N/A'
            if file_name == 'funfam' and fam_id not in fam_set:
                print(f"{fam_id} ---- {fam_name}")
                fam_set.add(fam_id)
                
    def get_fam(self, funfam_id):
        url_2 = f"http://www.cathdb.info/version/latest/superfamily/{self.superfamily_id}/funfam/{funfam_id}/alignment"
        r2 = self.client.get(url=url_2, timeout=50)
        soup2 = BeautifulSoup(r2.content, "html.parser")
        classe = soup2.find('a', class_="btn btn-small btn-info")
        stock_file = classe['href']
        
        return stock_file, funfam_id
    
    def get_species_file(self, stock_file, funfam_id):
        r3 = self.client.get(url=stock_file, timeout=50)
        soup3 = BeautifulSoup(r3.content, "html.parser")
        new_file_name = f"{self.superfamily_id}:{funfam_id}-Species.txt"
        with open(new_file_name, "w", encoding="utf-8") as f:
            f.write(str(soup3))
        self.species_names(new_file_name)
    
    @staticmethod
    def species_names(path):
        specs = []
        with open(path, 'r') as f:
            content = f.readlines()
            for line in content:
                if 'OS' in line:
                    spec = line.rsplit('OS')
                    spec = spec[-1]
                    specs.append(spec)
        for sp in specs:
            print(sp)
        
    @staticmethod
    def get_file_name(href: str, house: int):
        file_name = href.split("/")
        try:
            file_name = file_name[-house]
            return file_name
        except IndexError:
            return False
    

if __name__ == '__main__':
    id1 = '1.10.1780.10'
    id2 = '1.10.510.10'
    inst = CathRequest(id1)
    file, id_fam = inst.get_fam(16)
    inst.get_species_file(file, id_fam)
    
    
