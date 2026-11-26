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

        except(ValueError, TypeError):
            print("Erro: classificação indicativa inválida.")
            return False

    def add_ingresso(self, ingresso):
        try:
            teste = ingresso.get_id_ingresso()

            self.__historico_ingresso.append(ingresso)
            print("\nIngresso adicionado com sucesso!")
        except(AttributeError, TypeError):
            print("Erro: O objeto ingresso fornecido é inválido.")

    def ver_historico(self):
        if self.__historico_ingresso:
            print("\n>>>HISTÓRICO DE INGRESSOS<<<\n")
            for ingresso in self.__historico_ingresso:
                print(ingresso.mostrar_dados())
        else:
            print("\nNenhum ingresso comprado, tente novamente depois...")

