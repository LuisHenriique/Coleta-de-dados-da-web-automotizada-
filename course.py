from dataclasses import dataclass
from subject import Subject

class Course:
    majorName: str # nome do curso
    unitCampus: str # Unidade
    idealDuration: int # duração ideal
    minDuration: int # duração mínima
    maxDuration: int # duração máxima
    listOfMandatorySubjects:list[Subject] # lista de disciplinas obrigatórias
    listOfOptionalFreeSubjects:list[Subject] # lista de disciplinas Optativas livres
    listOfOptinalEletivasSubjects : list [Subject] # lista de disciplinas optativas eletivas
