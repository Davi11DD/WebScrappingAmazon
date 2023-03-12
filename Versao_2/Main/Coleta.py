# IMPORTS =========================================================================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

from Facilitar import *
import time

class Coletar :

    def __init__(self, driver, url, nome_produto, preco_min, preco_max, nPaginas, analisador=0) :

        self.CriarArquivos(nome_produto)
        self.Dados()

        self.preco_min = preco_min
        self.preco_max = preco_max
        self.produtos = {'nomes':[], 'preços':[], 'links':[]}



        
        for pagina in range(1, nPaginas+1) :
            inicio = time.time()

            Esperar.MudarURL(driver, url)
            url = driver.current_url

            BotaoProximo = Esperar.UmPorCss(driver, '.s-pagination-next'      )
            Grade     = Esperar.UmPorCss(driver,    '.s-main-slot'            )
            Elementos = Esperar.MuitosPorCss(Grade, '.s-card-container'       )


            if   analisador == 0  :self.AnalisarCadaProduto_Soup(Grade)
            elif analisador == 1 : self.AnalisarCadaProduto_Selenium(Grade)
            

          


            driver.execute_script('arguments[0].click()', BotaoProximo)

            fim = time.time()
            self.tempoPorPagina.append(fim - inicio)

        self.preencherGeral()


# FUNÇÕES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


    def AnalisarCadaProduto_Selenium(self, Grade) :
        produtos = Esperar.MuitosPorCss(Grade, '.s-card-container' )

        for produto in produtos :

            try: nome = produto.find_element(By.TAG_NAME, 'h2').text
            except : nome = -1

            try : preco = produto.find_element(By.CSS_SELECTOR, 'span[class="a-price-whole"]').text.replace('.', '')
            except: preco = -1

            try: link = 'https://www.amazon.com.br/'+produto.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except:  link = -1

            self.FiltroDeProduto(nome, preco, link)


            print(nome)
            print(preco)
            print(link,'\n')



    def AnalisarCadaProduto_Soup(self, Grade) :
        sopa = BeautifulSoup(Grade.get_property('outerHTML'), 'html.parser')
        produtos = sopa.find_all(class_='s-card-container' )

        for produto in produtos :
            self.produtosTotais += 1

            try: nome = produto.find('h2').get_text()
            except: nome = -1

            try: preco = produto.find('span', class_='a-price-whole').get_text().replace('.', '').replace(',', '')
            except: preco = -1

            try: link = 'https://www.amazon.com.br/'+produto.find('a').get('href')
            except: link = -1

            self.FiltroDeProduto(nome, preco, link)


            print(nome)
            print(preco)
            print(link,'\n')




    def FiltroDeProduto(self, nome, preco, link) :
        preco = float(preco)
        produtoAcimaOuAbaixoDoPreco = False

        if -1 < preco < self.preco_min or preco > self.preco_max: 
            produtoAcimaOuAbaixoDoPreco = True
            self.produtoForaDoPreco += 1

        if preco == -1 : self.produtosSemPreco += 1


        if (nome!=-1 and preco!=-1 and link!=-1) and produtoAcimaOuAbaixoDoPreco == False :
            self.arquivo.write(f'{nome} \n')
            self.arquivo.write(f'{preco}\n')
            self.arquivo.write(f'{link} \n\n')

            self.produtos['nomes'].append(nome)
            self.produtos['preços'].append(preco)
            self.produtos['links'].append(link)

            self.produtosArmazenados += 1
        else :
            self.produtosNaoColetados +=1

    


    
    def Dados(self) :
        self.produtosTotais       = 0
        self.produtosArmazenados  = 0
        self.produtoForaDoPreco   = 0
        self.produtosNaoColetados = 0
        self.produtosSemPreco     = 0
        self.tempoPorPagina       = []
        

    def CriarArquivos(self, nome_produto) :
        open(f'./Versao_2/DadosColetados/{nome_produto}.txt',       'w', encoding='UTF-8')
        open(f'./Versao_2/DadosColetados/Geral_{nome_produto}.txt', 'w', encoding='UTF-8')

        self.arquivo      = open(f'./Versao_2/DadosColetados/{nome_produto}.txt', 'a',       encoding='UTF-8')
        self.arquivoGeral = open(f'./Versao_2/DadosColetados/Geral_{nome_produto}.txt', 'a', encoding='UTF-8')


    def preencherGeral(self) :
        self.arquivoGeral.write(f"""Preço Mínimo: {self.preco_min} \nPreço Máximo: {self.preco_max}
        \nProdutos totais encontrados:    {self.produtosTotais}
        \nProdutos Armazenados:           {self.produtosArmazenados}
        \nProdutos não coletados:         {self.produtosNaoColetados}
        \nProdutos sem preço disponível : {self.produtosSemPreco} 
        \nProdutos acima ou abaixo das prefeências: {self.produtoForaDoPreco}  \n\n
        """)

        for e, p in enumerate(self.tempoPorPagina) :
            self.arquivoGeral.write(f'\nPagina {e+1} : {p:.2f}')

        
        self.arquivo.close()


# GETTERS ==================================================================================================================

    def getArquivoGeral(self):
        return self.arquivoGeral
    def getArquivo(self):
        return self.arquivo


    def getNomes(self) :
        return self.produtos['nomes']

    def getPrecos(self) :
        return self.produtos['preços']

    def getLinks(self) :
        return self.produtos['links']
    
