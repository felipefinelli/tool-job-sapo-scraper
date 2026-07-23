from playwright.sync_api import sync_playwright
import csv

URL_BASE = "https://emprego.sapo.pt/offers?local=porto&data-de-publicacao=ultimas-24-horas&pagina={pagina}&ordem=mais-recentes"
SELETOR_LINKS = 'h3 a[href*="/offers/"][href*="?id="]'
ARQUIVO_SAIDA = "dados_vagas.csv"

SELETORES_DADOS = {
    "Título": "div.description > h1",
    "Data": "div.metadata li.date span",
    "Empresa": "div.metadata li.company span",
    "Localização": "div.metadata li.location span",
    "Categoria": "div.metadata li.category span",
    "Regime_trabalho": "div.metadata li.workhome span",
    "Regime_horário": "div.metadata li.time span",
    "Tipo_contrato": "div.metadata li.contract span",
    "número_vagas": "div.metadata li.positions span",
    "Descrição": "div.description div.half-horizontal-padding",
}

def extrair_texto(pagina, seletor):
    elementos = pagina.locator(seletor)
    if elementos.count() == 0:
        return ""
    return elementos.first.inner_text().strip()   

def coletar_links(navegador, limite):
    pagina_web = navegador.new_page()
    links = []
    links_vistos = set()
    pagina_atual = 1

    while len(links) < limite:
        url = URL_BASE.format(pagina=pagina_atual)
        print(f"Buscando links na página {pagina_atual}...")
        pagina_web.goto(url)
        pagina_web.wait_for_load_state("networkidle")

        elementos = pagina_web.query_selector_all(SELETOR_LINKS)

        if not elementos:
            print("Nenhuma vaga a mais encontrada.")
            break

        for elemento in elementos:
            if len(links) >= limite:
                break
            href = elemento.get_attribute("href")
            if href and href not in links_vistos:
                links.append(href)
                links_vistos.add(href)

        pagina_atual += 1
        
    pagina_web.close()
    return links

def coletar_detalhes(navegador, links):
    pagina = navegador.new_page()
    colunas = list(SELETORES_DADOS.keys()) + ["Link"]
    
    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo_saida:
        escritor = csv.DictWriter(arquivo_saida, fieldnames=colunas)
        escritor.writeheader()

        total = len(links)
        for indice, link in enumerate(links, start=1):
            print(f"[{indice}/{total}] Coletando dados de: {link}")
            try:
                pagina.goto(link, wait_until="domcontentloaded", timeout=60000)
                pagina.locator("div.description > h1").first.wait_for(state="visible", timeout=30000)

                dados = {campo: extrair_texto(pagina, seletor) for campo, seletor in SELETORES_DADOS.items()}
                dados["Link"] = link
                escritor.writerow(dados)

            except Exception as erro:
                print(f"Erro ao processar {link}: {erro}")
                dados = {campo: "" for campo in SELETORES_DADOS}
                dados["Link"] = link
                escritor.writerow(dados)
                
    pagina.close()

def main():
    limite = int(input("Quantos links deseja capturar? "))
    
    # Abre o Playwright uma única vez para todo o processo
    with sync_playwright() as p:
        print("\nAbrindo navegador...")
        navegador = p.chromium.launch()
        
        # Etapa 1
        links = coletar_links(navegador, limite)
        print(f"\n{len(links)} links encontrados. Iniciando extração de detalhes...\n")
        
        # Etapa 2
        if links:
            coletar_detalhes(navegador, links)
            
        navegador.close()
        
    print(f"\nProcesso finalizado! Dados salvos em {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()