from dataclasses import dataclass
from typing import List

@dataclass
class Subject:
    code: int # código
    nameSubject: str # nome da disciplina
    creditsClass: int # créditos aulas
    creditsWorkClass: int = 0 # crédito trabalho
    workload: int  = 0 # carga horária
    internshipWorkload: int =  0 # carga horária de estágio
    workloadOfPraticalComponentsCurriculares: int =  0# carga horária de Práticas como Componentes Curriculares
    activitiesTheoryPraticalsAprofundamento: int = 0# atividades Teórico-Práticas de Aprofundamento

