import os

master_path = r"C:\Users\dkven\Desktop\AGRO_GUYANA_PROJECT\wordpress_pages_html\00_MASTER_ALL_IN_ONE_PAGE.html"

master_html = """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif; border-radius: 20px; max-width: 1200px; margin: 0 auto; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">

    <!-- HEADER / HERO -->
    <div style="text-align: center; border-bottom: 2px solid #10B981; padding-bottom: 25px; margin-bottom: 35px;">
        <h1 style="color: #10B981; text-transform: uppercase; font-size: 34px; font-weight: 800; letter-spacing: 2px; margin: 0;">
            AGRO-GUYANA SUSTAINABLE PROTEIN & INDUSTRIAL ECOSYSTEM
        </h1>
        <p style="font-size: 16px; color: #94A3B8; margin-top: 10px;">
            Master Project Dossiê: Pasture-Moringa Silvopastoral System, Livestock Breeding, Hydro-Tide Factory & Cross-Border Logistics
        </p>
    </div>

    <!-- SECTION 1: EXECUTIVE SUMMARY -->
    <div style="margin-bottom: 40px;">
        <h2 style="color: #38BDF8; font-size: 24px; text-transform: uppercase; border-left: 4px solid #38BDF8; padding-left: 12px; margin-bottom: 15px;">
            1. Sumário Executivo & Visão Global
        </h2>
        <p style="font-size: 15px; line-height: 1.8; color: #CBD5E1;">
            O <strong>Projeto Integrado Agro-Guyana</strong> é um ecossistema agroindustrial, energético, pecuário e de materiais avançados projetado para transformar a Guiana em um polo de segurança alimentar e logística nas Américas e no Caricom.
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
            <div style="background: #1E293B; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <h3 style="color: #34D399; margin-bottom: 8px; font-size: 16px;">🌾 Silvicultura & Forragens</h3>
                <p style="font-size: 13px; color: #94A3B8;">Consórcio de Moringa oleifera (25-32% Proteína), Bambu Guadua, Arachis pintoi e Brachiaria.</p>
            </div>
            <div style="background: #1E293B; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <h3 style="color: #F59E0B; margin-bottom: 8px; font-size: 16px;">🐂 Pecuária & Frigorífico</h3>
                <p style="font-size: 13px; color: #94A3B8;">Nelore x Angus F1. Frigorífico em Lethem para abate de 150 cab/dia e exportação Caricom.</p>
            </div>
            <div style="background: #1E293B; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <h3 style="color: #EC4899; margin-bottom: 8px; font-size: 16px;">🏭 Carvão Ativado & Filtros</h3>
                <p style="font-size: 13px; color: #94A3B8;">Pirólise de bambu para fabricação de filtros de água domésticos e carvão medicinal.</p>
            </div>
            <div style="background: #1E293B; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <h3 style="color: #10B981; margin-bottom: 8px; font-size: 16px;">🏗️ Vergalhões de Grafite para Casas</h3>
                <p style="font-size: 13px; color: #94A3B8;">Compósito grafite-epóxi imune à ferrugem para atender ao plano de 40.000 casas na Guiana (US$ 75k/casa).</p>
            </div>
        </div>
    </div>

    <!-- SECTION 2: MODELO AGRONÔMICO -->
    <div style="margin-bottom: 40px;">
        <h2 style="color: #34D399; font-size: 24px; text-transform: uppercase; border-left: 4px solid #34D399; padding-left: 12px; margin-bottom: 15px;">
            2. Modelo Agronômico & Nutrição (100 Acres)
        </h2>
        <table style="width: 100%; border-collapse: collapse; background: #1E293B; border-radius: 10px; overflow: hidden; margin-top: 15px;">
            <thead>
                <tr style="background: #10B981; color: #FFF; text-transform: uppercase; font-size: 12px;">
                    <th style="padding: 12px; text-align: left;">Sistema</th>
                    <th style="padding: 12px; text-align: center;">Massa Seca (T/ha/ano)</th>
                    <th style="padding: 12px; text-align: center;">Proteína Bruta (%)</th>
                    <th style="padding: 12px; text-align: left;">Resistência Seca</th>
                </tr>
            </thead>
            <tbody style="font-size: 13px; color: #E2E8F0;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <td style="padding: 12px;">Brachiaria brizantha Monocultura</td>
                    <td style="padding: 12px; text-align: center;">10 - 16 Toneladas</td>
                    <td style="padding: 12px; text-align: center;">7% - 11%</td>
                    <td style="padding: 12px;">Baixa</td>
                </tr>
                <tr style="background: rgba(16, 185, 129, 0.15);">
                    <td style="padding: 12px; font-weight: bold; color: #34D399;">Consórcio Moringa + Amendoim Forrageiro</td>
                    <td style="padding: 12px; text-align: center; font-weight: bold;">18 - 28 Toneladas</td>
                    <td style="padding: 12px; text-align: center; font-weight: bold; color: #34D399;">18% - 24% (Folhas 32%)</td>
                    <td style="padding: 12px; font-weight: bold; color: #34D399;">Alta (Bio-resiliente)</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 3: PECUÁRIA & LOGÍSTICA -->
    <div style="margin-bottom: 40px;">
        <h2 style="color: #F59E0B; font-size: 24px; text-transform: uppercase; border-left: 4px solid #F59E0B; padding-left: 12px; margin-bottom: 15px;">
            3. Pecuária F1, Frigorífico & Corredor Logístico
        </h2>
        <div style="background: #1E293B; padding: 20px; border-radius: 12px; margin-bottom: 15px;">
            <h3 style="color: #38BDF8; font-size: 16px;">🐂 Nelore x Angus & Frigorífico Lethem</h3>
            <p style="font-size: 14px; color: #CBD5E1;">Inseminação IATF de matrizes Nelore com Angus Black (GMD 1.10 - 1.35 kg/dia). Abate e congelamento rápido em Lethem para exportação Caricom.</p>
        </div>
        <div style="background: #1E293B; padding: 20px; border-radius: 12px;">
            <h3 style="color: #10B981; font-size: 16px;">🚚 Troca de Cavalos Mecânicos em Lethem</h3>
            <p style="font-size: 14px; color: #CBD5E1;">Troca rápida de contêineres em 15 min no pátio de Lethem ligando Roraima/Manaus ao Porto de Linden na Guiana.</p>
        </div>
    </div>

    <!-- SECTION 4: ESTUFA SOMBRITE & CIRURGIA REGENERATIVA -->
    <div style="margin-bottom: 40px;">
        <h2 style="color: #EC4899; font-size: 24px; text-transform: uppercase; border-left: 4px solid #EC4899; padding-left: 12px; margin-bottom: 15px;">
            4. Estufa Sombrite, Maresia & Cirurgia de Raiz
        </h2>
        <div style="background: #1E293B; padding: 20px; border-radius: 12px;">
            <p style="font-size: 14px; color: #CBD5E1; line-height: 1.7;">
                Mesa de pipetas com subida e descida de água de chorume tratado. O esticamento da raiz é cortado com bisturi e cauterizado com <strong>Extrato Pirolenhoso sem Alcatrão</strong>, estimulando 3 a 4 novas raízes e permitindo colheita infinita sem matar a muda (Raiz farmacêutica: US$ 150 a US$ 450/kg).
            </p>
        </div>
    </div>

    <!-- SECTION 5: PROPOSTA COMERCIAL & TEASER -->
    <div style="background: rgba(16, 185, 129, 0.1); border: 2px solid #10B981; padding: 25px; border-radius: 16px;">
        <h2 style="color: #10B981; font-size: 24px; text-transform: uppercase; margin-bottom: 20px; text-align: center;">
            Proposta Comercial & Etapas de Contratação
        </h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px;">
            <div style="background: #1E293B; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="color: #38BDF8; font-size: 12px; font-weight: bold;">FASE 1: DOSSIÊ & CONTATOS</div>
                <div style="font-size: 22px; font-weight: bold; color: #FFF; margin: 8px 0;">USD $2.000</div>
                <div style="font-size: 11px; color: #94A3B8;">Acesso imediato aos fornecedores e fornecedores logísticos.</div>
            </div>
            <div style="background: #1E293B; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="color: #F59E0B; font-size: 12px; font-weight: bold;">FASE 2: AUDITORIA & FRETE</div>
                <div style="font-size: 22px; font-weight: bold; color: #FFF; margin: 8px 0;">USD $3.000</div>
                <div style="font-size: 11px; color: #94A3B8;">Viagem pessoal ao fornecedor no Brasil e curadoria de carga.</div>
            </div>
            <div style="background: #1E293B; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="color: #10B981; font-size: 12px; font-weight: bold;">FASE 3: ENTREGA NA FAZENDA</div>
                <div style="font-size: 22px; font-weight: bold; color: #FFF; margin: 8px 0;">USD $5.000</div>
                <div style="font-size: 11px; color: #94A3B8;">Despacho de fronteira e entrega final das sementes.</div>
            </div>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6; background: #1E293B; padding: 15px; border-radius: 10px;">
            <strong>Fase 4 (Gestão Continuada):</strong> Pro-Labore de USD $5.000/mês + 10% Royalties sobre vendas + 3% sobre financiamentos obtidos + 5% sobre compras do projeto. Custeio de hospedagem, alimentação e logística por conta do importador.
        </div>
    </div>

</div>"""

with open(master_path, "w", encoding="utf-8") as f:
    f.write(master_html)

print("Master All-In-One Page created successfully!")
