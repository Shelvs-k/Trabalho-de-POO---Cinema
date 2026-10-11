from classes import Filme, Sala, Sessao, Cliente, Ingresso

class GerenciadorFilmes: #Gerencia tudo relacionado aos filmes do cinema
    def __init__(self):
        self.__filmes = []
    def get_filme_by_id(self, id: int): #Retorna um filme pelo ID, retorna False se não houver o filme na lista
        for filme in self.__filmes:
            if getattr(filme, "id", None) == id:
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
            if getattr(salas, "numero", None) == num:
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
        for sessao in self.__sessoes:
            if getattr(sessao, "id_sessao", None) == id:
                return sessao
        return False
    def criar_sessao(self, id: int, filme: Filme, sala: Sala, data: str, horario: str, preco: float, assentos: int = 0): #Cria uma sessão caso ela não exista na lista
        if self.get_sessao_by_id(id):
            print("Essa sessão já existe")
            return
        sessao = Sessao(id, filme, sala, data, horario, preco, assentos)
        self.__sessoes.append(sessao)
        return sessao
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
        return sessao
    def listar_sessoes(self): #Lista todas as sessões
        for sessao in self.__sessoes:
            print(f"Sessão {sessao.id_sessao}:\nFilme:{sessao.filme.titulo}\tSala:{sessao.sala.numero}\tData: {sessao.data}\tHorario: {sessao.horario}\tPreco: {sessao.preco}\tAssentos: {sessao.assentos_ocupados}")

class GerenciadorClientes:
    def __init__(self):
        self.__clientes = []
    def get_cliente_by_id(self, id: int):
        for cliente in self.__clientes:
            if getattr(cliente, "id", None) == id:
                return cliente
        return False
    def adicionar_cliente(self, nome: str, idade: int, id: int = None):
        if self.get_cliente_by_nome(nome):
            print("Esse cliente já está cadastrado")
            return
        cliente = Cliente(nome, idade, id)
        self.__clientes.append(cliente)
        return cliente
    def excluir_cliente(self, id: int):
        cliente = self.get_cliente_by_id(id)
        if not cliente:
            print("Cliente não encontrado")
            return
        self.__clientes.remove(cliente)
    def atualizar_cliente(self, id: int, novo_nome: str = None, nova_idade: int = None, novo_id: int = None):
        cliente = self.get_cliente_by_id(id)
        if not cliente:
            print("Cliente não encontrado")
            return
        if novo_nome:
            cliente.nome = novo_nome
        if nova_idade is not None:
            cliente.idade = nova_idade
        if novo_id is not None:
            cliente.id = novo_id
        return cliente
    def listar_clientes(self):
        for cliente in self.__clientes:
            print(f"Cliente: {cliente.nome} | Idade: {cliente.idade} | Ingressos: {len(cliente.ingressos)}")


