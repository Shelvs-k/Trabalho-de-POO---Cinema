"""
Módulo Filmes - Sistema de Cinema (Grupo 1)
Programação Orientada a Objetos - UFC Itapajé - Profa. Renata Vieira Rios - 2026.2

Classes: ClassificacaoIndicativa, Filme e GerenciadorFilmes,
além das exceções FilmeDuplicadoError e FilmeNaoEncontradoError.
"""

from enum import Enum


class FilmeDuplicadoError(Exception):
    """Cadastro de filme com id_filme já existente.

    Lançado por GerenciadorFilmes.cadastrar_filme quando o ID do filme
    que está sendo cadastrado já existe no sistema.
    """


class FilmeNaoEncontradoError(Exception):
    """Busca por id_filme inexistente.

    Lançado por GerenciadorFilmes.buscar_por_id quando o filme pesquisado
    não existe no sistema, ou seja, não está cadastrado (não possui ID).
    """


class ClassificacaoIndicativa(Enum):
    """Faixa etária indicada para um filme, como as etiquetas na capa do DVD.

    Cada opção tem um nome e um valor. O valor é a idade mínima (em anos).
    Por ser uma lista fechada de opções, evita erros de digitação, como
    escrever "18 anos", "dezoito" ou "+18".
    """

    LIVRE = 0
    DEZ_ANOS = 10
    DOZE_ANOS = 12
    CATORZE_ANOS = 14
    DEZESSEIS_ANOS = 16
    DEZOITO_ANOS = 18

    @property
    def idade_minima(self) -> int:
        """int: idade mínima, em anos.

        É um apelido mais fácil para o valor da classificação: devolve o
        número da idade em vez da escrita dessa idade.
        """
        return self.value

    @property
    def descricao(self) -> str:
        """str: texto da classificação para o público.

        Pega o nome da classificação atual (ex: DEZ_ANOS) e devolve
        "Não recomendado para menores de 10 anos".
        """
        descricoes = {
            "LIVRE": "Livre para todos os públicos",
            "DEZ_ANOS": "Não recomendado para menores de 10 anos",
            "DOZE_ANOS": "Não recomendado para menores de 12 anos",
            "CATORZE_ANOS": "Não recomendado para menores de 14 anos",
            "DEZESSEIS_ANOS": "Não recomendado para menores de 16 anos",
            "DEZOITO_ANOS": "Não recomendado para menores de 18 anos",
        }
        return descricoes[self.name]


