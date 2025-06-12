
import functionsUSP

"""Minhas classes """
from unit import Unit
from course import Course
import functionsUSP
from subject import Subject

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
from bs4.element import Tag
import time



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
            creditClass = cells[2].get_text(strip=True) or "0"
            credTrab = cells[3].get_text(strip=True) or "0"
            ch = cells[4].get_text(strip=True) or "0"
            ce = cells[5].get_text(strip=True) or "0"
            cp = cells[6].get_text(strip=True) or "0"
            atpa = cells[7].get_text(strip=True) or "0"
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
while True:

    try:
        quantityUnits = int (input())
        break
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


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

    for course in selectCourse.options[1:]:  # pula primeiro item da lista de options(lista de cursos)
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
                course.status_course()

                #Procura o botão de buscar e clica nele
                button_buscar(driver)

        except:

            # criação da instância do objeto Curso apenas, pois ele não possui dados a mais.
            course = Course(courseName, unitName)

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

while True:
    print("\n" + "=" * 55)
    print("Menu de Seleção:")
    print("1. Listar cursos por unidade")
    print("2. Dados de um determinado curso (com filtros um ou um conjunto deles: Nome do curso; Nome da unidade; Duração ideal; Duração mínima; Duração máxima; Código de disciplina; Nome de disciplina )")
    print("3. Dados de todos os cursos")
    print("4. Dados de uma determinada disciplina por filtro: (Código da disciplina; nome da disciplina; Crédito aulas; Carga horário; CH = Carga horária Total; CE = Carga horária de Estágio; CP = Carga horária de Práticas como Componentes Curriculares; ATPA = Atividades Teórico-Práticas de Aprofundamento) , inclusive quais cursos ela faz parte")
    print("5. Ver disciplinas compartilhadas por mais de um curso")
    print("6. Encerrar programa")
    print("=" * 55)

    opcao = input("Escolha uma opção: ")

    match opcao:


        case "1":
            print("Executando a opção 1....")

            print("\n--- Lista de cursos por unidades ---")
            functionsUSP.print_all_courses(all_units)

        case "2":
            print("Executando a opção 2....")

            print("\n--- Filtros do curso ---")
            nome = input("Digite o nome do curso (ou deixe em branco): ").strip() or None
            unidade = input("Digite a unidade do curso (ou deixe em branco): ").strip() or None

            try:
                minDur = int(input("Digite a duração mínima (ou 0 para ignorar): "))
                minDur = minDur if minDur > 0 else None
            except ValueError:
                minDur = None

            try:
                maxDur = int(input("Digite a duração máxima (ou 0 para ignorar): "))
                maxDur = maxDur if maxDur > 0 else None
            except ValueError:
                maxDur = None

            try:
                ideal = int(input("Digite a duração ideal (ou 0 para ignorar): "))
                ideal = ideal if ideal > 0 else None
            except ValueError:
                ideal = None

            codDisc = input("Código da disciplina (ou deixe em branco): ").strip() or None
            nomeDisc = input("Nome da disciplina (ou deixe em branco): ").strip() or None

            functionsUSP.data_course(
                all_units,
                courseName=nome,
                unitName=unidade,
                minDuration=minDur,
                maxDuration=maxDur,
                idealDuration=ideal,
                code=codDisc,
                nameSubject=nomeDisc
            )

        case "3":
            print("Executando a opção 3....")
            print("\n--- Dados de todos os cursos ---")
            functionsUSP.data_all_courses(all_units)

        case "4":
            print("Executando a opção 4....")
            print("\n--- Filtros da disciplina ---")
            code = input("Código (ou deixe em branco): ").strip() or None
            name = input("Nome da disciplina (ou deixe em branco): ").strip() or None

            try:
                ch = input("CH (ou pressione Enter para ignorar): ").strip()
                if ch == "":
                    ch = None  # considera que o filtro não será aplicado
            except ValueError:
                ch = None

            try:
                ce = input("CE (ou pressione Enter para ignorar): ").strip()
                if ce == "":
                    ce = None  # considera que o filtro não será aplicado
            except ValueError:
                ce = None

            try:
                cp = input("CP (ou pressione Enter para ignorar): ").strip()
                if cp == "":
                    cp = None  # considera que o filtro não será aplicado
            except ValueError:
                cp = None

            try:
                atpa = input("CH (ou pressione Enter para ignorar): ").strip()
                if atpa == "":
                    atpa = None  # considera que o filtro não será aplicado
            except ValueError:
                atpa = None

            functionsUSP.data_subject(
                all_units,
                code=code,
                nameSubject=name,
                ch=ch,
                ce=ce,
                cp=cp,
                atpa=atpa
            )

        case "5":
            print("Executando a opção 5....")
            print("\n--- Disciplinas compartilhadas entre cursos ---")
            functionsUSP.find_shared_subjects(all_units)

        case "6":
            print("Executando a opção 6....")
            print("Encerrando programa. Até logo!")
            break

        case _:
            print("Opção inválida! Por favor, tente novamente.")







