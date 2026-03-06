# Relatório de Modelagem de Ameaças (STRIDE)
**Imagem analisada:** `inputs/arch10.png`  
**Gerado em:** 2026-03-06 05:09 UTC
## 1) Resumo
- Componentes detectados: **0**
- Contagem por classe:

## 2) Componentes Detectados
| # | Classe | Confiança | Bounding Box |
|---|--------|-----------|--------------|

## 3) Ameaças por Componente (STRIDE)

## 4) Limitações do MVP
- O detector reconhece um conjunto limitado de classes (multi-cloud genéricas).
- O mapeamento STRIDE é baseado em regras (base de conhecimento estática).
- Não inferimos fluxos/DFDs; apenas analisamos componentes detectados.

## 5) Próximos Passos
- Aumentar o dataset e refinar classes (ex.: queue, secrets manager, CI/CD).
- Detectar relações/fluxos (setas) para gerar DFD e melhorar STRIDE por fronteira de confiança.
- Integrar busca de vulnerabilidades (CWE/CVE) por tipo de componente.
