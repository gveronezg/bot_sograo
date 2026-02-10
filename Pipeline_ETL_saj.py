import sys
from constantes import logger
from extrator import executar_extracao
from transformador import executar_transformacao
from carregador import executar_carga

# Orquestrador Principal
def main():
    """
    Gerencia o ciclo de vida completo do ETL com tratamento de erros global.
    """
    
    print("\n" + "="*100)
    print("                                    PIPELINE DE DADOS SAJ")
    print("="*100)

    try:
        # Step 1: Extract
        logger.info("Iniciando Etapa de Extração...")
        df_bruto, meses_disponiveis = executar_extracao()
        
        # Step 2: Transform
        logger.info("Iniciando Etapa de Transformação...")
        df_limpo, mes_nome = executar_transformacao(df_bruto, meses_disponiveis)
        
        # Step 3: Load
        logger.info("Iniciando Etapa de Carga...")
        executar_carga(df_limpo, mes_nome)

        print("\n" + "="*100)
        logger.info("                  ETL FINALIZADO COM SUCESSO.")
        print("="*100 + "\n")

    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Erro de Validação de Dados: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Falha Inesperada no Pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
