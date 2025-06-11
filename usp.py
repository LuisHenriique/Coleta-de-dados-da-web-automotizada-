from selenium.common import TimeoutException

from course import Course
import functionsUSP

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
import functionsUSP



def processar_tabela(table: Tag, course):
    """
    Processa uma única tabela HTML do BeautifulSoup

    """
    if not isinstance(table, Tag):
        raise TypeError("O argumento deve ser um objeto bs4.element.Tag")

    # pega as linhas da tabela atual
    rows = table.find_all('tr', style=lambda s: s and "height: 20px" in s and "background-color" not in s)

    if not rows:
        raise ValueError("Nenhuma linha válida encontrada na tabela")

    flagDisciplina = 0
    if (table.find(string="Disciplinas Obrigatórias")):
        flagDisciplina = 1
    elif (table.find(string="Disciplinas Optativas Livres")):
        flagDisciplina = 2
    if (table.find(string="Disciplinas Optativas Eletivas")):
        flagDisciplina = 3

    for row in rows:
        # procura as colunas da linha
        cells = row.find_all('td')

        if len(cells) >= 8:  # Ajuste conforme o número de colunas esperado
            codeSubject = cells[0].get_text(strip=True)
            nameSubject = cells[1].get_text(strip=True)
            creditClass = cells[2].get_text(strip=True) or "00"
            credTrab = cells[3].get_text(strip=True) or "00"
            ch = cells[4].get_text(strip=True) or "00"
            ce = cells[5].get_text(strip=True) or "00"
            cp = cells[6].get_text(strip=True) or "00"
            atpa = cells[7].get_text(strip=True) or "00"
            subjectRead = Subject(codeSubject, nameSubject, creditClass, credTrab, ch, ce, cp, atpa)


            course.insert_subject(subjectRead, flagDisciplina)




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



# Ler a quantidade de unidades que serão lidas
quantityUnits = int (input())


# Lista global para armazenar todas as unidades
all_units = []


# Inicializa o driver com timeout configurado
driver = setup_driver()
driver.set_page_load_timeout(25)  # Timeout de 30 segundos para carregar a página

url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"

try:
    # acessar url
    driver.get(url)

    # Espera por um elemento específico que indica que a página carregou
    WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.ID, "comboUnidade"))
    )
except TimeoutException:
    # Se houver erros, tenta recarregar a página
    driver.refresh()
    WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.ID, "comboUnidade"))
    )

selectUnits = Select(driver.find_element(By.ID, "comboUnidade"))


# Itera sobre TODAS as unidades (exceto a primeira que é vazia )

for units in selectUnits.options[1:]:  # pula primeiro item da lista de options(lista de unidades)
    # Para o loop se a quantidade unidades para serem lidas foram atingidas
    if quantityUnits == 0:
        break

    unitName = units.text
    unitValue = units.get_attribute("value")

    #Cria instância do objeto unidade e insere a unidade lista de unidades
    current_unit = Unit(name=unitName)
    all_units.append(current_unit)



    print(f"Selecionando unidade: {unitName} (valor={unitValue})")

    # Seleciona a nova unidade
    selectUnits.select_by_value(unitValue)

    # Espera até o número de cursos mudar — isso garante que os cursos novos carregaram
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "comboCurso")))
    time.sleep(0.4)

    # Agora sim, re-obtem os cursos
    selectCourse = Select(driver.find_element(By.ID, "comboCurso"))

    for course in selectCourse.options[7:]:  # pula primeiro item da lista de options(lista de cursos)
        courseName = course.text
        courseValue = course.get_attribute("value")
        print(f"Selecionando curso: {courseName} (valor={courseValue})")
        selectCourse.select_by_value(courseValue)

        time.sleep(0.4)

        # Após ter selecionada o curso clica no butão buscar
        searchButtonOne = driver.find_element(By.ID, "enviar")
        searchButtonOne.click()

        # Cria uma instância do objeto unidade
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


            # criação da instância do objeto Curso
            course = Course(courseName, unitName, int(durationIdeal), int(durationMin), int(durationMax))

            try:
                # verifica se o primeiro  os links presentes na tabela de disciplinas está disponível, se não estiver cai no execept
                linksDisciplina = soup.find_all("a", class_="disciplina")

                # captura informações da div  que contém as tabelas de disciplinas
                divGradeCurricular = soup.find('div', id="gradeCurricular")
                # seleciona todas as tabelas presentes na div gradeCurricular, obtenho uma lista de tabelas
                tables = divGradeCurricular.find_all('table')


                # raspando os dados das linhas(tr) da  tabela 1 que tenham esse style

                for table in tables:
                    processar_tabela(table, course)
                time.sleep(2)
            except:
                raise ValueError("Erro ao tentar processar tabela de disciplinas ")

            finally:
                #imprime o estado atual do course
                course.status()

                #Procura o botão de buscar e clica nele
                button_buscar(driver)

        except:
            # se não achou procura o botão de voltar
            closeButton = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Fechar']"))
            )
            closeButton.click()
            time.sleep(1)

        finally:
            #insere os cursos na lista de cursos da unidade respectiva
            current_unit.add_courses(course)

    # decrementa a quantidade de unidades
    quantityUnits-=1


#Finaliza o webScraping
driver.quit()

"""Funcionalidades após a coleta de dados da web"""
print("\n############Finalizado a coleta de dados, agora imprime o solicitado##################\n")
#lista de cursos por unidade
functionsUSP.print_all_courses(all_units)


# Dados de um determinado curso:
functionsUSP.data_course(all_units, "marketing")
print()


#Dados de todos os cursos
functionsUSP.data_all_courses(all_units)
print()
