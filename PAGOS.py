from playwright.sync_api import sync_playwright
import pandas as pd
import os

def obter_dados():
    """Gerencia a escolha do arquivo e carrega os dados."""
    arquivos = [arq for arq in os.listdir() if arq.endswith(('.xlsx', '.csv'))]
    
    if not arquivos:
        print("Nenhum arquivo de dados encontrado.")
        return None, None, None

    print("\nArquivos disponíveis:")
    for i, arq in enumerate(arquivos, start=1):
        print(f"{i}. {arq}")

    while True:
        try:
            idx = int(input("Escolha o número do arquivo: "))
            # Verifica se o número está entre 1 e o total de arquivos na lista
            if 1 <= idx <= len(arquivos):
                idx = idx - 1
                break
            else:
                print(f"Número inválido! Escolha uma opção entre 1 e {len(arquivos)}.")
        except ValueError:
            print("Entrada inválida! Por favor, digite apenas números.")

    pausa = 4
    while True:
        entrada_pausa = input("Defina quantos segundos de pausa entre 5 e 9. Para 4 apenas pressione ENTER: ").strip()
        if entrada_pausa == "":
            break
        if entrada_pausa in ["5", "6", "7", "8", "9"]:
            pausa = int(entrada_pausa)
            break
        print("Entrada inválida! Digite um número de 0 a 1.")
    print(f'Número de JP definido como: {pausa}')

    pw = "@.3461@BHc"
    while True:
        input_pw = (input("Entre com sua nova senha, ou aperte ENTER para: @....Hc"))
        if input_pw == "":
            break
        else:
            pw = input_pw
            print(f"Senha alterada de [ {pw} ] para [ {input_pw} ]")
            break
    print(f"Entrando com a senha: {pw}")

    return pausa, pw, pd.read_excel(arquivos[idx], engine='calamine', header=0, dtype={'PROCESSO': str})

def realizar_login(pw, page):
    page.goto("https://www.tjsp.jus.br/atc/cdm/auth/login")
    page.get_by_role("button", name="Entrar com @tjsp.jus.br").click()
    page.get_by_role("textbox", name="someone@example.com").fill("robinsonp@tjsp.jus.br")
    page.get_by_role("button", name="Avançar").click()
    page.get_by_role("textbox", name="Senha").fill(pw)
    page.get_by_role("button", name="Entrar").click()
    print("Aguardando aprovação no Microsoft Authenticator...")
    
    # 1. Verifica se aparece a opção "Aprovar uma solicitação"
    try:
        # Timeout curto (5s) pois se não aparecer rápido, o sistema deve ter ido direto para o MFA
        page.get_by_role("button", name="Aprovar uma solicitação em").wait_for(state="visible", timeout=5000)
        page.get_by_role("button", name="Aprovar uma solicitação em").click()
        print("Botão de solicitação clicado. Verifique o Authenticator.")
    except:
        pass

    # 2. Processo de confirmação de permanência logado
    try:
        # Espera o checkbox de 'Não mostrar novamente' (indica que o MFA foi aprovado)
        page.get_by_role("checkbox", name="Não mostrar isso novamente").wait_for(state="visible", timeout=60000)
        page.get_by_role("checkbox", name="Não mostrar isso novamente").check()
        page.get_by_role("button", name="Sim").wait_for(state="visible", timeout=5000)
        page.get_by_role("button", name="Sim").click()
        page.get_by_text("Olá, ROBINSON BARBOSA").wait_for(state="visible", timeout=60000)
        print("Login realizado com sucesso!")
    except Exception as e:
        print("Ocorreu um erro ou o tempo de aprovação expirou.")
        raise e

def lancar_mandado(pausa, page, linha, num_atual, total):
    # INSERINDO PROCESSO
    page.get_by_role("textbox", name="N° do Processo").click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha['PROCESSO']))
    page.keyboard.press("Tab")

    # INSERINDO MANDADO
    page.keyboard.type(str(linha['MANDADO']))
    page.keyboard.press("Tab")

    # INSERINDO DESTINATÁRIO
    page.keyboard.type(str(linha['DESTINATÁRIO']))
    page.keyboard.press("Tab")

    # INSERINDO GUIA (N.GRD)
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha['N.GRD']))
    page.keyboard.press("Tab")

    # INSERINDO RECEB. OFICIAL
    page.wait_for_timeout(300)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha['RECEB. OFICIAL']))
    page.keyboard.press("Tab")
    page.wait_for_timeout(100)
    page.keyboard.press("Tab")

    # INSERINDO RECEB. CENTRAL
    page.wait_for_timeout(300)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha['RECEB. CENTRAL']))
    page.keyboard.press("Tab")
    page.wait_for_timeout(100)
    page.keyboard.press("Tab")

    page.wait_for_timeout(300)

    # INSERINDO VALOR
    page.wait_for_timeout(100)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha['VALOR']))
    page.keyboard.press("Enter")

    page.wait_for_timeout(300)
    if num_atual == total:
        print(f"Último registro ({num_atual}/{total}) detectado. Salvando e fechando...")
        page.get_by_role("button", name="Salvar e Fechar").click()
    else:
        print(f"Registro {num_atual}/{total} concluído. Abrindo nova inclusão...")
        page.get_by_role("button", name="Nova Inclusão").click()
    page.wait_for_timeout(pausa*1000) # Aguarda o sistema processar a transição
    
    print(f"Processo: {linha['PROCESSO']} incluído com sucesso!")

def iniciar_automacao():
    pausa, pw, df_dados = obter_dados()
    if df_dados is None: return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            realizar_login(pw, page)

            # Navegação inicial para Gratuitos
            page.get_by_role("link").nth(2).click()
            # page.get_by_role("tab", name="Gratuitos").click()
            print('Lançando em PAGOS')

            btn1 = page.get_by_role("button", name=" Adicionar Mandado").first # .first evita conflitos se houver dois na tela
            btn1.wait_for(state="visible", timeout=5000)
            if btn1.is_enabled():
                btn1.click()

            btn2 = page.get_by_label("Adicionar").get_by_role("button", name=" Adicionar Mandado")
            btn2.wait_for(state="visible", timeout=5000)
            if btn2.is_enabled():
                btn2.click()

            total_registros = len(df_dados)

            for index, linha in df_dados.iterrows():
                if linha['FORMA PAGAMENTO'] == 'JUSTIÇA PAGA':
                    print(f"Lançando processo: {linha['PROCESSO']}")
                    lancar_mandado(pausa, page, linha, index + 1, total_registros)
                else:
                    pass
            
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            page.wait_for_timeout(5000)
            #browser.close()

if __name__ == "__main__":
    iniciar_automacao()