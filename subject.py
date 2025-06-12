from dataclasses import dataclass, field
from typing import List

@dataclass
class Subject:
    code: str # código
    nameSubject: str # nome da disciplina
    creditsClass: str  # créditos aulas
    creditsWorkClass: str # crédito trabalho
    ch: str   # carga horária
    ce: str # carga horária de estágio
    cp: str # carga horária de Práticas como Componentes Curriculares
    atpa: str # atividades Teórico-Práticas de Aprofundamento


    def status_subject(self):
        print(f"{self.code} | {self.nameSubject} | {self.creditsClass} | {self.creditsWorkClass} | {self.ch} | {self.ce} | {self.cp} | {self.atpa}")