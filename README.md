# BOT_SOGRAO - Automação TJSP

Este projeto contém scripts em Python para automatizar o lançamento de mandados e processos no sistema do Tribunal de Justiça de São Paulo (TJSP).

## 📋 Pré-requisitos

Para executar os scripts, você precisará ter instalado:

*   **Python 3.x**: [Download Python](https://www.python.org/downloads/)
*   **Bibliotecas Python**: As dependências principais são `playwright`, `pandas` e `calamine`.

Instale as dependências executando:

```bash
pip install playwright pandas calamine openpyxl
playwright install
```

## 🚀 Como Usar

O fluxo de trabalho consiste em duas etapas principais: **Transformação de Dados** e **Automação de Lançamento**.

### 1. Transformação de Dados (`TRANSFORMADOR.py`)

O primeiro passo é preparar a planilha de dados extraída do sistema (relatório SAJ).

1.  Coloque o arquivo Excel (`.xlsx`) na mesma pasta do script.
2.  Execute o script:
    ```bash
    python TRANSFORMADOR.py
    ```
3.  Siga as instruções no terminal:
    *   Selecione o arquivo desejado.
    *   Informe o mês de referência.
    *   Confirme os valores de Cota, JG (Justiça Gratuita) e Deslocamento.
4.  O script irá gerar um novo arquivo Excel (ex: `Dados_Tratados_do_Mês_X.xlsx`) pronto para a automação.

### 2. Automação de Lançamento (`GRATUITOS.py` e `PAGOS.py`)

Com os dados tratados, você pode iniciar a automação. Existem dois scripts, dependendo do tipo de processo:

*   **`GRATUITOS.py`**: Para processos com Justiça Gratuita.
*   **`PAGOS.py`**: Para processos com Justiça Paga.

**Passos:**

1.  Execute o script correspondente:
    ```bash
    python GRATUITOS.py
    # ou
    python PAGOS.py
    ```
2.  Selecione o arquivo *tratado* gerado na etapa anterior.
3.  O script abrirá um navegador (Chromium) controlado pelo Playwright.
4.  Realize o login no sistema TJSP quando solicitado (o script auxilia preenchendo o usuário, mas pode requerer aprovação MFA).
5.  A automação começará a lançar os dados linha por linha.

## 🛠️ Estrutura dos Arquivos

*   `TRANSFORMADOR.py`: Limpa e padroniza os dados do relatório SAJ.
*   `TRANSFORMADOR8Colums.py`: Versão alternativa/template do transformador.
*   `GRATUITOS.py`: Script de automação para lançamentos gratuitos.
*   `PAGOS.py`: Script de automação para lançamentos pagos (inclui verificação de pausas).
*   `inicial.ipynb`: Notebook Jupyter para testes e desenvolvimento (opcional).

## ⚠️ Notas Importantes

*   **Senha**: O script possui uma senha padrão configurada (`@.3461@BHc`), mas permite alteração durante a execução.
*   **MFA (Autenticação de Dois Fatores)**: O script aguarda a aprovação no Microsoft Authenticator. Fique atento ao seu dispositivo móvel.
*   **Monitoramento**: Acompanhe o terminal para ver o progresso e possíveis mensagens de erro.
