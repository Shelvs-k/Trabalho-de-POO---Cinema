"""Camada de persistência: lê e grava os registros em arquivos JSON.

Cada registro é um arquivo ``ID - Nome.json`` dentro de ``dados/<Entidade>/``.
Este módulo também converte Sessao e Ingresso de e para dicionários, já que
essas classes não têm métodos de salvar e carregar.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

import debug
from classes import (
    Filme, Ingresso, Sessao,
    ClassificacaoIndicativa, TipoSessao, StatusSessao, TipoIngresso,
)


def registrar_log(nivel, mensagem):
    """Registra um evento somente quando o modo debug está ativo."""
    if not debug.log_ativo:
        return
    metodo = getattr(debug.logger, nivel)
    metodo(mensagem, stacklevel=2)


# ====================================================== #
# ================= PASTAS DE ARMAZENAMENTO ============ #

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


# ====================================================== #
# ============== LEITURA E GRAVAÇÃO DE ARQUIVOS ======== #

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


def _gravar_atomico(caminho, dados):
    """Grava em um arquivo temporário e o troca de uma vez pelo definitivo.

    Se o programa for interrompido no meio da gravação, o JSON original
    continua intacto em vez de ficar pela metade.
    """
    temporario = caminho.with_name(caminho.name + ".tmp")
    try:
        with temporario.open("w", encoding="utf-8") as arquivo:
            # allow_nan=False impede gravar NaN/Infinity, que não são JSON válido.
            json.dump(
                dados, arquivo, ensure_ascii=False, indent=4, allow_nan=False
            )
        os.replace(temporario, caminho)
    except BaseException:
        temporario.unlink(missing_ok=True)
        raise


def salvar_json(caminho, dados):
    """Cria um JSON novo, sem sobrescrever registros existentes."""
    if caminho.exists():
        raise FileExistsError(f"O arquivo '{caminho.name}' já existe.")
    _gravar_atomico(caminho, dados)
    registrar_log("debug", f"Arquivo JSON criado: {caminho.name}")


def atualizar_json(caminho, dados):
    """Substitui o conteúdo de um JSON já existente."""
    _gravar_atomico(caminho, dados)
    registrar_log("debug", f"Arquivo JSON atualizado: {caminho.name}")


def ler_json(caminho):
    """Lê um JSON e informa erros de arquivo ou conteúdo."""
    if caminho is None:
        return None
    registrar_log("debug", f"Lendo arquivo JSON: {caminho.name}")
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as erro:
        print(f"Erro ao ler '{caminho.name}': {erro}")
        registrar_log(
            "exception",
            f"Falha ao ler arquivo JSON: {caminho.name}"
        )
        return None

    # Todo registro do sistema é um objeto JSON (dicionário). Qualquer outra
    # coisa (lista, texto, número) faria as telas falharem em ``dados.get``.
    if not isinstance(dados, dict):
        print(f"Erro ao ler '{caminho.name}': o conteúdo não é um registro válido.")
        registrar_log(
            "error",
            f"Conteúdo inesperado em {caminho.name}: "
            f"esperado um objeto JSON, recebido {type(dados).__name__}."
        )
        return None

    registrar_log("debug", f"Arquivo JSON lido com sucesso: {caminho.name}")
    return dados


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


# ====================================================== #
# ===== SERIALIZAÇÃO (SESSÃO E INGRESSO) =============== #
# As classes novas (Sessao, Ingresso) não têm to_dict/from_dict.
# Por isso a serialização é feita aqui.
# WORKAROUND: sessao_from_dict e ingresso_from_dict usam
# __new__ + atributos internos (_Sessao__id_sessao, _Ingresso__id, ...)
# porque os __init__ geram id automático e/ou vendem o ingresso.
# Se o grupo renomear esses atributos, o carregamento quebra.


def sessao_to_dict(sessao, sala):
    return {
        "id_sessao": sessao.id_sessao,
        "filme_id": sessao.filme.id_filme,
        "sala_numero": sessao.sala.get_numero(),
        "data_hora": sessao.data_hora.strftime("%d/%m/%Y %H:%M"),
        "tipo": int(sessao.tipo),
        "preco": sessao.preco,
        "status": int(sessao.status),
        "assentos_ocupados": mapa_assentos(sessao, sala),
    }


def sessao_from_dict(dados, filme, sala):
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
        except ValueError as erro:
            registrar_log(
                "warning",
                f"Assento {numero} da sessão {sessao.id_sessao} ignorado ao carregar: {erro}"
            )
    return sessao


def ingresso_to_dict(ingresso):
    return {
        "id_ingresso": ingresso.id_ingresso,
        "preco": ingresso.valor,
        "poltrona": ingresso.numero_assento,
        "tipo": "inteira" if ingresso.tipo == TipoIngresso.INTEIRA else "meia",
        "cliente_id": ingresso.cliente.id,
        "sessao_id": ingresso.sessao.id_sessao,
    }


def ingresso_from_dict(dados, sessao, cliente):
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


def mapa_assentos(sessao, sala):
    """Devolve a lista de números de assento ocupados nesta sessão."""
    ocupados = []
    for numero in range(1, sala.get_capacidade() + 1):
        if not sala.assento_disponivel(sessao.id_sessao, numero):
            ocupados.append(numero)
    return ocupados
