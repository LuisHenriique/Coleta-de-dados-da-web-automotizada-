from collections import defaultdict

#Função que imprime uma lista de cursos por unidade
def print_all_courses(all_units):
    for unit in all_units:
        print(f"\nUnidade: {unit.name}")
        courses = unit.get_all_courses()
        print(f"Cursos oferecidos - quantidade de cursos [{len(courses)}] :\n")

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
        # se lista é de vazia
        if not courses:
            continue
        # for que itera na lista dos cursos e imprime seus dados
        for course in courses:
            course.status_course()
            found = True
            print()


    if not found:
        # Mostra o nome se estiver no filtro, senão mostra "filtros aplicados"

        print(f"Os dados deste curso não foi encontrado em nenhuma unidade.")


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
                    print("-"*110)
                    print(f"Curso: {course.majorName}\n")
                    subj.status_subject()
                    print("-"*110 + "\n")

                    found = True

    if not found:
        # Mostra o nome se estiver no filtro, senão mostra "filtros aplicados"
        print(f"Disciplina  não encontrada em nenhum curso.")


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
    strPrint = "-" * 110
    for (cod, nameSubj), cursos in shared.items():
        cursos_str = "\n - ".join(cursos)

        print(f"\n{strPrint}\n"
              f"Disciplina: [ {cod} | {nameSubj} ] está presente nos cursos: \n{strPrint}\n - {cursos_str}\n")