class GerenciadorIngressos:
    def __init__(self):
        self.__ingressos = []
    def get_ingresso_by_id(self, id: int):
        for ingresso in self.__ingressos:
            if getattr(ingresso, "id_ingresso", None) == id:
                return ingresso
        return False
    def adicionar_ingresso(self, id: int, preco: float, poltrona: int, tipo: str, quant: int = 1, cliente: Cliente = None, sessao: Sessao = None):
        if self.get_ingresso_by_id(id):
            print("Esse ingresso já existe")
            return
        ingresso = Ingresso(id, preco, poltrona, tipo, quant, cliente, sessao)
        self.__ingressos.append(ingresso)
        if cliente is not None and ingresso not in cliente.ingressos:
            cliente.ingressos.append(ingresso)
        return ingresso
    def remover_ingresso(self, id: int):
        ingresso = self.get_ingresso_by_id(id)
        if not ingresso:
            print("Esse ingresso não existe")
            return
        self.__ingressos.remove(ingresso)
        if ingresso.cliente is not None and ingresso in ingresso.cliente.ingressos:
            ingresso.cliente.ingressos.remove(ingresso)
        if ingresso.sessao is not None and ingresso.sessao.assentos_ocupados > 0:
            ingresso.sessao.assentos_ocupados = max(0, ingresso.sessao.assentos_ocupados - ingresso.quant)
    def listar_ingressos(self):
        for ingresso in self.__ingressos:
            cliente = ingresso.cliente.nome if ingresso.cliente else "N/A"
            print(f"ID: {ingresso.id_ingresso} | Cliente: {cliente} | Tipo: {ingresso.tipo} | Poltrona: {ingresso.poltrona} | Quantidade: {ingresso.quant} | Preço: {ingresso.preco}")
    def vender_ingresso(self, cliente: Cliente, sessao: Sessao, tipo: str, quantidade: int = 1, poltrona: int = None, id: int = None):
        if cliente is None or not cliente.validacao:
            print("Cliente inválido")
            return
        if sessao is None:
            print("Sessão inválida")
            return
        if quantidade <= 0:
            print("Quantidade de ingressos inválida")
            return
        capacidade = getattr(sessao.sala, "capacidade", 0)
        if capacidade > 0 and (sessao.assentos_ocupados + quantidade > capacidade):
            print("Não há assentos disponíveis para essa sessão")
            return
        # 5. Descobrir quais poltronas já estão ocupadas
        poltronas_ocupadas = {ingresso.poltrona for ingresso in self.__ingressos if ingresso.sessao is sessao}
        # 6. Escolher as poltronas
        if poltrona is None:
            poltrona = 1
            while any(p in poltronas_ocupadas for p in range(poltrona, poltrona + quantidade)):
                poltrona += 1
        if poltrona <= 0:
            print("Poltrona inválida")
            return
        novas_poltronas = list(range(poltrona, poltrona + quantidade))
        if capacidade > 0 and novas_poltronas[-1] > capacidade:
            print("Poltrona fora da capacidade da sala")
            return
        if any(p in poltronas_ocupadas for p in novas_poltronas):
            print("Uma ou mais poltronas já estão ocupadas")
            return
        # 7. Definir os IDs dos ingressos
        if id is None:
            primeiro_id = (1 if not self.__ingressos else max(ingresso.id_ingresso for ingresso in self.__ingressos) + 1)
        else:
            primeiro_id = id

        novos_ids = range(primeiro_id, primeiro_id + quantidade)
        if any(self.get_ingresso_by_id(novo_id) for novo_id in novos_ids):
            print("Um ou mais IDs de ingresso já existem")
            return
        # 8. Criar um ingresso individual para cada poltrona
        ingressos_criados = []
        for i in range(quantidade):
            ingresso = self.adicionar_ingresso(
                primeiro_id + i,
                sessao.preco,
                novas_poltronas[i],
                tipo,
                1,
                cliente,
                sessao
            )
            if ingresso is None:
                print("Não foi possível cadastrar todos os ingressos")
                return
            ingressos_criados.append(ingresso)
        # 9. Atualizar a ocupação da sessão
        sessao.assentos_ocupados += len(ingressos_criados)
        return ingressos_criados


class Cinema:
    def __init__(self, n):
        self.__nome = n
        self.__filmes = GerenciadorFilmes()
        self.__salas = GerenciadorSalas()
        self.__sessoes = GerenciadorSessoes()
        self.__clientes = GerenciadorClientes()
        self.__ingressos = GerenciadorIngressos()

    def gerenciar_filmes(self): #chama o gerenciador de filmes e a partir dele realiza as ações
        return self.__filmes

    def gerenciar_salas(self): #chama o gerenciador de salas e a partir dele realiza as ações
        return self.__salas

    def gerenciar_sessoes(self): #Cria uma sessão caso ela não esteja na lista
        return self.__sessoes

    def criar_sessao(self):
        return self.__sessoes

    def gerenciar_clientes(self):
        return self.__clientes

    def gerenciar_ingressos(self):
        return self.__ingressos

    def vender_ingresso(self, cliente: Cliente, sessao: Sessao, tipo: str, quantidade: int = 1, poltrona: int = None, id: int = None):
        return self.__ingressos.vender_ingresso(cliente, sessao, tipo, quantidade, poltrona, id)

    def exibir_menu(self):
        pass
