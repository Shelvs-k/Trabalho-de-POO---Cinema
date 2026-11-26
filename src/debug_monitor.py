import os
import sys
import time
import re
from pathlib import Path

try:
    import colorama
except ImportError:
    colorama = None

# A colorama é opcional: ela só ajuda o console do Windows a exibir as cores.
if colorama is not None:
    if hasattr(colorama, "just_fix_windows_console"):
        colorama.just_fix_windows_console()  # colorama 0.4.6 ou superior
    else:
        colorama.init()
elif os.name == "nt":
    os.system("")  # habilita sequências ANSI no Windows 10 ou superior

RESET = "\033[0m"

CORES = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[37;41m",
}

# Um registro novo começa com "data hora | NÍVEL |". Linhas que não começam
# assim (como as de um traceback) continuam o registro anterior.
PADRAO_NIVEL = re.compile(
    r"^\S+ \S+ \| (DEBUG|INFO|WARNING|ERROR|CRITICAL) \|"
)

cor_atual = ""


def imprimir_linha_colorida(linha):
    """Aplica uma cor à linha conforme o nível do registro."""
    global cor_atual

    resultado = PADRAO_NIVEL.match(linha)

    if resultado:
        cor_atual = CORES.get(resultado.group(1), "")

    if cor_atual:
        print(f"{cor_atual}{linha.rstrip()}{RESET}", flush=True)
    else:
        print(linha.rstrip(), flush=True)

def monitorar_log(caminho_log):
    arquivo_log = Path(caminho_log)

    print("=" * 70)
    print("       MONITOR DE DEBUG | SISTEMA DE CINEMA")
    print("=" * 70)
    print(f"Arquivo monitorado: {arquivo_log}")
    print("Aguardando registros...")
    print("=" * 70, flush=True)

    while not arquivo_log.exists():
        time.sleep(0.1)

    with arquivo_log.open("r", encoding="utf-8") as arquivo:
        # Exibe os registros que já existem no arquivo.
        for linha in arquivo:
            imprimir_linha_colorida(linha)

        # Continua acompanhando os novos registros em tempo real.
        while True:
            linha = arquivo.readline()

            if linha:
                imprimir_linha_colorida(linha)
            else:
                time.sleep(0.1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: nenhum arquivo de log foi informado.")
        input("Pressione Enter para fechar...")
        raise SystemExit(1)
    try:
        monitorar_log(sys.argv[1])
    except KeyboardInterrupt:
        print(f"\n{RESET}Monitor de debug encerrado.")
