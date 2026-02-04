import pandas as pd
from pathlib import Path
from constantes import logger

class CarregadorExcel:
    """Lógica para salvar e exportar dados processados."""

    @staticmethod
    def para_excel(df: pd.DataFrame, mes_nome: str):
        """Salva o DataFrame final em um arquivo Excel."""
        if df.empty:
            logger.warning("Nenhum dado para salvar.")
            return

        try:
            # Nome do arquivo profissional: Dados_Tratados_Mes.xlsx
            nome_arquivo = f"Dados_Tratados_{mes_nome}.xlsx"
            caminho_saida = Path(nome_arquivo).resolve()
            
            df.to_excel(caminho_saida, index=False)
            
            logger.info(f"💾 Carga concluída: {len(df)} registros processados.")
            logger.info(f"📍 Arquivo salvo em: {caminho_saida}")
            
            print("\n" + "="*60)
            print(f" ✅ SUCESSO! Arquivo gerado: {nome_arquivo}")
            print(f" 📊 Total de linhas: {len(df)}")
            print("="*60 + "\n")
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {e}")
            raise

def executar_carga(df: pd.DataFrame, mes_nome: str):
    """Entrypoint para etapa de Load."""
    CarregadorExcel.para_excel(df, mes_nome)
