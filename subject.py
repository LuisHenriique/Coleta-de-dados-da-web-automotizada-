from dataclasses import dataclass, field
from typing import List

@dataclass
class Subject:
    code: str # código
    nameSubject: str # nome da disciplina
    creditsClass: str  # créditos aulas
    creditsWorkClass: str # crédito trabalho
    workload: str   # carga horária
    internshipWorkload: str # carga horária de estágio
    workloadOfPracticalComponentsCurriculares: str # carga horária de Práticas como Componentes Curriculares
    atpa: str # atividades Teórico-Práticas de Aprofundamento


    def status(self):
        print(f"Código: {self.code} -- Disciplina: {self.nameSubject} -- Créditos: {self.creditsClass} -- Créditos Trabalho: {self.creditsWorkClass} -- Carga Horária: {self.workload} -- CE: {self.internshipWorkload} -- CP: {self.workloadOfPracticalComponentsCurriculares} --     ATPA: {self.atpa}")