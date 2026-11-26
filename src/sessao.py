from datetime import datetime
from enum import IntEnum


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

    # ----- atributos -----

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
        # A ocupação desta sessão fica guardada na sala atual; trocar de sala
        # depois de vender faria os ingressos apontarem para assentos perdidos.
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

    # ----- assentos (repassados à Sala, por sessão) -----

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

    # ----- disponibilidade (responsabilidade da Sessão; regra 8) -----

    def quantidade_assentos_disponiveis(self) -> int:
        return self.__sala.quantidade_disponivel(self.__id_sessao)

    def esta_disponivel(self) -> bool:
        """True se a sessão ainda não começou e tem assento livre."""
        return self.__status == StatusSessao.EM_BREVE and self.quantidade_assentos_disponiveis() > 0

    # ----- resumo -----

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

def _converter_enum(classe_enum, valor, nome: str):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"O {nome} deve ser um inteiro ou {classe_enum.__name__}.")
    try:
        return classe_enum(valor)
    except ValueError:
        opcoes = ", ".join(f"{e.value}={e.descricao}" for e in classe_enum)
        raise ValueError(f"{nome} inválido: {valor}. Opções: {opcoes}.") from None


# Nome exato usado no contrato de integração.
Sessão = Sessao
