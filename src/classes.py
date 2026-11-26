from enum import Enum, IntEnum
from datetime import datetime


# ================= EXCEÇÕES ================= #

class FilmeDuplicadoError(Exception):
    """Erro ao cadastrar um filme com ID já existente."""


class FilmeNaoEncontradoError(Exception):
    """Erro ao buscar um filme inexistente."""


# ================= CLASSIFICAÇÃO INDICATIVA ================= #

class ClassificacaoIndicativa(Enum):
    """Classificações etárias disponíveis para os filmes."""

    LIVRE = 0
    DEZ_ANOS = 10
    DOZE_ANOS = 12
    CATORZE_ANOS = 14
    DEZESSEIS_ANOS = 16
    DEZOITO_ANOS = 18

    @property
    def idade_minima(self) -> int:
        """Retorna a idade mínima da classificação."""
        return self.value

    @property
    def descricao(self) -> str:
        """Retorna a descrição da classificação."""
        descricoes = {
            "LIVRE": "Livre para todos os públicos",
            "DEZ_ANOS": "Não recomendado para menores de 10 anos",
            "DOZE_ANOS": "Não recomendado para menores de 12 anos",
            "CATORZE_ANOS": "Não recomendado para menores de 14 anos",
            "DEZESSEIS_ANOS": "Não recomendado para menores de 16 anos",
            "DEZOITO_ANOS": "Não recomendado para menores de 18 anos",
        }
        return descricoes[self.name]


# ================= CLASSE FILME ================= #

