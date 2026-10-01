Foi decidido que o funcionamento do sistema do cinema ocorrerá pela composição de várias classes auxiliares, como "GerenciadorFilmes", "GerenciadorSalas" e etc.
Cada classe auxiliar ficará responsável pelo gerenciamento de suas respectivas classes, a classe GerenciadorFilmes conterá a lista de filmes do catálogo como atributo, e seus
métodos serão responsáveis por adicionar, remover, atualizar e listar os filmes, também contendo métodos para pegar um filme pelo id ou todos os filmes da lista. O mesmo vale
para a classe auxiliar GerenciadorSalas e para as próximas classes auxiliares

 * GerenciadorFilmes: classe auxiliar responsável pelo gerenciamento dos filmes no catálogo

 - "__init__(self)" inicializa a classe e contém um atributo chamado "self.__filmes = []" que é uma lista de todos os filmes do catálogo; 
    os filmes na lista devem ser da classe Filme
 - "get_filme_by_id(self, id: int)" é um método que retorna um filme que contém o id inserido no parâmetro, caso o filme não seja encontrado, retorna False
 - "adicionar_filme(self, id: int, titulo: str, duracao: str, genero: str, sinopse: str)" é um método que cria um filme contendo todos os seus atributos, e caso o filme
    não exista na lista de filmes, adiciona-o a lista; se o filme já existir na lista, o método retorna antes e o filme não é adicionado
 - "excluir_filme(self, id: int)" é um método que verifica se há um filme na lista através do id do filme inserido, se o filme estiver na lista, ele é removido
 - "atualizar_filme(self, id: int, n_titulo: str, n_duracao: str, n_genero: str, n_sinopse: str)" é um método que pega um filme na lista através do id, e caso o filme esteja
    na lista, atualiza todos os seus atributos, menos o id que precisa ser único
 - "listar_filmes(self)" é um métodos que mostra todos os filmes da lista de filmes, mostrando o ID, título, duração e gênero

 * GerenciadorSalas: classe auxiliar responsável pelo gerenciamento das salas do cinema

 - "__ini__(self)" inicializa a classe e contém um atributo chamado "self.__salas = []" que é uma lista de todas as salas do cinema; 
    as salas na lista devem ser da classe Sala
 - "get_sala_by_num(self, num: int)" é um método que retorna uma sala que contém o número inserido no parâmetro, caso a sala não seja encontrada, retorna False
 - "adicionar_sala(self, num: int, cap: int, ocup: int = 0)" é um método que cria uma sala contendo todos os seus atributos, e caso a sala não exista na lista de salas, 
    adiciona-a a lista; se a sala já existir na lista, o método retorna antes e a sala não é adicionada
 - "excluir_sala(self, num: int)" é um método que verifica se há uma sala na lista através do número da sala inserida, se a sala estiver na lista, ela é removida
 - "atualizar_sala(self, num: int, cap: int, ocup: int = 0)" é um método que pega uma sala na lista através do número, e caso a sala esteja na lista, atualiza todos os seus 
    atributos, menos o número que precisa ser único
 - "listar_salas(self)" é um métodos que mostra todas as salas da lista de salas, mostrando o número, capacidade, e assentos ocupados

 * GerenciadorSessoes: classe auxiliar responsável pelo gerenciamento das sessões do cinema

 - "__ini__(self)" inicializa a classe e contém um atributo chamado "self.__sessoes = []" que é uma lista de todas as sessões do cinema; 
    as sessões na lista devem ser da classe Sessao
 - "get_sessao_by_id(self, id: int)" é um método que retorna uma sessão que contém o id inserido no parâmetro, caso a sessão não seja encontrada, retorna False
 - "criar_sessao(self, id: int, filme: Filme, sala: Sala, data: str, horario: str, preco: float, assentos: int = 0)" é um método que cria uma sessão contendo todos os seus 
    atributos, e caso a sessão não exista na lista de sessões, adiciona-a a lista; se a sessão já existir na lista, o método retorna antes e a sessão não é adicionada
 - "remover_sessao(self, id: int)" é um método que verifica se há uma sessão na lista através do id da sessão inserida, se a sessão estiver na lista, ela é removida
 - "atualizar_sessao(self, id: int, filme: Filme, sala: Sala, data: str, horario: str, preco: float, assentos: int = 0)" é um método que pega uma sessão na lista através do 
    id, e caso a sessão esteja na lista, atualiza todos os seus atributos, menos o id que precisa ser único
 - "listar_sessoes(self)" é um métodos que mostra todas as sessões da lista de salas, mostrando o id, filme, sala, data, horário, preço do ingresso e assentos ocupados

As outras demais classes como Cliente e Ingresso ainda serão trabalhadas.
A classe Cinema conterá as classes auxiliares como atributo, e seus métodos retornarão o próprio atributo em questão, assim fazendo um encadeamento de métodos para cada ação que for ser realizada.
Exemplo: "cinema.gerenciar_filmes().adicionar_filme(...)" adiciona um filme na lista de filmes, que ficará no atributo que contém a classe GerenciadorFilmes
