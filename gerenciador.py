
# =================== Importações ====================== #

import os

from classes import Filme, Sala, Sessao, Cliente, Ingresso
from pathlib import Path
import json
import re

# ====================================================== #
# ============= AVISO DE CÓDIGO PROVISÓRIO ============= #

def aviso():
    """Exibe um aviso de que o código é provisório."""
    print(
        "\nAVISO: Este código é provisório e não representa o trabalho final da equipe responsável\n"
        "Ele serve apenas para fins de teste do menu principal. Use com cautela e não o considere como versão final do sistema.\n"
    )
    input("Pressione Enter para continuar...")
    
    os.system('cls' if os.name == 'nt' else 'clear')

# ====================================================== #
# ============== GERENCIAMENTO DE ARQUIVOS ============= #

BASE_DIR = Path(__file__).resolve().parent / "dados"

filme_bucket = BASE_DIR / "Filmes"
sala_bucket = BASE_DIR / "Salas"
cliente_bucket = BASE_DIR / "Clientes"
sessao_bucket = BASE_DIR / "Sessoes"
ingresso_bucket = BASE_DIR / "Ingressos"

for bucket in (
    filme_bucket,
    sala_bucket,
    cliente_bucket,
    sessao_bucket,
    ingresso_bucket
):
    bucket.mkdir(parents=True, exist_ok=True)


def listar_arquivos(bucket):
    """Retorna os arquivos JSON que seguem o padrão 'ID - Nome.json'."""
    return sorted(
        (
            arquivo
            for arquivo in bucket.iterdir()
            if arquivo.is_file()
            and arquivo.suffix.lower() == ".json"
            and re.match(r"^\d+ - .+\.json$", arquivo.name)
        ),
        key=lambda arquivo: int(arquivo.name.split(" - ", 1)[0])
    )


def buscar_arquivo(bucket, identificador):
    """Busca um arquivo pelo identificador numérico exato."""
    identificador = str(identificador).strip()

    if not identificador.isdigit():
        return None

    return next(
        (
            arquivo
            for arquivo in listar_arquivos(bucket)
            if arquivo.name.startswith(f"{identificador} - ")
        ),
        None
    )


def proximo_id(bucket):
    """Retorna o menor ID positivo disponível."""
    ids = {
        int(arquivo.name.split(" - ", 1)[0])
        for arquivo in listar_arquivos(bucket)
    }

    identificador = 1
    while identificador in ids:
        identificador += 1

    return identificador


