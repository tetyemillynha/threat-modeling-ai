# Relatório de Modelagem de Ameaças (STRIDE)
**Imagem analisada:** `inputs/arch10.png`  
**Gerado em:** 2026-03-06 18:47 UTC
## 1) Resumo
- Componentes detectados: **5**
- Contagem por classe:
  - `api_gateway`: **1**
  - `cdn`: **2**
  - `load_balancer`: **1**
  - `monitoring_logging`: **1**

## 2) Componentes Detectados
| # | Classe | Confiança | Bounding Box |
|---|--------|-----------|--------------|
| 1 | `cdn` | 0.99 | x=536, y=205, w=126, h=129 |
| 2 | `cdn` | 0.98 | x=844, y=337, w=143, h=114 |
| 3 | `load_balancer` | 0.97 | x=836, y=210, w=158, h=130 |
| 4 | `monitoring_logging` | 0.94 | x=852, y=62, w=124, h=129 |
| 5 | `api_gateway` | 0.91 | x=127, y=287, w=193, h=144 |

## 3) Ameaças por Componente (STRIDE)

### 3.1 `cdn` (conf: 0.99)

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Cache de conteúdo sensível
- **Descrição:** Conteúdo com dados privados pode ser cacheado indevidamente.
- **Contramedidas:**
  - Cache-control correto
  - Separar domínios
  - Evitar cache para endpoints sensíveis

**T — Tampering (Adulteração)**
- **Ameaça:** Injeção via conteúdo estático malicioso
- **Descrição:** Arquivos estáticos podem ser adulterados.
- **Contramedidas:**
  - Assinatura/integ. de artefatos
  - Controle de versão
  - SRI (web) quando aplicável

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Amplificação de tráfego
- **Descrição:** CDN pode amplificar impacto se mal configurada.
- **Contramedidas:**
  - Rate limiting
  - WAF na borda
  - Proteção DDoS

### 3.2 `cdn` (conf: 0.98)

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Cache de conteúdo sensível
- **Descrição:** Conteúdo com dados privados pode ser cacheado indevidamente.
- **Contramedidas:**
  - Cache-control correto
  - Separar domínios
  - Evitar cache para endpoints sensíveis

**T — Tampering (Adulteração)**
- **Ameaça:** Injeção via conteúdo estático malicioso
- **Descrição:** Arquivos estáticos podem ser adulterados.
- **Contramedidas:**
  - Assinatura/integ. de artefatos
  - Controle de versão
  - SRI (web) quando aplicável

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Amplificação de tráfego
- **Descrição:** CDN pode amplificar impacto se mal configurada.
- **Contramedidas:**
  - Rate limiting
  - WAF na borda
  - Proteção DDoS

### 3.3 `load_balancer` (conf: 0.97)

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Exaustão de conexões
- **Descrição:** Muitas conexões simultâneas derrubam o LB ou backends.
- **Contramedidas:**
  - Timeouts corretos
  - Limites de conexão
  - Auto scaling
  - Health checks

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** TLS fraco / downgrade
- **Descrição:** Cifras fracas ou TLS mal configurado expõe dados.
- **Contramedidas:**
  - TLS moderno
  - HSTS (web)
  - mTLS interno quando necessário

**T — Tampering (Adulteração)**
- **Ameaça:** Header spoofing (X-Forwarded-For)
- **Descrição:** IP de origem pode ser forjado sem validação.
- **Contramedidas:**
  - Confiar apenas em headers do LB
  - Sanitização de headers
  - Logs no LB

### 3.4 `monitoring_logging` (conf: 0.94)

**T — Tampering (Adulteração)**
- **Ameaça:** Adulteração de logs
- **Descrição:** Atacante tenta apagar/alterar trilhas.
- **Contramedidas:**
  - Logs imutáveis
  - Write-once/retention
  - Acesso restrito

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Logs com dados sensíveis
- **Descrição:** PII/segredos em logs.
- **Contramedidas:**
  - Redação
  - Política de logging
  - Scrubbing

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Explosão de logs/telemetria
- **Descrição:** Logging excessivo derruba performance/custo.
- **Contramedidas:**
  - Rate limit de logs
  - Sampling
  - Alertas de volume

### 3.5 `api_gateway` (conf: 0.91)

**S — Spoofing (Falsificação de identidade)**
- **Ameaça:** Chamadas sem autenticação
- **Descrição:** Endpoints expostos aceitam requests sem credenciais válidas.
- **Contramedidas:**
  - Auth obrigatória (OAuth2/JWT)
  - mTLS para integrações
  - Chaves/API keys com rotação

**T — Tampering (Adulteração)**
- **Ameaça:** Manipulação de payload
- **Descrição:** Alteração de parâmetros/corpo pode explorar lógica de negócio.
- **Contramedidas:**
  - Validação de input (schema)
  - Assinatura de requests quando aplicável
  - Rejeitar campos desconhecidos

**R — Repudiation (Repúdio)**
- **Ameaça:** Falta de rastreio por request
- **Descrição:** Sem request-id e logs, não há atribuição de autoria.
- **Contramedidas:**
  - Request ID
  - Logs estruturados
  - Tracing distribuído

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Headers/logs com dados sensíveis
- **Descrição:** Tokens/PII podem vazar via logs ou respostas.
- **Contramedidas:**
  - Redação de logs
  - Política de erro sem detalhes
  - Criptografia em trânsito

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Ataque de volumetria
- **Descrição:** Flood de requests derruba API.
- **Contramedidas:**
  - Rate limit/quotas
  - WAF
  - Auto scaling
  - Circuit breaker

**E — Elevation of Privilege (Elevação de privilégio)**
- **Ameaça:** Acesso indevido a rotas administrativas
- **Descrição:** Rotas internas acessadas por perfis comuns.
- **Contramedidas:**
  - Separar rotas admin
  - Autorização por escopo
  - Network segmentation

## 4) Limitações do MVP
- O detector reconhece um conjunto limitado de classes (multi-cloud genéricas).
- O mapeamento STRIDE é baseado em regras (base de conhecimento estática).
- Não inferimos fluxos/DFDs; apenas analisamos componentes detectados.

## 5) Próximos Passos
- Aumentar o dataset e refinar classes (ex.: queue, secrets manager, CI/CD).
- Detectar relações/fluxos (setas) para gerar DFD e melhorar STRIDE por fronteira de confiança.
- Integrar busca de vulnerabilidades (CWE/CVE) por tipo de componente.
