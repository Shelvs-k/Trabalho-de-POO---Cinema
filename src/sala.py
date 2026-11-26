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