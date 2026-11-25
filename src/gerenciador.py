# =================== Importações ====================== #

import os
from datetime import datetime

from classes import (
    Filme, Sala, Sessao, Cliente, Ingresso,
    ClassificacaoIndicativa,
    TipoSessao, StatusSessao, TipoIngresso, IngressoError,
)
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
    if caminho is None:
        return None
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


def carregar_filme(identificador):
    """Carrega um filme do JSON e o reconstrói como objeto Filme."""
    caminho = buscar_arquivo(filme_bucket, identificador)

    if caminho is None:
        return None

    dados = ler_json(caminho)

    if not isinstance(dados, dict):
        return None

    try:
        classificacao = ClassificacaoIndicativa(dados["classificacao"])

        return Filme(
            dados["id"],
            dados["titulo"],
            dados["duracao"],
            dados["genero"],
            dados["sinopse"],
            classificacao
        )

    except (KeyError, ValueError, TypeError) as erro:
        registrar_log(
            "exception",
            f"Falha ao reconstruir filme do arquivo {caminho.name}: {erro}"
        )
        print(f"Não foi possível carregar o filme: {erro}")
        return None


def possui_sessao(campo, identificador):
    """Verifica se existem sessões vinculadas a um filme ou sala."""
    registrar_log("debug", "Verificando sessões vinculadas.")

    try:
        arquivos = listar_arquivos(sessao_bucket)
    except OSError:
        return None

    for arquivo in arquivos:
        dados = ler_json(arquivo)

        if dados is None:
            return None

        if str(dados.get(campo, "")) == str(identificador):
            return True

    return False


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
# ===== SERIALIZAÇÃO DE SESSÃO E INGRESSO =============== #
# As classes novas (Sessao, Ingresso) não têm to_dict/from_dict.
# Por isso a serialização é feita aqui.
#
# WORKAROUND: _sessao_from_dict e _ingresso_from_dict usam
# __new__ + atributos internos (_Sessao__id_sessao, _Ingresso__id, ...)
# porque os __init__ geram id automático e também vendem o ingresso.
# ====================================================== #

def _sessao_to_dict(sessao, sala):
    return {
        "id_sessao": sessao.id_sessao,
        "filme_id": sessao.filme.id_filme,
        "sala_numero": sessao.sala.get_numero(),
        "data_hora": sessao.data_hora.strftime("%d/%m/%Y %H:%M"),
        "tipo": int(sessao.tipo),
        "preco": sessao.preco,
        "status": int(sessao.status),
        "assentos_ocupados": _mapa_assentos(sessao, sala),
    }


def _sessao_from_dict(dados, filme, sala):
    """Reconstrói Sessao sem gerar id novo. WORKAROUND."""
    sessao = Sessao.__new__(Sessao)
    sessao._Sessao__id_sessao = dados["id_sessao"]
    sessao._Sessao__filme = filme
    sessao._Sessao__sala = sala
    sessao._Sessao__data_hora = datetime.strptime(
        dados["data_hora"], "%d/%m/%Y %H:%M"
    )
    sessao._Sessao__tipo = TipoSessao(dados["tipo"])
    sessao._Sessao__preco = float(dados["preco"])
    sessao._Sessao__status = StatusSessao(dados["status"])

    for numero in dados.get("assentos_ocupados", []):
        try:
            sala.ocupar_assento(sessao.id_sessao, numero)
        except ValueError:
            pass
    return sessao


def _ingresso_to_dict(ingresso):
    return {
        "id_ingresso": ingresso.id_ingresso,
        "preco": ingresso.valor,
        "poltrona": ingresso.numero_assento,
        "tipo": "inteira" if ingresso.tipo == TipoIngresso.INTEIRA else "meia",
        "cliente_id": ingresso.cliente.id,
        "sessao_id": ingresso.sessao.id_sessao,
    }


def _ingresso_from_dict(dados, sessao, cliente):
    """Reconstrói Ingresso SEM vender de novo. WORKAROUND."""
    ingresso = Ingresso.__new__(Ingresso)
    ingresso._Ingresso__id = dados["id_ingresso"]
    ingresso._Ingresso__sessao = sessao
    ingresso._Ingresso__cliente = cliente
    ingresso._Ingresso__assento = dados["poltrona"]
    ingresso._Ingresso__tipo = (
        TipoIngresso.INTEIRA if dados["tipo"] == "inteira"
        else TipoIngresso.MEIA
    )
    ingresso._Ingresso__valor = float(dados["preco"])
    ingresso._Ingresso__cancelado = False
    return ingresso


