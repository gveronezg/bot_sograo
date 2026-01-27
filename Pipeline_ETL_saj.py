from imports import *
from extrair_dados_saj import *
from transformar_dados_saj import *

# criando uma interface parecida com terminal de banco usando print()

print('''
    -----------------------------------
    -- Pipeline de ETL dos dados SAJ --
    -----------------------------------
''')

arquivos = identificar_arquivos_saj()
print('...')
listar_arquivos_saj(arquivos)
print('...')
saj = selecionar_arquivo_saj(arquivos)
print('...')
dados, meses_disponiveis = carregar_dados_saj(saj)
print('...')
