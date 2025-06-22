"""
Script principal executável para o projeto de Web Scraper da USP.

Este script executa duas funções primárias:
1.  Raspagem de Dados (Web Scraping): Inicia um navegador Chrome controlado
    pelo Selenium para navegar no site Júpiter Web da USP. Ele itera
    sistematicamente através das unidades e seus cursos, analisando o HTML
    com BeautifulSoup para extrair dados sobre cada curso e suas disciplinas.
2.  Interação com o Usuário: Após a conclusão da raspagem, apresenta um menu
    de linha de comando que permite ao usuário consultar os dados coletados
    de várias maneiras.
"""
# Imports de classes locais
from unit import Unit
from course import Course
import functionsUSP
from subject import Subject

# Imports de bibliotecas de terceiros
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
     Processa uma tabela HTML contendo as disciplinas de um curso.

    Função responsável por extrair os dados de disciplinas de uma tabela HTML (obtida via BeautifulSoup),
    identificar o tipo de disciplina (Obrigatória, Optativa Livre ou Optativa Eletiva),
    criar objetos da classe Subject e inseri-los no curso correspondente.
    """
    if not isinstance(table, Tag):
        raise TypeError("O argumento deve ser um objeto bs4.element.Tag")

    # Captura todas as linhas da tabela com o estilo específico de linha de disciplina
    rows = table.find_all('tr', style=lambda s: s and "height: 20px" in s and "background-color" not in s)

    if not rows:
        raise ValueError("Nenhuma linha válida encontrada na tabela")

    # Determina o tipo de disciplina com base no texto encontrado na tabela
    flagDisciplina = 0
    if (table.find(string="Disciplinas Obrigatórias")):
        flagDisciplina = 1
    elif (table.find(string="Disciplinas Optativas Livres")):
        flagDisciplina = 2
    elif (table.find(string="Disciplinas Optativas Eletivas")):
        flagDisciplina = 3

    # Para cada linha, cria um objeto Subject e insere no curso
    for row in rows:
        # procura as colunas da linha
        cells = row.find_all('td')

        if len(cells) >= 8:   # Garante que a linha tenha ao menos 8 colunas
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
    """
    Clica no botão de busca (etapa 1) na interface do JupiterWeb.
    Esta função aguarda o carregamento dos elementos necessários antes de realizar o clique.
    """
    searchButtonTwo = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "step1-tab"))
    )

    time.sleep(1.2)
    searchButtonTwo.click()
    
    # Aguarda o carregamento da lista de unidades após o clique
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "comboUnidade")))


# ---------- Início da execução principal ----------

# Lê a quantidade de unidades que o usuário deseja processar
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
driver.set_page_load_timeout(25) 

url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"

# Tenta abrir a página inicial até 5 vezes em caso de falha
max_tentativas = 5
sucesso = False

for tentativa in range(1, max_tentativas + 1):
    try:
        print(f"Tentativa {tentativa} de {max_tentativas} para abrir a página...")
        driver.get(url)
        time.sleep(3)  # Dá tempo para a página estabilizar

        # Aguarda o carregamento dos menus de unidade e curso
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

# Captura as unidades disponíveis no site
selectUnits = Select(driver.find_element(By.ID, "comboUnidade"))

# Itera sobre TODAS as unidades (exceto a primeira que é vazia)
for units in selectUnits.options[1:]:  # pula primeiro item da lista de options(lista de unidades)
    # Para o loop se a quantidade unidades para serem lidas foram atingidas
    if quantityUnits == 0:
        break

    unitName = units.text
    unitValue = units.get_attribute("value")

    # Cria uma nova instância de Unit e adiciona à lista global
    current_unit = Unit(name=unitName)
    all_units.append(current_unit)

    print(f"\nSelecionando unidade: {unitName} (valor={unitValue})")

    # Seleciona a unidade no site
    selectUnits.select_by_value(unitValue)

    # Aguarda o carregamento da lista de cursos para a unidade escolhida
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "comboCurso")))
    time.sleep(0.4)

    # Atualiza a lista de cursos
    selectCourse = Select(driver.find_element(By.ID, "comboCurso"))

    
    for course in selectCourse.options[1:]:  # pula primeiro item da lista de options(lista de cursos)
        courseName = course.text
        courseValue = course.get_attribute("value")

        print(f"\nSelecionando curso: {courseName} (valor={courseValue})")
        selectCourse.select_by_value(courseValue)


        # Após selecionar o curso, clica no botão "Buscar"
        searchButtonOne = driver.find_element(By.ID, "enviar")
        time.sleep(2)
        searchButtonOne.click()

        # Aguarda o carregamento da aba de detalhes do curso
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "tabs")))

        try:  ## tentar achar o botão de grades
            # Espera o overlay de carregamento sumir antes de continuar
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "blockUI"))
            )

            # Tenta localizar e clicar na aba "Grade Curricular"
            gradesCurriculum = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "step4-tab"))
            )
            time.sleep(2) 
            gradesCurriculum.click()


            time.sleep(3.2) # Aguarda a aba carregar completamente


            # Captura o conteúdo da página
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')

            # Captura os dados de duração do curso
            durationIdeal = soup.find('span', class_="duridlhab").get_text(strip=True)
            durationMin = soup.find('span', class_="durminhab").get_text(strip=True)
            durationMax = soup.find('span', class_="durmaxhab").get_text(strip=True)


            # Cria o objeto Course com os dados de duração
            course_obj = Course(courseName, unitName, int(durationIdeal), int(durationMin), int(durationMax))

            try:
                # Verifica se existem links de disciplinas
                linksDisciplina = soup.find_all("a", class_="disciplina")

                # Captura a div que contém as tabelas de disciplinas
                divGradeCurricular = soup.find('div', id="gradeCurricular")
                
                # Seleciona todas as tabelas presentes na div gradeCurricular, obtenho uma lista de tabelas
                tables = divGradeCurricular.find_all('table')

                # Processa cada tabela encontrada (uma por tipo de disciplina)
                for table in tables:
                    processar_tabela(table,course_obj)
                time.sleep(2)
                
            except:
                raise ValueError("Erro ao tentar processar tabela de disciplinas ")

            finally:
                # Imprime o estado completo do curso com as disciplinas coletadas
                course_obj.status_course()

                # Volta para o menu de busca de cursos
                button_buscar(driver)

        except:
            # Caso a aba de grades curriculares não exista, cria o curso só com nome e unidade
            course_obj = Course(courseName, unitName)

            # Fecha o popup/modal se necessário
            closeButton = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Fechar']"))
            )
            closeButton.click()
            time.sleep(1)

        finally:
            # Adiciona o curso na lista de cursos da unidade
            current_unit.add_courses(course_obj)

    # Decrementa a quantidade de unidades restantes
    quantityUnits-=1

# Finaliza o WebDriver (fecha o navegador após terminar o scraping)
driver.quit()

"""===================== Menu de Funcionalidades =====================

