# Sistema de Gerenciamento de Cinema

Projeto acadêmico de Programação Orientada a Objetos (POO), desenvolvido em Python. O programa oferece menus de terminal para administrar filmes, salas, sessões, clientes e ingressos. Os registros são persistidos em arquivos JSON dentro de `src/dados/`.

## Funcionalidades

- **Filmes:** cadastro, listagem, consulta e exclusão.
- **Salas:** cadastro, listagem, consulta e exclusão.
- **Sessões:** cadastro, listagem, consulta de disponibilidade e detalhes, edição e exclusão.
- **Clientes:** cadastro, listagem, consulta, histórico de ingressos, edição e exclusão.
- **Ingressos:** emissão, listagem, consulta e cancelamento.
- **Música:** reprodutor que procura arquivos `.mp3`, `.wav`, `.flac`, `.aac` e `.ogg` em `src/music/`.
- **Depuração:** logs ativados ao digitar `debug` no menu inicial.

As regras de venda verificam a disponibilidade da sessão e do assento, além da classificação indicativa do filme. A meia-entrada custa metade do preço da sessão. Consulte [Persistência de dados](docs/Persistencia.md) para conhecer as regras completas e o formato dos arquivos.

## Requisitos

- Python 3.9 ou superior.
- Windows para executar diretamente o instalador `instalar_dependencias.bat`. Em outros sistemas, instale as dependências pelo `pip`.

O arquivo `requirements.txt` instala `pygame`, `keyboard` e `colorama`. O `pygame` é usado pelo áudio; se `keyboard` não estiver disponível, os atalhos globais são desativados. `colorama` auxilia na exibição de cores no terminal.

## Instalação e execução

Na pasta do projeto, crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bat
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

No Windows, também é possível executar `instalar_dependencias.bat` na raiz do projeto. Para iniciar o sistema, ainda na raiz:

```bash
python src/cinema.py
```

O programa cria as pastas de dados necessárias em `src/dados/` se elas ainda não existirem. Os caminhos são definidos a partir da localização dos módulos, então a aplicação pode ser iniciada de outra pasta.

## Menus e atalhos

No menu inicial, escolha **1** Filmes, **2** Salas, **3** Sessões, **4** Clientes ou **5** Ingressos. Digite **M** para abrir o reprodutor de música; **0** volta ou encerra conforme o menu. A opção `debug` ativa os logs durante a execução.

Ao iniciar, o programa também tenta registrar os atalhos globais do easter egg:

- `Alt+H+P`: reproduz `src/secrets/Ultra_Secret.mp3`.
- `Alt+H+S`: interrompe a reprodução do easter egg.

Os atalhos dependem da biblioteca `keyboard` e das permissões do sistema. O menu e as operações de cinema continuam disponíveis se o registro dos atalhos falhar.

## Organização do projeto

```text
.
├── README.md
├── docs/
│   ├── Arquitetura.md
│   └── Persistencia.md
├── src/
│   ├── cinema.py
│   ├── telas.py
│   ├── classes.py
│   ├── persistencia.py
│   ├── debug.py
│   ├── debug_monitor.py
│   ├── música.py
│   ├── dados/       (registros JSON)
│   ├── music/       (criada pelo reprodutor, para arquivos de música)
│   └── secrets/
│       └── Ultra_Secret.mp3
├── requirements.txt
├── executar.bat
└── instalar_dependencias.bat
```

O fluxo usado pelos menus é `cinema.py` → `telas.py` → `classes.py` e `persistencia.py`. Veja [Arquitetura](docs/Arquitetura.md) para a descrição dos módulos e [Persistência](docs/Persistencia.md) para o esquema JSON.

## Documentação

- [Arquitetura do sistema](docs/Arquitetura.md)
- [Persistência de dados](docs/Persistencia.md)

