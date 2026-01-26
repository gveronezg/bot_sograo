import os
import pandas as pd

print('----------------------------------------------------------------------------------------------------')
print('Bem vindo Sogrão!')
print('----------------------------------------------------------------------------------------------------')

def iniciar():
    # Lendo os arquivos presentes na pasta atual ignorando arquivos desnecessários
    arquivos = [arq for arq in os.listdir() if not arq.endswith(('.ipynb', '.venv', '.py', '.git', '.txt', '.exe'))]

    print("Arquivos disponíveis para processamento:")
    for i, arq in enumerate(arquivos, start=1):
        print(f"{i}. {arq}")
    print('----------------------------------------------------------------------------------------------------')
    while True:
        try:
            saj = int(input("Entre com o número do relatório SAJ a ser transformado: ")) - 1
            arquivo_selecionado = arquivos[saj]
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Digite um número válido da lista.")
    print('----------------------------------------------------------------------------------------------------')
    dados = pd.read_excel(arquivo_selecionado, engine='calamine', header=2, dtype={'Processo': str}) 
    
    # Validações iniciais
    try:
        assert len(dados.columns) >= 7, "Número de colunas menor que 7!"
    except AssertionError:
        print("Erro: O arquivo selecionado não parece conter o padrão esperado do SAJ.")
        exit(1)
        
    # Processamento dos meses disponíveis
    dados['Receb. central'] = pd.to_datetime(dados['Receb. central'], dayfirst=True)
    meses_disponiveis = sorted(dados['Receb. central'].dt.month.unique().tolist())
    
    print(f'Dados carregados com sucesso num total de {len(dados)} linhas e {len(dados.columns)} colunas.')
    print(f'Meses identificados na tabela, disponiveis para filtragem: {meses_disponiveis}')
    print('----------------------------------------------------------------------------------------------------')

    return dados, meses_disponiveis

def parametrizar(meses_disponiveis):

    # 1º Solicitando o mês para referência
    meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    while True:
        print(f"Meses disponíveis: {', '.join([meses_nomes[m-1] for m in meses_disponiveis])}")
        mes_numero_str = input(f"Entre apenas com o NÚMERO do mês desejado: ").strip()
        
        if mes_numero_str.isdigit():
            mes_numero = int(mes_numero_str)
            # Verifica se o mês digitado está na lista de meses disponíveis
            if mes_numero in meses_disponiveis: 
                mes_nome = meses_nomes[mes_numero - 1]
                break
            else:
                print(f"Erro: O mês {mes_nome} não possui dados na planilha selecionada.")
        else:
            print("Entrada inválida! Entre com um número inteiro válido.")
            
    print(f'Mês definido como: {mes_nome}')
    print('----------------------------------------------------------------------------------------------------')

    # 2º Solicitando o valor da cota
    cota = 111.06
    while True:
        entrada_cota = input(f"Entre com o valor da cota atual.\nOu apenas pressione ENTER para R${cota}: ").strip().replace(',', '.')
        if entrada_cota == "":
            break
        if entrada_cota.replace('.', '', 1).isdigit():
            valor_digitado = float(entrada_cota)
            if valor_digitado >= 0:
                cota = valor_digitado
                break
        else:
            print("Entrada inválida! Digite apenas números positivos, ponto ou vírgula.")
    print(f'Valor da cota definido como: R${cota:.2f}')
    print('----------------------------------------------------------------------------------------------------')

    # 3º Solicitando o valor do JG
    JG = 1
    while True:
        entrada_JG = input("Entre com 0 para o valor de JG.\nOu apenas pressione ENTER para 1: ").strip()
        if entrada_JG == "":
            break
        if entrada_JG in ["0", "1"]:
            JG = int(entrada_JG)
            break
        print("Entrada inválida! Digite um número de 0 a 1.")
    print(f'Número de JG definido como: {JG}')
    print('----------------------------------------------------------------------------------------------------')

    # 4º Solicitando o valor de deslocamento
    deslocamento = 'S'
    while True:
        entrada_deslocamento = input("Entre com 'N' para o valor de deslocamento.\nOu apenas pressione ENTER para 'S': ").strip().upper()
        if entrada_deslocamento == "":
            break
        elif entrada_deslocamento in ['N', 'S']:
            deslocamento = entrada_deslocamento
            break
        print("Entrada inválida! Entre com N ou S.")
    print(f'Deslocamento definido como: {deslocamento}')
    print('----------------------------------------------------------------------------------------------------')

    return mes_numero, cota, JG, deslocamento

