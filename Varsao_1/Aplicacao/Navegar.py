# IMPORTS ================================================================
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ////////////////////////////////////////////////////////////////////////
# CONFIGS INICIAIS =======================================================
chormeService = Service(ChromeDriverManager().install())
chromeOptions = Options()

class Coletar :
    def __init__(self, nome_produto, preco_min=0, preco_max=999999, visibilidade = True) :
        
        open(f'./DadosColetados/{nome_produto}.txt', 'w', encoding='UTF-8')
        arquivo = open(f'./DadosColetados/{nome_produto}.txt', 'a', encoding='UTF-8')

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////
# DRIVER =====================================================================================================
        driver = webdriver.Chrome(service=chormeService, options=chromeOptions)
        driver.get('https://www.amazon.com.br/')

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
# PAGINA INICIAL ============================================================================================
        url = driver.current_url # URL - Pag Inicial

        try : inputDeProcura = WebDriverWait(driver, 1100).until( EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        except : inputDeProcura = WebDriverWait(driver, 1100).until( EC.presence_of_element_located((By.CSS_SELECTOR, ".nav-bb-serach")))
        inputDeProcura.send_keys(nome_produto)
        inputDeProcura.submit()

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
#  PAGINAS DE CONTEUDO ======================================================================================
        WebDriverWait(driver , 11).until(EC.url_changes(url))
        pagina = 1
        totalProdutos = 0
        totalProdutosPref = 0
        falsoProdutos = 0
        numPags = WebDriverWait( driver , 11 ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, '.s-pagination-strip') ) ).find_elements(By.TAG_NAME, 'span')[-1].text
        print(f'\n\n\n\033[1;36mPAGINAS {numPags}\033[m\n\n\n')


        for c in range(0, int(numPags)) :
            print(f'\n\n\n\033[1;34mPAGINA {pagina}\033[m')

            WebDriverWait(driver , 11).until(EC.url_changes(url))
            url = driver.current_url


            Next   =  WebDriverWait( driver, 5 ).until( EC.presence_of_element_located(      ( By.CSS_SELECTOR, '.s-pagination-next') ) )
            grade  =  WebDriverWait( driver, 5 ).until( EC.presence_of_element_located(      ( By.CSS_SELECTOR, '.s-main-slot'      ) ) )
            elemts =  WebDriverWait( grade , 5 ).until( EC.presence_of_all_elements_located( ( By.CSS_SELECTOR, '.s-card-container' ) ) )
            print('\033[1;32mTotal de produtos encontrados: ',len(elemts), end='\033[m\n\n')


            for c in elemts : # COLETA DE CADA PRODUTO
                totalProdutos += 1
                tem_preco = True

                try :
                    nome = c.find_element(By.TAG_NAME, 'h2').text
                    try: preco = c.find_element(By.CSS_SELECTOR, 'span[class="a-price-whole"]').text.replace('.', '')
                    except: 
                        preco ='\033[1;31mSEM INFORMAÇÃO DE PREÇO\033[m\n'
                        tem_preco = False
               


                    if tem_preco == True and (preco_min <= float(preco) <= preco_max) :
                        arquivo.write(nome+'\n')
                        arquivo.write(preco+'\n\n')
                        totalProdutosPref += 1
                except : 
                    nome = ''
                    preco = ''
                    falsoProdutos += 1
                    
                print(nome)
                print(preco)


            Next.click()
            pagina += 1


        with open(f'./DadosColetados/Geral_{nome_produto}.txt', 'w', encoding="UTF-8") as geral :
            geral.write(f'Preço Minimo: {preco_min} \nPreço Maximo: {preco_max}\n')
            geral.write(f'Total de produtos : {totalProdutos-falsoProdutos} \nTotal de produtos sobre preferencias : {totalProdutosPref}\n')
            geral.write(f'Total de paginas vistas : {pagina-1}')



    







      


