import os
import time
from pathlib import Path
import pygame

# ============================ UTILITÁRIOS ============================ #

MUSIC_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg"}
MUSIC_DIRECTORY = Path(__file__).parent / "music"


def initialize_audio():
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def create_music_directory(directory):
    path = Path(directory)

    if path.exists() and not path.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    path.mkdir(parents=True, exist_ok=True)
    return path


def list_music_files(directory):
    path = Path(directory)

    if not path.is_dir():
        return []

    return sorted(
        (
            file for file in path.rglob("*")
            if file.is_file() and file.suffix.lower() in MUSIC_EXTENSIONS
        ),
        key=lambda file: str(file).lower(),
    )


def play_music(file_path, loop=True):
    initialize_audio()
    pygame.mixer.music.load(str(file_path))
    pygame.mixer.music.play(-1 if loop else 0)


def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("Pressione Enter para continuar...")


# =========================== FUNÇÕES PRINCIPAIS =========================== #


def main():
    music_directory = create_music_directory(MUSIC_DIRECTORY)
    tocando_agora = None

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
            print(f"\nNão foi possível reproduzir o arquivo: {erro}")

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