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


    def get_subject_of_list(self, listOfSubjects, **filters) -> Optional[Subject]:
        """Função que dado uma lista de disciplinas retorna uma disciplina que bateu com os critérios do filtro"""
        """
                   Todos os filtros a qual contém strings 
        """


        if listOfSubjects:
            for subject in listOfSubjects:
                matches = True


                # Filtro por código das disciplinas
                if 'code' in filters  is not None:
                    filterCode = filters['code'].strip().lower()
                    subjectTest  = subject.code.strip().lower()
                    if filterCode not in subjectTest:
                        matches = False



                if 'nameSubject' in filters  and filters['nameSubject'] is not None:
                    filterNameSubject = filters['nameSubject'].strip().lower()
                    subjectName = subject.nameSubject.strip().lower()
                    if filterNameSubject not in subjectName:
                        matches = False

                if 'creditsClass' in filters  and filters['creditsClass']  is not None:
                    if int(subject.creditsClass) < filters['creditsClass']:
                        matches = False
                if 'ch' in filters   and filters['ch'] is not None:
                    if int(subject.ch) < filters['ch']:
                        matches = False
                if 'ce' in filters  and filters['ce'] is not None:
                    if int(subject.ce) < filters['ce']:
                        matches = False
                if 'cp' in filters  and filters['cp'] is not None:
                    if int(subject.cp) < filters['cp']:
                        matches = False
                if 'atpa' in filters  and filters['atpa']  is not None:
                    if int(subject.atpa) < filters['atpa']:
                        matches = False

                if matches:
                    return  subject

            #retorna a disciplina que atendeu os critérios do filtro

        return None


    def get_subjects(self, **filters) -> Optional[Subject]:
        """Retorna disciplinas a depender do filtro encaminhado pelo usuário"""
        """   - filters será um dicionário com todos os argumentos nomeados
             
            Busca disciplinas com filtros flexíveis.
            
            Filtros disponíveis:
            code: str
            nameSubject: str
            creditClass: str 
            ch: str 
            ce: str
            cp: str
            atpa: str
        """

        matchingSubject = None

        # armazeno em matchingSubject o valor retornado de uma das chamadas, pois uma disciplina não tem como ser
        # obrigatório e eletiva ao mesmo tempo
        matchingSubject = (
                self.get_subject_of_list(self.listOfMandatorySubjects, **filters)
                or self.get_subject_of_list(self.listOfOptionalElectiveSubjects, **filters)
                or self.get_subject_of_list(self.listOfOptionalFreeSubjects, **filters)
        )

        return matchingSubject




    #Função auxiliar que imprime os dados das disciplinas
    def print_data_subjects(self, listSubjects):
        # se a lista não estive vazia
        if listSubjects:
            for subj in listSubjects:
                subj.status_subject()
            return
        print("Nenhuma disciplina encontrada")


    def status_course(self) -> None:
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