class Filme:
    """Representa um filme do catálogo do cinema."""

    def __init__(self, id_filme: int, titulo: str, duracao: float,
                 genero: str, sinopse: str,
                 classificacao: ClassificacaoIndicativa) -> None:

        if id_filme <= 0:
            raise ValueError("id_filme deve ser maior que 0.")
        self._id_filme = id_filme

        self.titulo = titulo
        self.duracao = duracao
        self.genero = genero
        self.sinopse = sinopse
        self.classificacao = classificacao

    @property
    def id_filme(self) -> int:
        """Retorna o ID do filme."""
        return self._id_filme

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("O título não pode ser vazio.")
        self._titulo = valor.strip()

    @property
    def duracao(self) -> float:
        return self._duracao

    @duracao.setter
    def duracao(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("A duração deve ser maior que 0.")
        self._duracao = valor

    @property
    def genero(self) -> str:
        return self._genero

    @genero.setter
    def genero(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("O gênero não pode ser vazio.")
        self._genero = valor.strip()

    @property
    def sinopse(self) -> str:
        return self._sinopse

    @sinopse.setter
    def sinopse(self, valor: str) -> None:
        self._sinopse = valor

    @property
    def classificacao(self) -> ClassificacaoIndicativa:
        return self._classificacao

    @classificacao.setter
    def classificacao(self, valor: ClassificacaoIndicativa) -> None:
        if not isinstance(valor, ClassificacaoIndicativa):
            raise TypeError(
                "classificacao deve ser um ClassificacaoIndicativa.")
        self._classificacao = valor

    def permitido_para(self, idade_cliente: int) -> bool:
        """Verifica se o cliente tem idade para assistir ao filme."""
        if idade_cliente < 0:
            raise ValueError("idade_cliente não pode ser negativa.")
        return idade_cliente >= self._classificacao.idade_minima

    def exibir_detalhes(self) -> str:
        """Retorna os dados do filme formatados."""
        return (
            f"[{self._id_filme}] {self._titulo}\n"
            f"Gênero: {self._genero}\n"
            f"Duração: {self._duracao} min\n"
            f"Classificação: {self._classificacao.descricao}\n"
            f"Sinopse: {self._sinopse}"
        )

    def __repr__(self) -> str:
        """Retorna uma representação do filme."""
        return f"Filme(id_filme={self._id_filme}, titulo={self._titulo!r})"


# ================= GERENCIADOR DE FILMES ================= #

class GerenciadorFilmes:
    """Gerencia o catálogo de filmes em memória."""

    def __init__(self) -> None:
        self._filmes: dict[int, Filme] = {}

    def cadastrar_filme(self, filme: Filme) -> None:
        """Adiciona um filme ao catálogo."""
        if not isinstance(filme, Filme):
            raise TypeError("filme deve ser uma instância de Filme.")

        if filme.id_filme in self._filmes:
            raise FilmeDuplicadoError(
                f"Já existe um filme com id {filme.id_filme}.")

        self._filmes[filme.id_filme] = filme

    def buscar_por_id(self, id_filme: int) -> Filme:
        """Busca um filme pelo ID."""
        try:
            return self._filmes[id_filme]
        except KeyError:
            raise FilmeNaoEncontradoError(
                f"Filme com id {id_filme} não encontrado.") from None

    def pesquisar_por_titulo(self, termo: str) -> list[Filme]:
        """Pesquisa filmes pelo título."""
        termo = termo.strip().lower()
        return [
            f for f in self._filmes.values()
            if termo in f.titulo.lower()
        ]

    def pesquisar_por_genero(self, genero: str) -> list[Filme]:
        """Pesquisa filmes pelo gênero."""
        genero = genero.strip().lower()
        return [
            f for f in self._filmes.values()
            if f.genero.lower() == genero
        ]

    def listar_filmes(self) -> list[Filme]:
        """Retorna todos os filmes cadastrados."""
        return list(self._filmes.values())


# ================= CLASSE CLIENTE ================= #

class Cliente:
    def __init__(self, id: int, nome: str, idade: int, email: str):
        self.__id = id
        self.__nome = nome
        self.__idade = idade
        self.__email = email
        self.__historico_ingresso = []

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def idade(self):
        return self.__idade

    @property
    def email(self):
        return self.__email

    def validar_idade(self, classification):
        try:
            idade_minima = classification.value
        except AttributeError:
            idade_minima = classification

        try:
            idade_minima_num = int(idade_minima)
            return self.__idade >= idade_minima_num

        except (ValueError, TypeError):
            print("Erro: classificação indicativa inválida.")
            return False

    def add_ingresso(self, ingresso):
        try:
            teste = ingresso.get_id_ingresso()
            self.__historico_ingresso.append(ingresso)
            print("\nIngresso adicionado com sucesso!")

        except (AttributeError, TypeError):
            print("Erro: O objeto ingresso fornecido é inválido.")

    def ver_historico(self):
        if self.__historico_ingresso:
            print("\n>>>HISTÓRICO DE INGRESSOS<<<\n")
            for ingresso in self.__historico_ingresso:
                print(ingresso.mostrar_dados())
        else:
            print("\nNenhum ingresso comprado, tente novamente depois...")


# ================= CLASSE SALA (MANTIDA) ================= #

class Sala:
    """Representa uma sala de cinema, gerenciando numeração, capacidade e mapa de assentos."""

    def __init__(self, numero: int, capacidade: int) -> None:
        """Inicializa a instância da classe Sala e popula o dicionário de assentos.

        :param numero: Código identificador único da sala.
        :param capacidade: Quantidade total de assentos suportados pela sala.
        :raises ValueError: Caso o número da sala não seja um inteiro maior que zero.
        :raises ValueError: Caso a capacidade informada seja menor ou igual a zero.
        """
        if not isinstance (numero, int) or numero <= 0:
            raise ValueError ("O número da sala deve ser um inteiro maior que zero.")
        
        if capacidade <= 0:
            raise ValueError("A capacidade informada deve ser maior que zero.")

        self.__numero: int = numero
        self.__capacidade: int = capacidade
        self.__assentos_ocupados: dict[int, set[int]] = {}

    def validar_numero_assento(self, numero: int) -> bool:
        """Verifica a validade numérica de um assento na sala.

        :param numero: Número do assento a ser verificado.
        :return: True se 1 <= numero <= capacidade, senão False.
        """
        return numero >= 1 and numero <= self.__capacidade

    def assento_disponivel(self, id_sessao: int, numero: int) -> bool:
        """Consulta se um assento específico está livre.

        :param id_sessao: identificador da sessao.
        :param numero: Número do assento.
        :return: True se livre, False se ocupado ou fora do intervalo da sala.
        """
        if not self.validar_numero_assento(numero):
            return False
        return numero not in self.__assentos_ocupados.get(id_sessao, set())

    def ocupar_assento(self, id_sessao: int, numero: int) -> None:
        """Marca um assento livre como ocupado.

        :param id_sessao: identificador da sessao.
        :param numero: Número do assento a ser ocupado.
        :raises ValueError: Se o assento for inválido ou se já estiver ocupado.
        """
        if not self.validar_numero_assento(numero):
            raise ValueError("O assento informado é inválido.")
        if numero in self.__assentos_ocupados.get(id_sessao, set()):
            raise ValueError("O assento já se encontra ocupado.")
        self.__assentos_ocupados.setdefault(id_sessao, set()).add(numero)

    def liberar_assento(self, id_sessao: int, numero: int) -> None:
        """Marca um assento ocupado como disponível.

        :param id_sessao: identificador da sessao.
        :param numero: Número do assento a ser liberado.
        :raises ValueError: Se o assento for inválido ou se já estiver livre.
        """
        if not self.validar_numero_assento(numero):
            raise ValueError("O assento informado é inválido.")
        if numero not in self.__assentos_ocupados.get(id_sessao, set()):
            raise ValueError("O assento já está livre.")
        self.__assentos_ocupados[id_sessao].remove(numero)

    def quantidade_disponivel(self, id_sessao: int) -> int:
        """Obtém a contagem total de assentos vagos.

        :param id_sessao: Identificador da sessão.
        :return: Quantidade de assentos com valor True.
        """
        return self.__capacidade - len(self.__assentos_ocupados.get(id_sessao, set()))

    def quantidade_ocupada(self, id_sessao: int) -> int:
        """Obtém a contagem total de assentos ocupados.

        :param id_sessao: Identificador da sessão.
        :return: Quantidade de assentos com valor False.
        """
        return len(self.__assentos_ocupados.get(id_sessao, set()))

    def get_numero(self) -> int:
        """Retorna o identificador da sala.

        :return: Número identificador da sala.
        """
        return self.__numero

    def get_capacidade(self) -> int:
        """Retorna a capacidade total da sala.

        :return: Capacidade total de assentos da sala.
        """
        return self.__capacidade


# ================= TIPO E STATUS DE SESSÃO ================= #

class TipoSessao(IntEnum):
    """Tipo de exibição. Aceita o membro do enum ou o int correspondente."""

    TRES_D = 1
    DOIS_D = 2
    ASSISTIVA = 3

    @property
    def descricao(self) -> str:
        return {
            TipoSessao.TRES_D: "3D",
            TipoSessao.DOIS_D: "2D",
            TipoSessao.ASSISTIVA: "Assistiva",
        }[self]

    def __str__(self) -> str:
        return self.descricao


class StatusSessao(IntEnum):
    """Status da exibição. Aceita o membro do enum ou o int correspondente."""

    EM_BREVE = 1
    EM_PROGRESSO = 2
    CONCLUIDA = 3

    @property
    def descricao(self) -> str:
        return {
            StatusSessao.EM_BREVE: "Em Breve",
            StatusSessao.EM_PROGRESSO: "Em Progresso",
            StatusSessao.CONCLUIDA: "Concluída",
        }[self]

    def __str__(self) -> str:
        return self.descricao


def _converter_enum(classe_enum, valor, nome: str):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"O {nome} deve ser um inteiro ou {classe_enum.__name__}.")
    try:
        return classe_enum(valor)
    except ValueError:
        opcoes = ", ".join(f"{e.value}={e.descricao}" for e in classe_enum)
        raise ValueError(f"{nome} inválido: {valor}. Opções: {opcoes}.") from None


# ================= CLASSE SESSÃO (NOVA) ================= #

class Sessao:
    """Exibição de um filme em uma sala, com data/horário, tipo, preço e status."""

    _proximo_id = 1

    def __init__(self, filme, sala, data_hora: datetime, tipo: int, preco: float,
                 status: int = StatusSessao.EM_BREVE):
        self.__sala = None
        self.filme = filme
        self.sala = sala
        self.data_hora = data_hora
        self.tipo = tipo
        self.preco = preco
        self.status = status

        # O id só é consumido depois que todos os argumentos foram validados.
        self.__id_sessao = Sessao._proximo_id
        Sessao._proximo_id += 1

    @property
    def id_sessao(self) -> int:
        """Identificador único, gerado automaticamente. Somente leitura."""
        return self.__id_sessao

    @property
    def filme(self):
        return self.__filme

    @filme.setter
    def filme(self, filme) -> None:
        if filme is None:
            raise ValueError("A sessão precisa de um filme.")
        self.__filme = filme

    @property
    def sala(self):
        return self.__sala

    @sala.setter
    def sala(self, sala) -> None:
        if sala is None:
            raise ValueError("A sessão precisa de uma sala.")
        atual = self.__sala
        if atual is not None and atual.quantidade_disponivel(self.__id_sessao) < atual.get_capacidade():
            raise ValueError("Não é possível trocar a sala de uma sessão com ingressos vendidos.")
        self.__sala = sala

    @property
    def data_hora(self) -> datetime:
        return self.__data_hora

    @data_hora.setter
    def data_hora(self, data_hora: datetime) -> None:
        if not isinstance(data_hora, datetime):
            raise TypeError("A data/horário deve ser um datetime.")
        self.__data_hora = data_hora

    @property
    def tipo(self) -> TipoSessao:
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: int) -> None:
        self.__tipo = _converter_enum(TipoSessao, tipo, "tipo")

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, preco: float) -> None:
        if isinstance(preco, bool) or not isinstance(preco, (int, float)):
            raise TypeError("O preço deve ser um número.")
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        self.__preco = float(preco)

    @property
    def status(self) -> StatusSessao:
        return self.__status

    @status.setter
    def status(self, status: int) -> None:
        self.__status = _converter_enum(StatusSessao, status, "status")

    def assento_disponivel(self, numero: int) -> bool:
        return self.__sala.assento_disponivel(self.__id_sessao, numero)

    def ocupar_assento(self, numero: int) -> None:
        """Ocupa o assento nesta sessão. Usado na venda do ingresso."""
        if self.__status != StatusSessao.EM_BREVE:
            raise ValueError(f"Não é possível vender para uma sessão com status '{self.__status}'.")
        self.__sala.ocupar_assento(self.__id_sessao, numero)

    def liberar_assento(self, numero: int) -> None:
        """Libera o assento nesta sessão. Usado no cancelamento do ingresso."""
        self.__sala.liberar_assento(self.__id_sessao, numero)

    def quantidade_assentos_disponiveis(self) -> int:
        return self.__sala.quantidade_disponivel(self.__id_sessao)

    def esta_disponivel(self) -> bool:
        """True se a sessão ainda não começou e tem assento livre."""
        return self.__status == StatusSessao.EM_BREVE and self.quantidade_assentos_disponiveis() > 0

    def resumo(self) -> str:
        preco = f"{self.__preco:.2f}".replace(".", ",")
        return (
            f"Sessão #{self.__id_sessao}\n"
            f"Filme: {self.__filme.titulo}\n"
            f"Sala: {self.__sala.get_numero()}\n"
            f"Data: {self.__data_hora:%d/%m/%Y %H:%M}\n"
            f"Tipo: {self.__tipo}\n"
            f"Preço: R$ {preco}\n"
            f"Status: {self.__status}\n"
            f"Assentos disponíveis: {self.quantidade_assentos_disponiveis()} "
            f"de {self.__sala.get_capacidade()}"
        )

    def __str__(self) -> str:
        return self.resumo()

    def __repr__(self) -> str:
        return (
            f"Sessao(id_sessao={self.__id_sessao}, data_hora={self.__data_hora:%d/%m/%Y %H:%M}, "
            f"tipo={self.__tipo}, preco={self.__preco:.2f}, status={self.__status})"
        )