def salvar_json(caminho, dados):
    """Salva um dicionário em JSON sem sobrescrever registros existentes."""
    with caminho.open("x", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def ler_json(caminho):
    """Lê um JSON e informa erros de arquivo ou conteúdo."""
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (OSError, json.JSONDecodeError) as erro:
        print(f"Erro ao ler '{caminho.name}': {erro}")
        return None


def nome_seguro(nome):
    """Remove caracteres que podem causar problemas no nome do arquivo."""
    nome = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", nome.strip())
    nome = nome.rstrip(". ")
    return nome or "Sem título"


def ler_numero(mensagem, tipo, minimo):
    """Lê um número, rejeitando valores inválidos."""
    while True:
        try:
            valor = tipo(input(mensagem).strip())

            if valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue

            return valor

        except ValueError:
            print("Valor inválido. Tente novamente.")


# ====================================================== #
# ================ GERENCIAMENTO DE FILMES ============= #

def list_filmes():
    aviso()
    """Lista os filmes cadastrados."""
    arquivos = listar_arquivos(filme_bucket)

    if not arquivos:
        print("Nenhum filme cadastrado.")
        return

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(f"ID: {dados.get('id', '?')} | "
                  f"Título: {dados.get('titulo', 'Sem título')}")


def add_filme():
    aviso()
    """Cadastra um filme em um arquivo JSON separado."""
    titulo = input("Digite o título do filme: ").strip()

    if not titulo:
        print("O título não pode ficar vazio.")
        return

    duracao = ler_numero(
        "Digite a duração do filme em minutos: ",
        float,
        0.01
    )

    genero = input("Digite o gênero do filme: ").strip()
    sinopse = input("Digite a sinopse do filme: ").strip()

    if not genero or not sinopse:
        print("O gênero e a sinopse não podem ficar vazios.")
        return

    identificador = proximo_id(filme_bucket)

    filme = Filme(identificador, titulo, duracao, genero, sinopse)

    dados = {
        "id": identificador,
        "titulo": titulo,
        "duracao": duracao,
        "genero": genero,
        "sinopse": sinopse
    }

    caminho = (
        filme_bucket
        / f"{identificador} - {nome_seguro(titulo)}.json"
    )

    try:
        salvar_json(caminho, dados)
        print(f"Filme '{filme.titulo}' cadastrado com sucesso. "
              f"ID: {identificador}")

    except OSError as erro:
        print(f"Não foi possível salvar o filme: {erro}")


def aparatar_filmes():
    aviso()
    """Exclui um filme pelo ID."""
    list_filmes()
    identificador = input("Digite o ID do filme que deseja excluir: ").strip()

    caminho = buscar_arquivo(filme_bucket, identificador)

    if caminho is None:
        print(f"Filme com ID {identificador} não encontrado.")
        return

    try:
        caminho.unlink()
        print(f"Filme com ID {identificador} excluído com sucesso.")

    except OSError as erro:
        print(f"Não foi possível excluir o filme: {erro}")


def info_filme():
    aviso()
    """Exibe os detalhes de um filme pelo ID."""
    list_filmes()
    identificador = input(
        "Digite o ID do filme que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(filme_bucket, identificador)

    if caminho is None:
        print(f"Filme com ID {identificador} não encontrado.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    print(f"\nID: {dados.get('id', '?')}")
    print(f"Título: {dados.get('titulo', 'Não informado')}")
    print(f"Duração: {dados.get('duracao', 'Não informada')} minutos")
    print(f"Gênero: {dados.get('genero', 'Não informado')}")
    print(f"Sinopse: {dados.get('sinopse', 'Não informada')}")


# ====================================================== #
# ================ GERENCIAMENTO DE SALAS ============== #

def list_salas():
    aviso()
    """Lista as salas cadastradas."""
    arquivos = listar_arquivos(sala_bucket)

    if not arquivos:
        print("Nenhuma sala cadastrada.")
        return

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(f"Número: {dados.get('numero', '?')} | "
                  f"Capacidade: {dados.get('capacidade', '?')}")


def add_sala():
    aviso()
    """Cadastra uma sala com todos os assentos inicialmente livres."""
    capacidade = ler_numero(
        "Digite a capacidade da sala: ",
        int,
        1
    )

    numero = proximo_id(sala_bucket)

    sala = Sala(numero, capacidade, [False] * capacidade)

    dados = {
        "numero": sala.numero,
        "capacidade": sala.capacidade,
        "assentos_ocupados": sala.assentos_ocupados
    }

    caminho = sala_bucket / f"{numero} - Sala.json"

    try:
        salvar_json(caminho, dados)
        print(f"Sala {numero} cadastrada com sucesso.")

    except OSError as erro:
        print(f"Não foi possível salvar a sala: {erro}")


def aparatar_salas():
    """Exclui uma sala pelo número."""
    aviso()
    list_salas()
    numero = input("Digite o número da sala que deseja excluir: ").strip()

    caminho = buscar_arquivo(sala_bucket, numero)

    if caminho is None:
        print(f"Sala de número {numero} não encontrada.")
        return

    try:
        caminho.unlink()
        print(f"Sala {numero} excluída com sucesso.")

    except OSError as erro:
        print(f"Não foi possível excluir a sala: {erro}")


def info_sala():
    """Exibe os detalhes de uma sala pelo número."""
    aviso()
    list_salas()
    numero = input(
        "Digite o número da sala que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(sala_bucket, numero)

    if caminho is None:
        print(f"Sala de número {numero} não encontrada.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    print(f"\nNúmero: {dados.get('numero', '?')}")
    print(f"Capacidade: {dados.get('capacidade', '?')}")
    print(f"Assentos ocupados: {dados.get('assentos_ocupados', [])}")

# ====================================================== #
# ============== GERENCIAMENTO DE SESSÕES ============== #

def list_sessoes():
    """Lista as sessões cadastradas."""
    aviso()
    arquivos = listar_arquivos(sessao_bucket)

    if not arquivos:
        print("Nenhuma sessão cadastrada.")
        return

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(
                f"ID: {dados.get('id_sessao', '?')} | "
                f"Filme: {dados.get('filme_id', '?')} | "
                f"Sala: {dados.get('sala_numero', '?')} | "
                f"Data: {dados.get('data', '?')} | "
                f"Horário: {dados.get('horario', '?')}"
            )


def add_sessao():
    """Cadastra uma sessão vinculada a um filme e a uma sala."""
    aviso()
    list_filmes()
    filme_id = input("Digite o ID do filme: ").strip()
    caminho_filme = buscar_arquivo(filme_bucket, filme_id)

    if caminho_filme is None:
        print(f"Filme com ID {filme_id} não encontrado.")
        return

    filme = ler_json(caminho_filme)

    if filme is None:
        return

    list_salas()
    sala_numero = input("Digite o número da sala: ").strip()
    caminho_sala = buscar_arquivo(sala_bucket, sala_numero)

    if caminho_sala is None:
        print(f"Sala de número {sala_numero} não encontrada.")
        return

    sala = ler_json(caminho_sala)

    if sala is None:
        return

    data = input("Digite a data da sessão: ").strip()
    horario = input("Digite o horário da sessão: ").strip()
    preco = ler_numero("Digite o preço do ingresso: ", float, 0.01)

    if not data or not horario:
        print("A data e o horário não podem ficar vazios.")
        return

    identificador = proximo_id(sessao_bucket)

    sessao = Sessao(
        identificador,
        filme_id,
        sala_numero,
        data,
        horario,
        preco,
        [False] * sala["capacidade"]
    )

    dados = {
        "id_sessao": sessao.id_sessao,
        "filme_id": filme["id"],
        "sala_numero": sala["numero"],
        "data": sessao.data,
        "horario": sessao.horario,
        "preco": sessao.preco,
        "assentos_ocupados": sessao.assentos_ocupados
    }

    caminho = sessao_bucket / f"{identificador} - Sessao.json"

    try:
        salvar_json(caminho, dados)
        print(f"Sessão {identificador} cadastrada com sucesso.")

    except OSError as erro:
        print(f"Não foi possível salvar a sessão: {erro}")


def info_sessao():
    """Exibe os detalhes de uma sessão pelo ID."""
    aviso()
    list_sessoes()
    identificador = input(
        "Digite o ID da sessão que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(sessao_bucket, identificador)

    if caminho is None:
        print(f"Sessão com ID {identificador} não encontrada.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    caminho_filme = buscar_arquivo(filme_bucket, dados["filme_id"])
    caminho_sala = buscar_arquivo(sala_bucket, dados["sala_numero"])

    filme = ler_json(caminho_filme) if caminho_filme else None
    sala = ler_json(caminho_sala) if caminho_sala else None

    assentos = dados.get("assentos_ocupados", [])
    ocupados = sum(assento is True for assento in assentos)

    print(f"\nID: {dados.get('id_sessao', '?')}")
    print(
        f"Filme: {filme.get('titulo', 'Não encontrado')}"
        if filme else "Filme: Não encontrado"
    )
    print(
        f"Sala: {sala.get('numero', 'Não encontrada')}"
        if sala else "Sala: Não encontrada"
    )
    print(f"Data: {dados.get('data', 'Não informada')}")
    print(f"Horário: {dados.get('horario', 'Não informado')}")
    print(f"Preço: R$ {dados.get('preco', 0):.2f}")
    print(f"Assentos ocupados: {ocupados}/{len(assentos)}")


def editar_sessao():
    """Edita a data, o horário e o preço de uma sessão."""
    aviso()
    list_sessoes()
    identificador = input(
        "Digite o ID da sessão que deseja editar: "
    ).strip()

    caminho = buscar_arquivo(sessao_bucket, identificador)

    if caminho is None:
        print(f"Sessão com ID {identificador} não encontrada.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    print("Pressione Enter para manter o valor atual.")

    data = input(f"Data [{dados['data']}]: ").strip()
    horario = input(f"Horário [{dados['horario']}]: ").strip()
    preco = input(f"Preço [{dados['preco']}]: ").strip()

    if data:
        dados["data"] = data

    if horario:
        dados["horario"] = horario

    if preco:
        try:
            novo_preco = float(preco)

            if novo_preco <= 0:
                print("O preço deve ser maior que zero.")
                return

            dados["preco"] = novo_preco

        except ValueError:
            print("Preço inválido.")
            return

    try:
        caminho.write_text(
            json.dumps(dados, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )
        print(f"Sessão {identificador} atualizada com sucesso.")

    except OSError as erro:
        print(f"Não foi possível atualizar a sessão: {erro}")


def aparatar_sessoes():
    """Exclui uma sessão pelo ID, desde que não tenha assentos ocupados."""
    aviso()
    list_sessoes()
    identificador = input(
        "Digite o ID da sessão que deseja excluir: "
    ).strip()

    caminho = buscar_arquivo(sessao_bucket, identificador)

    if caminho is None:
        print(f"Sessão com ID {identificador} não encontrada.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    if any(dados.get("assentos_ocupados", [])):
        print("Não é possível excluir uma sessão com assentos ocupados.")
        return

    try:
        caminho.unlink()
        print(f"Sessão {identificador} excluída com sucesso.")

    except OSError as erro:
        print(f"Não foi possível excluir a sessão: {erro}")


# ====================================================== #
# ============== GERENCIAMENTO DE CLIENTES ============== #

def list_clientes():
    """Lista os clientes cadastrados."""
    aviso()
    arquivos = listar_arquivos(cliente_bucket)

    if not arquivos:
        print("Nenhum cliente cadastrado.")
        return

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(
                f"ID: {dados.get('id', '?')} | "
                f"Nome: {dados.get('nome', 'Não informado')} | "
                f"Idade: {dados.get('idade', '?')}"
            )


def add_cliente():
    """Cadastra um cliente."""
    aviso()
    nome = input("Digite o nome do cliente: ").strip()

    if not nome:
        print("O nome não pode ficar vazio.")
        return

    idade = ler_numero("Digite a idade do cliente: ", int, 0)
    identificador = proximo_id(cliente_bucket)

    cliente = Cliente(nome, idade, identificador)

    dados = {
        "id": cliente.id,
        "nome": cliente.nome,
        "idade": cliente.idade,
        "ingressos": [],
        "validacao": cliente.validacao
    }

    caminho = (
        cliente_bucket
        / f"{identificador} - {nome_seguro(nome)}.json"
    )

    try:
        salvar_json(caminho, dados)
        print(
            f"Cliente '{cliente.nome}' cadastrado com sucesso. "
            f"ID: {identificador}"
        )

    except OSError as erro:
        print(f"Não foi possível salvar o cliente: {erro}")


def info_cliente():
    """Exibe os dados de um cliente."""
    aviso()
    list_clientes()

    identificador = input(
        "Digite o ID do cliente que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(cliente_bucket, identificador)

    if caminho is None:
        print(f"Cliente com ID {identificador} não encontrado.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    print(f"\nID: {dados.get('id', '?')}")
    print(f"Nome: {dados.get('nome', 'Não informado')}")
    print(f"Idade: {dados.get('idade', '?')}")
    print(f"Ingressos: {dados.get('ingressos', [])}")


def editar_cliente():
    """Edita o nome e a idade de um cliente."""
    aviso()
    list_clientes()

    identificador = input(
        "Digite o ID do cliente que deseja editar: "
    ).strip()

    caminho = buscar_arquivo(cliente_bucket, identificador)

    if caminho is None:
        print(f"Cliente com ID {identificador} não encontrado.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    nome = input(
        f"Nome [{dados['nome']}]: "
    ).strip()

    idade = input(
        f"Idade [{dados['idade']}]: "
    ).strip()

    if nome:
        dados["nome"] = nome

    if idade:
        try:
            nova_idade = int(idade)

            if nova_idade < 0:
                print("A idade não pode ser negativa.")
                return

            dados["idade"] = nova_idade

        except ValueError:
            print("Idade inválida.")
            return

    novo_caminho = (
        cliente_bucket
        / f"{dados['id']} - {nome_seguro(dados['nome'])}.json"
    )

    try:
        caminho.write_text(
            json.dumps(dados, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )

        if novo_caminho != caminho:
            caminho.rename(novo_caminho)

        print(f"Cliente {identificador} atualizado com sucesso.")

    except OSError as erro:
        print(f"Não foi possível atualizar o cliente: {erro}")


def aparatar_clientes():
    """Exclui um cliente que não possua ingressos ativos."""
    aviso()
    list_clientes()

    identificador = input(
        "Digite o ID do cliente que deseja excluir: "
    ).strip()

    caminho = buscar_arquivo(cliente_bucket, identificador)

    if caminho is None:
        print(f"Cliente com ID {identificador} não encontrado.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    ingressos_cliente = [
        arquivo
        for arquivo in listar_arquivos(ingresso_bucket)
        if (
            (ingresso := ler_json(arquivo)) is not None
            and str(ingresso.get("cliente_id")) == str(dados["id"])
        )
    ]

    if ingressos_cliente:
        print(
            "Não é possível excluir o cliente: "
            "existem ingressos vinculados a ele."
        )
        return

    try:
        caminho.unlink()
        print(f"Cliente {identificador} excluído com sucesso.")

    except OSError as erro:
        print(f"Não foi possível excluir o cliente: {erro}")


# ====================================================== #
# ============== GERENCIAMENTO DE INGRESSOS ============= #

def list_ingressos():
    """Lista os ingressos emitidos."""
    aviso()
    arquivos = listar_arquivos(ingresso_bucket)

    if not arquivos:
        print("Nenhum ingresso emitido.")
        return

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(
                f"ID: {dados.get('id_ingresso', '?')} | "
                f"Cliente: {dados.get('cliente_id', '?')} | "
                f"Sessão: {dados.get('sessao_id', '?')} | "
                f"Poltrona: {dados.get('poltrona', '?')} | "
                f"Preço: R$ {dados.get('preco', 0):.2f}"
            )


def add_ingresso():
    """Emite um ingresso e atualiza a ocupação da sessão."""
    aviso()
    list_clientes()

    cliente_id = input(
        "Digite o ID do cliente: "
    ).strip()

    caminho_cliente = buscar_arquivo(cliente_bucket, cliente_id)

    if caminho_cliente is None:
        print(f"Cliente com ID {cliente_id} não encontrado.")
        return

    cliente = ler_json(caminho_cliente)

    if cliente is None:
        return

    list_sessoes()

    sessao_id = input(
        "Digite o ID da sessão: "
    ).strip()

    caminho_sessao = buscar_arquivo(sessao_bucket, sessao_id)

    if caminho_sessao is None:
        print(f"Sessão com ID {sessao_id} não encontrada.")
        return

    sessao = ler_json(caminho_sessao)

    if sessao is None:
        return

    assentos = sessao.get("assentos_ocupados", [])

    if not assentos or all(assentos):
        print("A sessão está lotada.")
        return

    poltrona = ler_numero(
        f"Digite a poltrona desejada (1 a {len(assentos)}): ",
        int,
        1
    )

    if poltrona > len(assentos):
        print("Poltrona inexistente nessa sessão.")
        return

    indice = poltrona - 1

    if assentos[indice]:
        print("Essa poltrona já está ocupada.")
        return

    ingressos_existentes = listar_arquivos(ingresso_bucket)

    for arquivo in ingressos_existentes:
        ingresso_existente = ler_json(arquivo)

        if ingresso_existente is None:
            continue

        mesma_sessao = (
            str(ingresso_existente.get("sessao_id"))
            == str(sessao["id_sessao"])
        )

        mesma_poltrona = (
            ingresso_existente.get("poltrona") == poltrona
        )

        if mesma_sessao and mesma_poltrona:
            print("Já existe um ingresso para essa poltrona.")
            return

    tipo = input(
        "Tipo do ingresso (inteira/meia): "
    ).strip().lower()

    if tipo not in ("inteira", "meia"):
        print("Tipo inválido. Digite 'inteira' ou 'meia'.")
        return

    preco = float(sessao["preco"])

    if tipo == "meia":
        preco /= 2

    identificador = proximo_id(ingresso_bucket)

    ingresso = Ingresso(
        identificador,
        preco,
        poltrona,
        tipo,
        1,
        cliente["id"],
        sessao["id_sessao"]
    )

    dados_ingresso = {
        "id_ingresso": ingresso.id_ingresso,
        "preco": ingresso.preco,
        "poltrona": ingresso.poltrona,
        "tipo": ingresso.tipo,
        "quant": 1,
        "cliente_id": cliente["id"],
        "sessao_id": sessao["id_sessao"]
    }

    sessao["assentos_ocupados"][indice] = True
    cliente.setdefault("ingressos", []).append(identificador)

    caminho_ingresso = (
        ingresso_bucket / f"{identificador} - Ingresso.json"
    )

    try:
        salvar_json(caminho_ingresso, dados_ingresso)

        caminho_sessao.write_text(
            json.dumps(sessao, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )

        caminho_cliente.write_text(
            json.dumps(cliente, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )

        print(f"Ingresso {identificador} emitido com sucesso.")
        print(f"Cliente: {cliente['nome']}")
        print(f"Sessão: {sessao['id_sessao']}")
        print(f"Poltrona: {poltrona}")
        print(f"Preço: R$ {preco:.2f}")

    except OSError as erro:
        print(f"Não foi possível concluir a emissão: {erro}")


def info_ingresso():
    """Exibe os dados de um ingresso."""
    aviso()
    list_ingressos()

    identificador = input(
        "Digite o ID do ingresso que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(ingresso_bucket, identificador)

    if caminho is None:
        print(f"Ingresso com ID {identificador} não encontrado.")
        return

    dados = ler_json(caminho)

    if dados is None:
        return

    caminho_cliente = buscar_arquivo(
        cliente_bucket,
        dados["cliente_id"]
    )

    caminho_sessao = buscar_arquivo(
        sessao_bucket,
        dados["sessao_id"]
    )

    cliente = ler_json(caminho_cliente) if caminho_cliente else None
    sessao = ler_json(caminho_sessao) if caminho_sessao else None

    print(f"\nID: {dados.get('id_ingresso', '?')}")
    print(
        f"Cliente: {cliente.get('nome', 'Não encontrado')}"
        if cliente else "Cliente: Não encontrado"
    )
    print(
        f"Sessão: {sessao.get('id_sessao', 'Não encontrada')}"
        if sessao else "Sessão: Não encontrada"
    )
    print(f"Poltrona: {dados.get('poltrona', '?')}")
    print(f"Tipo: {dados.get('tipo', '?')}")
    print(f"Quantidade: {dados.get('quant', 1)}")
    print(f"Preço: R$ {dados.get('preco', 0):.2f}")


def aparatar_ingressos():
    """Cancela um ingresso e libera a poltrona da sessão."""
    aviso()
    list_ingressos()

    identificador = input(
        "Digite o ID do ingresso que deseja cancelar: "
    ).strip()

    caminho_ingresso = buscar_arquivo(
        ingresso_bucket,
        identificador
    )

    if caminho_ingresso is None:
        print(f"Ingresso com ID {identificador} não encontrado.")
        return

    ingresso = ler_json(caminho_ingresso)

    if ingresso is None:
        return

    caminho_sessao = buscar_arquivo(
        sessao_bucket,
        ingresso["sessao_id"]
    )

    caminho_cliente = buscar_arquivo(
        cliente_bucket,
        ingresso["cliente_id"]
    )

    sessao = ler_json(caminho_sessao) if caminho_sessao else None
    cliente = ler_json(caminho_cliente) if caminho_cliente else None

    if sessao is None:
        print("A sessão vinculada não foi encontrada.")
        return

    poltrona = ingresso["poltrona"]
    indice = poltrona - 1
    assentos = sessao.get("assentos_ocupados", [])

    if indice < 0 or indice >= len(assentos):
        print("A poltrona registrada no ingresso é inválida.")
        return

    assentos[indice] = False

    if cliente is not None:
        cliente["ingressos"] = [
            ingresso_id
            for ingresso_id in cliente.get("ingressos", [])
            if str(ingresso_id) != str(ingresso["id_ingresso"])
        ]

    try:
        caminho_sessao.write_text(
            json.dumps(sessao, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )

        if cliente is not None:
            caminho_cliente.write_text(
                json.dumps(cliente, ensure_ascii=False, indent=4),
                encoding="utf-8"
            )

        caminho_ingresso.unlink()

        print(f"Ingresso {identificador} cancelado com sucesso.")
        print(f"Poltrona {poltrona} liberada.")

    except OSError as erro:
        print(f"Não foi possível cancelar o ingresso: {erro}")

# ====================================================== #
# ================ PONTO DE ENTRADA ==================== #

if __name__ == "__main__":
    print("Gerenciador de filmes e salas.")
    print("Módulo carregado sem executar cadastros automaticamente.")
    # Chame as funções necessárias aqui ou no menu principal.
