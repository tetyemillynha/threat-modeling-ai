# Relatório de Modelagem de Ameaças (STRIDE)
**Imagem analisada:** `inputs/arch2.png`  
**Gerado em:** 2026-03-06 04:18 UTC
## 1) Resumo
- Componentes detectados: **7**
- Contagem por classe:
  - `database`: **1**
  - `load_balancer`: **4**
  - `storage`: **1**
  - `waf_firewall`: **1**

## 2) Componentes Detectados
| # | Classe | Confiança | Bounding Box |
|---|--------|-----------|--------------|
| 1 | `load_balancer` | 0.99 | x=330, y=498, w=139, h=99 |
| 2 | `database` | 0.99 | x=12, y=487, w=113, h=110 |
| 3 | `load_balancer` | 0.98 | x=631, y=279, w=98, h=97 |
| 4 | `waf_firewall` | 0.97 | x=339, y=270, w=122, h=113 |
| 5 | `load_balancer` | 0.96 | x=978, y=618, w=141, h=133 |
| 6 | `load_balancer` | 0.93 | x=971, y=484, w=150, h=127 |
| 7 | `storage` | 0.67 | x=14, y=18, w=110, h=143 |

## 3) Ameaças por Componente (STRIDE)

### 3.1 `load_balancer` (conf: 0.99)

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

### 3.2 `database` (conf: 0.99)

**T — Tampering (Adulteração)**
- **Ameaça:** SQL injection / alteração de dados
- **Descrição:** Entrada não validada permite manipular queries e dados.
- **Contramedidas:**
  - ORM/prepared statements
  - Validação de input
  - WAF rules

**R — Repudiation (Repúdio)**
- **Ameaça:** Mudanças sem auditoria
- **Descrição:** Alterações sem trilha dificultam investigação.
- **Contramedidas:**
  - Auditoria (logs)
  - Trilhas de alteração
  - Controle de acesso por função

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Vazamento de dados em repouso
- **Descrição:** Dados expostos por backups/snapshots ou acesso indevido.
- **Contramedidas:**
  - Criptografia at-rest
  - KMS/Key Vault
  - Privilégios mínimos
  - Masking onde aplicável

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Exaustão de conexões/locks
- **Descrição:** Muitas conexões ou queries lentas derrubam banco.
- **Contramedidas:**
  - Pool de conexões
  - Índices
  - Limites
  - Read replicas

**E — Elevation of Privilege (Elevação de privilégio)**
- **Ameaça:** Escalada via credenciais do DB
- **Descrição:** Credenciais com permissões amplas permitem elevar acesso.
- **Contramedidas:**
  - Usuários separados por app
  - Least privilege
  - Rotação de senhas

### 3.3 `load_balancer` (conf: 0.98)

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

### 3.4 `waf_firewall` (conf: 0.97)

**T — Tampering (Adulteração)**
- **Ameaça:** Bypass de regras
- **Descrição:** Ataques ajustam payload para contornar assinaturas.
- **Contramedidas:**
  - Regras atualizadas
  - Managed rules + custom
  - Monitorar falsos negativos

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** DoS na borda
- **Descrição:** Ataques de L7 pressionam o WAF.
- **Contramedidas:**
  - Rate limit na borda
  - Shield/Protection
  - Caching quando aplicável

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Exposição de endpoints por configuração
- **Descrição:** Regras permissivas deixam rotas sensíveis acessíveis.
- **Contramedidas:**
  - Hardening
  - Allowlist quando possível
  - Revisão periódica de regras

### 3.5 `load_balancer` (conf: 0.96)

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

### 3.6 `load_balancer` (conf: 0.93)

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

### 3.7 `storage` (conf: 0.67)

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Buckets/containers públicos
- **Descrição:** Armazenamento exposto por política incorreta.
- **Contramedidas:**
  - Bloquear acesso público
  - Políticas mínimas
  - Revisão de ACLs

**T — Tampering (Adulteração)**
- **Ameaça:** Upload malicioso
- **Descrição:** Arquivos podem conter malware ou scripts.
- **Contramedidas:**
  - Antivírus/scan
  - Validação de tipo
  - Assinatura de uploads

**R — Repudiation (Repúdio)**
- **Ameaça:** Sem trilha de acesso a objetos
- **Descrição:** Sem logs não é possível rastrear downloads/alterações.
- **Contramedidas:**
  - Logs de acesso
  - Versionamento
  - Imutabilidade (quando necessário)

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Abuso de armazenamento
- **Descrição:** Crescimento descontrolado gera custo/indisponibilidade.
- **Contramedidas:**
  - Quotas
  - Lifecycle policies
  - Alertas de uso

## 4) Limitações do MVP
- O detector reconhece um conjunto limitado de classes (multi-cloud genéricas).
- O mapeamento STRIDE é baseado em regras (base de conhecimento estática).
- Não inferimos fluxos/DFDs; apenas analisamos componentes detectados.

## 5) Próximos Passos
- Aumentar o dataset e refinar classes (ex.: queue, secrets manager, CI/CD).
- Detectar relações/fluxos (setas) para gerar DFD e melhorar STRIDE por fronteira de confiança.
- Integrar busca de vulnerabilidades (CWE/CVE) por tipo de componente.
