# 🎬 Sistema de Gerenciamento de Cinema

Sistema de gerenciamento de cinema desenvolvido em Python como projeto acadêmico da disciplina de **Programação Orientada a Objetos (POO)**. O projeto permite administrar filmes, salas, sessões, clientes e ingressos por meio de uma interface de terminal, com persistência de dados em arquivos JSON.

O objetivo do projeto é aplicar conceitos de programação, organização de código, manipulação de arquivos e separação de responsabilidades em um sistema funcional.

## 📋 Funcionalidades

O sistema organiza as operações de gerenciamento nas seguintes categorias:

- **Filmes:** cadastro, listagem, consulta de informações e exclusão.
- **Salas:** cadastro, listagem, consulta de informações e exclusão.
- **Sessões:** cadastro, listagem, consulta de disponibilidade e de informações, edição e exclusão.
- **Clientes:** cadastro, listagem, consulta de informações, histórico de ingressos, edição e exclusão.
- **Ingressos:** emissão, listagem, consulta de informações e cancelamento.
- **Persistência de dados:** armazenamento dos registros em arquivos JSON, permitindo que os dados sejam mantidos entre execuções.
- **Interface de terminal:** menus interativos para acessar as funcionalidades disponíveis.
- **Easter eggs:** funcionalidades extras acionadas por atalhos de teclado.

As operações disponíveis podem variar conforme as opções implementadas nos menus de cada categoria.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **JSON:** formato utilizado para armazenar os dados.
- **`keyboard`:** biblioteca utilizada para detectar atalhos de teclado.
- **`pygame`:** biblioteca utilizada na reprodução de áudio.
- **`colorama`:** biblioteca utilizada para exibir os logs coloridos no terminal do Windows (modo debug).
- **Git e GitHub:** controle de versão e colaboração entre os integrantes da equipe.

O projeto também utiliza módulos da biblioteca padrão do Python, como `os`, `pathlib`, `json`, `re`, `datetime`, `math`, `logging` e `subprocess`.

## 📦 Pré-requisitos

Antes de executar o projeto, é necessário ter:

- Python 3.9 ou superior instalado e disponível no terminal.
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

No Linux ou macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar as dependências

**Opção A — Utilizando o script de instalação**

Execute o arquivo `instalar_dependencias.bat`, localizado na raiz do projeto. Ele automatiza a instalação das dependências configuradas para o sistema.

**Opção B — Utilizando o `requirements.txt`**

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` reúne as bibliotecas externas necessárias para a execução do projeto: `pygame`, `keyboard` e `colorama`.

## ▶️ Como executar

Com as dependências instaladas, execute o arquivo principal a partir da raiz do repositório:

```bash
python src/cinema.py
```

O programa apresentará o menu principal no terminal. Utilize as opções exibidas para acessar as operações de gerenciamento disponíveis.

Os dados (`src/dados/`) e os logs (`src/logs/`) são gravados ao lado do código-fonte, independentemente da pasta de onde o comando é executado.

Se um registro tiver um erro inesperado (por exemplo, um arquivo JSON editado à mão e com campos faltando), a falha é exibida e registrada no log, e o sistema volta ao menu em vez de ser encerrado.

## 🏗️ Arquitetura do projeto

O código está organizado em módulos com responsabilidades específicas: um módulo de modelo para cada entidade (cada um desenvolvido pela equipe responsável), mais as telas, a persistência e a interface, além de módulos auxiliares de depuração e música.

### Modelos de dados — um módulo por entidade

Cada entidade fica no módulo da equipe que a desenvolveu, e não há arquivo que as reúna:

- `src/filmes.py`: `Filme`, `ClassificacaoIndicativa`, `GerenciadorFilmes` e as exceções de filme.
- `src/sala.py`: `Sala`.
- `src/sessao.py`: `Sessao`, `TipoSessao` e `StatusSessao`.
- `src/clientes.py`: `Cliente`.
- `src/ingresso.py`: `Ingresso`, `TipoIngresso`, `IngressoError` e `GerenciadorIngressos`.

Essas classes estruturam os dados utilizados pelo sistema e concentram as regras de negócio (por exemplo, idade mínima e assento já ocupado na venda de ingressos). Um módulo pode importar outro quando depende dele: `ingresso.py` usa `StatusSessao` de `sessao.py`.

Os testes automatizados do módulo de filmes ficam em `src/test_filmes.py`. Para executá-los:

```bash
cd src
python -m unittest test_filmes
```

### `src/telas.py` — Telas de cada operação

Concentra as funções chamadas pelos menus. Cada uma pergunta os dados no terminal, usa as classes dos módulos de modelo (que validam as regras de negócio) e pede ao módulo de persistência para guardar ou recuperar os registros. Entre suas responsabilidades estão:

- Cadastrar, listar, consultar, editar e excluir (ou cancelar) registros.
- Consultar a disponibilidade de uma sessão e o histórico de ingressos de um cliente.
- Emitir e cancelar ingressos.

### `src/persistencia.py` — Persistência em JSON

Responsável por ler e gravar os arquivos JSON. Entre suas responsabilidades estão:

- Localizar arquivos e registros existentes.
- Gerenciar identificadores.
- Ler e gravar informações em arquivos JSON, de forma que uma interrupção não deixe um arquivo pela metade.
- Converter `Sessao` e `Ingresso` de e para dicionários.
- Organizar os dados persistidos em diretórios específicos.

### `src/cinema.py` — Interface e execução

É o ponto de entrada da aplicação. Esse módulo organiza os menus apresentados ao usuário, recebe as escolhas realizadas no terminal e chama as funções correspondentes do módulo `src/telas.py`.

Também contém as funcionalidades extras relacionadas aos atalhos de teclado e à reprodução de áudio.

### Fluxo geral de execução

```text
Usuário
   |
   v
