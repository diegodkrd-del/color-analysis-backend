import os

base_dir = r"C:\Users\dkven\Desktop\AGRO_GUYANA_PROJECT"
html_dir = os.path.join(base_dir, "wordpress_pages_html")
plugin_dir = os.path.join(base_dir, "wordpress_plugin")

os.makedirs(html_dir, exist_ok=True)
os.makedirs(plugin_dir, exist_ok=True)

files = {
    os.path.join(base_dir, "README_PROJETO.md"): """# AGRO-GUYANA PROJECT & INDUSTRIAL HUB
Este diretório contém todos os documentos, códigos HTML e plugins prontos do Projeto Integrado Agro-Guyana.
""",
    os.path.join(html_dir, "01_sumario_executivo.html"): """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif; border-radius: 16px;">
    <h1 style="color: #10B981; text-transform: uppercase;">AGRO-GUYANA SUSTAINABLE PROTEIN & INDUSTRIAL ECOSYSTEM</h1>
    <p>O Projeto Integrado Agro-Guyana é um ecossistema agroindustrial, energético, pecuário e de materiais avançados.</p>
</div>""",
    os.path.join(html_dir, "02_projeto_agronomico.html"): """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif;">
    <h2 style="color: #34D399;">MODELO AGRONÔMICO & NUTRIÇÃO INTEGRADA</h2>
    <p>Consórcio de Moringa oleifera (25-32% PB), Arachis pintoi e Brachiaria.</p>
</div>""",
    os.path.join(html_dir, "03_pecuaria_iatf.html"): """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif;">
    <h2 style="color: #F59E0B;">PECUÁRIA F1 ANGUS x NELORE & FRIGORÍFICO EM LETHEM</h2>
    <p>IATF de matrizes Nelore com touros Angus Black. Frigorífico em Lethem para abate de 150 cab/dia.</p>
</div>""",
    os.path.join(html_dir, "04_logistica_e_fronteira.html"): """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif;">
    <h2 style="color: #38BDF8;">CORREDOR LOGÍSTICO BI-OCEÂNICO (BOA VISTA - LETHEM - LINDEN)</h2>
    <p>Troca rápida de contêineres fechados no pátio de Lethem.</p>
</div>""",
    os.path.join(html_dir, "05_fabrica_sombrite_hidro.html"): """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif;">
    <h2 style="color: #EC4899;">ESTUFA SOMBRITE, CIRURGIA REGENERATIVA & EXTRATO PIROLENHOSO</h2>
    <p>Corte regenerativo de raiz com bisturi e cauterização com extrato pirolenhoso sem alcatrão.</p>
</div>""",
    os.path.join(html_dir, "06_bambu_carvao_e_grafite.html"): """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif;">
    <h2 style="color: #F59E0B;">BAMBU GUADUA, CARVÃO ATIVADO & VERGALHÕES PARA 40.000 CASAS</h2>
    <p>Substituição do ferro por vergalhões de grafite pirolítico + epóxi para o plano de 40.000 casas da Guiana.</p>
</div>""",
    os.path.join(html_dir, "07_proposta_comercial_teaser.html"): """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif;">
    <h2 style="color: #10B981;">PROPOSTA COMERCIAL & ETAPAS DE CONTRATAÇÃO</h2>
    <p>Fase 1: USD $2.000 | Fase 2: USD $3.000 | Fase 3: USD $5.000 | Fase 4: USD $5.000/mês + 10% Royalties.</p>
</div>"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("AGRO_GUYANA_PROJECT folder created and written successfully!")
