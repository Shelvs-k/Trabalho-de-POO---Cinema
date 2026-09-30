class Ingresso:
    def __init__(self, id, p, l, t, q):
        self.id_ingresso = id
        self.preco = p
        self.poltrona = l
        self.tipo = t
        self.quant = q

class Cliente:
    def __init__(self, n, i):
        self.nome = n
        self.idade = i
        self.ingressos = []
        self.validacao = True

class Sessao:
    def __init__(self, id, f, s, d, h, p, a):
        self.id_sessao = id
        self.filme = f
        self.sala = s
        self.data = d
        self.horario = h
        self.preco = p
        self.assentos_ocupados = a

class Sala:
    def __init__(self, n, c, a):
        self.numero = n
        self.capacidade = c
        self.assentos_ocupados = a

class Filme:
    def __init__(self, id, t, d, g, s):
        self.id = id
        self.titulo = t
        self.duracao = d
        self.genero = g
        self.sinopse = s