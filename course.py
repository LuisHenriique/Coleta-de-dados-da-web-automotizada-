from dataclasses import dataclass, field
from typing import List, Optional
from subject import Subject

@dataclass
class Course:
    majorName: str # nome do curso
    unitCampus: str # Unidade
    idealDuration: str =  field(default="0")# duração ideal
    minDuration: str =  field(default="0")# duração mínima
    maxDuration: str = field(default="0") # duração máxima
    listOfMandatorySubjects: List[Subject] = field(default_factory=list) # lista de disciplinas obrigatórias (inicializadas vazia)
    listOfOptionalFreeSubjects: List[Subject] = field(default_factory=list) # lista de disciplinas Optativas livres (inicializadas vazia)
    listOfOptionalElectiveSubjects: List[Subject] = field(default_factory=list) # lista de disciplinas optativas eletivas (inicializadas vazia)

    def insert_subject(self, subject: Subject, subjectType: int) -> None:
        """Adiciona uma disciplina na lista apropriada de disciplinas """



        if(subjectType == 1):
            #Add uma Disciplina Obrigatória
            self.listOfMandatorySubjects.append(subject)

        elif(subjectType == 2):
            #Add uma Disciplina Optativa Livre
            self.listOfOptionalFreeSubjects.append(subject)

        elif(subjectType== 3):
            #Add uma Disciplina Optativa Eletiva
            self.listOfOptionalElectiveSubjects.append(subject)
        else:
            raise ValueError(f"Tipo de disciplina inválido: {subjectType}")


    def get_all_subjects(self) -> List[Subject]:
        """Retorna todas as disciplinas do curso"""
        return (self.listOfMandatorySubjects + self.listOfOptionalElectiveSubjects + self.listOfOptionalFreeSubjects)

    def get_subjects(self) -> Optional[Subject]:
        """Retorna """
    def status(self) -> None:
        """Imprime informações do curso"""
        print(
            f"Course: {self.majorName}\n"
            f"Unit: {self.unitCampus}\n"
            f"Duration - Ideal: {self.idealDuration}, Min: {self.minDuration}, Max: {self.maxDuration}\n"
            f"Subjects - Mandatory: {len(self.listOfMandatorySubjects)}, "
            f"Optional Free: {len(self.listOfOptionalFreeSubjects)}, "
            f"Optional Elective: {len(self.listOfOptionalElectiveSubjects)}"
        )