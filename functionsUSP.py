#Função que imprime uma lista de cursos por unidade
def print_all_course(all_units):
    for unit in all_units:
        print(f"\n{unit}")
        print("Cursos oferecidos: ")
        courses = unit.get_all_courses()

        # Se lista diferente de vazia então imprime
        if courses:
            for course in courses:
                print(f"{course.name}")

# Função que encontra um unidade pelo nome
def find_unit_by_name(unit_name, all_units):
    for unit in all_units:
        if unit.name == unit_name:
            return unit
    return None

# Função que retorna os dados de um determinado curso
def data_course(all_units, nameCourse):

    found = False
    for unit in all_units:

        # Forma uma lista de cursos que atende o critério estabelecido
        courses = unit.get_courses(courseName= nameCourse)
        # se lista é diferente de vazia
        if courses:
            # for que itera na lista dos cursos e imprime seus dados
            for course in courses:
                course.status()
                found = True


    if not found:
        print(f"Curso '{nameCourse}' não encontrado em nenhuma unidade.")


# Função que retorna os dados de todos os cursos armazenados na lista de cursos de cada unidade
def  data_all_courses(all_units):
    for unit in all_units:
        # forma uma lista de cursos da respectiva unidade
        courses = unit.get_all_courses()
        if courses:
            for course in courses:
                course.status()