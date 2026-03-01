import os
import pandas as pd
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def configurar_navegador(p):
    """Inicializa o browser e a página."""
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    return browser, page

def selecionar_arquivo_e_dados():
    """Gerencia a escolha do arquivo e carregamento do DataFrame."""
    arquivos = [arq for arq in os.listdir() if arq.endswith(('.xlsx', '.csv'))]
    if not arquivos:
        print("❌ Nenhum arquivo encontrado.")
        return None, None, None

    print("\n📂 Arquivos disponíveis:")
    for i, arq in enumerate(arquivos, start=1):
        print(f"[{i}] {arq}")

    while True:
        try:
            idx = int(input("\nSelecione o número do arquivo: ")) - 1
            if 0 <= idx < len(arquivos):
                caminho = arquivos[idx]
                df = pd.read_excel(caminho, engine='calamine', header=0, 
                                 dtype={'PROCESSO': str, 'MANDADO': str, 'N.GRD': str})
                return caminho, df
            print(f"⚠️ Escolha entre 1 e {len(arquivos)}.")
        except ValueError:
            print("⚠️ Digite um número válido.")

def obter_configuracoes_execucao():
    """Obtém senha e configurações de pausa."""
    # Senha
    pw = os.getenv("USER_PASS")
    while True:
        prompt = "Entre com a nova senha ou ENTER para usar a do .env: " if pw else "Entre com a senha: "
        input_pw = input(prompt).strip()
        if not input_pw and pw: 
            break
        elif input_pw:
            pw = input_pw
            break
        print("⚠️ Senha obrigatória.")
    
    # Pausa
    pausa = 4
    entrada_pausa = input("Pausa entre registros (5-9 segundos, ou ENTER para 4s): ").strip()
    if entrada_pausa.isdigit() and 5 <= int(entrada_pausa) <= 9:
        pausa = int(entrada_pausa)
    
    print(f"✅ Configurando: Pausa de {pausa}s")
    return pw, pausa

def realizar_login(page, pw):
    """Executa o fluxo de login no TJSP."""
    email = os.getenv("USER_EMAIL")
    nome_usuario = os.getenv("USER_NAME", "SOGRAO")
    
    if not email:
        raise ValueError("❌ USER_EMAIL não definido no .env")

    print(f"🔐 Iniciando login para {email}...")
    page.goto("https://www.tjsp.jus.br/atc/cdm/auth/login")
    page.get_by_role("button", name="Entrar com @tjsp.jus.br").click()
    page.get_by_role("textbox", name="someone@example.com").fill(email)
    page.get_by_role("button", name="Avançar").click()
    page.get_by_role("textbox", name="Senha").fill(pw)
    page.get_by_role("button", name="Entrar").click()
    
    print("⏳ Aguardando aprovação no Microsoft Authenticator...")
    
    # Janela de aprovação do MFA
    try:
        btn_mfa = page.get_by_role("button", name="Aprovar uma solicitação em")
        btn_mfa.wait_for(state="visible", timeout=5000)
        btn_mfa.click()
    except: pass

    # Permanecer logado
    try:
        page.get_by_role("checkbox", name="Não mostrar isso novamente").wait_for(state="visible", timeout=60000)
        page.get_by_role("checkbox", name="Não mostrar isso novamente").check()
        page.get_by_role("button", name="Sim").click()
        page.get_by_text(f"Olá, {nome_usuario}").wait_for(state="visible", timeout=60000)
        print("✅ Login realizado com sucesso!")
    except Exception as e:
        print(f"❌ Erro no login ou timeout: {e}")
        raise e
