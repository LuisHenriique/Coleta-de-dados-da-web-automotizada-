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
        print(f"  Código disciplina: {self.code} | Nome disciplina: {self.nameSubject} | Créditos Aulas: {self.creditsClass} | Crédito Trabalho: {self.creditsWorkClass} | Carga horária: {self.ch} |  Carga horária de Estágio: {self.ce} | Carga horária de Práticas como Componentes Curriculares: {self.cp} | Atividades Teórico-Práticas de Aprofundamento: {self.atpa}")
