import sys
from playwright.sync_api import sync_playwright
import bot_utils
from GRATUITOS import lancar_mandado_gratuito
from PAGOS import lancar_mandado_pago

def main():
    print("\n" + "="*80)
    print("                      ROBÔ SOGRÃO - AUTOMAÇÃO TJSP")
    print("="*80 + "\n")

    # 1. Configurações Iniciais
    res = bot_utils.selecionar_arquivo_e_dados()
    if res[0] is None: return
    caminho_arquivo, df_dados = res[0], res[1]

    pw, pausa = bot_utils.obter_configuracoes_execucao()
    
    tipo_processamento = input("\nTipo de Processamento: [1] GRATUITOS [2] PAGOS: ").strip()
    if tipo_processamento not in ["1", "2"]:
        print("❌ Opção inválida. Encerrando.")
        return

    # 2. Início do Navegador
    with sync_playwright() as p:
        browser, page = bot_utils.configurar_navegador(p)

        try:
            # Login Centralizado
            bot_utils.realizar_login(page, pw)

            # Navegação conforme escolha
            print('📍 Navegando para Central de Mandados...')
            page.get_by_role("link").nth(2).click()
            
            if tipo_processamento == "1":
                page.get_by_role("tab", name="Gratuitos").click()
                print('🚀 Lançando em GRATUITOS...')
                filtro = 'JUSTIÇA GRATUITA'
                func_lancar = lancar_mandado_gratuito
            else:
                print('🚀 Lançando em PAGOS...')
                filtro = 'JUSTIÇA PAGA'
                func_lancar = lancar_mandado_pago

            # Botões de Inclusão
            btn1 = page.get_by_role("button", name=" Adicionar Mandado").first
            btn1.wait_for(state="visible", timeout=60000)
            btn1.click()

            # Extrai o MM_AAAA do nome do arquivo
            import re
            match = re.search(r"(\d{2})_(\d{4})", caminho_arquivo)
            mes_ano_portal = ""
            if match:
                mes_ano_portal = f"{match.group(1)}/{match.group(2)}"
                print(f"📅 Mês/Ano detectado no arquivo: {mes_ano_portal}")

            # seleciona o campo de mes para lancamentos
            page.get_by_role("combobox", name="mm/aaaa").click()
            # control + a para selecionar todo o texto
            page.keyboard.press("Control+A")
            # apaga o texto selecionado
            page.keyboard.press("Delete")
            # entra com o mes e ano do definido no nome do arquivo
            if mes_ano_portal:
                page.keyboard.type(mes_ano_portal)
                page.keyboard.press("Enter")

            btn2 = page.get_by_label("Adicionar").get_by_role("button", name=" Adicionar Mandado")
            btn2.wait_for(state="visible", timeout=5000)
            btn2.click()

            # 3. Loop de Processamento Centralizado
            total_registros = len(df_dados[df_dados['FORMA PAGAMENTO'] == filtro])
            if total_registros == 0:
                print(f"⚠️ Nenhum registro do tipo {filtro} encontrado.")
                return

            contador = 1
            for index, linha in df_dados.iterrows():
                # Processa apenas o tipo selecionado e que ainda (não) foi enviado
                if linha['FORMA PAGAMENTO'] == filtro and linha.get('CONTROLE') != 'S':
                    print(f"[{contador}/{total_registros}] Processo: {linha['PROCESSO']}")
                    
                    # Chama o especialista correto
                    func_lancar(page, linha, index, contador, total_registros, pausa, caminho_arquivo, df_dados)
                    contador += 1
                else:
                    # Pula quem já foi enviado ou não é do tipo
                    pass
            
            print("\n✅ TAREFA CONCLUÍDA COM SUCESSO!")
            
        except Exception as e:
            print(f"\n❌ ERRO FATAL: {e}")
        finally:
            print("\nEncerrando em 5 segundos...")
            page.wait_for_timeout(5000)
            browser.close()

if __name__ == "__main__":
    main()
