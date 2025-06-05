from dataclasses import dataclass

class Subject:
    code: int # código
    nameSubject: str # nome da disciplina
    creditsClass: int # créditos aulas
    creditsWorkClass: int # crédito trabalho
    workload: int # carga horária
    internshipWorkload: int # carga horária de estágio
    workloadOfPraticalComponentsCurriculares: float # carga horária de Práticas como Componentes Curriculares
    activitiesTheory_PraticalsAprofundamento: int # atividades Teórico-Práticas de Aprofundamento
