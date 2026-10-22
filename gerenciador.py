
# =================== Importações ====================== #

import os
from unittest import registerResult

from numpy import quantile

from classes import Filme, Sala, Sessao, Cliente, Ingresso
from pathlib import Path
import json
import re
import debug

def registrar_log(nivel, mensagem):
    """Registra um evento somente quando o modo debug está ativo."""
    if not debug.log_ativo:
        return

    metodo = getattr(debug.logger, nivel)
    metodo(mensagem, stacklevel=2)

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
    registrar_log("debug", f"Listando arquivos em: {bucket}")
    try:
        arquivos = sorted(
            (
                arquivo
                for arquivo in bucket.iterdir()
                if arquivo.is_file()
                and arquivo.suffix.lower() == ".json"
                and re.match(r"^\d+ - .+\.json$", arquivo.name)
            ),
            key=lambda arquivo: int(arquivo.name.split(" - ", 1)[0])
        )
    except OSError:
        registrar_log(
            "exception",
            f"Falha ao listar arquivos da pasta: {bucket}"
        )
        raise
    registrar_log(
        "debug",
        f"Arquivos JSON válidos encontrados em {bucket}: {len(arquivos)}."
    )
    return arquivos



def buscar_arquivo(bucket, identificador):
    """Busca um arquivo pelo identificador numérico exato."""
    identificador = str(identificador).strip()
    registrar_log(
        "debug",
        f"Buscando ID '{identificador}' na pasta {bucket}."
    )

    if not identificador.isdigit():
        registrar_log(
            "debug",
            f"Busca cancelada: ID não numérico ('{identificador}')."
        )
        return None

    arquivo_encontrado = next(
        (
            arquivo
            for arquivo in listar_arquivos(bucket)
            if arquivo.name.startswith(f"{identificador} - ")
        ),
        None
    )

    if arquivo_encontrado is not None:
        registrar_log(
            "debug",
            f"Arquivo encontrado para o ID {identificador}: "
            f"{arquivo_encontrado.name}"
        )
    else:
        registrar_log(
            "debug",
            f"Nenhum arquivo encontrado para o ID {identificador}."
        )

    return arquivo_encontrado


def proximo_id(bucket):
    """Retorna o menor ID positivo disponível."""
    registrar_log("debug", f"Calculando próximo ID disponível em {bucket}.")
    ids = {
        int(arquivo.name.split(" - ", 1)[0])
        for arquivo in listar_arquivos(bucket)
    }

    identificador = 1
    while identificador in ids:
        identificador += 1

    registrar_log(
        "debug",
        f"Próximo ID disponível em {bucket}: {identificador}."
    )
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
    registrar_log("debug", f"Arquivo JSON criado: {caminho.name}")


def ler_json(caminho):
    """Lê um JSON e informa erros de arquivo ou conteúdo."""
    registrar_log("debug", f"Lendo arquivo JSON: {caminho.name}")
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        registrar_log("debug", f"Arquivo JSON lido com sucesso: {caminho.name}")
        return dados

    except (OSError, json.JSONDecodeError) as erro:
        print(f"Erro ao ler '{caminho.name}': {erro}")
        registrar_log(
            "exception",
            f"Falha ao ler arquivo JSON: {caminho.name}"
        )
        return None



def nome_seguro(nome):
    """Remove caracteres que podem causar problemas no nome do arquivo."""
    nome_original = nome
    nome = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", nome.strip())
    nome = nome.rstrip(". ")
    nome = nome or "Sem título"
    if nome != nome_original:
        registrar_log(
            "debug",
            f"Nome de arquivo adaptado: '{nome_original}' -> '{nome}'."
        )
    return nome



def ler_numero(mensagem, tipo, minimo):
    """Lê um número, rejeitando valores inválidos."""
    while True:
        try:
            valor = tipo(input(mensagem).strip())

            if valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                registrar_log(
                    "warning",
                    f"Valor abaixo do mínimo permitido ({minimo}) na leitura numérica."
                )
                continue

            return valor

        except ValueError:
            print("Valor inválido. Tente novamente.")
            registrar_log(
                "warning",
                "Entrada numérica inválida: conversão para o tipo solicitado falhou."
            )


