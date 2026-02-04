import pandas as pd
from typing import List, Tuple
from constantes import config, logger

class TransformadorDados:
    """Lógica de negócio e transformações avançadas de dados SAJ."""

    def __init__(self):
        self.mes_numero = None
        self.mes_nome = None
        self.cota = 111.06
        self.jg = 1
        self.deslocamento = 'S'

    def parametrizar(self, meses_disponiveis: List[int]):
        """Solicita os parâmetros de processamento ao usuário."""
        # 1. Seleção do Mês
        lookup_meses = {m: config.MESES_NOMES[m-1] for m in meses_disponiveis}
        print("\n🗓️  Calendário de dados identificado:")
        for num, nome in lookup_meses.items():
            print(f"[{num}] {nome}")
            
        while True:
            escolha = input("\nQual mês deseja processar (Digite o número)? ").strip()
            if escolha.isdigit() and int(escolha) in lookup_meses:
                self.mes_numero = int(escolha)
                self.mes_nome = lookup_meses[self.mes_numero]
                break
            print("⚠️ Mês inválido ou sem dados.")

        # 2. Valor da Cota
        while True:
            entrada = input(f"Valor da cota (Pressione Enter para R${self.cota:.2f}): ").strip().replace(',', '.')
            if not entrada: break
            try:
                val = float(entrada)
                if val >= 0: 
                    self.cota = val
                    break
            except ValueError: pass
            print("⚠️ Valor inválido. Use números positivos.")

        # 3. Valor do JG
        while True:
            entrada = input("Valor de JG (0 ou Pressione Enter para 1): ").strip()
            if not entrada: break
            if entrada in ["0", "1"]:
                self.jg = int(entrada)
                break
            print("⚠️ Digite 0 ou 1.")

        # 4. Deslocamento
        while True:
            entrada = input("Deslocamento (N ou Pressione Enter para S): ").strip().upper()
            if not entrada: break
            if entrada in ['N', 'S']:
                self.deslocamento = entrada
                break
            print("⚠️ Digite N ou S.")

    def aplicar_transformacoes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Executa a limpeza e formatação pesada dos dados."""
        logger.info(f"Iniciando tratamento pesado: Mês {self.mes_nome}, Cota {self.cota}")
        
        # Filtro inicial pelo mês
        mask = df[config.DATE_COLUMN].dt.month == self.mes_numero
        df_filtrado = df[mask].copy()
        
        if df_filtrado.empty:
            logger.warning(f"Nenhum dado para o mês {self.mes_nome}")
            return pd.DataFrame()

        # Criando o DataFrame de saída com o schema correto
        tratados = pd.DataFrame()

        # 1. PROCESSO (20 dígitos zfill)
        tratados['PROCESSO'] = (
            df_filtrado['Processo']
            .astype(str)
            .str.replace(r'\D', '', regex=True)
            .str.zfill(20)
        )

        # 2. MANDADO (Formato CNJ)
        def formatar_mandado(num):
            s = str(num).replace('.', '').replace('-', '').replace('/', '').strip()
            return f"{s[:3]}.{s[3:7]}/{s[7:13]}-{s[13:]}" if len(s) == 14 else s
        
        tratados['MANDADO'] = df_filtrado['Mandado'].apply(formatar_mandado)

        # 3. DESTINATÁRIO
        tratados['DESTINATÁRIO'] = df_filtrado['Destinatário'].astype(str).str.strip().str.upper()

        # 4. DATAS
        tratados['RECEB. OFICIAL'] = pd.to_datetime(df_filtrado['Receb. oficial'], dayfirst=True).dt.strftime('%d/%m/%Y')
        tratados['RECEB. CENTRAL'] = pd.to_datetime(df_filtrado['Receb. central'], dayfirst=True).dt.strftime('%d/%m/%Y')

        # 5. N.GRD
        tratados['N.GRD'] = df_filtrado['Guia de Recolhimento'].astype(str).str.strip()

        # 6. FORMA PAGAMENTO
        mapeamento_pgto = {'Justiça Gratuita': 'JUSTIÇA GRATUITA', 'Justiça Paga': 'JUSTIÇA PAGA'}
        tratados['FORMA PAGAMENTO'] = df_filtrado['Forma de pagamento'].map(mapeamento_pgto).fillna('JUSTIÇA PAGA')

        # 7. VALOR (Baseado na cota e tipo de pagamento)
        valor_str = f"{self.cota:.2f}".replace('.', ',')
        tratados['VALOR'] = tratados['FORMA PAGAMENTO'].apply(
            lambda x: '0,00' if x == 'JUSTIÇA GRATUITA' else valor_str
        )

        # 8. COLUNAS FIXAS / PARÂMETROS
        tratados['COTA'] = str(self.jg)
        tratados['DESLOCAMENTO'] = self.deslocamento
        tratados['REGRA ESPECIAL'] = 'N'
        tratados['CONTROLE'] = 'N'
        tratados['CONFERE'] = 'O'

        return tratados

def executar_transformacao(df: pd.DataFrame, meses: List[int]) -> Tuple[pd.DataFrame, str]:
    """Orquestra a parametrização e transformação."""
    t = TransformadorDados()
    t.parametrizar(meses)
    df_final = t.aplicar_transformacoes(df)
    return df_final, t.mes_nome