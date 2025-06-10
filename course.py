from dataclasses import dataclass, field
from typing import List
from subject import Subject

@dataclass
class Course:
    majorName: str # nome do curso
    unitCampus: str # Unidade
    idealDuration: str # duração ideal
    minDuration: str # duração mínima
    maxDuration: str # duração máxima
    listOfMandatorySubjects: List[Subject] = field(default_factory=list) # lista de disciplinas obrigatórias (inicializadas vazia)
    listOfOptionalFreeSubjects: List[Subject] = field(default_factory=list) # lista de disciplinas Optativas livres (inicializadas vazia)
    listOfOptinalEletivasSubjects: List[Subject] = field(default_factory=list) # lista de disciplinas optativas eletivas (inicializadas vazia)


    def insert_subject(self, subject: Subject , type):
        """Add uma disciplina obrigatori"""
        if(type == "Disciplinas Obrigatórias"):
            self.listOfMandatorySubjects.append(subject)
        elif(type == "Disciplinas Optativas Eletivas"):
            self.listOfOptinalEletivasSubjects.append(subject)
        else:
            self.listOfOptionalFreeSubjects.append(subject)

    def status(self):
        print(f"Nome do curso: {self.majorName} -- Unidade: {self.unitCampus} --  Duração ideal: {self.idealDuration} -- Duração mínima: {self.minDuration} -- Duração máxima:{self.maxDuration}\n")