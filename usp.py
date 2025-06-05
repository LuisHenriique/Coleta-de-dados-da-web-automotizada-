from dataclasses import dataclass

"""Minhas classes """
from unit import Unit
from subject import Subject
from course import Course

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # usado para esperar entre ações

i = 0
j = 0
# Coleta de dados da página web
# vai pra o navegador
driver = webdriver.Chrome()

#vai para o link abaixo
driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

# aguarda o site carregar completamente
driver.implicitly_wait(20) # seconds


selectUnits =Select(driver.find_element(By.ID, "comboUnidade"))


# Itera sobre TODAS as unidades (exceto a primeira que é vazia )


for units in selectUnits.options[1:]: # pula primeiro item da lista de options(lista de unidades)

    unitName = units.text
    unitValue = units.get_attribute("value")

    print(f"Selecionando unidade: {unitName} (valor={unitValue})")

    # Seleciona a nova unidade
    selectUnits.select_by_value(unitValue)
    i+=1
    # Espera até o número de cursos mudar — isso garante que os cursos novos carregaram
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "comboCurso")))
    time.sleep(0.4)

    # Agora sim, re-obtem os cursos
    selectCourse = Select(driver.find_element(By.ID, "comboCurso"))

    for course in selectCourse.options[1:]:  # pula primeiro item da lista de options(lista de cursos)
        courseName = course.text
        courseValue = course.get_attribute("value")
        print(f"Selecionando curso: {courseName} (valor={courseValue})")
        selectCourse.select_by_value(courseValue)
        j += 1
        time.sleep(0.4)

        # Após ter selecionada o curso clica no butão buscar
        searchButtonOne = driver.find_element(By.ID, "enviar")
        searchButtonOne.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "step1-tab")))
        time.sleep(0.5)

        # encontra o link de grades curriculares e clica nele para acessar a página a qual seá lida as informações
        gradesCurriculum = driver.find_element(By.ID, "step4-tab")

        # Teste para verificar possível erro: espera que overlay desapareça

        time.sleep(0.7)
        gradesCurriculum.click()
        time.sleep(0.6)

        # usa o beautiful para ler baixar a página web

        # retorna para aba buscar
        searchButtonTwo = driver.find_element(By.ID, "step1-tab")
        searchButtonTwo.click()



driver.quit()

print(f"numeros de unidades:{i}")
print(f"numeros de cursos{j}")
