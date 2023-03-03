# IMPORTS ================================================================
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#/////////////////////////////////////////////////////////////////////////
# CONFIGS INICIAIS =======================================================
chormeService = Service(ChromeDriverManager().install())
chromeOptions = Options() 

#/////////////////////////////////////////////////////////////////////////
# MAIN ===================================================================


#/////////////////////////////////////////////////////////////////////////
# CÓDIGO =================================================================

class Navegar :
    def __init__(self, nome_produto) :

        open(f'./DadosColetados/{nome_produto}.txt', 'w', encoding='UTF-8')

        driver = webdriver.Chrome(service=chormeService, options=chromeOptions)
        driver.get('https://www.amazon.com.br/')

        url = driver.current_url

        inputDeProcura = WebDriverWait(driver, 11).until( EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        inputDeProcura.send_keys(nome_produto)
        inputDeProcura.submit()



        pagina = 0
        tentativas = 0

        while True :
            
            
            tentativas +=1
            if pagina == 11 : break

            if url != driver.current_url :    
                pagina += 1

                print(f'\n\n\n\033[1;34mPAGINA {pagina}\033[m')
                print(f'\033[1;33mAté carregar : {tentativas}\033[m')
                arquivo = open(f'./DadosColetados/{nome_produto}.txt', 'a', encoding='UTF-8')
                arquivo.write(f'=================================== PAGINA {pagina} ====================================\n\n\n')


                WebDriverWait(driver, 11).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.s-pagination-next')))
                produtos = WebDriverWait(driver, 11).until( EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.s-card-container')))
                print('\033[1;32mTotal de produtos encontrados: ',len(produtos), end='\033[m\n\n')


                for c in produtos : 

                    nome = c.find_element(By.CSS_SELECTOR, 'h2').text
                    try: preco = c.find_element(By.CSS_SELECTOR, 'span[class="a-price-whole"]').text
                    except: preco ='\033[1;31mSEM INFORMAÇÃO DE PREÇO\033[m\n'

                    arquivo.write(nome+'\n')
                    arquivo.write(preco+'\n\n')

                    print(nome)
                    print(preco)


                botao_proximo = WebDriverWait(driver, 11).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.s-pagination-next')))
                botao_proximo.click()

                tentativas = 0









