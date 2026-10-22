import os
from pathlib import Path
import debug
from debug import ativar_logger

import pygame

try:
    import keyboard
except ImportError:
    keyboard = None

try:
    import música
except ImportError:
    música = None

from gerenciador import (
    list_filmes, add_filme, info_filme, aparatar_filmes,
    list_salas, add_sala, info_sala, aparatar_salas,
    list_sessoes, add_sessao, info_sessao, aparatar_sessoes,
    list_clientes, add_cliente, info_cliente, aparatar_clientes,
    list_ingressos, add_ingresso, info_ingresso, aparatar_ingressos,
)

def registrar_log(nivel, mensagem):
    """Registra um evento somente se o debug estiver ativo."""

    if not debug.log_ativo:
        return

    metodo = getattr(debug.logger, nivel)
    metodo(mensagem, stacklevel=2)

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("Pressione Enter para continuar...")


def executar_menu(titulo, itens):
    acoes = {str(indice): acao for indice, (_, acao) in enumerate(itens, start=1)}

    while True:
        limpar_tela()
        if debug.log_ativo:
            print("\033[32mModo DEBUG ativado\033[0m")
        print(f"========= {titulo} =========")
        for indice, (rotulo, _) in enumerate(itens, start=1):
            print(f"{indice} — {rotulo}")

        print("M — Músicas")
        print("0 — Voltar")

        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "0":
            registrar_log("info", f"Saída do menu: {titulo}.")
            return

        if opcao.lower() == "m":
            registrar_log("info", "Menu de músicas solicitado.")
            if música is None:
                registrar_log(
                "error",
                "Não foi possível importar o módulo de músicas."
                )
                print("Falha ao acessar o sistema de músicas.")
                pausa()
                continue

            música.main()
            continue

        acao = acoes.get(opcao)

        if acao is None:
            registrar_log(
            "warning",
            f"Opção inválida no menu {titulo}: {opcao!r}."
            )
            print("Opção inválida.")
            pausa()
            continue

        limpar_tela()
        registrar_log(
        "info",
        f"Ação selecionada no menu {titulo}: {opcao}."
        )
        acao()
        pausa()


def main():
    menus = {
        "1": ("Filmes", [
            ("Cadastrar Filme", add_filme),
            ("Listar Filmes", list_filmes),
            ("Informações do Filme", info_filme),
            ("Excluir Filme", aparatar_filmes),
        ]),
        "2": ("Salas", [
            ("Cadastrar Sala", add_sala),
            ("Listar Salas", list_salas),
            ("Informações da Sala", info_sala),
            ("Excluir Sala", aparatar_salas),
        ]),
        "3": ("Sessões", [
            ("Cadastrar Sessão", add_sessao),
            ("Listar Sessões", list_sessoes),
            ("Informações da Sessão", info_sessao),
            ("Excluir Sessão", aparatar_sessoes),
        ]),
        "4": ("Clientes", [
            ("Cadastrar Cliente", add_cliente),
            ("Listar Clientes", list_clientes),
            ("Informações do Cliente", info_cliente),
            ("Excluir Cliente", aparatar_clientes),
        ]),
        "5": ("Ingressos", [
            ("Cadastrar Ingresso", add_ingresso),
            ("Listar Ingressos", list_ingressos),
            ("Informações do Ingresso", info_ingresso),
            ("Excluir Ingresso", aparatar_ingressos),
        ]),
    }

    while True:
        limpar_tela()
        if debug.log_ativo:
            print("\033[32mModo DEBUG ativado\033[0m")
        print("========= Sistema de Cinema =========")
        for chave, (titulo, _) in menus.items():
            print(f"{chave} — {titulo}")
        print("M — Músicas")
        print("0 — Sair")

        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "0":
            registrar_log("info", "Encerramento solicitado pelo usuário.")
            limpar_tela()
            print("Saindo do sistema...")
            pausa()
            return

        if opcao == "m":
            registrar_log("info", "Menu de músicas solicitado.")
            if música is None:
                registrar_log(
                    "error",
                    "Não foi possível importar o módulo de músicas."
                )
                print("Falha ao acessar o sistema de músicas.")
                pausa()
                continue
            música.main()
            continue

        if opcao == "debug":
            if debug.log_ativo:
                print("O modo DEBUG já está ativado")
            else:
                ativar_logger()
                print("O modo DEBUG foi ativado")
            pausa()
            continue

        if opcao in menus:
            titulo, itens = menus[opcao]
            executar_menu(titulo, itens)
        else:
            registrar_log(
            "warning",
            f"Opção inválida no menu inicial: {opcao!r}."
            )
            print("Opção inválida.")
            pausa()



