import sys
import time
import re
from pathlib import Path

import colorama
from colorama import Fore, Back, Style

colorama.just_fix_windows_console()

CORES = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Back.RED + Fore.WHITE,
}

PADRAO_NIVEL = re.compile(
    r"\|\s*(DEBUG|INFO|WARNING|ERROR|CRITICAL)\s*\|"
)

def imprimir_linha_colorida(linha):
    """Aplica uma cor à linha conforme o nível do registro."""
    resultado = PADRAO_NIVEL.search(linha)

    if resultado:
        nivel = resultado.group(1)
        cor = CORES.get(nivel, "")
        print(f"{cor}{linha.rstrip()}{Style.RESET_ALL}", flush=True)
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
        print(f"\n{Style.RESET_ALL}Monitor de debug encerrado.")
