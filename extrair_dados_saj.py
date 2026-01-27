from imports import *

def identificar_arquivos_saj():
    print('Iniciando o processo de identificação dos arquivos SAJ no diretório atual.')
    arquivos = [arq for arq in os.listdir() if arq.endswith(('.xlsx'))]
    return arquivos

def listar_arquivos_saj(arquivos):
    print('Listando os arquivos encontrados:')
    print('...')
    if arquivos:        
        print("Arquivos disponíveis para processamento:")
        for i, arq in enumerate(arquivos, start=1):
            print(f"{i}. {arq}")
    else:
        print("Nenhum arquivo SAJ.xslx encontrado no diretório atual!")
        exit(1) # Encerra o programa se nenhum arquivo for encontrado
        
def selecionar_arquivo_saj(arquivos):
    while True:
        try:
            saj = int(input("Entre com o número do relatório SAJ a ser transformado: "))
            if 1 <= saj <= len(arquivos):
                arquivo_selecionado = arquivos[saj - 1]
                break
            else:
                print(f"Número inválido! Escolha uma opção entre 1 e {len(arquivos)}.")
        except ValueError:
            print("Entrada inválida! Por favor, digite apenas o número do arquivo.")
    return arquivo_selecionado

def carregar_dados_saj(arquivo_selecionado):
    dados = pd.read_excel(arquivo_selecionado, engine='calamine', header=2, dtype={'Processo': str}) 
    try:
        assert len(dados.columns) >= 7, "Número de colunas menor que 7!"
    except AssertionError:
        print("Erro: O arquivo selecionado não parece conter o padrão esperado do SAJ.")
        exit(1)
    dados['Receb. central'] = pd.to_datetime(dados['Receb. central'], dayfirst=True)
    meses_disponiveis = sorted(dados['Receb. central'].dt.month.unique().tolist())
    print(f'Dados carregados com sucesso num total de {len(dados)} linhas e {len(dados.columns)} colunas.')
    print(f'Meses identificados na tabela, disponiveis para filtragem: {meses_disponiveis}')
    print
    return dados, meses_disponiveis