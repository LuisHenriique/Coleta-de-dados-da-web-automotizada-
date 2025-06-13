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
    elif (table.find(string="Disciplinas Optativas Eletivas")):
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

# Tenta abrir a página até 5 vezes
max_tentativas = 5
sucesso = False


for tentativa in range(1, max_tentativas + 1):
    try:
        print(f"Tentativa {tentativa} de {max_tentativas} para abrir a página...")
        driver.get(url)
        # Dá tempo da página estabilizar
        time.sleep(3)


        # Espera o carregamento do elemento
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "comboUnidade"))
        )

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "comboCurso"))
        )



        sucesso = True
        print("Página carregada com sucesso.")
        break  # Sai do loop se der certo

    except TimeoutException:
        print(f"Timeout na tentativa {tentativa}. Recarregando a página...")
        try:
            driver.refresh()
            print("Recarregando a página em 2 segundos...")
            time.sleep(2)  # Espera um pouco antes de tentar novamente
        except Exception as e:
            print(f"Erro ao tentar recarregar: {e}")
            time.sleep(2)



if not sucesso:
    print("Não foi possível carregar a página após várias tentativas.")
    print("Encerrando programa....")
    exit()

# Cria uma lista de options, que no caso cada options é uma unidade
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



    print(f"\nSelecionando unidade: {unitName} (valor={unitValue})")

    # Seleciona a nova unidade
    selectUnits.select_by_value(unitValue)

    # Espera até o número de cursos mudar — isso garante que os cursos novos carregaram
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "comboCurso")))
    time.sleep(0.4)

    # Agora sim, re-obtem os cursos
    selectCourse = Select(driver.find_element(By.ID, "comboCurso"))
    course_obj = None
    for course in selectCourse.options[1:]:  # pula primeiro item da lista de options(lista de cursos)
        courseName = course.text
        courseValue = course.get_attribute("value")

        print(f"\nSelecionando curso: {courseName} (valor={courseValue})")
        selectCourse.select_by_value(courseValue)

        time.sleep(0.4)

        # Após ter selecionada o curso clica no butão buscar
        searchButtonOne = driver.find_element(By.ID, "enviar")
        searchButtonOne.click()

        # Cria uma instância do objeto unidade
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "tabs")))

        try:  ## tentar achar o botão de grades

            # Espera o overlay de carregamento sumir
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "blockUI"))
            )

            gradesCurriculum = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "step4-tab"))
            )

            gradesCurriculum.click()


            # após ter entrada na aba de grades curriculares, espera certa de 3 segundos para sair dela
            time.sleep(3)

            # obtém o conteúdo html da página
            page_content = driver.page_source

            # cria um objeto beautifulSoup
            soup = BeautifulSoup(page_content, 'html.parser')

            # captura os dados de duração do curso
            durationIdeal = soup.find('span', class_="duridlhab").get_text(strip=True)
            durationMin = soup.find('span', class_="durminhab").get_text(strip=True)
            durationMax = soup.find('span', class_="durmaxhab").get_text(strip=True)


            # criação da instância do objeto Curso
            course_obj = Course(courseName, unitName, int(durationIdeal), int(durationMin), int(durationMax))

            try:
                # verifica se o primeiro  os links presentes na tabela de disciplinas está disponível, se não estiver cai no execept
                linksDisciplina = soup.find_all("a", class_="disciplina")

                # captura informações da div  que contém as tabelas de disciplinas
                divGradeCurricular = soup.find('div', id="gradeCurricular")
                # seleciona todas as tabelas presentes na div gradeCurricular, obtenho uma lista de tabelas
                tables = divGradeCurricular.find_all('table')


                # raspando os dados das linhas(tr) da  tabela 1 que tenham esse style

                for table in tables:
                    processar_tabela(table,course_obj)
                time.sleep(2)
            except:
                raise ValueError("Erro ao tentar processar tabela de disciplinas ")

            finally:
                #imprime o estado atual do course_obj
                course_obj.status_course()

                #Procura o botão de buscar e clica nele
                button_buscar(driver)

        except:

            # criação da instância do objeto Curso apenas, pois ele não possui dados a mais.
            course_obj = Course(courseName, unitName)

            # se não achou procura o botão de voltar
            closeButton = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Fechar']"))
            )
            closeButton.click()
            time.sleep(1)

        finally:
            #insere os cursos na lista de cursos da unidade respectiva
            current_unit.add_courses(course_obj)

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
            print("\nExecutando a opção 1....")

            print("\n--- Lista de cursos por unidades ---")
            print()

            functionsUSP.print_all_courses(all_units)

        case "2":
            print("\nExecutando a opção 2....")

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


            print(f"\nfiltros selecionados: ({unidade if unidade != None else "-"}, {nome if nome != None else "-"}, {minDur if minDur != None else "-"}, {maxDur if maxDur != None else "-"}, {ideal if ideal != None else "-"}, {codDisc if codDisc != None else "-"}, {nomeDisc if nomeDisc != None else "-"})  *Obs:(-) filtros não utilizados ")
            print()

            functionsUSP.data_course(
                all_units,
                unitName=unidade,
                courseName=nome,
                minDuration=minDur,
                maxDuration=maxDur,
                idealDuration=ideal,
                subjectCode=codDisc,
                subjectName=nomeDisc
            )

        case "3":
            print("\nExecutando a opção 3....")
            print("\n--- Dados de todos os cursos ---")
            print()

            functionsUSP.data_all_courses(all_units)

        case "4":
            print("\nExecutando a opção 4....")
            print("\n--- Filtros da disciplina ---")
            code = input("Código (ou deixe em branco): ").strip() or None
            name = input("Nome da disciplina (ou deixe em branco): ").strip() or None

            try:
                creditsClass = int(input("Créd. Aulas (ou pressione Enter para ignorar): ").strip())
                creditsClass = creditsClass if creditsClass > 0 else None
            except ValueError:
                creditsClass = None

            try:
                ch = int(input("CH (ou pressione Enter para ignorar): ").strip())
                ch =  ch if ch > 0 else None
            except ValueError:
                ch = None

            try:
                ce = int(input("CE (ou pressione Enter para ignorar): ").strip())
                ce = ce if ce > 0 else None
            except ValueError:
                ce = None

            try:
                cp = int(input("CP (ou pressione Enter para ignorar): ").strip())
                cp = cp if cp > 0 else None
            except ValueError:
                cp = None

            try:
                atpa = int(input("CH (ou pressione Enter para ignorar): ").strip())
                atpa = atpa if atpa > 0 else None
            except ValueError:
                atpa = None


            print(f"\nfiltros selecionados: ({code if code != None else "-"}, {name if name!=None else "-"}, {creditsClass if creditsClass !=None else "-"}, {ch if ch !=None else "-"}, {ce if ce !=None else "-"}, {cp if cp !=None else "-"}, {atpa if atpa !=None else "-" })  *Obs:(-) filtros não utilizados")
            print()
            functionsUSP.data_subject(
                all_units,
                code=code,
                nameSubject=name,
                creditsClass = creditsClass,
                ch=ch,
                ce=ce,
                cp=cp,
                atpa=atpa
            )

        case "5":
            print("\nExecutando a opção 5....")
            print("\n--- Disciplinas compartilhadas entre cursos ---")
            print()

            functionsUSP.find_shared_subjects(all_units)

        case "6":
            print("\nExecutando a opção 6....")
            print("Encerrando programa. Até logo!")
            print()

            break

        case _:
            print("\nOpção inválida! Por favor, tente novamente.\n")







