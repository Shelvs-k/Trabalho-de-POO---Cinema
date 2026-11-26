"""Ingressos do sistema de cinema (Grupo 5).

Depende destas classes dos outros grupos:
    Sessao  esta_disponivel, assento_disponivel, ocupar_assento,
            liberar_assento, preco, status, filme, sala, data_hora, id_sessao
    Filme   titulo, classificacao
    Sala    get_numero (via sessao.sala)
    Cliente idade, validar_idade, add_ingresso
"""

from enum import IntEnum

from sessao import StatusSessao


class TipoIngresso(IntEnum):
    INTEIRA = 1
    MEIA = 2

    def __str__(self) -> str:
        return "Inteira" if self is TipoIngresso.INTEIRA else "Meia-entrada"


class IngressoError(ValueError):
    """Regra de negócio violada na venda ou no cancelamento."""


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

    def get_id_ingresso(self) -> int:  # exigido por Cliente.add_ingresso
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

    def mostrar_dados(self) -> str:  # exigido por Cliente.ver_historico
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
