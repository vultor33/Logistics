from selenium import webdriver
from selenium.webdriver.common.keys import Keys

caminho_geckodriver = r'D:/PROGRAMAS/geckodriver.exe'
driver = webdriver.Firefox(executable_path=caminho_geckodriver)
driver.get('https://novo.org.br/')
loja = driver.find_element_by_link_text('LOJA')
loja.click()
newsletter = driver.find_element_by_id('newsletter-input') # e possivel achar o id clicando com o botao direito e selecionando "inspecionar elemento"
newsletter.send_keys('me inscrevendo no novo')
newsletter.send_keys(Keys.ENTER)