def ItsLeviOsa_not_LeviosAR():
    """Reproduz o easter egg musical de Harry Potter."""
    registrar_log(
        "debug",
        "Atalho de reprodução do easter egg acionado."
    )
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            registrar_log(
                "debug",
                "Mixer do pygame inicializado."
            )
        # Não reinicia a música se ela já estiver tocando.
        if pygame.mixer.music.get_busy():
            registrar_log(
                "debug",
                "Easter egg não iniciado: já existe música tocando."
            )
            return
        audio = Path(__file__).resolve().parent / "secrets" / "Ultra_Secret.mp3"
        registrar_log(
            "debug",
            f"Tentando reproduzir o arquivo: {audio.name}"
        )
        pygame.mixer.music.load(str(audio))
        pygame.mixer.music.play()
        registrar_log(
            "info",
            "Easter egg musical iniciado."
        )
    except (pygame.error, OSError) as erro:
        print(f"Erro ao reproduzir o easter egg: {erro}")
        registrar_log(
            "exception",
            "Falha ao reproduzir o easter egg musical."
        )



def parar_easter_egg():
    """Interrompe a reprodução do easter egg."""
    registrar_log(
        "debug",
        "Atalho para interromper o easter egg acionado."
    )
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            registrar_log(
                "info",
                "Reprodução do easter egg interrompida."
            )
        else:
            registrar_log(
                "debug",
                "Não foi possível parar a música: mixer não inicializado."
            )
    except pygame.error:
        print("Erro ao parar o easter egg.")
        registrar_log(
            "exception",
            "Falha ao interromper o easter egg musical."
        )



def registrar_atalhos():
    """Registra os atalhos de teclado do easter egg."""
    registrar_log(
        "debug",
        "Iniciando o registro dos atalhos de teclado."
    )
    if keyboard is None:
        print("A biblioteca 'keyboard' não está instalada. Atalhos desativados.")
        print("Para instalar: pip install keyboard ou execute 'instalar_dependencias.bat'")
        registrar_log(
            "warning",
            "Biblioteca 'keyboard' indisponível. Atalhos desativados."
        )

        pausa()
        return False
    try:
        keyboard.add_hotkey(
            "alt+h+p",
            ItsLeviOsa_not_LeviosAR,
            suppress=True
        )
        keyboard.add_hotkey(
            "alt+h+s",
            parar_easter_egg,
            suppress=True
        )
        registrar_log(
            "debug",
            "Atalhos do easter egg registrados com sucesso."
        )
        return True
    except (ImportError, OSError):
        print("Atalhos de teclado indisponíveis.")

        registrar_log(
            "exception",
            "Falha ao registrar os atalhos de teclado."
        )

        pausa()
        return False


if __name__ == "__main__":
    atalhos_ativos = registrar_atalhos()
    registrar_log(
        "info",
        "Inicializando o sistema de cinema."
    )
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrando o sistema...")
        registrar_log(
            "warning",
            "Encerramento solicitado por interrupção do teclado."
        )
    except EOFError:
        print("\nEncerrando o sistema...")
        registrar_log(
            "warning",
            "Entrada encerrada inesperadamente (EOF)."
        )
    finally:
        registrar_log(
            "info",
            "Iniciando a limpeza dos recursos do sistema."
        )
        if atalhos_ativos:
            keyboard.unhook_all()
            registrar_log(
                "debug",
                "Atalhos de teclado removidos."
            )
        pygame.mixer.quit()
        registrar_log(
            "info",
            "Mixer do pygame encerrado."
        )
        debug.encerrar_monitor()