import requests
from bs4 import BeautifulSoup
import time


class CathRequest:
    def __init__(self, superfamily_id):
        self.superfamily_id = superfamily_id
        self.client = requests.session()
        
    def _get_info(self):
        fam_set = set()
        url_1 = f"http://www.cathdb.info/version/latest/superfamily/{self.superfamily_id}/alignments" 
        r1 = self.client.get(url=url_1, timeout=50)
        
        # BS4
        soup = BeautifulSoup(r1.content, "html.parser")
        if 'CATH: Internal Error' in soup.text:
            raise CathInternalError(f"An error has ocurred when retrieving the superfamily - {self.superfamily_id}"
                                    f" information from CATH database, verify if"
                                    f" you are putting the correct superfamily id")

        with open("arquivo.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        all_a = soup.find_all('a')
        funfam_menu = f"FUNCTIONAL FAMILIES OF SUPERFAMILY: {self.superfamily_id}\n"
        for a in all_a[17:]:
            if 'CATH News' in a.text:
                break
            path = a["href"]
            file_name = self._get_file_name(path, 2)
            fam_id = self._get_file_name(path, 1)
            fam_name = a.text
            if fam_name.isnumeric():
                continue
            elif fam_name == '':
                fam_name = 'N/A'
            if file_name == 'funfam' and fam_id not in fam_set:
                funfam_menu += f"  {fam_id} ----- {fam_name}\n"
                fam_set.add(int(fam_id))
        print(funfam_menu)
        self._select_family(fam_set)

    def _select_family(self, fam_set: set):
        while True:
            try:
                input_number = int(input("\n\nSelect funfam number:"))
                if input_number in fam_set:
                    break
                else:
                    print(f'The input: {input_number} is not a functional'
                          f'family in the superfamily: {self.superfamily_id}')
                    time.sleep(1.5)

            except ValueError:
                print("You must put a number representative of a functional family for this superfamily")
        stock, funfam_name = self._get_fam(input_number)
        self._get_species_file(stock, input_number, funfam_name)

    def _get_fam(self, funfam_id: int):
        url_2 = f"http://www.cathdb.info/version/latest/superfamily/{self.superfamily_id}/funfam/{funfam_id}/alignment"
        r2 = self.client.get(url=url_2, timeout=50)
        soup2 = BeautifulSoup(r2.content, "html.parser")
        funfam_name = ''
        has_name = False
        for name in soup2.find_all('h2'):
            if 'FunFam' in name.text:
                funfam_name = name.text.split(':')
                funfam_name = funfam_name[-1]
                if funfam_name == '':
                    has_name = True
        if not has_name:
            funfam_name = funfam_id

        if '(en) Please come back later' in soup2.text:
            raise CathInternalError(f"An error has ocurred when retrieving the functional family"
                                    f" information from CATH database, verify if"
                                    f" you are putting the correct funfam id")
        classe = soup2.find('a', class_="btn btn-small btn-info")
        stock_file = classe['href']
        
        return stock_file, funfam_name
    
    def _get_species_file(self, stock_file, funfam_id: int, funfam_name: str):
        r3 = self.client.get(url=stock_file, timeout=50)
        soup3 = BeautifulSoup(r3.content, "html.parser")
        new_file_name = f"{self.superfamily_id}:{funfam_id}-Species.txt"
        with open(new_file_name, "w", encoding="utf-8") as f:
            f.write(str(soup3))
        self._species_names(new_file_name, funfam_name)

    @staticmethod
    def _species_names(path: str, funfam_name: str):
        specs = []
        sps_verified = set()
        sp_msg = f'\n------- UNIQUE SPECIES FROM: {funfam_name} -------\n'
        with open(path, 'r') as f:
            content = f.readlines()
        for line in content:
            if 'OS' in line:
                spec = line.rsplit('OS')
                spec = spec[-1]
                specs.append(spec)
        for sp in specs:
            if sp not in sps_verified:
                sp_msg += f"{sp}\n"
                sps_verified.add(sp)
        print(sp_msg)

    @staticmethod
    def _get_file_name(href: str, house: int):
        file_name = href.split("/")
        try:
            file_name = file_name[-house]
            return file_name
        except IndexError:
            return False
    
    def run(self, opt: int, funfam_id: int):
        if opt == 1:
            self._get_info()
        elif opt == 2:
            stock, funfam_name = self._get_fam(funfam_id)
            self._get_species_file(stock, funfam_id, funfam_name)


class CathInternalError(Exception):
    pass


if __name__ == '__main__':
    id1 = '1.10.1780.10'
    id2 = '1.10.510.10'
    inst = CathRequest(id2)
    inst.run(1, 16)
    