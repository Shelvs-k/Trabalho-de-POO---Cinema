# 💾 Persistência de Dados

O sistema foi projetado para salvar as informações mesmo após ser fechado. Em vez de manter apenas na memória RAM, todas as operações de CRUD (criação, leitura, edição e exclusão) são gravadas diretamente no disco em formato JSON. 

## Estrutura de Armazenamento

Na primeira execução do sistema, uma pasta chamada `dados/` é criada automaticamente no mesmo diretório do código-fonte. Para manter a organização, os registros são separados em subpastas (buckets) de acordo com a sua entidade:

```text
dados/
├── Filmes/
├── Salas/
├── Clientes/
├── Sessoes/
└── Ingressos/
```

Cada registro é um arquivo `ID - Nome.json` (por exemplo, `2 - Sessao.json`). O ID é o menor número positivo ainda livre na pasta da entidade. Os arquivos são gravados em um temporário e trocados de uma vez, para que uma interrupção não deixe um JSON pela metade. Arquivos fora do padrão `ID - Nome.json` são ignorados, e todo arquivo precisa conter um objeto JSON (um dicionário); qualquer outro conteúdo é tratado como erro de leitura.

## Formato dos arquivos

```text
Filmes/    id, titulo, duracao, genero, sinopse, classificacao (0, 10, 12, 14, 16 ou 18)
Salas/     numero, capacidade
Clientes/  id, nome, idade, email, ingressos (lista de IDs)
Sessoes/   id_sessao, filme_id, sala_numero, data_hora ("dd/mm/aaaa hh:mm"),
           tipo (1=3D, 2=2D, 3=Assistiva), preco, status (1=Em Breve,
           2=Em Progresso, 3=Concluída), assentos_ocupados (lista de números)
Ingressos/ id_ingresso, cliente_id, sessao_id, poltrona, tipo ("inteira" ou "meia"), preco
```

Os assentos ocupados de uma sessão ficam em `assentos_ocupados` (arquivo da sessão); a sala guarda apenas número e capacidade. Cancelar um ingresso apaga o arquivo dele, libera o assento na sessão e remove o ID da lista do cliente.
