from playwright.sync_api import Page
import pandas as pd

def lancar_mandado_gratuito(page: Page, linha, index, num_atual, total, pausa, caminho_arquivo, df_dados):
    """Lógica específica para preenchimento de mandados Gratuitos."""
    
    # INSERINDO PROCESSO, MANDADO E DESTINATÁRIO
    page.get_by_role("textbox", name="N° do Processo").fill(str(linha['PROCESSO']))
    page.get_by_role("textbox", name="N° do Mandado").fill(str(linha['MANDADO']))
    page.get_by_role("textbox", name="Nome do Destinatário").fill(str(linha['DESTINATÁRIO']))
    
    # DATAS
    def preencher_data(selector, data):
        page.locator(selector).click()
        page.wait_for_timeout(100)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.type(str(data))
        page.keyboard.press("Enter")

    preencher_data("#dataCarga input", linha['RECEB. OFICIAL'])
    page.wait_for_timeout(300)
    preencher_data("#dataDevolucao input", linha['RECEB. CENTRAL'])

    # DESLOCAMENTO E COTAS
    page.wait_for_timeout(300)
    if linha['DESLOCAMENTO'] == "S":
        page.locator(".p-inputswitch-slider").first.click()
        if linha['COTA'] == 0:
            page.wait_for_timeout(300)
            page.locator(".p-radiobutton-box").first.click()
        if linha['REGRA ESPECIAL'] == "S":
            page.wait_for_timeout(300)
            page.locator(".item.ml-6 > .flex > .p-element.ng-untouched > .p-inputswitch > .p-inputswitch-slider").click()
    else:
        page.locator(".p-inputswitch-slider").last.click()
        if linha['COTA'] == 0:
            page.wait_for_timeout(300)
            page.locator(".flex.items-center.ml-\\[96px\\] > .p-element.ng-valid > .p-radiobutton > .p-radiobutton-box").click()

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
    except PermissionError:
        print(f"⚠️ Erro ao salvar planilha: feche o arquivo {caminho_arquivo}!")

    page.wait_for_timeout(pausa * 1000)