# Nome exato usado no contrato de integração.
Sessão = Sessao


# ================= TIPO DE INGRESSO ================= #

class TipoIngresso(IntEnum):
    INTEIRA = 1
    MEIA = 2

    def __str__(self) -> str:
        return "Inteira" if self is TipoIngresso.INTEIRA else "Meia-entrada"


class IngressoError(ValueError):
    """Regra de negócio violada na venda ou no cancelamento."""


# ================= CLASSE INGRESSO (NOVA) ================= #

class Ingresso:
    """Criar o objeto efetua a venda."""

    FATOR_MEIA = 0.5  # regra 5
    _proximo_id = 1

    def __init__(self, sessao, cliente, numero_assento: int,
                 tipo: int = TipoIngresso.INTEIRA):
        tipo = TipoIngresso(tipo)
        if not sessao.esta_disponivel():
            raise IngressoError(f"Sessão #{sessao.id_sessao} indisponível "
                                f"(status '{sessao.status}' ou lotada).")
        if not sessao.assento_disponivel(numero_assento):
            raise IngressoError(f"Assento {numero_assento} inexistente ou "
                                f"já ocupado na sessão #{sessao.id_sessao}.")
        if not cliente.validar_idade(sessao.filme.classificacao):
            raise IngressoError(f"Cliente com {cliente.idade} anos não pode "
                                f"assistir: {sessao.filme.classificacao.descricao}.")

        self.__sessao, self.__cliente = sessao, cliente
        self.__assento, self.__tipo = numero_assento, tipo
        self.__valor = round(sessao.preco * (self.FATOR_MEIA if tipo is TipoIngresso.MEIA else 1), 2)
        self.__cancelado = False

        sessao.ocupar_assento(numero_assento)
        self.__id = Ingresso._proximo_id
        Ingresso._proximo_id += 1
        cliente.add_ingresso(self)

    @property
    def id_ingresso(self) -> int: return self.__id
    @property
    def sessao(self): return self.__sessao
    @property
    def cliente(self): return self.__cliente
    @property
    def numero_assento(self) -> int: return self.__assento
    @property
    def tipo(self) -> TipoIngresso: return self.__tipo
    @property
    def valor(self) -> float: return self.__valor

    def get_id_ingresso(self) -> int:
        return self.__id

    def esta_ativo(self) -> bool:
        return not self.__cancelado

    def cancelar(self) -> None:
        """Cancela e libera o assento (regra 6)."""
        if self.__cancelado:
            raise IngressoError("Este ingresso já foi cancelado.")
        if self.__sessao.status != StatusSessao.EM_BREVE:
            raise IngressoError(f"Não é possível cancelar: sessão '{self.__sessao.status}'.")
        self.__sessao.liberar_assento(self.__assento)
        self.__cancelado = True

    def mostrar_dados(self) -> str:
        s = self.__sessao
        valor = f"{self.__valor:.2f}".replace(".", ",")
        situacao = "Ativo" if self.esta_ativo() else "Cancelado"
        return (f"Ingresso #{self.__id} | {s.filme.titulo} | "
                f"{s.data_hora:%d/%m/%Y %H:%M} | Sala {s.sala.get_numero()} | "
                f"Assento {self.__assento} | {self.__tipo} | R$ {valor} | {situacao}")

    __str__ = mostrar_dados


class GerenciadorIngressos:
    """Guarda os ingressos vendidos."""

    def __init__(self) -> None:
        self._ingressos: dict[int, Ingresso] = {}

    def vender(self, sessao, cliente, numero_assento, tipo=TipoIngresso.INTEIRA) -> Ingresso:
        ingresso = Ingresso(sessao, cliente, numero_assento, tipo)
        self._ingressos[ingresso.id_ingresso] = ingresso
        return ingresso

    def cancelar(self, id_ingresso: int) -> None:
        if id_ingresso not in self._ingressos:
            raise IngressoError(f"Ingresso {id_ingresso} não encontrado.")
        self._ingressos[id_ingresso].cancelar()

    def listar_por_cliente(self, cliente) -> list[Ingresso]:
        return [i for i in self._ingressos.values() if i.cliente is cliente]