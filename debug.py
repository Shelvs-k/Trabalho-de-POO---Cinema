import logging
from pathlib import Path
from datetime import datetime
import subprocess
import sys
import os

import colorama

colorama.just_fix_windows_console()

# --------------------------------------------------
# 1. Formatação dos registros
# --------------------------------------------------

class LocalizacaoFormatter(logging.Formatter):
    """Adiciona a localização aos avisos e erros."""

    def format(self, record):
        mensagem = super().format(record)

        if record.levelno >= logging.WARNING:
            localizacao = (
                f"{record.filename}:{record.lineno}"
                f" | função: {record.funcName}"
            )
            mensagem = f"{mensagem} | {localizacao}"

        return mensagem


class ColorFormatter(LocalizacaoFormatter):
    """Aplica cores aos registros exibidos no terminal."""

    CORES = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[37;41m",
    }

    RESET = "\033[0m"

    def format(self, record):
        mensagem = super().format(record)
        cor = self.CORES.get(record.levelno, self.RESET)

        return f"{cor}{mensagem}{self.RESET}"


# --------------------------------------------------
# 2. Logger central
# --------------------------------------------------

logger = logging.getLogger("cinema")
logger.setLevel(logging.DEBUG)
logger.propagate = False

log_ativo = False
arquivo_log_atual = None
processo_monitor = None


# --------------------------------------------------
# 3. Ativação do sistema de logs
# --------------------------------------------------


def ativar_logger():
    """Ativa o logger e abre o monitor de debug."""

    global log_ativo, arquivo_log_atual, processo_monitor

    if log_ativo:
        return logger

    pasta_logs = Path(__file__).resolve().parent / "logs"
    pasta_logs.mkdir(parents=True, exist_ok=True)

    nome_execucao = datetime.now().strftime(
        "cinema_%d-%m-%Y_%H-%M-%S.log"
    )

    arquivo_log_atual = pasta_logs / nome_execucao

    formato = "%(asctime)s | %(levelname)s | %(message)s"
    data_formato = "%d/%m/%Y %H:%M:%S"

    # Destino 1: terminal principal, com cores.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(
        ColorFormatter(formato, datefmt=data_formato)
    )

    # Destino 2: arquivo completo, incluindo DEBUG.
    arquivo = logging.FileHandler(
        arquivo_log_atual,
        encoding="utf-8"
    )
    arquivo.setLevel(logging.DEBUG)
    arquivo.setFormatter(
        LocalizacaoFormatter(formato, datefmt=data_formato)
    )

    logger.addHandler(console)
    logger.addHandler(arquivo)

    log_ativo = True
    logger.debug("Sistema de debug ativado.")

    # A segunda janela é criada em um novo console do Windows.
    if os.name == "nt":
        caminho_monitor = Path(__file__).resolve().parent / "debug_monitor.py"

        try:
            processo_monitor = subprocess.Popen(
                [
                    sys.executable,
                    str(caminho_monitor),
                    str(arquivo_log_atual)
                ],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=str(caminho_monitor.parent)
            )

            logger.info("Monitor de debug iniciado.")

        except OSError:
            logger.exception(
                "Não foi possível abrir o monitor de debug."
            )
    else:
        logger.warning(
            "A abertura automática do monitor está configurada "
            "somente para Windows."
        )
    return logger


def encerrar_monitor():
    """Encerra o processo do monitor, se estiver ativo."""

    global processo_monitor

    if processo_monitor is not None:
        if processo_monitor.poll() is None:
            processo_monitor.terminate()

        processo_monitor = None



# --------------------------------------------------
# 4. Testes executados somente diretamente
# --------------------------------------------------

if __name__ == "__main__":
    ativar_logger()

    logger.debug("Mensagem de teste DEBUG.")
    logger.info("Mensagem de teste INFO.")
    logger.warning("Mensagem de teste WARNING.")
    logger.error("Mensagem de teste ERROR.")
    logger.critical("Mensagem de teste CRITICAL.")
