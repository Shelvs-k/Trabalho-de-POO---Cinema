# 🏗️ Arquitetura do Sistema

O Sistema de Cinema foi desenvolvido utilizando Programação Orientada a Objetos (POO) combinado com uma arquitetura modular. O objetivo dessa divisão é garantir a separação de responsabilidades, facilitar a manutenção do código e permitir que o sistema cresça de forma organizada.

A arquitetura é dividida em camadas bem definidas, onde cada arquivo possui uma função específica:

## Camadas do Sistema

### 1. Camada de Apresentação (Interface de Usuário)
*   **Arquivo:** `cinema.py`
*   **Responsabilidade:** Gerencia a interface do sistema, exibe menus interativos, limpeza do terminal e captura as interações do usuário. Também inicializa recursos de áudio e gerencia os logs do sistema. 

### 2. Camada de Controle
*   **Arquivo:** `gerenciador.py`
*   **Responsabilidade:** Responsável por gerenciar o sistema. Contém as funções responsáveis por validar os dados e manipular os arquivos JSON no disco, administrando o CRUD do sistema.

### 3. Camada de Modelos 
*   **Arquivo:** `classes.py`
*   **Responsabilidade:** Define as estruturas do sistema (`Filme`, `Sala`, `Sessao`, `Cliente` e `Ingresso`). Serve para padronizar como os dados agem entre as camadas antes de serem convertidos para o formato JSON.

### 4. Camada de Persistência
*   **Local:** Pasta `dados/` e funções de arquivo (ex: `salvar_json`) em `gerenciador.py`.
*   **Responsabilidade:** Responsável pela leitura e escrita de arquivos `.json`. Cada registro é salvo individualmente (`ID - Nome.json`) organizando em diretórios específicos por entidade. 

### 5. Serviços Auxiliares
*   **Arquivos:** `debug.py`, `debug_monitor.py` e `musica.py`
*   **Responsabilidade:** Fornecem serviços auxiliares ao sistema, como o monitoramento de logs com uso de cores no terminal, além de possuir um recurso extra de reprodutor de áudio.

