from dataclasses import dataclass
from typing import List

@dataclass
class Subject:
    code: str # código
    nameSubject: str # nome da disciplina
    creditsClass: str # créditos aulas
    creditsWorkClass: str # crédito trabalho
    workload: str  # carga horária
    internshipWorkload: str # carga horária de estágio
    workloadOfPraticalComponentsCurriculares: str # carga horária de Práticas como Componentes Curriculares
    activitiesTheoryPraticalsAprofundamento: str # atividades Teórico-Práticas de Aprofundamento

