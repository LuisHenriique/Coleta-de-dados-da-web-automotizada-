from dataclasses import dataclass, field
from typing import List

@dataclass
class Subject:
    """
    Classe que representa uma disciplina (matéria) de um curso.

    Atributos:
        code (str): Código da disciplina (exemplo: "MAC0323").
        nameSubject (str): Nome da disciplina (exemplo: "Estruturas de Dados").
        creditsClass (str): Quantidade de créditos aula.
        creditsWorkClass (str): Créditos de trabalho (atividades práticas).
        ch (str): Carga horária total da disciplina.
        ce (str): Carga horária de estágio.
        cp (str): Carga horária de práticas como componentes curriculares.
        atpa (str): Horas de Atividades Teórico-Práticas de Aprofundamento (ATPA).
    """
    
    code: str  # Código da disciplina
    nameSubject: str  # Nome da disciplina
    creditsClass: str  # Créditos aula
    creditsWorkClass: str  # Créditos trabalho
    ch: str  # Carga horária total (CH)
    ce: str  # Carga horária de estágio (CE)
    cp: str  # Carga horária de práticas (CP)
    atpa: str  # Atividades Teórico-Práticas de Aprofundamento (ATPA)


    def status_subject(self):
        """
        Exibe de forma formatada todos os atributos da disciplina.

        Essa função imprime os detalhes da disciplina no console,
        seguindo o padrão usado nas listagens de disciplinas dos cursos.
        """
        print(
            f"  Código disciplina: {self.code} | "
            f"Nome disciplina: {self.nameSubject} | "
            f"Créditos Aulas: {self.creditsClass} | "
            f"Crédito Trabalho: {self.creditsWorkClass} | "
            f"Carga horária: {self.ch} | "
            f"Carga horária de Estágio: {self.ce} | "
            f"Carga horária de Práticas como Componentes Curriculares: {self.cp} | "
            f"Atividades Teórico-Práticas de Aprofundamento: {self.atpa}"
        )
