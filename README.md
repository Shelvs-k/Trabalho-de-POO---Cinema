# 🎬 Sistema de Gerenciamento de Cinema

Sistema de gerenciamento de cinema desenvolvido em Python como projeto acadêmico da disciplina de **Programação Orientada a Objetos (POO)**. O projeto permite administrar filmes, salas, sessões, clientes e ingressos por meio de uma interface de terminal, com persistência de dados em arquivos JSON.

O objetivo do projeto é aplicar conceitos de programação, organização de código, manipulação de arquivos e separação de responsabilidades em um sistema funcional.

## 📋 Funcionalidades

O sistema organiza as operações de gerenciamento nas seguintes categorias:

- **Filmes:** cadastro, listagem, consulta de informações e exclusão.
- **Salas:** cadastro, listagem, consulta de informações e exclusão.
- **Sessões:** cadastro, listagem, consulta de informações e exclusão.
- **Clientes:** cadastro, listagem, consulta de informações e exclusão.
- **Ingressos:** cadastro, listagem, consulta de informações e exclusão.
- **Persistência de dados:** armazenamento dos registros em arquivos JSON, permitindo que os dados sejam mantidos entre execuções.
- **Interface de terminal:** menus interativos para acessar as funcionalidades disponíveis.
- **Easter eggs:** funcionalidades extras acionadas por atalhos de teclado.

As operações disponíveis podem variar conforme as opções implementadas nos menus de cada categoria.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **JSON:** formato utilizado para armazenar os dados.
- **`keyboard`:** biblioteca utilizada para detectar atalhos de teclado.
- **`pygame`:** biblioteca utilizada na reprodução de áudio.
- **Git e GitHub:** controle de versão e colaboração entre os integrantes da equipe.

O projeto também utiliza módulos da biblioteca padrão do Python, como `os`, `pathlib`, `json` e `re`.

## 📦 Pré-requisitos

Antes de executar o projeto, é necessário ter:

- Python instalado e disponível no terminal.
- Git instalado, caso deseje clonar o repositório.
- Windows para utilizar diretamente o script `instalar_dependencias.bat`.

## 🚀 Instalação

### 1. Clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/Shelvs-k/Trabalho-de-POO---Cinema.git
```

Entre na pasta do projeto:

```bash
cd Trabalho-de-POO---Cinema
```

### 2. Criar um ambiente virtual

Recomenda-se utilizar um ambiente virtual para manter as dependências do projeto isoladas de outras instalações do Python.

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bat
.venv\Scripts\activate
```

### 3. Instalar as dependências

**Opção A — Utilizando o script de instalação**

Execute o arquivo `instalar_dependencias.bat`, localizado na raiz do projeto. Ele automatiza a instalação das dependências configuradas para o sistema.

**Opção B — Utilizando o `requirements.txt`**

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` reúne as bibliotecas externas necessárias para a execução do projeto.

## ▶️ Como executar

Com as dependências instaladas, execute o arquivo principal a partir da raiz do repositório:

```bash
python cinema.py
```

O programa apresentará o menu principal no terminal. Utilize as opções exibidas para acessar as operações de gerenciamento disponíveis.

## 🏗️ Arquitetura do projeto

O código está organizado em três módulos principais, cada um com uma responsabilidade específica.

### `classes.py` — Modelos de dados

Define as classes que representam as entidades do sistema:

- `Filme`
- `Sala`
- `Sessao`
- `Cliente`
- `Ingresso`

Essas classes estruturam os dados utilizados pelo sistema, representando os objetos manipulados pelas operações de gerenciamento.

### `gerenciador.py` — Gerenciamento e persistência

Concentra as funções responsáveis pelas operações sobre as entidades do sistema. Entre suas responsabilidades estão:

- Cadastrar, listar, consultar e excluir registros.
- Localizar arquivos e registros existentes.
- Gerenciar identificadores.
- Ler e gravar informações em arquivos JSON.
- Organizar os dados persistidos em diretórios específicos.

Esse módulo conecta os modelos de dados ao armazenamento em arquivos.

### `cinema.py` — Interface e execução

É o ponto de entrada da aplicação. Esse módulo organiza os menus apresentados ao usuário, recebe as escolhas realizadas no terminal e chama as funções correspondentes do módulo `gerenciador.py`.

Também contém as funcionalidades extras relacionadas aos atalhos de teclado e à reprodução de áudio.

### Fluxo geral de execução

```text
Usuário
   |
   v
cinema.py
(Menu e interação)
   |
   v
gerenciador.py
(Operações e persistência)
   |
   +------> classes.py
   |        (Modelos de dados)
   |
   v
Arquivos JSON
(Armazenamento persistente)
```

## 💾 Persistência de dados

Diferentemente de uma implementação que mantém todos os registros somente na memória durante a execução, este projeto utiliza arquivos JSON para armazenar os dados.

Os registros são organizados em diretórios separados por categoria, dentro da pasta `dados/`.

Estrutura geral:

```text
dados/
├── Filmes/
├── Salas/
├── Clientes/
├── Sessoes/
└── Ingressos/
```

Cada registro é armazenado em um arquivo JSON individual, utilizando um padrão de nome semelhante a:

```text
ID - Nome.json
```

Por exemplo:

```text
dados/
└── Filmes/
    └── 1 - Filme Exemplo.json
```

O conteúdo de cada arquivo representa os dados de um registro em formato JSON.

O módulo `gerenciador.py` contém as funções responsáveis por localizar, ler, criar e organizar esses arquivos. Os diretórios necessários também são criados automaticamente quando a aplicação é inicializada.

**Importante:** os arquivos JSON fazem parte do funcionamento do sistema. Caso os dados precisem ser preservados, não exclua a pasta `dados/` sem antes manter uma cópia dos registros.

## 📁 Estrutura do repositório

```text
Trabalho-de-POO---Cinema/
├── cinema.py
├── classes.py
├── gerenciador.py
├── requirements.txt
├── instalar_dependencias.bat
├── dados/
│   ├── Filmes/
│   ├── Salas/
│   ├── Clientes/
│   ├── Sessoes/
│   └── Ingressos/
└── secrets/
    └── Ultra_Secret.mp3
```

A estrutura acima representa a organização geral do projeto. Os arquivos JSON são criados e modificados conforme as operações realizadas, e alguns diretórios podem ser gerados automaticamente durante a execução.

## 🧪 Solução de problemas

### O comando `python` não é reconhecido

Verifique se o Python está instalado e se foi adicionado ao `PATH` do sistema. No Windows, também pode ser possível utilizar o comando `py`.

### Ocorreu um erro ao importar uma biblioteca

Certifique-se de que o ambiente virtual está ativado e de que as dependências foram instaladas:

```bash
python -m pip install -r requirements.txt
```

### O sistema não encontra os dados

Execute o programa a partir da raiz do repositório e verifique se os arquivos JSON necessários estão presentes nos diretórios correspondentes dentro de `dados/`.

### O áudio ou os atalhos de teclado não funcionam

Verifique se as dependências estão instaladas e se o arquivo de áudio está no caminho esperado. O funcionamento dos atalhos também pode depender do sistema operacional e das permissões disponíveis.

## 👥 Desenvolvimento em equipe

Este projeto foi desenvolvido colaborativamente como atividade acadêmica. O repositório utiliza Git e GitHub para acompanhar as alterações no código e facilitar a integração do trabalho dos integrantes.