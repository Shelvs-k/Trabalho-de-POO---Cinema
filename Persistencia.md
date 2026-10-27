# 💾 Persistência de Dados

O sistema foi projetado para salvar as informações mesmo após ser fechado. Em vez de manter apenas na memória RAM, todas as operações de CRUD (criação, leitura, edição  e exclusão) são gravadas diretamente no disco em formato JSON. 

## Estrutura de Armazenamento

Na primeira execução do sistema, uma pasta chamada `dados/` é criada automaticamente no mesmo diretório do código-fonte. Para manter a organização, os registros são separados em subpastas (buckets) de acordo com a sua entidade:

```text
dados/
├── Filmes/
├── Salas/
├── Clientes/
├── Sessoes/
└── Ingressos/ 