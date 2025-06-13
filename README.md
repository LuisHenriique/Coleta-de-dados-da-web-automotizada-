# Manual de Utilização do Programa

Integrantes do grupo:
- Aluno: Luis Henrique Ponciano dos Santos      NUSP: 15577760
- Aluno: Wiltord    NUSP:
- Aluno:            NUSP:

Este manual fornece instruções passo a passo para configurar o ambiente, instalar as dependências e executar o programa WebScrapping.

## Pré-Requisitos

- Python 3.7+
- Google Chrome instalado
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatível com a versão do seu Chrome

## 1. Criando um Ambiente Virtual

### Linux ou macOS

Abra o terminal e digite:

```bash
python3 -m venv venv
source venv/bin/activate
```

---


## 2. Instale as dependências 

Com o ambiente virtual ativado para o linux (Windows não precisa criar ambiente virtual pode executar direto o comando abaixo), instale as bibliotecas necessárias no terminal:
```bash
pip install beautifulsoup4 selenium
```

---

## 3. Executar programa

Certifique-se de estar no diretório onde estão os arquivos do projeto, utilizando o comando cd (Linux) para encontrar a pasta fonte do projeto

Para rodar o programa:
```bash
make
make run
```
Após rodar o programa forneça a quantidades de unidades que serão lidas, após o processo de raspagem de dados da web que será exiba via terminal para ciência do usuário 
quais dados estão sendo coletados, você verá algo como:
 <br>
Selecione uma opção:
 <br>
1 - Listar cursos por unidade
 <br>
2 - Obter dados de um curso específico
 <br>
3 - Obter dados de todos os cursos
 <br>
4 - Obter dados de uma disciplina
 <br>
5 - Ver disciplinas comuns a vários cursos
 <br>
0 - Sair




## 4. Como funciona o programa:

Este é um projeto Python que utiliza **Web Scraping** para coletar dados de disciplinas e cursos da USP e organiza essas informações de maneira estruturada, permitindo diversas consultas após a coleta.

---

### Funcionalidades

Com este sistema, você pode:

- Fazer **raspagem de dados** do site da USP (usando `Selenium` e `BeautifulSoup`)
- Listar todos os cursos por unidade 
- Buscar dados de um determinado **curso**
- Obter dados completos de todos os cursos
- Obter informações de uma **disciplina específica**, incluindo:
  - Em quais cursos ela faz parte
- Descobrir **disciplinas que fazem parte de mais de um curso**

---

### Estrutura de Classes e arquivos

`Unit` (`unit.py`) - Representa uma unidade da USP.
 <br>
`Course` (`course.py`) - Representa um curso de graduação.
 <br>
`Subject` (`subject.py`) - Representa uma disciplina. 
 <br>
`usp` (`usp.py`) -  **Arquivo principal**. Executa a raspagem de dados e após isso exibe uma interface de interação com o usuário via terminal.
 <br>
`functionsUSP` (`functionsUSP.py`) -  Contém as **funções auxiliares** de scraping e manipulação de dados a qual são utilizadas na interface com o usuário.
 <br>
`Makefile` - Executa todos os arquivos e o programa


