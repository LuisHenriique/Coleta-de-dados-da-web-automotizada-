from selenium.common import TimeoutException

from course import Course

"""Minhas classes """
from unit import Unit
from subject import Subject

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from bs4.element import Tag
import time

i = 0
j = 0


def processar_tabela(tabela: Tag):
    """
    Processa uma única tabela HTML do BeautifulSoup

    """
    if not isinstance(tabela, Tag):
        raise TypeError("O argumento deve ser um objeto bs4.element.Tag")

    # pega as linhas da tabela atual
    rows = tabela.find_all('tr', style=lambda s: s and "height: 20px" in s and "background-color" not in s)

    if not rows:
        raise ValueError("Nenhuma linha válida encontrada na tabela")
    indice = 0  # variavel auxiliar para saber qual é a tabela que estamos trabalhando
    # seleciona uma linha das linhas

    for row in rows:
        # procura as colunas da linha
        cells = row.find_all('td')

        if len(cells) >= 8:  # Ajuste conforme o número de colunas esperado
            codeSubject = cells[0].get_text(strip=True)
            nameSubject = cells[1].get_text(strip=True)
            credtSub = cells[2].get_text(strip=True)
            credTrab = cells[3].get_text(strip=True)
            ch = cells[4].get_text(strip=True)
            ce = cells[5].get_text(strip=True)
            cp = cells[6].get_text(strip=True)
            atpa = cells[7].get_text(strip=True)

            match indice:
                case 0:
                    print("Disciplinas Obrigatórias")
                    subjectsMan = Subject(codeSubject, nameSubject, credtSub, credTrab, ch, ce, cp, atpa)
                case 1:
                    print("Disciplinas Optativas Livres")
                    subjectsOpLiv = Subject(codeSubject, nameSubject, credtSub, credTrab, ch, ce, cp, atpa)

                case 2:
                    print("Disciplinas Optativas Eletivas")
                    subjectsOpEl = Subject(codeSubject, nameSubject, credtSub, credTrab, ch, ce, cp, atpa)

            print(
                f"\nCódigo: {codeSubject} -- Disciplina: {nameSubject} -- Créditos: {credtSub} -- Créditos Trabalho: {credTrab} -- Carga Horária: {ch} -- CE: {ce} -- CP: {cp} --     ATPA: {atpa}\n")
            indice += 1


def setup_driver():
    """Configura o driver com opções para melhor estabilidade"""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # Evita problemas de memória
    options.add_argument('--start-maximized')  # Maximiza a janela
    options.add_argument('--disable-extensions')
    return webdriver.Chrome(options=options)

def button_buscar(driver):
    searchButtonTwo = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "step1-tab"))
    )

    searchButtonTwo.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "comboUnidade")))


# Inicializa o driver com timeout configurado
driver = setup_driver()
driver.set_page_load_timeout(20)  # Timeout de 30 segundos para carregar a página

url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"

try:
    # acessar url
    driver.get(url)

    # Espera por um elemento específico que indica que a página carregou
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "comboUnidade"))
    )
except TimeoutException:
    # Se houver erros, tenta recarregar a página
    driver.refresh()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "comboUnidade"))
    )

selectUnits = Select(driver.find_element(By.ID, "comboUnidade"))


# Itera sobre TODAS as unidades (exceto a primeira que é vazia )


for units in selectUnits.options[11:]:  # pula primeiro item da lista de options(lista de unidades)

    unitName = units.text
    unitValue = units.get_attribute("value")

    print(f"Selecionando unidade: {unitName} (valor={unitValue})")

    # Seleciona a nova unidade
    selectUnits.select_by_value(unitValue)
    i += 1
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

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "tabs")))

        try:  ## tentar achar o botão de grades

            # Espera o overlay de carregamento sumir
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "blockUI"))
            )

            gradesCurriculum = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "step4-tab"))
            )

            gradesCurriculum.click()

            # após ter entrada na aba de grades curriculares, espera certa de 2 segundos para sair dela
            time.sleep(2.5)

            # obtém o conteúdo html da página
            page_content = driver.page_source

            # cria um objeto beautifulSoup
            soup = BeautifulSoup(page_content, 'html.parser')

            # captura os dados de duração do curso
            durationIdeal = soup.find('span', class_="duridlhab").get_text(strip=True)
            durationMin = soup.find('span', class_="durminhab").get_text(strip=True)
            durationMax = soup.find('span', class_="durmaxhab").get_text(strip=True)

            courseTest = Course(courseName, unitName, durationIdeal, durationMin, durationMax)

            try:
                # verifica se o primeiro  os links presentes na tabela de disciplinas está disponível, se não estiver cai no execept
                linksDisciplina = soup.find_all("a", class_="disciplina")

                # captura informações da div  que contém as tabelas de disciplinas
                divGradeCurricular = soup.find('div', id="gradeCurricular")
                # seleciona todas as tabelas presentes na div gradeCurricular, obtenho uma lista de tabelas
                tables = divGradeCurricular.find_all('table')

                courseTest.status()

                # raspando os dados das linhas(tr) da  tabela 1 que tenham esse style

                for table in tables:
                    processar_tabela(table)
                time.sleep(2)
            except:
                print("Erro ao tentar processar tabela de disciplinas ")
            finally:

                button_buscar(driver)



        except:
            # se não achou procura o botão de voltar
            closeButton = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Fechar']"))
            )
            closeButton.click()
            time.sleep(1)



driver.quit()
print(f"numeros de unidades:{i}")
print(f"numeros de cursos{j}")