from playwright.sync_api import Page
import pandas as pd

def lancar_mandado_pago(page: Page, linha, index, num_atual, total, pausa, caminho_arquivo, df_dados):
    """Lógica específica para preenchimento de mandados Pagos."""
    
    # PREENCHIMENTO VIA TECLADO (Padrão PAGOS)
    page.get_by_role("textbox", name="N° do Processo").click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha['PROCESSO']))
    page.keyboard.press("Tab")

    # MANDADO, DESTINATÁRIO, N.GRD
    page.keyboard.type(str(linha['MANDADO']))
    page.keyboard.press("Tab")
    page.keyboard.type(str(linha['DESTINATÁRIO']))
    page.keyboard.press("Tab")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha.get('N.GRD', '')))
    page.keyboard.press("Tab")

    # DATAS
    def preencher_data_pago(data):
        page.wait_for_timeout(300)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.type(str(data))
        page.keyboard.press("Tab")
        page.wait_for_timeout(100)
        page.keyboard.press("Tab")

    preencher_data_pago(linha['RECEB. OFICIAL'])
    preencher_data_pago(linha['RECEB. CENTRAL'])

    # VALOR
    page.wait_for_timeout(300)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(str(linha.get('VALOR', '0,00')))
    page.keyboard.press("Enter")

    # SALVAR OU NOVA INCLUSÃO
    page.wait_for_timeout(300)
    if num_atual == total:
        print(f"🏁 Último registro ({num_atual}/{total}) detectado.")
        page.get_by_role("button", name="Salvar e Fechar").click()
    else:
        print(f"✅ Registro {num_atual}/{total} concluído.")
        page.get_by_role("button", name="Nova Inclusão").click()

    # SALVAR PROGRESSO NO EXCEL
    df_dados.at[index, 'CONTROLE'] = 'S'
    try:
        df_dados.to_excel(caminho_arquivo, index=False)
        print(f"💾 Planilha salva: {linha['PROCESSO']}")
    except Exception:
        print(f"⚠️ Erro ao salvar planilha: feche o arquivo {caminho_arquivo}!")

    page.wait_for_timeout(pausa * 1000)