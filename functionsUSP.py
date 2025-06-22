from collections import defaultdict

# Função que imprime a lista de cursos agrupados por unidade
def print_all_courses(all_units):
    """
    Exibe a lista de cursos organizados por unidade.
    """
    for unit in all_units:
        print(f"\nUnidade: {unit.name}")
        courses = unit.get_all_courses()
        print(f"Cursos oferecidos - quantidade de cursos [{len(courses)}] :\n")

        # Se houver cursos, imprime o nome de cada um
        if courses:
            for course in courses:
                print(f"{course.majorName}")
        print()


# Função que exibe os dados de cursos específicos, de acordo com filtros informados
def data_course(all_units, **filters):
    """
    Exibe os dados detalhados de cursos que atendam aos filtros especificados.
    """
    found = False
    for unit in all_units:
        # Obtém os cursos da unidade que satisfazem os filtros
        courses = unit.get_courses(**filters)
        # Se a unidade não tiver cursos que atendem ao filtro, passa para a próxima
        if not courses:
            continue

        # Exibe os dados de cada curso encontrado
        for course in courses:
            course.status_course()
            found = True
            print()

    if not found:
        # Caso nenhum curso atenda os filtros
        print(f"Os dados deste curso não foi encontrado em nenhuma unidade.")


# Função que exibe os dados de todos os cursos cadastrados
def  data_all_courses(all_units):
    """
    Exibe os dados detalhados de todos os cursos, de todas as unidades.
    """
    for unit in all_units:
        # forma uma lista de cursos da respectiva unidade
        courses = unit.get_all_courses()
        if courses:
            for course in courses:
                course.status_course()

# Função que exibe os dados de uma disciplina específica, além de indicar em quais cursos ela aparece
def data_subject (all_units, **filters):
    """
    Exibe os detalhes de uma disciplina específica, de acordo com os filtros fornecidos,
    incluindo os cursos aos quais ela pertence.
    """
    found = False
    for unit in all_units:
        courses = unit.get_all_courses()

        if courses:
            for course in courses:
                subj = course.get_subjects(**filters)
                if subj:
                    print("-"*110)
                    print(f"Curso: {course.majorName}\n")
                    subj.status_subject()
                    print("-"*110 + "\n")

                    found = True

    if not found:
        # Mostra o nome se estiver no filtro, senão mostra "filtros aplicados"
        print(f"Disciplina  não encontrada em nenhum curso.")


# Função que localiza disciplinas que são compartilhadas entre mais de um curso
def find_shared_subjects(all_units):
    """
    Localiza e exibe disciplinas que aparecem em mais de um curso.

    Para cada disciplina compartilhada, exibe o código, o nome e a lista de cursos onde ela aparece.
    """
    mapa = defaultdict(set) # Dicionário onde chave é (codigo, nome) da disciplina e valor é o conjunto de cursos

    # Mapeia todas as disciplinas de todos os cursos
    for unit in all_units:
        courses = unit.get_all_courses()
        for course in courses:
            subjects = course.get_all_subjects()
            for subj in subjects:
                cod = subj.code
                nameSubj = subj.nameSubject
                key = (cod, nameSubj)
                mapa[key].add(course.majorName)

    # Filtra apenas as disciplinas presentes em mais de um curso
    shared = {  key: courses for key, courses in mapa.items() if len(courses) > 1}
    strPrint = "-" * 110
    for (cod, nameSubj), cursos in shared.items():
        cursos_str = "\n - ".join(cursos)

        print(f"\n{strPrint}\n"
              f"Disciplina: [ {cod} | {nameSubj} ] está presente nos cursos: \n{strPrint}\n - {cursos_str}\n")










