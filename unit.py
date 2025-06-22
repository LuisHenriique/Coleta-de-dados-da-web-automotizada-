from dataclasses import dataclass, field
from typing import List, Optional
from course import Course

@dataclass
class Unit:
    # Nome da unidade (exemplo: "IME", "EACH", etc.)
    name: str 
    
    # Lista de cursos oferecidos por essa unidade
    courses: List[Course] = field(default_factory=list) # lista de cursos da respectiva unidade


    def add_courses(self, course: Course) -> None  :
        """Adiciona um curso para esta unidade se ele não existe já na lista de cursos"""
        
        # Verifica se o curso já existe na unidade, comparando pelo nome do curso
        if not any(c.majorName == course.majorName for c in self.courses):
            self.courses.append(course)
        else:
            print(f"Este curso: {course.majorName} já existe nesta unidade {self.name}")

    def get_courses(self, **filters) -> List[Course]:
        """
        Retorna uma lista de cursos desta unidade que atendem aos critérios de filtro.

        Filtros aceitos:
            - unitName (str): Nome (ou parte do nome) da unidade.
            - courseName (str): Nome (ou parte do nome) do curso.
            - minDuration (int): Duração mínima do curso.
            - maxDuration (int): Duração máxima do curso.
            - idealDuration (int): Duração ideal máxima permitida.
            - subjectCode (str): Código (ou parte) de uma disciplina que o curso possui.
            - subjectName (str): Nome (ou parte) de uma disciplina que o curso possui.
        """

        # Se nenhum filtro for informado, retorna lista vazia
        if all(value is None for value in filters.values()):
            return [] 

        matchingCourses = []

        for course in self.courses:
            matches = True

            """
            Observação geral sobre os filtros de texto:
            - Campos como unitName, courseName, subjectCode e subjectName são tratados de forma case-insensitive
            - Também são tolerantes a espaços extras.
            - A correspondência é parcial: exemplo, buscar por "marketing" vai localizar "Marketing - Integral"
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

        # Retorna a lista de cursos que passaram por todos os filtros
        return matchingCourses

    def get_all_courses(self) -> List[Course]:
        """Retorna lista de todos os cursos da respectiva unidade """
        return self.courses

