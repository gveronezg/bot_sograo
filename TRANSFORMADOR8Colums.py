import os
import pandas as pd

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
            saj = int(input("Entre com o número do arquivo SAJ a ser transformado: ")) - 1
            arquivo_selecionado = arquivos[saj]
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Digite um número válido da lista.")

    print('----------------------------------------------------------------------------------------------------')
    
    # Forçar a leitura da coluna 'Processo' como texto desde o início
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
        print(f"\nMeses disponíveis: {', '.join([meses_nomes[m-1] for m in meses_disponiveis])}")
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

    # ... (Restante da função parametrizar para Cota, JG e Deslocamento) ...
    # (Mantenha o código original dessas partes)
    cota = 111.06
    # ... (lógica while True para cota) ...
    JG = 1
    # ... (lógica while True para JG) ...
    deslocamento = 'S'
    # ... (lógica while True para deslocamento) ...

    return str(mes_numero), cota, JG, deslocamento

# ... (Mantenha a função transformar como ajustada anteriormente, usando dados_filtrados) ...
def transformar(mes_numero, dados):
    # ... (código da função transformar) ...
    pass # Substitua esta linha pelo seu código completo da função transformar

if __name__ == "__main__":
    # Inicia e já recebe os dados completos e a lista de meses disponíveis
    dados_completos, meses_disponiveis = iniciar() 
    
    # Passa a lista de meses disponíveis para a função parametrizar fazer a validação
    mes_numero, cota, JG, deslocamento = parametrizar(meses_disponiveis)
    
    # Chama a função transformar com os dados completos, que fará a filtragem interna
    tratados = transformar(mes_numero, dados_completos)

    # Salvando o arquivo tratado
    nome_arquivo = f'Dados_Tratados_do_Mês_{mes_numero}.xlsx'
    tratados.to_excel(nome_arquivo, index=False)
