import os
import time
from pathlib import Path
import pygame
import debug

def registrar_log(nivel, mensagem):
    """Registra um evento somente quando o modo debug está ativo."""
    if not debug.log_ativo:
        return

    metodo = getattr(debug.logger, nivel)
    metodo(mensagem, stacklevel=2)

# ============================ UTILITÁRIOS ============================ #

MUSIC_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg"}
MUSIC_DIRECTORY = Path(__file__).parent / "music"



def initialize_audio():
    if not pygame.mixer.get_init():
        registrar_log("debug", "Inicializando mixer do Pygame.")
        try:
            pygame.mixer.init()
        except pygame.error:
            registrar_log(
                "exception",
                "Falha ao inicializar o mixer do Pygame."
            )
            raise
        registrar_log(
            "debug",
            "Mixer do Pygame inicializado com sucesso."
        )



def create_music_directory(directory):
    path = Path(directory)
    if path.exists() and not path.is_dir():
        registrar_log(
            "error",
            f"Falha ao criar diretório de músicas: "
            f"{path} não é um diretório."
        )
        raise NotADirectoryError(
            f"'{path}' is not a directory."
        )
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        registrar_log(
            "exception",
            f"Não foi possível criar ou acessar o diretório: {path}"
        )
        raise
    registrar_log(
        "debug",
        f"Diretório de músicas verificado: {path}"
    )
    return path


def list_music_files(directory):
    path = Path(directory)
    registrar_log(
        "debug",
        f"Iniciando listagem de músicas em: {path}"
    )
    if not path.is_dir():
        registrar_log(
            "warning",
            f"Listagem cancelada: {path} não é um diretório."
        )
        return []
    try:
        music_files = sorted(
            (
                file for file in path.rglob("*")
                if file.is_file()
                and file.suffix.lower() in MUSIC_EXTENSIONS
            ),
            key=lambda file: str(file).lower(),
        )
        registrar_log(
            "info",
            f"Listagem concluída: {len(music_files)} "
            f"arquivo(s) de música encontrado(s)."
        )
        return music_files
    except OSError:
        registrar_log(
            "exception",
            f"Falha ao listar músicas no diretório: {path}"
        )
        raise


def play_music(file_path, loop=True):
    registrar_log(
        "debug",
        f"Tentando reproduzir: {file_path}"
    )
    initialize_audio()
    pygame.mixer.music.load(str(file_path))
    pygame.mixer.music.play(-1 if loop else 0)
    registrar_log(
        "info",
        f"Música iniciada: {file_path.name}. "
        f"Loop: {'ativado' if loop else 'desativado'}."
    )



def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        registrar_log(
            "info",
            "Reprodução da música interrompida."
        )
    else:
        registrar_log(
            "debug",
            "Solicitação de parada ignorada: mixer não inicializado."
        )


def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("Pressione Enter para continuar...")


# =========================== FUNÇÕES PRINCIPAIS =========================== #


def main():
    music_directory = create_music_directory(MUSIC_DIRECTORY)
    tocando_agora = None
    registrar_log("info", "Reprodutor de músicas iniciado")
    while True:
        limpar_terminal()
        print("#====================================#")
        print("| BEM-VINDO AO REPRODUTOR DE MÚSICA! |")
        print("|====================================|")
        print("|                                    |")
        print("|  Selecione uma música para tocar:  |")
        print("|                                    |")
        print("#====================================#")
        print("\n AVISO ⚠️ : O programa suporta arquivos .ogg, mas podem ocorrer erros.")

        music_files = list_music_files(music_directory)

        if not music_files:
            print("\nFaltam as músicas...")
            time.sleep(1)
            print(f"Coloque arquivos de música na pasta localizada em '{music_directory}'.")
            print("\nEnter — Tentar novamente")
            print("0 — Sair")

            if input("\nSua escolha: ").strip() == "0":
                break
            continue

        if tocando_agora and pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            print(f"\n♪ Tocando agora: {tocando_agora}")

        print()
        for index, music in enumerate(music_files, start=1):
            print(f"{index}. {music.name}")

        print("\n0. Sair")
        print("S. Parar a música atual")

        escolha = input("\nSua escolha: ").strip().lower()

        if escolha == "0":
            break

        if escolha == "s":
            stop_music()
            tocando_agora = None
            continue

        try:
            indice = int(escolha) - 1
        except ValueError:
            print("\nDigite um número válido.")
            pause()
            continue

        if not 0 <= indice < len(music_files):
            print("\nIsso não é uma opção...")
            pause()
            continue

        musica_selecionada = music_files[indice]

        try:
            play_music(musica_selecionada)
            tocando_agora = musica_selecionada.name
            print(f"\nTocando em loop: {tocando_agora}")
        except pygame.error as erro:
            registrar_log(
                "exception",
                f"Falha ao reproduzir "
                f"{musica_selecionada.name}: {erro}"
            )
            print(
                f"\nNão foi possível reproduzir o arquivo: {erro}"
            )

        pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAté logo!")
    finally:
        stop_music()
        if pygame.mixer.get_init():
            pygame.mixer.quit()