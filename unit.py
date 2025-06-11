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

    def get_course(self, courseName: str) -> Optional[Course]:
        """Encontra um curso atráves do nome na unidade respectiva"""
        for course in self.courses:
            if course.majorName == courseName:
                return  course

        return  None

    def get_all_courses(self) -> List[Course]:
        """Retorna lista de todos os cursos da respectiva unidade """
        return self.courses

