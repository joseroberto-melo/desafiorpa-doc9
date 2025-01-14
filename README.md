## RPA Challenge - Extração de Faturas

### Visão Geral
Este script automatiza o processo de extração de dados de uma tabela no site [RPA Challenge OCR](https://rpachallengeocr.azurewebsites.net) e realiza o download das respectivas faturas. O processo inclui:
- Extração de informações como ID, data de vencimento e link de download.
- Download automático de arquivos PDF ou imagens (JPEG).
- Geração de um arquivo CSV consolidado com os dados extraídos.

---

### Estrutura do Projeto
```plaintext
/desafio-rpa
├── desafio.py             # Código principal
├── script_log.log        # Arquivo de log gerado pela execução
├── resultado.csv         # CSV gerado com os dados extraídos
├── requirements.txt      # Lista de dependências do projeto
├── README.md             # Documentação
└── faturas/              # Diretório para os arquivos baixados
```

---

### Requisitos
- Python 3.8 ou superior.
- Google Chrome instalado.
- ChromeDriver compatível com a versão do Google Chrome.

---

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o **ChromeDriver**:
   - Baixe a versão correspondente ao seu navegador em [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).
   - Certifique-se de que o ChromeDriver está no `PATH` do sistema.

---

### Execução
1. Execute o script:
   ```bash
   python script.py
   ```
2. Resultados:
   - Os arquivos baixados estarão na pasta `faturas`.
   - Um arquivo CSV chamado `resultado.csv` será gerado com os dados extraídos.
   - O arquivo de log `script_log.log` conterá detalhes da execução.

---

### Estrutura do CSV
O arquivo `resultado.csv` será gerado com a seguinte estrutura:
```csv
Número da Fatura,Data de Vencimento,URL da Fatura,Status do Download
12345,14-01-2025,https://rpachallengeocr.azurewebsites.net/invoices/4.pdf,Sucesso
67890,15-01-2025,https://rpachallengeocr.azurewebsites.net/invoices/1.pdf,Falha
```

---

### Decisões Técnicas
1. **Selenium**:
   - Usado para acessar e interagir com a tabela no site.
   - Aguarda os elementos carregarem com `WebDriverWait` para maior estabilidade.

2. **Requests**:
   - Utilizado para realizar o download dos arquivos diretamente a partir dos links extraídos.

3. **Logs**:
   - Registro detalhado de cada etapa da execução no arquivo `script_log.log`.

4. **Pandas**:
   - Utilizado para manipulação e geração do arquivo CSV.

---

### Otimizações Implementadas
- **Performance**:
  - Reutilização do WebDriver para minimizar chamadas repetitivas.
  - Download direto usando `requests`, que é mais rápido do que cliques via Selenium.
- **Manutenção**:
  - Código modularizado (`setup_driver`, `download_file`, `main`).
  - Logs detalhados para depuração.

---

### Contato
Para dúvidas ou problemas, entre em contato com José Roberto Melo.

