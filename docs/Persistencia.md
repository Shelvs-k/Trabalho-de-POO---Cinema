# Persistência de dados

O sistema guarda cada registro em um arquivo JSON individual. A pasta base é `src/dados/`, definida a partir da localização de `persistencia.py`; por isso, o local de execução do comando não muda o destino dos dados. As pastas das entidades são criadas automaticamente quando o módulo de persistência é carregado.

```text
src/dados/
├── Filmes/
├── Salas/
├── Sessoes/
├── Clientes/
└── Ingressos/
```

Os arquivos seguem o padrão `<ID> - <nome>.json`. O prefixo numérico é o identificador usado para localizar o registro. O nome é adaptado para remover caracteres que não podem ser usados em nomes de arquivo. Os nomes variam por entidade, por exemplo `1 - Moana.json`, `1 - Sala.json`, `2 - Sessao.json` e `1 - Ingresso.json`.

Os diretórios `src/dados/` deste projeto já podem conter registros de exemplo. Faça uma cópia dessa pasta antes de remover ou editar arquivos manualmente se quiser preservar os dados.

## Formato dos registros

Os arquivos devem conter um objeto JSON (dicionário), com os campos abaixo:

| Diretório | Campos persistidos |
| --- | --- |
| `Filmes/` | `id`, `titulo`, `duracao` (minutos), `genero`, `sinopse`, `classificacao` |
| `Salas/` | `numero`, `capacidade` |
| `Sessoes/` | `id_sessao`, `filme_id`, `sala_numero`, `data_hora` (`dd/mm/aaaa hh:mm`), `tipo`, `preco`, `status`, `assentos_ocupados` |
| `Clientes/` | `id`, `nome`, `idade`, `email`, `ingressos` (lista de IDs de ingressos) |
| `Ingressos/` | `id_ingresso`, `cliente_id`, `sessao_id`, `poltrona`, `tipo`, `preco` |

Os valores de enum gravados nos arquivos são numéricos:

- `classificacao`: `0` (Livre), `10`, `12`, `14`, `16` ou `18`.
- `tipo` da sessão: `1` (3D), `2` (2D) ou `3` (Assistiva).
- `status` da sessão: `1` (Em Breve), `2` (Em Progresso) ou `3` (Concluída).
- `tipo` do ingresso: texto `inteira` ou `meia`.

`assentos_ocupados` contém os números dos assentos vendidos naquela sessão. A sala guarda número e capacidade; os ocupados são associados a uma sessão específica.

## Relacionamentos e regras aplicadas

- Uma sessão referencia um filme por `filme_id` e uma sala por `sala_numero`.
- Um ingresso referencia um cliente e uma sessão. Seu campo `poltrona` identifica o assento reservado.
- A emissão valida se a sessão está **Em Breve**, se ainda há assento livre, se o número informado cabe na capacidade da sala e se a idade do cliente atende à classificação do filme. A meia-entrada é calculada como 50% do preço da sessão.
- O cancelamento só é permitido enquanto a sessão está **Em Breve**. Quando concluído, libera o assento, remove o ID do ingresso da lista do cliente e apaga o arquivo do ingresso.
- Um filme ou uma sala com sessão vinculada não pode ser excluído. Uma sessão com assentos ocupados não pode ser excluída. Um cliente com ingressos vinculados não pode ser excluído.

Essas operações não fazem exclusões em cascata. Os vínculos precisam estar consistentes nos arquivos relacionados.

## Identificadores, leitura e gravação

O módulo procura arquivos com nomes no formato `<ID> - <nome>.json`. O próximo cadastro usa o menor ID positivo que ainda não aparece na pasta daquela entidade; depois de uma exclusão, o ID removido pode voltar a ser usado. Os contadores em memória de `Sessao` e `Ingresso` são ajustados com base nos arquivos antes da criação de um novo objeto.

Ao gravar ou atualizar um JSON, `persistencia.py` escreve primeiro em um arquivo temporário e então o substitui pelo arquivo definitivo. Isso protege cada arquivo contra uma interrupção durante a escrita. Emissões e cancelamentos alteram vários arquivos em sequência, sem uma transação única para o conjunto.

Arquivos JSON inválidos, ilegíveis ou cujo conteúdo não seja um objeto são reportados e não são carregados como registros válidos. Arquivos que não seguem o padrão de nome também não entram nas buscas e listagens do sistema.

