import logging
from dataclasses import dataclass

# Configuração de Logging Profissional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

@dataclass(frozen=True)
class PipelineConfig:
    """Configurações imutáveis do pipeline (Data Class)."""
    HEADER_ROW: int = 2
    MIN_COLUMNS: int = 7
    EXCEL_ENGINE: str = 'calamine'
    REQUIRED_COLUMNS: tuple = ('Receb. central',)
    DATE_COLUMN: str = 'Receb. central'
    
    MESES_NOMES: tuple = (
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    )

config = PipelineConfig()
logger = logging.getLogger("ETL-SAJ")