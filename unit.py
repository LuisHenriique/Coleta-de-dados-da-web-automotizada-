from dataclasses import dataclass, field
from typing import List, Optional
from course import Course

@dataclass
class Unit:
    name: str # Nome da unidade
    courses: List[Course] = field(default_factory=list) # lista de cursos da respectiva unidade


    def add_courses(self, course: Course) -> None  :
        """Adiciona um curso para esta unidade se ele não existe já na lista de cursos"""
        if not any(c.majorName == course.majorName for c in self.courses):
            self.courses.append(course)
        else:
            print(f"Este curso: {course.majorName} já existe nesta unidade {self.name}")

    def get_courses(self, **filters) -> List[Course]:
        """Função que retorna um curso que atendeu os  critérios do filtro encaminhado pelo usuário"""
        """
            
            - filters será um dicionário com todos os argumentos nomeados, ou seja um exemplo:
                # Chamada da função
                unit.get_courses(unitName="IME", minDuration=4)
                
                # Dentro desta função, filters será:
                # {'unitName': 'IME', 'minDuration': 4}
add_courses

            Busca curso com filtros flexíveis.

            Filtros disponíveis:
                unitName: str
                courseName: str
                minDuration: str
                maxDuration: str
                idealDuration: str
                subjectCode: str
                subjectName: str
                
            """

        # Verifica se TODOS os filtros são None
        if all(value is None for value in filters.values()):
            return []  # Nenhum critério fornecido, retorna lista vazia

        matchingCourses = []

        for course in self.courses:
            matches = True

            """
            Todos os filtros a qual contém strings tals como:  (unitName, courseName, subjectCode, subjectName)
            usam .strip().lower() para normalizar as comparações ou seja retirando espaços e deixando tudo minúsculo
            e realizamos a comparação usando o in ou seja permitindo que apenas um trecho do texto já seja suficiente para considerar como correspondência.
            exemplo: busco "marketing"
            porém o nome do curso é Marketing - Integral 
            irar dar match normalmente, bastando que apenas que o será buscado esteja contido no cursoName
            """



            # Filtro por nome da unidade (unitName)
            if 'unitName' in filters  and filters['unitName'] is not None:
                filter_unit = filters['unitName'].strip().lower()
                course_unit = course.unitCampus.strip().lower()
                if filter_unit not in course_unit:
                    matches = False

            # Filtro por nome do curso (courseName)
            if 'courseName' in filters  and filters['courseName'] is not None:
                filter_name = filters['courseName'].strip().lower()
                course_name = course.majorName.strip().lower()
                if filter_name not in course_name:
                    matches = False

            # Filtro por duração mínima
            if 'minDuration' in filters and filters['minDuration']  is not None:
                if course.minDuration < filters['minDuration']:
                    matches = False

            # Filtro por duração máxima
            if 'maxDuration' in filters  and filters['maxDuration'] is not None:
                if course.maxDuration > filters['maxDuration']:
                    matches = False

            # Filtro por duração ideal
            if 'idealDuration' in filters and filters['idealDuration'] is not None:
                if course.idealDuration > filters['idealDuration']:
                    matches = False

            # Filtro por código da disciplina (subjectCode)
            if 'subjectCode' in filters and filters['subjectCode']  is not None:
                filter_code = filters['subjectCode'].strip().lower()
                subject_codes = [subj.code.strip().lower() for subj in course.get_all_subjects()]
                if not any(filter_code in code for code in subject_codes):
                    matches = False

            # Filtro por nome da disciplina (subjectName)
            if 'subjectName' in filters and filters['subjectName']   is not None:
                filter_subject = filters['subjectName'].strip().lower()
                subject_names = [subj.nameSubject.strip().lower() for subj in course.get_all_subjects()]
                if not any(filter_subject in name for name in subject_names):
                    matches = False

            if matches:
                matchingCourses.append(course)

        #Retorna a lista de cursos que atenderam os critérios do filtro
        return matchingCourses

    def get_all_courses(self) -> List[Course]:
        """Retorna lista de todos os cursos da respectiva unidade """
        return self.courses

