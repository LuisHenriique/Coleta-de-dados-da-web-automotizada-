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


            Busca curso com filtros flexíveis.

            Filtros disponíveis:
                unitName: str
                courseName: str
                minDuration: str
                maxDuration: str
                subjectCode: str
                subjectName: str
                
            """

        matchingCourses = []

        for course in self.courses:
            matches = True

            if 'unitName' in filters and course.unitCampus != filters['unitName']:
                matches = False

            if 'courseName' in filters and course.majorName != filters['courseName']:
                matches = False

            if 'minDuration' in filters and int(course.minDuration) < filters['minDuration']:
                matches = False

            if 'maxDuration' in filters and int(course.maxDuration) > filters['maxDuration']:
                matches = False

            if 'subjectCode' in filters:
                if not any(subj.code == filters['subjectCode'] for subj in course.get_all_subjects()):
                    matches = False


            if 'subjectName' in filters:
                if not any(subj.nameSubject == filters['subjectName'] for subj in course.get_all_subjects()):
                    matches = False

            if matches:
                matchingCourses.append(course)

        #Retorna a lista de cursos que atenderam os critérios do filtro
        return matchingCourses

    def get_all_courses(self) -> List[Course]:
        """Retorna lista de todos os cursos da respectiva unidade """
        return self.courses

