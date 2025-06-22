## Manual de Utilização: Web Scraper de Dados da USP

### 1. Visão Geral do Projeto

Este projeto, desenvolvido para a disciplina de **Programação Orientada a Objetos**, é um programa em **Python** que utiliza **Web Scraping** para extrair informações detalhadas sobre os cursos de graduação e disciplinas da **Universidade de São Paulo (USP)** diretamente do sistema **Júpiter Web**.

A automação da navegação é feita com o **Selenium**, e a análise do HTML com **BeautifulSoup**.

Após a coleta, os dados são estruturados em classes (`Unit`, `Course`, `Subject`) e uma **interface de linha de comando (CLI)** é apresentada, permitindo ao usuário realizar diversas consultas sobre as informações armazenadas.

**Integrantes do Grupo:**

* Aluno: **Luis Henrique Ponciano dos Santos** (NUSP: 15577760)
* Aluno: **Wiltord Nyakeruma Mosingi** (NUSP: 15595392)
* Aluno: **Gabriel Demba** (NUSP: 15618344)

---

### 2. Pré-requisitos

Antes de prosseguir, garanta que seu sistema atende aos seguintes requisitos:

* **Python 3.10+:** O projeto utiliza a sintaxe `match...case` introduzida no Python 3.10 para o gerenciamento do menu principal no arquivo `usp.py`. Versões anteriores do Python não conseguirão executar o script.
* **Google Chrome:** O navegador web **Google Chrome** deve estar instalado.
* **ChromeDriver:** Essencial para que o Selenium controle o Chrome.

**Importante:** A versão do ChromeDriver deve ser **compatível com a versão do seu Google Chrome**.

**Passos para Configurar o ChromeDriver:**

1. Verifique sua versão do Chrome: Na barra de endereços do Chrome, digite:

   ```
   chrome://settings/help
   ```
2. Baixe o ChromeDriver:
   Acesse a página oficial de downloads do ChromeDriver:
   [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)
3. Posicione o ChromeDriver:
   Coloque o executável (`chromedriver.exe` para Windows ou `chromedriver` para macOS/Linux) na **mesma pasta** onde se encontra o script `usp.py`.

---

### 3. Instalação e Configuração

**Passo 1: Criar e Ativar um Ambiente Virtual**

Isso mantém as dependências do projeto isoladas do seu sistema.

**Em Linux ou macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Em Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Passo 2: Instalar as Dependências:**

Com o ambiente virtual ativado, execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install beautifulsoup4 selenium
```

---

### 4. Como Executar o Programa

Primeiro, abra o terminal e navegue até a pasta raiz do projeto (onde o arquivo `usp.py` está localizado).

Escolha um dos métodos de execução abaixo:

**Método A: Execução Direta (Universal)**

Este método funciona em todos os sistemas (Windows, macOS, Linux):

```bash
python usp.py
```

**Método B: Via Makefile (macOS ou Linux)**

Se você estiver usando macOS ou Linux e tiver o `make` instalado, pode usar os seguintes comandos:

```bash
make
make run
```

> **Observação:** Ao iniciar, o programa solicitará a quantidade de unidades da USP que você deseja processar.
> Digite um número inteiro e pressione Enter.

> **Aguarde o processo de raspagem de dados.** O terminal exibirá o progresso da coleta em tempo real.

> **Finalizada a coleta**, um **menu interativo** aparecerá no terminal com as opções de consulta.

---

### 5. Detalhes do Menu e Funcionamento dos Filtros

**Opção 1: Listar cursos por unidade**

* **Descrição:** Exibe todos os cursos que foram coletados, agrupados por sua respectiva unidade.
* **Como usar:** Escolha a opção "1". Não requer filtros.
* **Saída Esperada:** Uma lista formatada mostrando o nome de cada unidade, seguido pelos nomes de todos os cursos oferecidos por ela.

Exemplo:

```
Unidade: Escola de Artes, Ciências e Humanidades
Cursos oferecidos - quantidade de cursos [11]:

- Marketing - Integral
- Obstetrícia
...
```

**Opção 2: Obter dados de um curso específico (com filtros)**

* **Descrição:** Permite uma busca detalhada por cursos usando um ou mais critérios.

**Como usar os filtros:**

* **Filtros de texto:** Nome do curso, Nome da unidade, Código da disciplina, Nome da disciplina

  * Não diferenciam maiúsculas de minúsculas.
  * Fazem busca parcial (exemplo: "Engenharia" encontrará "Engenharia de Produção").
  * Deixe o campo em branco para não aplicar o filtro.
* **Filtros numéricos:** Duração mínima, máxima ou ideal

  * Retorna cursos com duração **maior ou igual à mínima** e **menor ou igual à máxima/ideal**.
  * Digite "0" ou deixe em branco para ignorar o filtro.

**Saída Esperada:**
Para cada curso que corresponder aos filtros, o programa exibirá um **relatório completo**, incluindo nome, unidade, durações e a lista detalhada de todas as suas disciplinas. Se nenhum curso for encontrado, uma mensagem informativa será exibida.

**Opção 3: Obter dados de todos os cursos**

* **Descrição:** Exibe os dados completos de absolutamente todos os cursos coletados.
* **Como usar:** Escolha a opção "3". Não há filtros.
* **Saída Esperada:** Uma longa lista contendo o relatório detalhado para cada curso armazenado.

**Opção 4: Obter dados de uma disciplina específica (com filtros)**

* **Descrição:** Permite buscar por uma disciplina específica em todos os cursos e ver seus detalhes.

**Como usar os filtros:**

* **Filtros de texto:** Código da disciplina, Nome da disciplina

  * Busca parcial e sem diferenciação entre maiúsculas e minúsculas.
* **Filtros numéricos:** Créd. Aulas, CH, CE, CP, ATPA

  * Retorna disciplinas com valor **maior ou igual** ao que você digitou.
  * Deixe em branco para ignorar.

**Saída Esperada:**
O programa listará cada curso que possui a disciplina correspondente aos filtros. Para cada ocorrência, exibirá o nome do curso e, em seguida, os **dados completos da disciplina**.

**Opção 5: Ver disciplinas que aparecem em mais de um curso**

* **Descrição:** Identifica disciplinas que são compartilhadas entre múltiplos cursos.
* **Como usar:** Apenas selecione a opção "5".
* **Saída Esperada:** Uma lista de disciplinas compartilhadas. Para cada uma, o programa mostrará o código, o nome e a lista de todos os cursos onde ela é oferecida.

Exemplo de saída:

```
--------------------------------------------------------------------------------------------------------------
Disciplina: [ 4300322 | Contabilidade Introdutória ] está presente nos cursos:
--------------------------------------------------------------------------------------------------------------
 - Ciências Contábeis
 - Administração
```

**Opção 6: Encerrar o programa**

* **Descrição:** Finaliza a execução do programa de forma segura.

---

### 6. Estrutura do Projeto

O código está organizado nos seguintes arquivos:

| Arquivo           | Descrição                                                      |
| ----------------- | -------------------------------------------------------------- |
| `usp.py`          | Arquivo principal. Executa a raspagem de dados e o menu CLI.   |
| `unit.py`         | Define a classe `Unit`, representando uma unidade da USP.      |
| `course.py`       | Define a classe `Course`, representando um curso de graduação. |
| `subject.py`      | Define a classe `Subject`, representando uma disciplina.       |
| `functionsUSP.py` | Funções auxiliares para consulta e manipulação de dados.       |
| `Makefile`        | Automatiza a instalação de dependências e execução do programa |

---
