# 🏗️ Arquitetura do Sistema

O Sistema de Cinema foi desenvolvido utilizando Programação Orientada a Objetos (POO) combinado com uma arquitetura modular. O objetivo dessa divisão é garantir a separação de responsabilidades, facilitar a manutenção do código e permitir que o sistema cresça de forma organizada.

A arquitetura é dividida em camadas bem definidas, onde cada arquivo possui uma função específica:

## Camadas do Sistema

### 1. Camada de Apresentação (Interface de Usuário)
*   **Arquivo:** `cinema.py`
*   **Responsabilidade:** Gerencia a interface do sistema, exibe menus interativos, limpeza do terminal e captura as interações do usuário. Também inicializa recursos de áudio e gerencia os logs do sistema. Se uma ação de menu falhar de forma inesperada, o erro é exibido e registrado, e o sistema volta ao menu.

### 2. Camada de Controle
*   **Arquivo:** `telas.py`
*   **Responsabilidade:** Responsável por gerenciar o sistema. Contém as funções chamadas pelos menus: perguntam os dados, usam as classes para validar as regras e administram o CRUD do sistema, pedindo à camada de persistência que guarde ou recupere os registros.

### 3. Camada de Modelos 
*   **Arquivos:** `filmes.py`, `sala.py`, `sessao.py`, `clientes.py` e `ingresso.py`, um módulo por entidade, cada um desenvolvido pela equipe responsável e mantido separado dos demais.
*   **Responsabilidade:** Define as estruturas do sistema (`Filme`, `Sala`, `Sessao`, `Cliente` e `Ingresso`). Serve para padronizar como os dados agem entre as camadas antes de serem convertidos para o formato JSON. As regras de negócio da venda (idade mínima, assento ocupado, sessão disponível) ficam em `Ingresso`, não em `telas.py`. `filmes.py` e `ingresso.py` também trazem `GerenciadorFilmes` e `GerenciadorIngressos`, coleções em memória que o fluxo atual não usa, já que os registros ficam nos arquivos JSON. A única dependência entre modelos é `ingresso.py` importando `StatusSessao` de `sessao.py`.

### 4. Camada de Persistência
*   **Arquivo:** `persistencia.py` e a pasta `dados/`.
*   **Responsabilidade:** Responsável pela leitura e escrita de arquivos `.json`. Cada registro é salvo individualmente (`ID - Nome.json`) organizando em diretórios específicos por entidade. 

### 5. Serviços Auxiliares
*   **Arquivos:** `debug.py`, `debug_monitor.py` e `música.py`
*   **Responsabilidade:** Fornecem serviços auxiliares ao sistema, como o monitoramento de logs com uso de cores no terminal, além de possuir um recurso extra de reprodutor de áudio.

## Observações de integração

As classes `Sessao` e `Ingresso` não possuem métodos para salvar nem carregar dados, e geram o próprio ID por um contador em memória que volta a 1 a cada execução. Por isso:

*   o `telas.py` alinha o contador (`Sessao._proximo_id` e `Ingresso._proximo_id`) com os arquivos existentes em disco antes de criar cada objeto;
*   o `persistencia.py` reconstrói sessões e ingressos salvos por `sessao_from_dict` e `ingresso_from_dict`, que usam `__new__` e atributos internos das classes (`_Sessao__id_sessao`, `_Ingresso__id` e outros). Se as equipes renomearem esses atributos, o carregamento precisa ser ajustado.
