# Job Scraper: SAPO Emprego

A job scraper for SAPO Emprego built with Python and Playwright.

[Português](#português) · [English](#english)

---

## Português

### Sobre o projeto

Este script coleta vagas publicadas nas últimas 24 horas na região do Porto no site [SAPO Emprego](https://emprego.sapo.pt/).

Os resultados são salvos no arquivo `dados_vagas.csv`.

### Dados coletados

* Título
* Data de publicação
* Empresa
* Localização
* Categoria
* Regime de trabalho
* Regime de horário
* Tipo de contrato
* Número de vagas
* Descrição
* Link da vaga

### Requisitos

* Python 3.8 ou superior
* Playwright
* Chromium

### Instalação

```bash
pip install playwright
playwright install chromium
```

### Execução

```bash
python main.py
```

Ao executar o script, informe a quantidade de vagas que deseja coletar.

### Arquivo de saída

Os dados são exportados para:

```text
dados_vagas.csv
```

O arquivo utiliza codificação UTF-8 e pode ser aberto no Excel, LibreOffice ou em ferramentas de análise de dados.

---

## English

### About the project

This script collects job listings published within the last 24 hours in the Porto region from the [SAPO Emprego](https://emprego.sapo.pt/) website.

The results are saved to the `dados_vagas.csv` file.

### Collected data

* Job title
* Publication date
* Company
* Location
* Category
* Work arrangement
* Work schedule
* Contract type
* Number of openings
* Job description
* Job listing URL

### Requirements

* Python 3.8 or later
* Playwright
* Chromium

### Installation

```bash
pip install playwright
playwright install chromium
```

### Usage

```bash
python main.py
```

When prompted, enter the number of job listings you want to collect.

### Output file

The collected data is exported to:

```text
dados_vagas.csv
```

The file uses UTF-8 encoding and can be opened with Excel, LibreOffice, or data analysis tools.