def transformar(mes_numero, dados):

    print('Tratando os dados...')

    # 1. Converter a coluna original para datetime para poder filtrar pelo mês
    dados['Receb. central'] = pd.to_datetime(dados['Receb. central'], dayfirst=True)

    # 2. Filtrar os dados: mantém apenas onde o mês é igual ao mes_numero informado
    dados_filtrados = dados[dados['Receb. central'].dt.month == int(mes_numero)].copy()

    if dados_filtrados.empty:
        print(f"Aviso: Nenhum dado encontrado para o mês {mes_numero}.")
        # Retorna um DataFrame vazio com as colunas corretas se não houver dados
        return pd.DataFrame(columns=['PROCESSO', 'MANDADO', 'DESTINATÁRIO', 'RECEB. OFICIAL', 'RECEB. CENTRAL', 'N.GRD', 'FORMA PAGAMENTO', 'VALOR', 'COTA', 'DESLOCAMENTO', 'REGRA ESPECIAL', 'CONTROLE'])

    tratados = pd.DataFrame()

    # Setando dados na coluna 'PROCESSO'
    tratados['PROCESSO'] = (
        dados['Processo']
        .astype(str)                        # Garante que é string para manipular
        .str.replace(r'\D', '', regex=True) # Remove TUDO que não for número (ponto, traço, espaço)
        .str.zfill(20)                      # Preenche com 0 à esquerda até completar 20
    )

    # Setando dados na coluna 'MANDADO'
    def formatar_mandado(numero):
        """Formata 14 dígitos para formato CNJ: 123.4567/890123-4"""
        string = str(numero).replace('.', '').replace('-', '').replace('/', '').strip()
        if len(string) == 14:
            return f"{string[:3]}.{string[3:7]}/{string[7:13]}-{string[13:]}"
        return string
    tratados['MANDADO'] = dados['Mandado'].apply(formatar_mandado)

    # Setando dados na coluna 'DESTINATÁRIO'
    tratados['DESTINATÁRIO'] = (dados['Destinatário'].astype(str).str.strip().str.upper())

    # Setando dados na coluna 'RECEB. OFICIAL'
    tratados['RECEB. OFICIAL'] = (pd.to_datetime(dados['Receb. oficial'], dayfirst=True).dt.strftime('%d/%m/%Y').astype('string'))

    # Setando dados na coluna 'RECEB. CENTRAL'
    tratados['RECEB. CENTRAL'] = (pd.to_datetime(dados['Receb. central'], dayfirst=True).dt.strftime('%d/%m/%Y').astype('string'))

    # Setando dados na coluna 'N.GRD'
    tratados['N.GRD'] = dados['Guia de Recolhimento'].astype('string').str.strip()

    # Setando dados na coluna 'FORMA PAGAMENTO'
    tratados['FORMA PAGAMENTO'] = (dados['Forma de pagamento'].map({'Justiça Gratuita': 'JUSTIÇA GRATUITA','Justiça Paga': 'JUSTIÇA PAGA'}).fillna('JUSTIÇA PAGA').astype('string').str.strip())

    # Setando dados na coluna 'VALOR'
    tratados['VALOR'] = tratados['FORMA PAGAMENTO'].map({'JUSTIÇA GRATUITA': '0,00','JUSTIÇA PAGA': f"{float(cota):.2f}".replace('.', ',')}).fillna(f"{float(cota):.2f}".replace('.', ',')).astype('string')

    # Setando dados na coluna 'JG'
    tratados['COTA'] = str(int(JG))

    # Setando dados na coluna 'DESLOCAMENTO'
    tratados['DESLOCAMENTO'] = deslocamento

    # Setando dados na coluna 'REGRA ESPECIAL'
    tratados['REGRA ESPECIAL'] = 'N'

    # Setando dados na coluna 'CONTROLE'
    tratados['CONTROLE'] = 'N'

    # Setando dados na coluna 'CONFERE'
    tratados['CONFERE'] = 'O'

    print('Finalizando o tratamento dos dados.')

    return tratados

if __name__ == "__main__":
    dados, meses_disponiveis = iniciar()
    mes_numero, cota, JG, deslocamento = parametrizar(meses_disponiveis)
    tratados = transformar(mes_numero, dados)

    # Salvando o arquivo tratado em xlsx com o nome da variável mes_nome
    nome_arquivo = f'Dados_Tratados_do_Mês_{mes_numero}.xlsx'
    tratados.to_excel(nome_arquivo, index=False)
    print(f'Dados tratados e salvos em novo arquivo.xlsx chamado: {nome_arquivo}')