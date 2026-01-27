from imports import *

def filtrar_dados_saj(dados, meses_disponiveis):
    meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    while True:
        print(f"Meses disponíveis: {', '.join([meses_nomes[m-1] for m in meses_disponiveis])}")
        mes_numero_str = input(f"Entre apenas com o NÚMERO do mês desejado: ").strip()
        
        if mes_numero_str.isdigit():
            mes_numero = int(mes_numero_str)
            if mes_numero in meses_disponiveis: 
                mes_nome = meses_nomes[mes_numero - 1]
                break
            else:
                print(f"Erro: O mês {mes_nome} não possui dados na planilha selecionada.")
        else:
            print("Entrada inválida! Entre com um número inteiro válido.")
        
    print(f'Mês definido como: {mes_nome}')
    
    # apos selecionar o mes, eu pergunto se quer continuar ou se quer trocar...