def _mapa_assentos(sessao, sala):
    """Devolve a lista de números de assento ocupados nesta sessão."""
    ocupados = []
    for numero in range(1, sala.get_capacidade() + 1):
        if not sala.assento_disponivel(sessao.id_sessao, numero):
            ocupados.append(numero)
    return ocupados


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

    print("\nClassificações indicativas:")
    print("0 - Livre")
    print("10 - 10 anos")
    print("12 - 12 anos")
    print("14 - 14 anos")
    print("16 - 16 anos")
    print("18 - 18 anos")

    try:
        idade = int(input("Digite a classificação indicativa: "))
        classificacao = ClassificacaoIndicativa(idade)
    except ValueError:
        print("Classificação indicativa inválida.")
        return

    identificador = proximo_id(filme_bucket)

    filme = Filme(identificador, titulo, duracao, genero, sinopse, classificacao)

    dados = {
        "id": identificador,
        "titulo": titulo,
        "duracao": duracao,
        "genero": genero,
        "sinopse": sinopse,
        "classificacao": classificacao.value
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

    resultado = possui_sessao("filme_id", identificador)

    if resultado is None:
        print("Não foi possível verificar as sessões. Filme não excluído.")
        registrar_log("error", "Exclusão de filme cancelada: falha na verificação.")
        return

    if resultado:
        print("Não é possível excluir: existem sessões vinculadas a este filme.")
        registrar_log(
            "warning",
            f"Exclusão de filme cancelada: ID {identificador} possui sessões vinculadas."
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
    print(f"Classificação: {dados.get('classificacao', 'Não informada')} anos")

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
    """Cadastra uma sala."""
    registrar_log("debug", "Iniciando cadastro de sala.")
    capacidade = ler_numero(
        "Digite a capacidade da sala: ",
        int,
        1
    )

    numero = proximo_id(sala_bucket)

    try:
        sala = Sala(numero, capacidade)
    except ValueError as erro:
        print(f"Não foi possível cadastrar a sala: {erro}")
        registrar_log("warning", f"Sala inválida: {erro}")
        return

    dados = {
        "numero": sala.get_numero(),
        "capacidade": sala.get_capacidade(),
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

    resultado = possui_sessao("sala_numero", numero)

    if resultado is None:
        print("Não foi possível verificar as sessões. Sala não excluída.")
        registrar_log("error", "Exclusão de sala cancelada: falha na verificação.")
        return

    if resultado:
        print("Não é possível excluir: existem sessões vinculadas a esta sala.")
        registrar_log(
            "warning",
            f"Exclusão de sala cancelada: número {numero} possui sessões vinculadas."
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
            try:
                tipo = TipoSessao(dados["tipo"]).descricao
                status = StatusSessao(dados["status"]).descricao
            except (KeyError, ValueError):
                tipo, status = "?", "?"
            print(
                f"ID: {dados.get('id_sessao', '?')} | "
                f"Filme: {dados.get('filme_id', '?')} | "
                f"Sala: {dados.get('sala_numero', '?')} | "
                f"Data/Hora: {dados.get('data_hora', '?')} | "
                f"Tipo: {tipo} | Status: {status}"
            )
            quantidade += 1
    registrar_log(
        "info",
        f"Listagem de sessões concluída. Registros exibidos: {quantidade}."
    )


def add_sessao():
    """Cadastra uma sessão usando a nova Sessao."""
    registrar_log("debug", "Iniciando cadastro de sessão.")
    list_filmes()
    filme_id = input("Digite o ID do filme: ").strip()
    filme = carregar_filme(filme_id)
    if filme is None:
        print(f"Filme com ID {filme_id} não encontrado.")
        registrar_log("warning", f"Cadastro cancelado: filme {filme_id} não encontrado.")
        return

    list_salas()
    sala_numero = input("Digite o número da sala: ").strip()
    dados_sala = ler_json(buscar_arquivo(sala_bucket, sala_numero))
    if dados_sala is None:
        print(f"Sala {sala_numero} não encontrada.")
        registrar_log("warning", f"Cadastro cancelado: sala {sala_numero} não encontrada.")
        return
    try:
        sala = Sala(dados_sala["numero"], dados_sala["capacidade"])
    except (KeyError, ValueError, TypeError) as erro:
        print(f"Sala inválida: {erro}")
        return

    data_str = input("Data e hora (dd/mm/aaaa hh:mm): ").strip()
    try:
        data_hora = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
    except ValueError:
        print("Data/hora inválida. Use o formato dd/mm/aaaa hh:mm.")
        registrar_log("warning", "Cadastro cancelado: data/hora inválida.")
        return

    print("\nTipo: 1 — 3D | 2 — 2D | 3 — Assistiva")
    tipo = input("Escolha: ").strip()
    if tipo not in ("1", "2", "3"):
        print("Tipo inválido.")
        return

    print("\nStatus: 1 — Em Breve | 2 — Em Progresso | 3 — Concluída")
    status = input("Escolha: ").strip()
    if status not in ("1", "2", "3"):
        print("Status inválido.")
        return

    preco = ler_numero("Digite o preço do ingresso: ", float, 0.01)

    try:
        sessao = Sessao(
            filme=filme,
            sala=sala,
            data_hora=data_hora,
            tipo=int(tipo),
            preco=preco,
            status=int(status),
        )
    except (ValueError, TypeError) as erro:
        print(f"Não foi possível criar a sessão: {erro}")
        registrar_log("warning", f"Sessão inválida: {erro}")
        return

    identificador = sessao.id_sessao
    caminho = sessao_bucket / f"{identificador} - Sessao.json"
    try:
        salvar_json(caminho, _sessao_to_dict(sessao, sala))
        print(f"Sessão {identificador} cadastrada com sucesso.")
        registrar_log("info", f"Sessão {identificador} cadastrada.")
    except OSError as erro:
        print(f"Não foi possível salvar a sessão: {erro}")
        registrar_log("exception", f"Falha ao salvar sessão: {identificador}.")


def info_sessao():
    """Exibe os detalhes de uma sessão pelo ID."""
    registrar_log("debug", "Iniciando consulta de detalhes de sessão.")
    list_sessoes()
    identificador = input("Digite o ID da sessão: ").strip()
    dados = ler_json(buscar_arquivo(sessao_bucket, identificador))
    if dados is None:
        print("Sessão não encontrada.")
        return

    filme = carregar_filme(dados["filme_id"])
    if filme is None:
        print("Filme vinculado não encontrado.")
        return

    dados_sala = ler_json(buscar_arquivo(sala_bucket, dados["sala_numero"]))
    if dados_sala is None:
        print("Sala vinculada não encontrada.")
        return
    sala = Sala(dados_sala["numero"], dados_sala["capacidade"])

    sessao = _sessao_from_dict(dados, filme, sala)
    try:
        tipo = sessao.tipo.descricao
        status = sessao.status.descricao
    except Exception:
        tipo, status = "?", "?"

    print(f"\nID: {sessao.id_sessao}")
    print(f"Filme: {filme.titulo}")
    print(f"Sala: {sala.get_numero()}")
    print(f"Data/Hora: {sessao.data_hora:%d/%m/%Y %H:%M}")
    print(f"Tipo: {tipo}")
    print(f"Preço: R$ {sessao.preco:.2f}")
    print(f"Status: {status}")
    print(f"Assentos disponíveis: {sessao.quantidade_assentos_disponiveis()}/{sala.get_capacidade()}")
    registrar_log(
        "info",
        f"Detalhes da sessão consultados com sucesso: ID {identificador}."
    )


def editar_sessao():
    """Edita a data/hora, o preço e o status de uma sessão."""
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

    data_str = input(f"Data/hora [{dados.get('data_hora', '?')}]: ").strip()
    preco = input(f"Preço [{dados['preco']}]: ").strip()
    status_str = input(f"Status [{dados.get('status', '?')}]: ").strip()

    if data_str:
        try:
            datetime.strptime(data_str, "%d/%m/%Y %H:%M")
            dados["data_hora"] = data_str
        except ValueError:
            print("Data/hora inválida.")
            registrar_log(
                "warning",
                f"Edição de sessão cancelada: data/hora inválida para ID {identificador}."
            )
            return

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

    if status_str:
        if status_str not in ("1", "2", "3"):
            print("Status inválido.")
            return
        dados["status"] = int(status_str)

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

    if dados.get("assentos_ocupados"):
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


def ver_disponibilidade_sessao():
    """Mostra a disponibilidade de assentos de uma sessão."""
    registrar_log("debug", "Consulta de disponibilidade.")
    list_sessoes()
    identificador = input("ID da sessão: ").strip()
    dados = ler_json(buscar_arquivo(sessao_bucket, identificador))
    if dados is None:
        print("Sessão não encontrada.")
        return

    dados_sala = ler_json(buscar_arquivo(sala_bucket, dados["sala_numero"]))
    if dados_sala is None:
        print("Sala vinculada não encontrada.")
        return
    sala = Sala(dados_sala["numero"], dados_sala["capacidade"])

    ocupados = dados.get("assentos_ocupados", [])
    print(f"\nSessão {identificador} — Sala {sala.get_numero()}")
    print(f"Capacidade: {sala.get_capacidade()}")
    print(f"Ocupados: {len(ocupados)}")
    print(f"Disponíveis: {sala.get_capacidade() - len(ocupados)}")
    print("\nMapa (X = ocupado, . = livre):")
    for numero in range(1, sala.get_capacidade() + 1):
        marcador = "X" if numero in ocupados else "."
        print(f"{numero:>3}: {marcador}", end="   ")
        if numero % 5 == 0:
            print()


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
                f"Idade: {dados.get('idade', '?')} | "
                f"E-mail: {dados.get('email', 'Não informado')}"
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
    email = input("Digite o e-mail do cliente: ").strip()
    identificador = proximo_id(cliente_bucket)

    cliente = Cliente(identificador, nome, idade, email)

    dados = {
        "id": cliente.id,
        "nome": cliente.nome,
        "idade": cliente.idade,
        "email": cliente.email,
        "ingressos": [],
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
    print(f"E-mail: {dados.get('email', 'Não informado')}")
    print(f"Ingressos: {dados.get('ingressos', [])}")
    registrar_log(
        "info",
        f"Detalhes do cliente consultados com sucesso: ID {identificador}."
    )


def editar_cliente():
    """Edita o nome, a idade e o e-mail de um cliente."""
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

    email = input(
        f"E-mail [{dados.get('email', 'Não informado')}]: "
    ).strip()

    if nome:
        dados["nome"] = nome

    if email:
        dados["email"] = email

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


def ver_historico_cliente():
    """Exibe o histórico de ingressos de um cliente."""
    registrar_log("debug", "Histórico de cliente.")
    list_clientes()
    identificador = input("ID do cliente: ").strip()
    dados = ler_json(buscar_arquivo(cliente_bucket, identificador))
    if dados is None:
        print("Cliente não encontrado.")
        return

    ids = dados.get("ingressos", [])
    if not ids:
        print("\nNenhum ingresso comprado.")
        return

    print(f"\n>>> HISTÓRICO DE INGRESSOS — {dados['nome']} <<<\n")
    for id_ing in ids:
        dados_ing = ler_json(buscar_arquivo(ingresso_bucket, id_ing))
        if dados_ing is None:
            continue
        dados_sessao = ler_json(buscar_arquivo(sessao_bucket, dados_ing["sessao_id"]))
        if dados_sessao is None:
            continue
        dados_filme = ler_json(buscar_arquivo(filme_bucket, dados_sessao["filme_id"]))
        if dados_filme is None:
            continue
        tipo = "Inteira" if dados_ing["tipo"] == "inteira" else "Meia"
        print(
            f"Ingresso #{dados_ing['id_ingresso']} | "
            f"{dados_filme['titulo']} | "
            f"{dados_sessao['data_hora']} | "
            f"Sala {dados_sessao['sala_numero']} | "
            f"Assento {dados_ing['poltrona']} | "
            f"{tipo} | R$ {dados_ing['preco']:.2f}"
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
                f"Tipo: {dados.get('tipo', '?')} | "
                f"Preço: R$ {dados.get('preco', 0):.2f}"
            )
            quantidade += 1

    registrar_log(
        "info",
        f"Listagem de ingressos concluída. Registros exibidos: {quantidade}."
    )


def add_ingresso():
    """Emite um ingresso usando a nova Ingresso (que já vende no __init__)."""
    registrar_log("debug", "Iniciando emissão de ingresso.")
    list_clientes()
    cliente_id = input("Digite o ID do cliente: ").strip()
    dados_cliente = ler_json(buscar_arquivo(cliente_bucket, cliente_id))
    if dados_cliente is None:
        print("Cliente não encontrado.")
        return
    cliente = Cliente(
        dados_cliente["id"], dados_cliente["nome"],
        dados_cliente["idade"], dados_cliente["email"]
    )

    list_sessoes()
    sessao_id = input("Digite o ID da sessão: ").strip()
    dados_sessao = ler_json(buscar_arquivo(sessao_bucket, sessao_id))
    if dados_sessao is None:
        print("Sessão não encontrada.")
        return

    filme = carregar_filme(dados_sessao["filme_id"])
    if filme is None:
        print("Filme da sessão não encontrado.")
        return

    dados_sala = ler_json(buscar_arquivo(sala_bucket, dados_sessao["sala_numero"]))
    if dados_sala is None:
        print("Sala da sessão não encontrada.")
        return
    sala = Sala(dados_sala["numero"], dados_sala["capacidade"])

    sessao = _sessao_from_dict(dados_sessao, filme, sala)

    poltrona = ler_numero(
        f"Digite a poltrona (1 a {sala.get_capacidade()}): ", int, 1
    )

    print("\nTipo: 1 — Inteira | 2 — Meia")
    tipo = input("Escolha: ").strip()
    if tipo not in ("1", "2"):
        print("Tipo inválido.")
        return

    try:
        ingresso = Ingresso(sessao, cliente, poltrona, int(tipo))
    except IngressoError as erro:
        print(f"Não foi possível emitir: {erro}")
        registrar_log("warning", f"Ingresso recusado: {erro}")
        return

    identificador = proximo_id(ingresso_bucket)
    ingresso._Ingresso__id = identificador

    caminho = ingresso_bucket / f"{identificador} - Ingresso.json"
    try:
        salvar_json(caminho, _ingresso_to_dict(ingresso))

        dados_sessao["assentos_ocupados"] = _mapa_assentos(sessao, sala)
        (sessao_bucket / f"{sessao_id} - Sessao.json").write_text(
            json.dumps(dados_sessao, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )

        dados_cliente.setdefault("ingressos", []).append(identificador)
        (cliente_bucket / f"{cliente_id} - {nome_seguro(dados_cliente['nome'])}.json").write_text(
            json.dumps(dados_cliente, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )

        print(f"Ingresso {identificador} emitido com sucesso.")
        print(f"Cliente: {cliente.nome}")
        print(f"Sessão: {sessao_id}")
        print(f"Poltrona: {poltrona}")
        tipo_str = "Inteira" if ingresso.tipo == TipoIngresso.INTEIRA else "Meia"
        print(f"Tipo: {tipo_str}")
        print(f"Preço: R$ {ingresso.valor:.2f}")
        registrar_log("info", f"Ingresso {identificador} emitido.")
    except OSError as erro:
        print(f"Não foi possível salvar: {erro}")
        registrar_log("exception", f"Falha ao emitir ingresso: {identificador}.")


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
    """Cancela um ingresso via ingresso.cancelar() (libera o assento)."""
    registrar_log("debug", "Iniciando cancelamento de ingresso.")
    list_ingressos()
    identificador = input("Digite o ID do ingresso: ").strip()
    dados = ler_json(buscar_arquivo(ingresso_bucket, identificador))
    if dados is None:
        print("Ingresso não encontrado.")
        return

    dados_sessao = ler_json(buscar_arquivo(sessao_bucket, dados["sessao_id"]))
    dados_cliente = ler_json(buscar_arquivo(cliente_bucket, dados["cliente_id"]))
    if dados_sessao is None or dados_cliente is None:
        print("Dados vinculados não encontrados.")
        return

    filme = carregar_filme(dados_sessao["filme_id"])
    if filme is None:
        print("Filme vinculado não encontrado.")
        return

    dados_sala = ler_json(buscar_arquivo(sala_bucket, dados_sessao["sala_numero"]))
    if dados_sala is None:
        print("Sala vinculada não encontrada.")
        return
    sala = Sala(dados_sala["numero"], dados_sala["capacidade"])

    sessao = _sessao_from_dict(dados_sessao, filme, sala)
    cliente = Cliente(
        dados_cliente["id"], dados_cliente["nome"],
        dados_cliente["idade"], dados_cliente["email"]
    )
    ingresso = _ingresso_from_dict(dados, sessao, cliente)

    try:
        ingresso.cancelar()
    except IngressoError as erro:
        print(f"Não foi possível cancelar: {erro}")
        registrar_log("warning", f"Cancelamento recusado: {erro}")
        return

    try:
        dados_sessao["assentos_ocupados"] = _mapa_assentos(sessao, sala)
        (sessao_bucket / f"{dados['sessao_id']} - Sessao.json").write_text(
            json.dumps(dados_sessao, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )

        dados_cliente["ingressos"] = [
            i for i in dados_cliente.get("ingressos", [])
            if str(i) != str(identificador)
        ]
        (cliente_bucket / f"{dados['cliente_id']} - {nome_seguro(dados_cliente['nome'])}.json").write_text(
            json.dumps(dados_cliente, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )

        buscar_arquivo(ingresso_bucket, identificador).unlink()
        print(f"Ingresso {identificador} cancelado com sucesso.")
        print(f"Poltrona liberada.")
        registrar_log("info", f"Ingresso {identificador} cancelado.")
    except OSError as erro:
        print(f"Não foi possível salvar: {erro}")
        registrar_log("exception", f"Falha ao cancelar ingresso: {identificador}.")


# ====================================================== #
# ================ PONTO DE ENTRADA ==================== #

if __name__ == "__main__":
    print("Gerenciador de filmes e salas.")
    print("Módulo carregado sem executar cadastros automaticamente.")