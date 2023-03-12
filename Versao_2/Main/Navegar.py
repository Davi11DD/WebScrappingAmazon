# IMPORTS =========================================================================================
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep
from Facilitar import *
from Coleta    import *

# CONFIGS INICIAIS ================================================================================
chormeService = Service(ChromeDriverManager().install())
chromeOptions = Options() 
chromeOptions.add_argument('--window-size=1200,600')
chromeOptions.add_argument('--window-position=40,0')




class Navegar :
    def __init__(self, nome_produto, preco_min, preco_max, nPaginas) :

        driver = webdriver.Chrome(service=chormeService, options=chromeOptions) # DRIVER >>>>>>>>>>>>>>>>>>
        url = 'https://www.amazon.com.br/'
        driver.get(url)

# PAGINA INICIAL ==================================================================================

        inputSearch = Esperar.AlgumPorCss(driver ,['#twotabsearchtextbox', '.nav-bb-serach'])
        inputSearch.send_keys(nome_produto)
        inputSearch.send_keys(Keys.ENTER)

        Esperar.MudarURL(driver , url)

# PAGINAS DE CONTEUDO =============================================================================

        self.Busca = Coletar(driver, url, nome_produto, preco_min, preco_max, nPaginas)



        driver.quit()

    
    def getArquivoGeral(self) :
        return self.Busca.getArquivoGeral()
    
    def getArquivo(self) :
        return self.Busca.getArquivo()

    def getNomes(self) :
        return self.Busca.getNomes()
    
    def getPrecos(self) :
        return self.Busca.getPrecos()

    def getLinks(self) :
        return self.Busca.getLinks()