class Filme:
    """Filme do catálogo do cinema.

    O id_filme é definido na criação e não pode ser alterado depois.
    Os demais atributos podem ser alterados, e cada novo valor passa pela
    validação do respectivo setter.

    Attributes:
        id_filme (int): identificador único. Somente leitura.
        titulo (str): título, sem espaços nas pontas. Tem que ter algo escrito.
        duracao (float): duração em minutos. Deve ser maior que 0.
        genero (str): gênero, sem espaços nas pontas. Não pode ser vazio.
        sinopse (str): resumo da história.
        classificacao (ClassificacaoIndicativa): faixa etária do filme.
    """

    def __init__(self, id_filme: int, titulo: str, duracao: float,
                 genero: str, sinopse: str,
                 classificacao: ClassificacaoIndicativa) -> None:
        """Cria um filme validando os dados recebidos.

        Args:
            id_filme: identificador único. Deve ser maior que 0.
            titulo: título do filme. Não pode ser vazio.
            duracao: duração em minutos. Deve ser maior que 0.
            genero: gênero do filme. Não pode ser vazio.
            sinopse: resumo da história.
            classificacao: faixa etária do filme.

        Raises:
            ValueError: se id_filme <= 0, se titulo ou genero forem vazios
                (ou só espaços) ou se duracao <= 0.
            TypeError: se classificacao não for uma ClassificacaoIndicativa.
        """
        if id_filme <= 0:
            raise ValueError("id_filme deve ser maior que 0.")
        self._id_filme = id_filme

        # As atribuições abaixo passam pelos setters, que validam os valores.
        # Os tipos de titulo, duracao e genero não são verificados: um valor
        # de tipo errado (ex: titulo=123) gera AttributeError ou TypeError,
        # não ValueError.
        self.titulo = titulo
        self.duracao = duracao
        self.genero = genero
        self.sinopse = sinopse
        self.classificacao = classificacao

    @property
    def id_filme(self) -> int:
        """int: identificador único do filme. Somente leitura."""
        return self._id_filme

    @property
    def titulo(self) -> str:
        """str: título do filme, sem espaços no início e no fim.

        Raises:
            ValueError: se colocar um valor vazio ou só com espaços.
        """
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("O título não pode ser vazio.")
        self._titulo = valor.strip()

    @property
    def duracao(self) -> float:
        """float: duração do filme em minutos.

        Raises:
            ValueError: ao atribuir um valor menor ou igual a 0.
        """
        return self._duracao

    @duracao.setter
    def duracao(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("A duração deve ser maior que 0.")
        self._duracao = valor

    @property
    def genero(self) -> str:
        """str: gênero do filme, sem espaços no início e no fim.

        Raises:
            ValueError: ao atribuir um valor vazio ou só com espaços.
        """
        return self._genero

    @genero.setter
    def genero(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("O gênero não pode ser vazio.")
        self._genero = valor.strip()

    @property
    def sinopse(self) -> str:
        """str: resumo da história. Aceita qualquer valor e não tem validação."""
        return self._sinopse

    @sinopse.setter
    def sinopse(self, valor: str) -> None:
        self._sinopse = valor

    @property
    def classificacao(self) -> ClassificacaoIndicativa:
        """ClassificacaoIndicativa: faixa etária do filme.

        Raises:
            TypeError: ao atribuir um valor que não seja um
                ClassificacaoIndicativa.
        """
        return self._classificacao

    @classificacao.setter
    def classificacao(self, valor: ClassificacaoIndicativa) -> None:
        if not isinstance(valor, ClassificacaoIndicativa):
            raise TypeError(
                "classificacao deve ser um ClassificacaoIndicativa.")
        self._classificacao = valor

    def permitido_para(self, idade_cliente: int) -> bool:
        """Informa se um cliente tem idade para assistir ao filme.

        Args:
            idade_cliente: idade do cliente. Não pode ser negativa.

        Returns:
            True se idade_cliente for maior ou igual à idade mínima da
            classificação, False caso contrário.

        Raises:
            ValueError: se idade_cliente for negativa.
        """
        if idade_cliente < 0:
            raise ValueError("idade_cliente não pode ser negativa.")
        return idade_cliente >= self._classificacao.idade_minima

    def exibir_detalhes(self) -> str:
        """Monta um texto com os dados do filme, uma informação por linha.

        Returns:
            Texto com id, título, gênero, duração (em min), descrição da
            classificação e sinopse.
        """
        return (
            f"[{self._id_filme}] {self._titulo}\n"
            f"Gênero: {self._genero}\n"
            f"Duração: {self._duracao} min\n"
            f"Classificação: {self._classificacao.descricao}\n"
            f"Sinopse: {self._sinopse}"
        )

    def __repr__(self) -> str:
        """Representação para depuração, com id e título."""
        return f"Filme(id_filme={self._id_filme}, titulo={self._titulo!r})"


class GerenciadorFilmes:
    """Catálogo de filmes em memória.

    Guarda os filmes em um dicionário indexado por id_filme, o que torna a
    busca por id direta. Os filmes são listados na ordem que foram cadastrados.
    """

    def __init__(self) -> None:
        """Cria um catálogo sem nada."""
        self._filmes: dict[int, Filme] = {}

    def cadastrar_filme(self, filme: Filme) -> None:
        """Adiciona um filme ao catálogo.

        Observação: o contrato só prevê FilmeDuplicadoError aqui. O TypeError
        para algo que não seja Filme é uma proteção extra, que não muda a
        assinatura do método.

        Args:
            filme: filme a ser cadastrado.

        Raises:
            TypeError: se filme não for uma instância de Filme.
            FilmeDuplicadoError: se já existir um filme com o mesmo
                id_filme.
        """
        if not isinstance(filme, Filme):
            raise TypeError("filme deve ser uma instância de Filme.")
        if filme.id_filme in self._filmes:
            raise FilmeDuplicadoError(
                f"Já existe um filme com id {filme.id_filme}.")
        self._filmes[filme.id_filme] = filme

    def buscar_por_id(self, id_filme: int) -> Filme:
        """Retorna o filme com o id informado.

        Args:
            id_filme: identificador do filme.

        Returns:
            O filme correspondente.

        Raises:
            FilmeNaoEncontradoError: se não existir filme com esse id.
        """
        try:
            return self._filmes[id_filme]
        except KeyError:
            raise FilmeNaoEncontradoError(
                f"Filme com id {id_filme} não encontrado.") from None

    def pesquisar_por_titulo(self, termo: str) -> list[Filme]:
        """Busca filmes cujo título contenha o termo.

        A busca ignora maiúsculas/minúsculas e espaços nas pontas do termo.

        Args:
            termo: trecho do título. Ex: "Bad" encontra "Bad Ass".

        Returns:
            Lista de filmes encontrados ou a lista vazia se não houver nenhum.
        """
        termo = termo.strip().lower()
        return [f for f in self._filmes.values()
                if termo in f.titulo.lower()]

    def pesquisar_por_genero(self, genero: str) -> list[Filme]:
        """Busca filmes de um gênero.

        A comparação ignora maiúsculas/minúsculas e espaços nas pontas, mas
        exige o nome completo do gênero (diferente da busca por título).

        Args:
            genero: nome do gênero. Ex: "ficção".

        Returns:
            Lista de filmes do gênero, vazia se não houver nenhum.
        """
        genero = genero.strip().lower()
        return [f for f in self._filmes.values()
                if f.genero.lower() == genero]

    def listar_filmes(self) -> list[Filme]:
        """Lista todos os filmes cadastrados.

        Returns:
            Nova lista com os filmes, na ordem de cadastro. Adicionar ou
            remover itens dessa lista não altera o catálogo, mas os filmes
            dentro dela são os mesmos do catálogo: mudar o título de um
            deles muda o filme cadastrado.
        """
        return list(self._filmes.values())