# ====================================================== #
# ================ GERENCIAMENTO DE FILMES ============= #

def list_filmes():
    aviso()
    """Lista os filmes cadastrados."""
    registrar_log("debug", "Iniciando listagem de filmes.")
    arquivos = listar_arquivos(filme_bucket)

    if not arquivos:
        print("Nenhum filme cadastrado.")
        registrar_log("warning", "Tentativa de listar filmes sem nenhum cadastro.")
        return

    quantidade = 0

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(f"ID: {dados.get('id', '?')} | "
                  f"Título: {dados.get('titulo', 'Sem título')}")
            quantidade += 1

    registrar_log(
    "info",
    f"Listagem de filmes concluída. Registros exibidos: {quantidade}."
    )



def add_filme():
    aviso()
    """Cadastra um filme em um arquivo JSON separado."""
    registrar_log("debug", "Iniciando cadastro de filme.")
    titulo = input("Digite o título do filme: ").strip()

    if not titulo:
        print("O título não pode ficar vazio.")
        registrar_log("warning", "Cadastro de filme cancelado: título vazio.")
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
        registrar_log(
            "warning",
            "Cadastro de filme cancelado: gênero ou sinopse vazios."
        )
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

        registrar_log(
            "info",
            f"Filme cadastrado com sucesso: ID {identificador}, título '{titulo}'."
        )
    except OSError as erro:
        print(f"Não foi possível salvar o filme: {erro}")
        registrar_log(
            "exception",
            f"Falha ao salvar filme: ID {identificador}, título '{titulo}'."
        )



def aparatar_filmes():
    """Exclui um filme pelo ID."""
    registrar_log("debug", "Iniciando exclusão de filme.")
    list_filmes()
    identificador = input("Digite o ID do filme que deseja excluir: ").strip()

    caminho = buscar_arquivo(filme_bucket, identificador)

    if caminho is None:
        print(f"Filme com ID {identificador} não encontrado.")
        registrar_log(
            "warning",
            f"Tentativa de excluir filme inexistente. ID informado: '{identificador}'."
        )
        return

    try:
        caminho.unlink()
        print(f"Filme com ID {identificador} excluído com sucesso.")

        registrar_log(
            "info",
            f"Filme excluído com sucesso: ID {identificador}."
        )
    except OSError as erro:
        print(f"Não foi possível excluir o filme: {erro}")
        registrar_log(
            "exception",
            f"Falha ao excluir filme: ID {identificador}."
        )



