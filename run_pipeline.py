"""
run_pipeline.py
---------------
Orquestrador do pipeline de dados Olist.

Executa os notebooks na ordem correta:
    1. extract.ipynb   — leitura dos CSVs brutos
    2. transform.ipynb — limpeza e transformação
    3. load.ipynb      — carga no PostgreSQL
    4. analise.ipynb   — análise exploratória e gráficos

Uso:
    python run_pipeline.py
    python run_pipeline.py --only etl
    python run_pipeline.py --only analise
"""

import subprocess
import sys
import logging
import argparse
import time
from pathlib import Path


# ── Configuração de logging ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


# ── Definição dos notebooks ────────────────────────────────────────────────────
NOTEBOOKS_ETL = [
    Path("notebooks/ETL/extract.ipynb"),
    Path("notebooks/ETL/transform.ipynb"),
    Path("notebooks/ETL/load.ipynb"),
]

NOTEBOOKS_ANALISE = [
    Path("notebooks/analise.ipynb"),
]

NOTEBOOKS_COMPLETO = NOTEBOOKS_ETL + NOTEBOOKS_ANALISE

# Tempo máximo de execução por notebook em segundos (10 minutos)
TIMEOUT = 600


# ── Funções ────────────────────────────────────────────────────────────────────

def validar_notebooks(notebooks: list[Path]) -> None:
    """
    Verifica se todos os notebooks existem antes de iniciar o pipeline.
    Lança FileNotFoundError se algum arquivo estiver faltando.
    """
    arquivos_faltando = [nb for nb in notebooks if not nb.exists()]

    if arquivos_faltando:
        for arquivo in arquivos_faltando:
            logger.error(f"Notebook não encontrado: {arquivo}")
        raise FileNotFoundError(
            f"{len(arquivos_faltando)} notebook(s) não encontrado(s). "
            "Verifique a estrutura do projeto."
        )

    logger.info(f"{len(notebooks)} notebook(s) validado(s) com sucesso.")


def executar_notebook(notebook: Path) -> None:
    """
    Executa um notebook Jupyter via nbconvert.

    Parâmetros:
        notebook: caminho para o arquivo .ipynb

    Lança:
        RuntimeError se o notebook falhar durante a execução.
    """
    logger.info(f"Iniciando: {notebook}")
    inicio = time.time()

    resultado = subprocess.run(
        [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            f"--ExecutePreprocessor.timeout={TIMEOUT}",
            notebook.name,  # apenas o nome, pois cwd já define o diretório
        ],
        capture_output=True,
        text=True,
        cwd=str(notebook.parent.resolve()),
    )

    duracao = round(time.time() - inicio, 1)

    if resultado.returncode != 0:
        logger.error(f"Falha ao executar: {notebook} ({duracao}s)")
        logger.error(f"Detalhes do erro:\n{resultado.stderr}")
        raise RuntimeError(
            f"Notebook falhou: {notebook}\n"
            f"Verifique o arquivo pipeline.log para mais detalhes."
        )

    logger.info(f"Concluído: {notebook} ({duracao}s)")


def executar_pipeline(notebooks: list[Path]) -> None:
    """
    Executa uma lista de notebooks em sequência.
    Interrompe imediatamente se qualquer notebook falhar.

    Parâmetros:
        notebooks: lista ordenada de notebooks a executar
    """
    logger.info("=" * 55)
    logger.info("PIPELINE OLIST — INICIANDO")
    logger.info("=" * 55)

    inicio_total = time.time()

    # Valida existência dos arquivos antes de começar
    validar_notebooks(notebooks)

    # Executa cada notebook na ordem definida
    for i, notebook in enumerate(notebooks, start=1):
        logger.info(f"[{i}/{len(notebooks)}] {notebook.name}")
        try:
            executar_notebook(notebook)
        except RuntimeError as erro:
            logger.error(str(erro))
            logger.error("Pipeline interrompido.")
            sys.exit(1)

    duracao_total = round(time.time() - inicio_total, 1)

    logger.info("=" * 55)
    logger.info(f"PIPELINE CONCLUÍDO COM SUCESSO ({duracao_total}s)")
    logger.info("=" * 55)


# ── Interface de linha de comando ──────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """
    Define e processa os argumentos de linha de comando.

    Opções:
        --only etl     → executa apenas os notebooks de ETL
        --only analise → executa apenas o notebook de análise
        (sem --only)   → executa o pipeline completo
    """
    parser = argparse.ArgumentParser(
        description="Orquestrador do pipeline de dados Olist.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--only",
        choices=["etl", "analise"],
        default=None,
        help=(
            "Executa apenas parte do pipeline:\n"
            "  etl     → extract + transform + load\n"
            "  analise → apenas a análise exploratória\n"
            "(padrão: pipeline completo)"
        ),
    )
    return parser.parse_args()


# ── Entrada principal ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = parse_args()

    # Seleciona quais notebooks executar com base no argumento --only
    if args.only == "etl":
        notebooks_selecionados = NOTEBOOKS_ETL
        logger.info("Modo selecionado: apenas ETL")
    elif args.only == "analise":
        notebooks_selecionados = NOTEBOOKS_ANALISE
        logger.info("Modo selecionado: apenas análise")
    else:
        notebooks_selecionados = NOTEBOOKS_COMPLETO
        logger.info("Modo selecionado: pipeline completo")

    executar_pipeline(notebooks_selecionados)
