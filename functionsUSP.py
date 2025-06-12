from collections import defaultdict

#Função que imprime uma lista de cursos por unidade
def print_all_courses(all_units):
    for unit in all_units:
        print(f"\nUnidade: {unit.name}")
        print("Cursos oferecidos: ")
        courses = unit.get_all_courses()

        # Se lista diferente de vazia então imprime
        if courses:
            for course in courses:
                print(f"{course.majorName}")
        print()


# Função que retorna os dados de um determinado curso
def data_course(all_units, **filters):
# arrumar parametros da minha função
    found = False
    for unit in all_units:

        # Forma uma lista de cursos que atende o critério estabelecido
        courses = unit.get_courses(**filters)
        # se lista é diferente de vazia
        if courses:
            # for que itera na lista dos cursos e imprime seus dados
            for course in courses:
                course.status_course()
                found = True
                print()


    if not found:
        # Mostra o nome se estiver no filtro, senão mostra "filtros aplicados"
        nameCourse = filters.get("courseName", "com os filtros aplicados")
        print(f"Curso '{nameCourse}' não encontrado em nenhuma unidade.")


# Função que retorna os dados de todos os cursos armazenados na lista de cursos de cada unidade
def  data_all_courses(all_units):
    for unit in all_units:
        # forma uma lista de cursos da respectiva unidade
        courses = unit.get_all_courses()
        if courses:
            for course in courses:
                course.status_course()



# Função responsável por retornar os dados de uma determina disciplina e seus respectivos cursos
def data_subject (all_units, **filters):
    found = False
    for unit in all_units:
        courses = unit.get_all_courses()

        if courses:
            for course in courses:
                subj = course.get_subjects(**filters)
                if subj:
                    print(f"\nCurso: {course.majorName}")
                    subj.status_subject()
                    found = True

    if not found:
        # Mostra o nome se estiver no filtro, senão mostra "filtros aplicados"
        subjectName = filters.get("nameSubject", "com os filtros aplicados")
        print(f"Disciplina '{subjectName}' não encontrada em nenhum curso.")


# Função responsável por coletar disciplinas a qual são compartilhadas em mais de um curso
def find_shared_subjects(all_units):

    mapa = defaultdict(set)

    for unit in all_units:
        courses = unit.get_all_courses()
        for course in courses:
            subjects = course.get_all_subjects()
            for subj in subjects:
                cod = subj.code
                nameSubj = subj.nameSubject
                key = (cod, nameSubj)
                mapa[key].add(course.majorName)


    shared = {  key: courses for key, courses in mapa.items() if len(courses) > 1}

    for (cod, nameSubj), cursos in shared.items():
        cursos_str = ", ".join(cursos)
        print(f"Disciplina: [ {cod} | {nameSubj} ] está presente nos cursos: ( | {cursos_str} )\n")



def menu_interative(all_units):
    while True:
        print("\n" + "=" * 50)
        print("Menu de Seleção:")
        print("1. Listar cursos por unidade")
        print("2. Dados de um determinado curso (com filtros um ou um conjunto deles: Nome do curso, Nome da unidade, Duração ideal, Duração mínima, Duração máxima, Código de disciplina, Nome de disciplina )")
        print("3. Dados de todos os cursos")
        print("4. Dados de uma determinada disciplina por filtro: (Código da disciplina, nome da disciplina, Crédito aulas, Carga horário, Carga de Estágio, CP, ATPA) , inclusive quais cursos ela faz parte")
        print("5. Ver disciplinas compartilhadas por mais de um curso")
        print("6. Encerrar programa")
        print("=" * 50)


        opcao = input("Escolha uma opção: ")


        match opcao:


            case "1":
                print("\n--- Lista de cursos por unidades ---")
                print_all_courses(all_units)

            case "2":
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

                data_course(
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
                print("\n--- Dados de todos os cursos ---")
                data_all_courses(all_units)

            case "4":
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

                data_subject(
                    all_units,
                    code=code,
                    nameSubject=name,
                    ch=ch,
                    ce=ce,
                    cp=cp,
                    atpa=atpa
                )

            case "5":
                print("\n--- Disciplinas compartilhadas entre cursos ---")
                find_shared_subjects(all_units)

            case "6":
                print("Encerrando programa. Até logo!")
                break

            case _:
                print("Opção inválida! Por favor, tente novamente.")
