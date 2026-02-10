import pandas as pd
from pathlib import Path
from typing import List, Tuple
from constantes import config, logger

class ExtratorExcel:
    """Classe responsável pela extração e validação inicial de arquivos Excel."""

    def __init__(self, diretorio: str = "."):
        self.diretorio = Path(diretorio)

    def buscar_arquivos(self) -> List[Path]:
        """Localiza arquivos .xlsx de forma segura."""
        arquivos = sorted(self.diretorio.glob("*.xlsx"))
        if not arquivos:
            logger.error("Nenhum arquivo .xlsx encontrado no diretório.")
            raise FileNotFoundError("Nenhum relatório Excel (.xlsx) disponível.")
        return arquivos

    def selecionar_arquivo(self, arquivos: List[Path]) -> Path:
        """Gerencia a interação com o usuário para seleção do arquivo."""
        print("\n📂 Arquivos disponíveis:")
        for i, arq in enumerate(arquivos, 1):
            print(f"[{i}] {arq.name}")
            
        while True:
            try:
                escolha = int(input(f"\nSelecione o arquivo (1 a {len(arquivos)}): "))
                if 1 <= escolha <= len(arquivos):
                    return arquivos[escolha - 1]
                print(f"⚠️ Escolha entre 1 e {len(arquivos)}.")
            except ValueError:
                print("⚠️ Digite um número válido.")

    def carregar_e_validar(self, caminho: Path) -> pd.DataFrame:
        """Carrega o Excel e valida o schema mínimo esperado."""
        logger.info(f"Carregando: {caminho.name}")
        
        try:
            df = pd.read_excel(
                caminho, 
                engine=config.EXCEL_ENGINE, 
                header=config.HEADER_ROW,
                dtype={'Processo': str}
            )
        except Exception as e:
            logger.error(f"Falha ao ler arquivo Excel: {e}")
            raise

        # Validação de Schema
        if len(df.columns) < config.MIN_COLUMNS:
            raise ValueError(f"O arquivo {caminho.name} possui menos colunas ({len(df.columns)}) que o esperado.")
            
        if config.DATE_COLUMN not in df.columns:
            raise KeyError(f"Coluna obrigatória '{config.DATE_COLUMN}' não encontrada.")

        return df

def executar_extracao() -> Tuple[pd.DataFrame, List[int]]:
    """
    Função Wrapper que garante a extração de um arquivo válido.
    Permite múltiplas tentativas caso o arquivo selecionado seja inválido.
    """
    extrator = ExtratorExcel()
    arquivos = extrator.buscar_arquivos()
    
    while True:
        try:
            selecionado = extrator.selecionar_arquivo(arquivos)
            df = extrator.carregar_e_validar(selecionado)
            
            # Casting de data e metadados
            df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN], dayfirst=True)
            meses_disponiveis = sorted(df[config.DATE_COLUMN].dt.month.dropna().unique().astype(int).tolist())
            
            return df, meses_disponiveis
            
        except (ValueError, KeyError, Exception) as e:
            logger.warning(f"⚠️ O arquivo selecionado é inválido: {e}")
            print("\n" + "!"*100)
            print(f" ERRO NA ESTRUTURA: {e}")
            print(" Por favor, selecione outro relatório SAJ válido.")
            print("!"*100 + "\n")
            # O loop continua, permitindo nova seleção.
