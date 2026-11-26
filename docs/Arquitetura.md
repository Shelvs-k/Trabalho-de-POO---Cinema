# Arquitetura do sistema

O programa é uma aplicação de terminal organizada em módulos. O fluxo abaixo descreve o caminho executado pelos menus atuais:

```text
Usuário
   |
   v
src/cinema.py  ───────>  src/música.py
 (menus e execução)       (reprodutor opcional)
   |
   v
src/telas.py
 (operações de cada menu)
   |                 \
   v                  v
src/classes.py    src/persistencia.py
 (regras e modelos)  (leitura e gravação JSON)
                         |
                         v
                    src/dados/

src/debug.py ───────> src/debug_monitor.py
 (configura logs)       (acompanha o arquivo de log)
```

## Módulos

### `src/cinema.py` — entrada e menus

É o ponto de entrada executado por `python src/cinema.py`. Apresenta o menu principal e os menus de Filmes, Salas, Sessões, Clientes e Ingressos; encaminha cada escolha para a função correspondente de `telas.py`. Também permite abrir o reprodutor de música e ativar o modo de depuração digitando `debug` no menu inicial.

Ao iniciar, tenta registrar `Alt+H+P` para tocar `src/secrets/Ultra_Secret.mp3` e `Alt+H+S` para interromper essa reprodução. A integração com `keyboard` é opcional: se a biblioteca ou as permissões necessárias não estiverem disponíveis, os atalhos são desativados.

### `src/telas.py` — operações e interação

Implementa as ações invocadas pelos menus: solicita os dados no terminal, valida entradas, cria ou reconstrói objetos de domínio e chama a persistência. As operações disponíveis são:

| Categoria | Operações no menu |
| --- | --- |
| Filmes | Cadastrar, listar, consultar informações e excluir |
| Salas | Cadastrar, listar, consultar informações e excluir |
| Sessões | Cadastrar, listar, consultar disponibilidade e informações, editar e excluir |
| Clientes | Cadastrar, listar, consultar informações, ver histórico, editar e excluir |
| Ingressos | Emitir, listar, consultar informações e cancelar |

Uma exceção inesperada durante uma ação é exibida no terminal e registrada quando o debug está ativo; o menu continua disponível.

### `src/classes.py` — modelos e regras de domínio

Define `Filme`, `Sala`, `Sessao`, `Cliente` e `Ingresso`, assim como os enums de classificação indicativa, tipo e status da sessão e tipo de ingresso. As classes validam, entre outras condições, os valores de sessão, a capacidade e numeração dos assentos, a classificação etária do cliente, a disponibilidade para venda e a liberação de assento no cancelamento.

O arquivo também contém `GerenciadorFilmes` e `GerenciadorIngressos`, que mantêm coleções em memória. Os menus e as telas da versão atual não usam esses gerenciadores: os registros são consultados nos arquivos JSON. `Sessao` e `Ingresso` mantêm contadores de ID em memória, alinhados por `telas.py` com os arquivos existentes antes de criar um novo objeto.

### `src/persistencia.py` — arquivos JSON

Define os diretórios de cada entidade em `src/dados/`, localiza arquivos, escolhe IDs livres, lê e grava registros e converte sessões e ingressos entre objetos e dicionários. Cada gravação passa por um arquivo temporário e substituição do destino para evitar deixar um JSON parcialmente escrito.

Para reconstruir uma `Sessao` ou um `Ingresso` existente, as funções de carregamento montam o objeto sem executar o fluxo de criação/venda novamente. Elas preenchem atributos internos das classes; portanto, alterações nesses atributos precisam ser refletidas no módulo de persistência.

O processo de emissão e cancelamento atualiza mais de um JSON em sequência (ingresso, sessão e cliente). A gravação individual é protegida, mas o conjunto dessas atualizações não é uma transação única.

### `src/música.py` — reprodutor

Apresenta um menu de reprodução acessível pela opção **M**. Procura recursivamente arquivos `.mp3`, `.wav`, `.flac`, `.aac` e `.ogg` em `src/music/`; essa pasta é criada quando o reprodutor é aberto. A biblioteca `pygame` inicializa e controla o áudio.

### `src/debug.py` e `src/debug_monitor.py` — logs

O modo de depuração é ativado pela opção textual `debug` no menu inicial. Os arquivos de log são criados em `src/logs/`, com registros desde `DEBUG`; o terminal principal apresenta a partir de `INFO`. No Windows, `debug.py` tenta abrir uma nova janela para acompanhar o arquivo em tempo real usando `debug_monitor.py`. Nos demais sistemas, o logger informa que a abertura automática do monitor está configurada apenas para Windows.

`colorama` é usada para auxiliar na exibição de cores; o código possui alternativas para continuar sem ela.

## Visão das dependências

- `cinema.py` importa as ações de `telas.py` e os serviços de áudio, debug e atalhos.
- `telas.py` usa `classes.py` para regras e objetos e `persistencia.py` para os dados.
- `persistencia.py` também usa as classes para reconstruir objetos vinculados a registros existentes.
- `debug.py` fornece o logger que os demais módulos consultam quando o modo debug está ativo.

