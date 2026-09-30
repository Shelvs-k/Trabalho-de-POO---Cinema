from math import sin

from classes import Filme, Sala, Sessao, Cliente, Ingresso

class GerenciadorFilmes: #Gerencia tudo relacionado aos filmes do cinema
    def __init__(self):
        self.__filmes = []
    def get_filme_by_id(self, id: int): #Retorna um filme pelo ID, retorna False se não houver o filme na lista
        for filme in self.__filmes:
            if filme.id == id:
                return filme 
        return False
    def adicionar_filme(self, id: int, titulo: str, duracao: str, genero: str, sinopse: str): #Adiciona o filme somente se ele não estiver na lista
        if self.get_filme_by_id(id):
            print("Esse filme já está na lista")
            return
        filme = Filme(id, titulo, duracao, genero, sinopse)
        self.__filmes.append(filme)
    def excluir_filme(self, id: int): #Exclui um filme pelo ID, caso ele esteja na lista
        filme = self.get_filme_by_id(id)
        if not filme:
            print("O filme não está presente na lista")
            return
        self.__filmes.remove(filme)
    def atualizar_filme(self, id: int, n_titulo: str, n_duracao: str, n_genero: str, n_sinopse: str): #Atualiza todos os dados do filme através do ID se ele esttiver na lista
        filme: Filme = self.get_filme_by_id(id)
        if not filme:
            print("O filme não está presente na lista")
            return
        filme.titulo = n_titulo
        filme.duracao = n_duracao
        filme.genero = n_genero
        filme.sinopse = n_sinopse
    def listar_filmes(self): #Lista todos os filmes
        for filme in self.__filmes:
            print(f"ID: {filme.id}\t{filme.titulo}\t{filme.duracao}\t{filme.genero}")

    
class GerenciadorSalas: #Gerencia tudo relacionado a salas
    def __init__(self):
        self.__salas = []
    def get_sala_by_num(self, num: int): #Pega uma sala na lista pelo número, se ela não estiver na lista, retorna False
        for salas in self.__salas:
            if salas.numero == num:
                return salas
        return False
    def adicionar_sala(self, num: int, cap: int, ocup: int = 0): #Adiciona uma sala caso ela não exista na lista
        if self.get_sala_by_num(num):
            print("Essa sala já existe")
            return
        sala = Sala(num, cap, ocup)
        self.__salas.append(sala)
    def excluir_sala(self, num: int): #Exclui uma sala se ela estiver na lista
        sala = self.get_sala_by_num(num)
        if not sala:
            print("Não há essa sala no sistema")
            return
        self.__salas.remove(sala)
    def atualizar_sala(self, num: int, cap: int, ocup: int = 0): #Atuliza uma sala pelo número caso ela exista na lista
        sala: Sala = self.get_sala_by_num(num)
        if not sala:
            print("Não há essa sala no sistema")
            return
        sala.capacidade = cap
        sala.assentos_ocupados = ocup
    def listar_salas(self): #Lista todas as salas
        for salas in self.__salas:
            print(f"Sala {salas.numero}:\t Capacidade: {salas.capacidade}\t Assentos ocupados:{salas.assentos_ocupados}")

class GerenciadorSessoes: #Gerencia tudo relacionado a sessões
    def __init__(self):
        self.__sessoes = []
    def get_sessao_by_id(self, id: int): #Pega uma sala pelo id; se ela não estiver na lista, retorna False
        for sessoes in self.__sessoes:
            if sessoes.id == id:
                return sessoes
        return False
    def criar_sessao(self, id: int, filme: Filme, sala: Sala, data: str, horario: str, preco: float, assentos: int = 0): #Cria uma sessão caso ela não exista na lista
        if self.get_sessao_by_id(id):
            print("Essa sessão já existe")
            return
        sessao = Sessao(id, filme, sala, data, horario, preco, assentos)
        self.__sessoes.append(sessao)
    def remover_sessao(self, id: int): #Remove uma sessão caso ela esteja na lista
        sessao: Sessao = self.get_sessao_by_id(id)
        if not sessao:
            print("Essa sessão não existe")
            return
        self.__sessoes.remove(sessao)
    def atualizar_sessao(self, id: int, filme: Filme, sala: Sala, data: str, horario: str, preco: float, assentos: int = 0): #Atualiza uma sessão pelo id caso esteja na lista
        sessao: Sessao = self.get_sessao_by_id(id)
        if not sessao:
            print("Essa sessão não existe")
            return
        sessao.filme = filme
        sessao.sala = sala
        sessao.data = data
        sessao.horario = horario
        sessao.preco = preco
        sessao.assentos_ocupados = assentos
    def listar_sessoes(self): #Lista todas as sessões
        for sessao in self.__sessoes:
            print(f"""Sessão {sessao.id}:\n 
            Filme:{sessao.filme.titulo}\t 
            Sala:{sessao.sala.numero}\t 
            Data: {sessao.data}\t 
            Horario: {sessao.horario}\t 
            Preco: {sessao.preco}\t
            Assentos: {sessao.assentos_ocupados}""")

class Cinema:
    def __init__(self, n):
        self.__nome = n
        self.__filmes = GerenciadorFilmes()
        self.__salas = GerenciadorSalas()
        self.__sessoes = GerenciadorSessoes()
        self.__clientes = []
    def gerenciar_filmes(self): #chama o gerenciador de filmes e a partir dele realiza as ações
        return self.__filmes
    def gerenciar_salas(self): #chama o gerenciador de salas e a partir dele realiza as ações
        return self.__salas
    def criar_sessao(self): #Cria uma sessãao caso ela não esteja na lista
        return self.__sessoes
    def vender_ingresso(self):
        pass
    def exibir_menu(self):
        pass