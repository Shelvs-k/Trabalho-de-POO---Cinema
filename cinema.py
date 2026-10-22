import os
from pathlib import Path

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


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("Pressione Enter para continuar...")


def executar_menu(titulo, itens):
    acoes = {str(indice): acao for indice, (_, acao) in enumerate(itens, start=1)}

    while True:
        limpar_tela()
        print(f"========= {titulo} =========")
        for indice, (rotulo, _) in enumerate(itens, start=1):
            print(f"{indice} — {rotulo}")

        print("M — Músicas")
        print("0 — Voltar")

        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "0":
            return

        if opcao.lower() == "m":
            if música is None:
                print("Falha ao acessar o sistema de músicas.")
                pausa()
                continue

            música.main()
            continue

        acao = acoes.get(opcao)

        if acao is None:
            print("Opção inválida.")
            pausa()
            continue

        limpar_tela()
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
        print("========= Sistema de Cinema =========")
        for chave, (titulo, _) in menus.items():
            print(f"{chave} — {titulo}")
        print("M — Músicas")
        print("0 — Sair")

        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "0":
            limpar_tela()
            print("Saindo do sistema...")
            pausa()
            return

        if opcao == "m":
            música.main()
            continue

        if opcao in menus:
            titulo, itens = menus[opcao]
            executar_menu(titulo, itens)
        else:
            print("Opção inválida.")
            pausa()


def ItsLeviOsa_not_LeviosAR():
    """Reproduz o easter egg musical de Harry Potter."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Não reinicia a música se ela já estiver tocando.
        if pygame.mixer.music.get_busy():
            return

        audio = Path(__file__).resolve().parent / "secrets" / "Ultra_Secret.mp3"

        pygame.mixer.music.load(str(audio))
        pygame.mixer.music.play()

    except (pygame.error, OSError) as erro:
        print(f"Erro ao reproduzir o easter egg: {erro}")


def parar_easter_egg():
    """Interrompe a reprodução do easter egg."""
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    except pygame.error as erro:
        print(f"Erro ao parar o easter egg: {erro}")


def registrar_atalhos():
    if keyboard is None:
        print("A biblioteca 'keyboard' não está instalada. Atalhos desativados.")
        print("Para instalar: pip install keyboard")
        pausa()
        return False

    try:
        keyboard.add_hotkey("alt+h+p", ItsLeviOsa_not_LeviosAR, suppress=True)
        keyboard.add_hotkey("alt+h+s", parar_easter_egg, suppress=True)
        return True

    except (ImportError, OSError) as erro:
        print(f"Atalhos de teclado indisponíveis: {erro}")
        pausa()
        return False


if __name__ == "__main__":
    atalhos_ativos = registrar_atalhos()

    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando o sistema...")
    finally:
        if atalhos_ativos:
            keyboard.unhook_all()
        pygame.mixer.quit()