src/cinema.py
(Menu e interação)
   |
   v
src/telas.py
(Telas e operações)
   |
   +------> src/filmes.py, sala.py, sessao.py,
   |        clientes.py, ingresso.py
   |        (Modelos de dados)
   |
   v
src/persistencia.py
(Leitura e gravação)
   |
   v
Arquivos JSON
(Armazenamento persistente)
```

O `src/persistencia.py` também importa os módulos `filmes.py`, `sessao.py` e `ingresso.py`, pois reconstrói os objetos `Filme`, `Sessao` e `Ingresso` a partir dos arquivos JSON.

### `src/música.py` — Reprodutor de música

Reprodutor de áudio acessado pela opção `M` dos menus. Toca os arquivos da pasta `src/music/`.

### `src/debug.py` — Depuração e testes

É o módulo responsável por ativar o modo de depuração do sistema, extremamente útil para realizar testes e registrar falhas. Os registros ficam em arquivos dentro da pasta `src/logs/`, que é gerada automaticamente ao ativar o modo debug

Contém a funcionalidade:

- Ativar debug: ativa o modo de depuração para começar a registrar o log (usado em src/cinema.py)

O arquivo `src/debug_monitor.py` abre o segundo terminal que acompanha o log em tempo real (abertura automática somente no Windows; no Linux e no macOS, acompanhe o arquivo com `tail -f src/logs/<arquivo>.log`).

## 💾 Persistência de dados

Diferentemente de uma implementação que mantém todos os registros somente na memória durante a execução, este projeto utiliza arquivos JSON para armazenar os dados.

Os registros são organizados em diretórios separados por categoria, dentro da pasta `src/dados/`.

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

O módulo src/persistencia.py contém as funções responsáveis por localizar, ler, criar e organizar esses arquivos. Os diretórios necessários também são criados automaticamente quando a aplicação é inicializada.

**Importante:** os arquivos JSON fazem parte do funcionamento do sistema. Caso os dados precisem ser preservados, não exclua a pasta `dados/` sem antes manter uma cópia dos registros.

## 📁 Estrutura do repositório

```text
Trabalho-de-POO---Cinema/
│
├── src/
│   ├── cinema.py
│   ├── filmes.py
│   ├── sala.py
│   ├── sessao.py
│   ├── clientes.py
│   ├── ingresso.py
│   ├── test_filmes.py
│   ├── telas.py
│   ├── persistencia.py
│   ├── debug.py
│   ├── debug_monitor.py
│   ├── música.py
│   ├── music/
│   ├── logs/              (gerada ao ativar o debug)
│   ├── dados/
│   │   ├── Filmes/
│   │   ├── Salas/
│   │   ├── Clientes/
│   │   ├── Sessoes/
│   │   └── Ingressos/
│   └── secrets/
│       ├── README.md
│       └── Ultra_Secret.mp3
│
├── docs/
│   ├── Arquitetura.md
│   └── Persistencia.md
│
├── requirements.txt
├── instalar_dependencias.bat
└── README.md
```

A estrutura acima representa a organização geral do projeto. As pastas `dados/` e `logs/` ficam dentro de `src/`, ao lado dos módulos que as geram (`persistencia.py` e `debug.py`). Os arquivos JSON são criados e modificados conforme as operações realizadas, e alguns diretórios podem ser gerados automaticamente durante a execução.

## 🧪 Solução de problemas

### O comando `python` não é reconhecido

Verifique se o Python está instalado e se foi adicionado ao `PATH` do sistema. No Windows, também pode ser possível utilizar o comando `py`.

### Ocorreu um erro ao importar uma biblioteca

Certifique-se de que o ambiente virtual está ativado e de que as dependências foram instaladas:

```bash
python -m pip install -r requirements.txt
```

### O sistema não encontra os dados

Os dados ficam em `src/dados/`, ao lado do código-fonte, e não dependem da pasta de onde o programa é executado. Verifique se os arquivos JSON necessários estão presentes nos diretórios correspondentes e se seus nomes seguem o padrão `ID - Nome.json`; arquivos fora desse padrão são ignorados.

### O áudio ou os atalhos de teclado não funcionam

Verifique se as dependências estão instaladas e se o arquivo de áudio está no caminho esperado. O funcionamento dos atalhos também pode depender do sistema operacional e das permissões disponíveis: no Linux e no macOS, a biblioteca `keyboard` normalmente exige execução com privilégios de administrador (root). Sem ela, o sistema continua funcionando normalmente, apenas sem os atalhos.

## 🐞 Sistema de Debug e Logs

O projeto possui um sistema de logs para facilitar a identificação de erros e o acompanhamento das operações executadas durante o uso da aplicação.

### Como ativar

1. Execute o sistema normalmente:

   ```bash
   python src/cinema.py
   ```

2. No menu principal (somente nele), digite `debug` para ativar o sistema de debug.
3. No Windows, o sistema abre um segundo terminal dedicado ao monitoramento dos registros em tempo real.

### Níveis de registro

Os registros utilizam os níveis do módulo `logging` do Python:

- **`DEBUG`**: detalhes técnicos úteis para investigar o comportamento interno.
- **`INFO`**: operações realizadas com sucesso e eventos normais relevantes.
- **`WARNING`**: situações inesperadas que não impedem necessariamente a execução.
- **`ERROR`**: falhas que impedem uma operação específica.
- **`CRITICAL`**: problemas extremamente graves que podem comprometer o funcionamento do sistema.
- **`exception()`**: método usado dentro de blocos `except` para registrar uma falha junto com o traceback. Por padrão, esse registro tem nível `ERROR`.

### Onde os registros são exibidos

- **Terminal principal:** exibe registros a partir do nível `INFO`.
- **Segundo terminal:** acompanha o arquivo de log em tempo real e diferencia os níveis por cores.
- **Arquivos de log:** são salvos na pasta `src/logs/`, com nome baseado na data e no horário da execução. O arquivo registra mensagens a partir do nível `DEBUG` e inclui a localização do código em avisos e erros.

Exemplo da estrutura gerada:

```text
src/logs/
└── cinema_DD-MM-AAAA_HH-MM-SS.log
```

A pasta `logs/` e os arquivos `.log` são gerados durante a execução e não precisam ser versionados no Git.

### Como adicionar novos registros

Ao implementar uma nova função ou alterar uma existente, avalie quais eventos precisam ser registrados. Use a função `registrar_log(nivel, mensagem)` nos módulos que a disponibilizam.

Exemplos:

```python
registrar_log("debug", "Iniciando a busca por um filme.")
registrar_log("info", "Filme cadastrado com sucesso.")
registrar_log("warning", "O filme solicitado não foi encontrado.")
```

Dentro de um bloco `except`, use `registrar_log("exception", "...")` quando o traceback ajudar a investigar a falha. Registre o sucesso somente depois que a operação tiver sido concluída e evite mensagens repetitivas em funções chamadas por outras funções que já registram o mesmo evento.

## 👥 Desenvolvimento em equipe

Este projeto foi desenvolvido colaborativamente como atividade acadêmica. O repositório utiliza Git e GitHub para acompanhar as alterações no código e facilitar a integração do trabalho dos integrantes.