def info_filme():
    """Exibe os detalhes de um filme pelo ID."""
    registrar_log("debug", "Iniciando consulta de detalhes de filme.")
    list_filmes()
    identificador = input(
        "Digite o ID do filme que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(filme_bucket, identificador)

    if caminho is None:
        print(f"Filme com ID {identificador} não encontrado.")
        registrar_log(
            "warning",
            f"Consulta de filme inexistente. ID informado: '{identificador}'."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Não foi possível exibir os detalhes do filme de ID {identificador}."
        )
        return

    print(f"\nID: {dados.get('id', '?')}")
    print(f"Título: {dados.get('titulo', 'Não informado')}")
    print(f"Duração: {dados.get('duracao', 'Não informada')} minutos")
    print(f"Gênero: {dados.get('genero', 'Não informado')}")
    print(f"Sinopse: {dados.get('sinopse', 'Não informada')}")

    registrar_log(
        "info",
        f"Detalhes do filme consultados com sucesso: ID {identificador}."
    )

# ====================================================== #
# ================ GERENCIAMENTO DE SALAS ============== #

def list_salas():
    aviso()
    """Lista as salas cadastradas."""
    registrar_log("debug", "Iniciando listagem de salas.")
    arquivos = listar_arquivos(sala_bucket)

    if not arquivos:
        print("Nenhuma sala cadastrada.")
        registrar_log("warning", "Tentativa de listar salas sem nenhum cadastro.")
        return

    quantidade = 0

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(f"Número: {dados.get('numero', '?')} | "
                  f"Capacidade: {dados.get('capacidade', '?')}")
            quantidade += 1

    registrar_log(
        "info",
        f"Listagem de salas concluída. Registros exibidos: {quantidade}."
    )


def add_sala():
    aviso()
    """Cadastra uma sala com todos os assentos inicialmente livres."""
    registrar_log("debug", "Iniciando cadastro de sala.")
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
        registrar_log(
        "info",
        f"Sala cadastrada com sucesso: Número {numero}, capacidade: {capacidade}"
        )
        print(f"Sala {numero} cadastrada com sucesso.")

    except OSError as erro:
        print(f"Não foi possível salvar a sala: {erro}")
        registrar_log(
            "exception",
            f"Falha ao salvar sala: Número {numero}, capacidade: {capacidade}"
        )


def aparatar_salas():
    """Exclui uma sala pelo número."""
    registrar_log("debug", "Iniciando exclusão de sala.")
    list_salas()
    numero = input("Digite o número da sala que deseja excluir: ").strip()

    caminho = buscar_arquivo(sala_bucket, numero)

    if caminho is None:
        print(f"Sala de número {numero} não encontrada.")
        registrar_log(
        "warning",
        f"Tentativa de excluir sala inexistente. Número informado: '{numero}'."
        )
        return

    try:
        caminho.unlink()
        print(f"Sala {numero} excluída com sucesso.")
        registrar_log(
            "info",
            f"Sala excluída com sucesso: Número {numero}"
        )
    except OSError as erro:
        print(f"Não foi possível excluir a sala: {erro}")
        registrar_log(
        "exception",
        f"Falha ao excluir sala: Número {numero}"
        )


def info_sala():
    """Exibe os detalhes de uma sala pelo número."""
    registrar_log("debug", "Iniciando consulta de detalhes de salas.")
    list_salas()
    numero = input(
        "Digite o número da sala que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(sala_bucket, numero)

    if caminho is None:
        print(f"Sala de número {numero} não encontrada.")
        registrar_log(
            "warning",
            f"Consulta de sala inexistente. Número informado: '{numero}'."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Não foi possível exibir os detalhes da sala de número {numero}."
        )
        return

    print(f"\nNúmero: {dados.get('numero', '?')}")
    print(f"Capacidade: {dados.get('capacidade', '?')}")
    print(f"Assentos ocupados: {dados.get('assentos_ocupados', [])}")

    registrar_log(
        "info",
        f"Detalhes da sala consultados com sucesso: Número {numero}."
    )

# ====================================================== #
# ============== GERENCIAMENTO DE SESSÕES ============== #

def list_sessoes():
    """Lista as sessões cadastradas."""
    aviso()
    registrar_log(
        "debug",
        "Iniciando listagem de sessões."
    )
    arquivos = listar_arquivos(sessao_bucket)

    if not arquivos:
        print("Nenhuma sessão cadastrada.")
        registrar_log(
        "warning",
        "Tentativa de listar sessões sem nenhum cadastro."
        )
        return

    quantidade = 0

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
            quantidade += 1
    registrar_log(
    "info",
    f"Listagem de sessões concluída. Registros exibidos: {quantidade}."
    )


def add_sessao():
    """Cadastra uma sessão vinculada a um filme e a uma sala."""
    registrar_log("debug", "Iniciando cadastro de sessão.")
    list_filmes()
    filme_id = input("Digite o ID do filme: ").strip()
    caminho_filme = buscar_arquivo(filme_bucket, filme_id)

    if caminho_filme is None:
        print(f"Filme com ID {filme_id} não encontrado.")
        registrar_log(
            "warning",
            f"Cadastro de sessão cancelado: filme ID {filme_id} não encontrado."
        )
        return

    filme = ler_json(caminho_filme)

    if filme is None:
        registrar_log(
        "error",
        f"Cadastro de sessão cancelado: não foi possível ler o filme ID {filme_id}."
        )
        return

    list_salas()
    sala_numero = input("Digite o número da sala: ").strip()
    caminho_sala = buscar_arquivo(sala_bucket, sala_numero)

    if caminho_sala is None:
        print(f"Sala de número {sala_numero} não encontrada.")
        registrar_log(
        "warning",
        f"Cadastro de sessão cancelado: sala número {sala_numero} não encontrada."
        )
        return

    sala = ler_json(caminho_sala)

    if sala is None:
        registrar_log(
        "error",
        f"Cadastro de sessão cancelado: não foi possível ler a sala ID {sala_numero}."
        )
        return

    data = input("Digite a data da sessão: ").strip()
    horario = input("Digite o horário da sessão: ").strip()
    preco = ler_numero("Digite o preço do ingresso: ", float, 0.01)

    if not data or not horario:
        print("A data e o horário não podem ficar vazios.")
        registrar_log(
        "warning",
        f"Cadastro de sessão cancelado: a data e o horário não podem ficar vazios."
        )
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
        registrar_log(
        "info",
        f"Sessão {identificador} cadastrada com sucesso."
        )

    except OSError as erro:
        print(f"Não foi possível salvar a sessão: {erro}")
        registrar_log(
        "exception",
        f"Falha ao salvar sessão: ID {identificador}."
        )


def info_sessao():
    """Exibe os detalhes de uma sessão pelo ID."""
    registrar_log("debug", "Iniciando consulta de detalhes de sessão.")
    list_sessoes()
    identificador = input(
        "Digite o ID da sessão que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(sessao_bucket, identificador)

    if caminho is None:
        print(f"Sessão com ID {identificador} não encontrada.")
        registrar_log(
            "warning",
            f"Consulta de sessão inexistente. ID informado: '{identificador}'."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Não foi possível exibir os detalhes da sessão de ID {identificador}."
        )
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
    registrar_log(
        "info",
        f"Detalhes da sessão consultados com sucesso: ID {identificador}."
    )


def editar_sessao():
    """Edita a data, o horário e o preço de uma sessão."""
    registrar_log("debug", "Iniciando edição de sessão.")
    list_sessoes()
    identificador = input(
        "Digite o ID da sessão que deseja editar: "
    ).strip()

    caminho = buscar_arquivo(sessao_bucket, identificador)

    if caminho is None:
        print(f"Sessão com ID {identificador} não encontrada.")
        registrar_log(
            "warning",
            f"Edição de sessão cancelada: ID {identificador} não encontrado."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Edição de sessão cancelada: não foi possível ler o ID {identificador}."
        )
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
                registrar_log(
                    "warning",
                    f"Edição de sessão cancelada: preço inválido para ID {identificador}."
                )
                return

            dados["preco"] = novo_preco

        except ValueError:
            print("Preço inválido.")
            registrar_log(
                "warning",
                f"Edição de sessão cancelada: preço inválido para ID {identificador}."
            )
            return

    try:
        caminho.write_text(
            json.dumps(dados, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )
        print(f"Sessão {identificador} atualizada com sucesso.")
        registrar_log(
            "info",
            f"Sessão atualizada com sucesso: ID {identificador}."
        )

    except OSError as erro:
        print(f"Não foi possível atualizar a sessão: {erro}")
        registrar_log(
            "exception",
            f"Falha ao atualizar sessão: ID {identificador}."
        )


def aparatar_sessoes():
    """Exclui uma sessão pelo ID, desde que não tenha assentos ocupados."""
    registrar_log("debug", "Iniciando exclusão de sessão.")
    list_sessoes()
    identificador = input(
        "Digite o ID da sessão que deseja excluir: "
    ).strip()

    caminho = buscar_arquivo(sessao_bucket, identificador)

    if caminho is None:
        print(f"Sessão com ID {identificador} não encontrada.")
        registrar_log(
            "warning",
            f"Tentativa de excluir sessão inexistente. ID informado: '{identificador}'."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Exclusão de sessão cancelada: não foi possível ler o ID {identificador}."
        )
        return

    if any(dados.get("assentos_ocupados", [])):
        print("Não é possível excluir uma sessão com assentos ocupados.")
        registrar_log(
            "warning",
            f"Exclusão de sessão cancelada: existem assentos ocupados no ID {identificador}."
        )
        return

    try:
        caminho.unlink()
        print(f"Sessão {identificador} excluída com sucesso.")
        registrar_log(
            "info",
            f"Sessão excluída com sucesso: ID {identificador}."
        )

    except OSError as erro:
        print(f"Não foi possível excluir a sessão: {erro}")
        registrar_log(
            "exception",
            f"Falha ao excluir sessão: ID {identificador}."
        )


# ====================================================== #
# ============== GERENCIAMENTO DE CLIENTES ============== #

def list_clientes():
    """Lista os clientes cadastrados."""
    aviso()
    registrar_log("debug", "Iniciando listagem de clientes.")
    arquivos = listar_arquivos(cliente_bucket)

    if not arquivos:
        print("Nenhum cliente cadastrado.")
        registrar_log(
            "warning",
            "Tentativa de listar clientes sem nenhum cadastro."
        )
        return

    quantidade = 0
    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is not None:
            print(
                f"ID: {dados.get('id', '?')} | "
                f"Nome: {dados.get('nome', 'Não informado')} | "
                f"Idade: {dados.get('idade', '?')}"
            )
            quantidade += 1

    registrar_log(
        "info",
        f"Listagem de clientes concluída. Registros exibidos: {quantidade}."
    )


def add_cliente():
    """Cadastra um cliente."""
    aviso()
    registrar_log("debug", "Iniciando cadastro de cliente.")
    nome = input("Digite o nome do cliente: ").strip()

    if not nome:
        print("O nome não pode ficar vazio.")
        registrar_log("warning", "Cadastro de cliente cancelado: nome vazio.")
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
        registrar_log(
            "info",
            f"Cliente cadastrado com sucesso: ID {identificador}, nome '{nome}'."
        )

    except OSError as erro:
        print(f"Não foi possível salvar o cliente: {erro}")
        registrar_log(
            "exception",
            f"Falha ao salvar cliente: ID {identificador}, nome '{nome}'."
        )


def info_cliente():
    """Exibe os dados de um cliente."""
    registrar_log("debug", "Iniciando consulta de detalhes de cliente.")
    list_clientes()

    identificador = input(
        "Digite o ID do cliente que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(cliente_bucket, identificador)

    if caminho is None:
        print(f"Cliente com ID {identificador} não encontrado.")
        registrar_log(
            "warning",
            f"Consulta de cliente inexistente. ID informado: '{identificador}'."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Não foi possível exibir os detalhes do cliente de ID {identificador}."
        )
        return

    print(f"\nID: {dados.get('id', '?')}")
    print(f"Nome: {dados.get('nome', 'Não informado')}")
    print(f"Idade: {dados.get('idade', '?')}")
    print(f"Ingressos: {dados.get('ingressos', [])}")
    registrar_log(
        "info",
        f"Detalhes do cliente consultados com sucesso: ID {identificador}."
    )


def editar_cliente():
    """Edita o nome e a idade de um cliente."""
    registrar_log("debug", "Iniciando edição de cliente.")
    list_clientes()

    identificador = input(
        "Digite o ID do cliente que deseja editar: "
    ).strip()

    caminho = buscar_arquivo(cliente_bucket, identificador)

    if caminho is None:
        print(f"Cliente com ID {identificador} não encontrado.")
        registrar_log(
            "warning",
            f"Edição de cliente cancelada: ID {identificador} não encontrado."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Edição de cliente cancelada: não foi possível ler o ID {identificador}."
        )
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
                registrar_log(
                    "warning",
                    f"Edição de cliente cancelada: idade inválida para ID {identificador}."
                )
                return

            dados["idade"] = nova_idade

        except ValueError:
            print("Idade inválida.")
            registrar_log(
                "warning",
                f"Edição de cliente cancelada: idade inválida para ID {identificador}."
            )
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
        registrar_log(
            "info",
            f"Cliente atualizado com sucesso: ID {identificador}."
        )

    except OSError as erro:
        print(f"Não foi possível atualizar o cliente: {erro}")
        registrar_log(
            "exception",
            f"Falha ao atualizar cliente: ID {identificador}."
        )


def aparatar_clientes():
    """Exclui um cliente que não possua ingressos ativos."""
    registrar_log("debug", "Iniciando exclusão de cliente.")
    list_clientes()

    identificador = input(
        "Digite o ID do cliente que deseja excluir: "
    ).strip()

    caminho = buscar_arquivo(cliente_bucket, identificador)

    if caminho is None:
        print(f"Cliente com ID {identificador} não encontrado.")
        registrar_log(
            "warning",
            f"Tentativa de excluir cliente inexistente. ID informado: '{identificador}'."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Exclusão de cliente cancelada: não foi possível ler o ID {identificador}."
        )
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
        registrar_log(
            "warning",
            f"Exclusão de cliente cancelada: existem ingressos vinculados ao ID {identificador}."
        )
        return

    try:
        caminho.unlink()
        print(f"Cliente {identificador} excluído com sucesso.")
        registrar_log(
            "info",
            f"Cliente excluído com sucesso: ID {identificador}."
        )

    except OSError as erro:
        print(f"Não foi possível excluir o cliente: {erro}")
        registrar_log(
            "exception",
            f"Falha ao excluir cliente: ID {identificador}."
        )


# ====================================================== #
# ============== GERENCIAMENTO DE INGRESSOS ============= #

def list_ingressos():
    """Lista os ingressos emitidos."""
    aviso()
    registrar_log("debug", "Iniciando listagem de ingressos.")
    arquivos = listar_arquivos(ingresso_bucket)

    if not arquivos:
        print("Nenhum ingresso emitido.")
        registrar_log(
            "warning",
            "Tentativa de listar ingressos sem nenhum registro."
        )
        return

    quantidade = 0
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
            quantidade += 1

    registrar_log(
        "info",
        f"Listagem de ingressos concluída. Registros exibidos: {quantidade}."
    )


def add_ingresso():
    """Emite um ingresso e atualiza a ocupação da sessão."""
    registrar_log("debug", "Iniciando emissão de ingresso.")
    list_clientes()

    cliente_id = input(
        "Digite o ID do cliente: "
    ).strip()

    caminho_cliente = buscar_arquivo(cliente_bucket, cliente_id)

    if caminho_cliente is None:
        print(f"Cliente com ID {cliente_id} não encontrado.")
        registrar_log(
            "warning",
            f"Emissão de ingresso cancelada: cliente ID {cliente_id} não encontrado."
        )
        return

    cliente = ler_json(caminho_cliente)

    if cliente is None:
        registrar_log(
            "error",
            f"Emissão de ingresso cancelada: não foi possível ler o cliente ID {cliente_id}."
        )
        return

    list_sessoes()

    sessao_id = input(
        "Digite o ID da sessão: "
    ).strip()

    caminho_sessao = buscar_arquivo(sessao_bucket, sessao_id)

    if caminho_sessao is None:
        print(f"Sessão com ID {sessao_id} não encontrada.")
        registrar_log(
            "warning",
            f"Emissão de ingresso cancelada: sessão ID {sessao_id} não encontrada."
        )
        return

    sessao = ler_json(caminho_sessao)

    if sessao is None:
        registrar_log(
            "error",
            f"Emissão de ingresso cancelada: não foi possível ler a sessão ID {sessao_id}."
        )
        return

    assentos = sessao.get("assentos_ocupados", [])

    if not assentos or all(assentos):
        print("A sessão está lotada.")
        registrar_log(
            "warning",
            f"Emissão de ingresso cancelada: sessão ID {sessao_id} lotada."
        )
        return

    poltrona = ler_numero(
        f"Digite a poltrona desejada (1 a {len(assentos)}): ",
        int,
        1
    )

    if poltrona > len(assentos):
        print("Poltrona inexistente nessa sessão.")
        registrar_log(
            "warning",
            f"Emissão de ingresso cancelada: poltrona {poltrona} inexistente na sessão ID {sessao_id}."
        )
        return

    indice = poltrona - 1

    if assentos[indice]:
        print("Essa poltrona já está ocupada.")
        registrar_log(
            "warning",
            f"Emissão de ingresso cancelada: poltrona {poltrona} já ocupada na sessão ID {sessao_id}."
        )
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
            registrar_log(
                "warning",
                f"Emissão de ingresso cancelada: já existe ingresso para poltrona {poltrona} na sessão ID {sessao_id}."
            )
            return

    tipo = input(
        "Tipo do ingresso (inteira/meia): "
    ).strip().lower()

    if tipo not in ("inteira", "meia"):
        print("Tipo inválido. Digite 'inteira' ou 'meia'.")
        registrar_log(
            "warning",
            f"Emissão de ingresso cancelada: tipo '{tipo}' inválido."
        )
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
        registrar_log(
            "info",
            f"Ingresso emitido com sucesso: ID {identificador}, cliente {cliente_id}, sessão {sessao_id}, poltrona {poltrona}."
        )

    except OSError as erro:
        print(f"Não foi possível concluir a emissão: {erro}")
        registrar_log(
            "exception",
            f"Falha ao emitir ingresso: ID {identificador}, cliente {cliente_id}, sessão {sessao_id}."
        )


def info_ingresso():
    """Exibe os dados de um ingresso."""
    registrar_log("debug", "Iniciando consulta de detalhes de ingresso.")
    list_ingressos()

    identificador = input(
        "Digite o ID do ingresso que deseja consultar: "
    ).strip()

    caminho = buscar_arquivo(ingresso_bucket, identificador)

    if caminho is None:
        print(f"Ingresso com ID {identificador} não encontrado.")
        registrar_log(
            "warning",
            f"Consulta de ingresso inexistente. ID informado: '{identificador}'."
        )
        return

    dados = ler_json(caminho)

    if dados is None:
        registrar_log(
            "error",
            f"Não foi possível exibir os detalhes do ingresso de ID {identificador}."
        )
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
    registrar_log(
        "info",
        f"Detalhes do ingresso consultados com sucesso: ID {identificador}."
    )


def aparatar_ingressos():
    """Cancela um ingresso e libera a poltrona da sessão."""
    registrar_log("debug", "Iniciando cancelamento de ingresso.")
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
        registrar_log(
            "warning",
            f"Cancelamento de ingresso inexistente. ID informado: '{identificador}'."
        )
        return

    ingresso = ler_json(caminho_ingresso)

    if ingresso is None:
        registrar_log(
            "error",
            f"Cancelamento de ingresso interrompido: não foi possível ler o ID {identificador}."
        )
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
        registrar_log(
            "error",
            f"Cancelamento de ingresso interrompido: sessão vinculada não encontrada para o ID {identificador}."
        )
        return

    poltrona = ingresso["poltrona"]
    indice = poltrona - 1
    assentos = sessao.get("assentos_ocupados", [])

    if indice < 0 or indice >= len(assentos):
        print("A poltrona registrada no ingresso é inválida.")
        registrar_log(
            "error",
            f"Cancelamento de ingresso interrompido: poltrona inválida no ID {identificador}."
        )
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
        registrar_log(
            "info",
            f"Ingresso cancelado com sucesso: ID {identificador}, poltrona {poltrona} liberada."
        )

    except OSError as erro:
        print(f"Não foi possível cancelar o ingresso: {erro}")
        registrar_log(
            "exception",
            f"Falha ao cancelar ingresso: ID {identificador}."
        )

# ====================================================== #
# ================ PONTO DE ENTRADA ==================== #

if __name__ == "__main__":
    print("Gerenciador de filmes e salas.")
    print("Módulo carregado sem executar cadastros automaticamente.")
    # Chame as funções necessárias aqui ou no menu principal.
