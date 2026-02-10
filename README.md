# 🤖 BOT SOGRAO - Automação TJSP

Este projeto é uma solução completa de automação para o processamento e lançamento de mandados no portal do TJSP. Ele combina um pipeline de dados robusto (ETL) com scripts de automação de navegador para otimizar o fluxo de trabalho burocrático.

## 🚀 Funcionalidades

- **Pipeline ETL Inteligente**: Extrai, transforma e limpa relatórios brutos do sistema SAJ, preparando-os para o lançamento automático.
- **Automação de Lançamento**: Scripts dedicados para mandados **PAGOS** e **GRATUITOS** utilizando Playwright.
- **Gestão de Credenciais**: Armazenamento seguro de senhas e acessos via variáveis de ambiente (`.env`).
- **Validação de Dados**: Verificação automática de integridade dos arquivos Excel antes do processamento.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.x
- **Automação Web**: [Playwright](https://playwright.dev/python/)
- **Processamento de Dados**: [Pandas](https://pandas.pydata.org/)
- **Leitura de Excel**: `python-calamine` (alta performance)
- **Variáveis de Ambiente**: `python-dotenv`

---

## 📂 Estrutura do Projeto

- `Pipeline_ETL_SAJ.py`: Orquestrador principal que processa o relatório do SAJ.
- `GRATUITOS.py`: Automação de lançamentos de mandados de Justiça Gratuita.
- `PAGOS.py`: Automação de lançamentos de mandados com Guia de Recolhimento (Pagos).
- `extrator.py`, `transformador.py`, `carregador.py`: Módulos que compõem o pipeline de dados.
- `constantes.py`: Configurações globais e sistema de logs.

---

## 🔧 Configuração e Instalação

### 1. Requisitos
Certifique-se de ter o Python instalado e execute o seguinte comando para instalar as dependências:

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto conforme o modelo abaixo:

```env
USER_EMAIL=seu_email@tjsp.jus.br
USER_PASS=sua_senha_aqui
USER_NAME=SEU_NOME_COMPLETO
```

---

## 📋 Como Usar

### Passo 1: Preparar os Dados
Coloque o relatório Excel gerado pelo SAJ na pasta do projeto e execute o pipeline:
```bash
python Pipeline_ETL_SAJ.py
```
*Siga as instruções no terminal para selecionar o arquivo, o mês de referência e os valores das cotas.*

### Passo 2: Lançamento Automático
Com o arquivo tratado gerado (ex: `Dados_Tratados_Fevereiro.xlsx`), execute o robô correspondente:

**Para mandados gratuitos:**
```bash
python GRATUITOS.py
```

**Para mandados pagos:**
```bash
python PAGOS.py
```

---

## 🛡️ Segurança e Logs

- O arquivo `.env` está configurado no `.gitignore` para nunca ser enviado ao repositório.
- Todos os processos geram logs detalhados no arquivo `pipeline.log` para facilitar a auditoria e correção de erros.

---
*Desenvolvido para otimização de fluxos jurídicos.*
