from dataclasses import dataclass, field
from typing import List, Optional
from subject import Subject

@dataclass
class Course:
    majorName: str # nome do curso
    unitCampus: str # Unidade
    idealDuration: int =  field(default=0)# duração ideal
    minDuration: int =  field(default=0)# duração mínima
    maxDuration: int = field(default=0) # duração máxima
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

    #def get_subjects(self, **filters) -> List[Subject]:
       # Retorna disciplinas a depender do filtro encaminhado pelo usuário



    #Função auxiliar que imprime os dados das disciplinas
    def print_data_subjects(self, listSubjects):
        # se a lista não estive vazia
        if listSubjects:
            for subj in listSubjects:
                print(f"{subj.code} | {subj.nameSubject} | {subj.creditsClass} | {subj.creditsWorkClass} | {subj.workload} | {subj.internshipWorkload} | {subj.workloadOfPracticalComponentsCurriculares} | {subj.atpa}")
            return
        print("Nenhuma disciplina encontrada")


    def status(self) -> None:
        """Imprime informações do curso"""

        print(
            f"Curso: {self.majorName}\n"
            f"Unidade: {self.unitCampus}\n"
            f"Duração ideal: {self.idealDuration}, "
            f"Duração mínima: {self.minDuration}, "
            f"Duração máxima: {self.maxDuration}\n"
        )

        print(f"Disciplinas Obrigatórias ({len(self.listOfMandatorySubjects)}):")
        self.print_data_subjects(self.listOfMandatorySubjects)

        print(f"\nDisciplinas Optativas Livres ({len(self.listOfOptionalFreeSubjects)}):")
        self.print_data_subjects(self.listOfOptionalFreeSubjects)

        print(f"\nDisciplinas Optativas Eletivas ({len(self.listOfOptionalElectiveSubjects)}):")
        self.print_data_subjects(self.listOfOptionalElectiveSubjects)