Após a coleta dos dados de todas as unidades e cursos, o programa entra
nesta etapa de interação com o usuário, oferecendo um menu com consultas
e operações sobre os dados armazenados em memória.

"""

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
        # Opção 1 - Listar cursos por unidade
        case "1":
            print("\nExecutando a opção 1....")

            print("\n--- Lista de cursos por unidades ---")
            print()

            functionsUSP.print_all_courses(all_units)

        case "2":
            # Opção 2 - Buscar dados de um curso específico com filtros múltiplos
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

             # Filtros por disciplina
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
            # Opção 3 - Exibir todos os cursos coletados
            print("\nExecutando a opção 3....")
            print("\n--- Dados de todos os cursos ---")
            print()
            functionsUSP.data_all_courses(all_units)

        case "4":
            # Opção 4 - Buscar dados de uma disciplina específica (com vários filtros)
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
            # Opção 5 - Exibir disciplinas compartilhadas entre vários cursos
            print("\nExecutando a opção 5....")
            print("\n--- Disciplinas compartilhadas entre cursos ---")
            print()

            functionsUSP.find_shared_subjects(all_units)

        case "6":
            # Opção 6 - Encerrar o programa
            print("\nExecutando a opção 6....")
            print("Encerrando programa. Até logo!")
            print()

            break

        case _:
            # Caso o usuário digite uma opção inválida
            print("\nOpção inválida! Por favor, tente novamente.\n")







