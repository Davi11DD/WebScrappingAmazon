from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Esperar :
    def UmPorCss( area, seletor ) : 
        return WebDriverWait( area, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor )))

    def MuitosPorCss(area, seletor) :
        return WebDriverWait( area, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor ) ) )

    def AlgumPorCss(area , seletores) :
        for seletor in seletores :
            try : return WebDriverWait( area, 3).until(EC.presence_of_element_located((  By.CSS_SELECTOR, seletor ) ) )
            except : print(f'\033[1;33mO Seletor "{seletor}" não funcionou\033[m"')

    


    def MudarURL(area ,url) :
        return WebDriverWait( area, 5 ).until(EC.url_changes(url) )
