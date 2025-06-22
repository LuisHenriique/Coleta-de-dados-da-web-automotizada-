from dataclasses import dataclass, field
from typing import List, Optional
from subject import Subject



@dataclass
class Course:
    majorName: str # Nome do curso
    unitCampus: str # Nome da unidade (campus onde o curso é oferecido)
    idealDuration: int =  field(default=0) # Duração ideal do curso (em semestres)
    minDuration: int =  field(default=0) # Duração mínima do curso (em semestres)
    maxDuration: int = field(default=0) # Duração máxima do curso (em semestres)
    
	# Listas para armazenar as disciplinas classificadas por tipo
    listOfMandatorySubjects: List[Subject] = field(default_factory=list) # Disciplinas obrigatórias (inicializadas vazia)
    listOfOptionalFreeSubjects: List[Subject] = field(default_factory=list) # Disciplinas optativas livres (inicializadas vazia)
    listOfOptionalElectiveSubjects: List[Subject] = field(default_factory=list) # Disciplinas optativas eletivas (inicializadas vazia)

    def insert_subject(self, subject: Subject, subjectType: int) -> None:
        """Adiciona uma disciplina na lista apropriada de disciplinas """

        if(subjectType == 1):
            # Adiciona uma Disciplina Obrigatória
            self.listOfMandatorySubjects.append(subject)

        elif(subjectType == 2):
            # Adiciona uma Disciplina Optativa Livre
            self.listOfOptionalFreeSubjects.append(subject)

        elif(subjectType== 3):
            # Adiciona uma Disciplina Optativa Eletiva
            self.listOfOptionalElectiveSubjects.append(subject)
        else:
            raise ValueError(f"Tipo de disciplina inválido: {subjectType}")


    def get_all_subjects(self) -> List[Subject]:
        """Retorna todas as disciplinas do curso"""
        return (self.listOfMandatorySubjects + self.listOfOptionalElectiveSubjects + self.listOfOptionalFreeSubjects)


    def get_subject_of_list(self, listOfSubjects, **filters) -> Optional[Subject]:
        """ Busca uma disciplina em uma lista, aplicando múltiplos filtros opcionais."""
        """
                   Todos os filtros a qual contém strings 
        """


        if listOfSubjects:
            for subject in listOfSubjects:
                matches = True # Flag para verificar se todos os filtros foram atendidos


                # Filtro por código da disciplina
                if 'code' in filters  and filters['code'] is not None:
                    filterCode = filters['code'].strip().lower()
                    subjectTest  = subject.code.strip().lower()
                    if filterCode not in subjectTest:
                        matches = False

				# Filtro por nome da disciplina
                if 'nameSubject' in filters  and filters['nameSubject'] is not None:
                    filterNameSubject = filters['nameSubject'].strip().lower()
                    subjectName = subject.nameSubject.strip().lower()
                    if filterNameSubject not in subjectName:
                        matches = False

				# Filtro por créditos de aula
                if 'creditsClass' in filters  and filters['creditsClass']  is not None:
                    if int(subject.creditsClass) < filters['creditsClass']:
                        matches = False
                        
				# Filtro por carga horária total (CH)
                if 'ch' in filters   and filters['ch'] is not None:
                    if int(subject.ch) < filters['ch']:
                        matches = False
                        
				# Filtro por carga horária de estágio (CE)
                if 'ce' in filters  and filters['ce'] is not None:
                    if int(subject.ce) < filters['ce']:
                        matches = False
                
				# Filtro por carga horária de práticas (CP)
                if 'cp' in filters  and filters['cp'] is not None:
                    if int(subject.cp) < filters['cp']:
                        matches = False
                
				# Filtro por carga de atividades teórico-práticas de aprofundamento (ATPA)
                if 'atpa' in filters  and filters['atpa']  is not None:
                    if int(subject.atpa) < filters['atpa']:
                        matches = False
				
				# Retorna a disciplina que atendeu todos os filtros
                if matches:
                    # Retorna a disciplina que atendeu todos os filtros
                    return  subject

		# Nenhuma disciplina encontrada
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

        # Verifica em cada lista. Uma disciplina não pode estar simultaneamente em mais de uma categoria.
        matchingSubject = (
                self.get_subject_of_list(self.listOfMandatorySubjects, **filters)
                or self.get_subject_of_list(self.listOfOptionalElectiveSubjects, **filters)
                or self.get_subject_of_list(self.listOfOptionalFreeSubjects, **filters)
        )

        return matchingSubject


    def print_data_subjects(self, listSubjects):
        """
        Função auxiliar que imprime os dados de uma lista de disciplinas.
        """
        if listSubjects:
            for subj in listSubjects:
                subj.status_subject()
                print()
            return
        print("  Nenhuma disciplina encontrada\n")


    def status_course(self) -> None:
        """
        Exibe no console as informações gerais do curso,
        incluindo a duração e todas as disciplinas separadas por categoria.
        """
        print("-" *100)
        print(
            f"Curso: {self.majorName}\n"
            f"Unidade: {self.unitCampus}\n"
            f"Duração ideal: {self.idealDuration}, "
            f"Duração mínima: {self.minDuration}, "
            f"Duração máxima: {self.maxDuration}"
        )
        print("-" *100 + "\n")

		# Imprime as disciplinas obrigatórias
        print(f"- Disciplinas Obrigatórias ({len(self.listOfMandatorySubjects)}):\n")
        self.print_data_subjects(self.listOfMandatorySubjects)

		# Imprime as disciplinas optativas livres
        print(f"\n- Disciplinas Optativas Livres ({len(self.listOfOptionalFreeSubjects)}):\n")
        self.print_data_subjects(self.listOfOptionalFreeSubjects)

		# Imprime as disciplinas optativas eletivas
        print(f"\n- Disciplinas Optativas Eletivas ({len(self.listOfOptionalElectiveSubjects)}):\n")
        self.print_data_subjects(self.listOfOptionalElectiveSubjects)
