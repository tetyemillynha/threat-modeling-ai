# Relatório de Modelagem de Ameaças (STRIDE)
**Imagem analisada:** `inputs/arch1.png`  
**Gerado em:** 2026-03-06 20:13 UTC
## 1) Resumo
- Componentes detectados: **15**
- Contagem por classe:
  - `app_service`: **1**
  - `cdn`: **4**
  - `database`: **2**
  - `identity_auth`: **1**
  - `load_balancer`: **4**
  - `monitoring_logging`: **1**
  - `storage`: **2**

## 2) Componentes Detectados
| # | Classe | Confiança | Bounding Box |
|---|--------|-----------|--------------|
| 1 | `cdn` | 0.92 | x=146, y=584, w=125, h=147 |
| 2 | `load_balancer` | 0.87 | x=971, y=669, w=119, h=144 |
| 3 | `cdn` | 0.78 | x=440, y=609, w=134, h=122 |
| 4 | `database` | 0.72 | x=341, y=39, w=118, h=132 |
| 5 | `database` | 0.72 | x=633, y=37, w=117, h=135 |
| 6 | `load_balancer` | 0.64 | x=216, y=800, w=106, h=147 |
| 7 | `load_balancer` | 0.49 | x=958, y=828, w=136, h=152 |
| 8 | `monitoring_logging` | 0.48 | x=969, y=530, w=117, h=132 |
| 9 | `storage` | 0.43 | x=967, y=364, w=122, h=154 |
| 10 | `storage` | 0.42 | x=969, y=669, w=121, h=143 |
| 11 | `cdn` | 0.41 | x=436, y=552, w=152, h=180 |
| 12 | `identity_auth` | 0.40 | x=961, y=224, w=132, h=137 |
| 13 | `app_service` | 0.33 | x=471, y=45, w=135, h=126 |
| 14 | `cdn` | 0.31 | x=435, y=538, w=159, h=136 |
| 15 | `load_balancer` | 0.26 | x=468, y=43, w=138, h=127 |

## 3) Ameaças por Componente (STRIDE)

### 3.1 `cdn` (conf: 0.92)

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

### 3.2 `load_balancer` (conf: 0.87)

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

### 3.3 `cdn` (conf: 0.78)

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

### 3.4 `database` (conf: 0.72)

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

### 3.5 `database` (conf: 0.72)

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

### 3.6 `load_balancer` (conf: 0.64)

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

### 3.7 `load_balancer` (conf: 0.49)

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

### 3.8 `monitoring_logging` (conf: 0.48)

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

### 3.9 `storage` (conf: 0.43)

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

### 3.10 `storage` (conf: 0.42)

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

### 3.11 `cdn` (conf: 0.41)

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

### 3.12 `identity_auth` (conf: 0.40)

**S — Spoofing (Falsificação de identidade)**
- **Ameaça:** Sequestro/forja de tokens
- **Descrição:** Tokens de sessão/JWT podem ser roubados ou forjados.
- **Contramedidas:**
  - Assinatura e rotação de chaves
  - Curto TTL + refresh seguro
  - MFA
  - TLS obrigatório

**T — Tampering (Adulteração)**
- **Ameaça:** Adulteração de claims/perfis
- **Descrição:** Claims podem ser manipuladas se validação for fraca.
- **Contramedidas:**
  - Validação de assinatura
  - Audience/issuer checks
  - Scopes/roles no servidor

**R — Repudiation (Repúdio)**
- **Ameaça:** Falha de auditoria de autenticação
- **Descrição:** Sem logs de login, tentativas e mudanças de privilégios.
- **Contramedidas:**
  - Logs de autenticação
  - Alertas de brute force
  - Integração com SIEM

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Brute force / credential stuffing
- **Descrição:** Ataques massivos de login degradam o serviço.
- **Contramedidas:**
  - Rate limit
  - CAPTCHA/step-up auth
  - Bloqueio progressivo
  - WAF rules

**E — Elevation of Privilege (Elevação de privilégio)**
- **Ameaça:** Bypass de autorização
- **Descrição:** Permissões erradas permitem acesso elevado.
- **Contramedidas:**
  - RBAC/ABAC bem definido
  - Least privilege
  - Revisões periódicas de acesso

### 3.13 `app_service` (conf: 0.33)

**S — Spoofing (Falsificação de identidade)**
- **Ameaça:** Service-to-service spoofing
- **Descrição:** Serviço malicioso finge ser outro serviço interno.
- **Contramedidas:**
  - mTLS
  - Service identity
  - Network policies

**T — Tampering (Adulteração)**
- **Ameaça:** RCE / dependências vulneráveis
- **Descrição:** Código/dependências permitem execução remota ou alteração de dados.
- **Contramedidas:**
  - SAST/DAST
  - SBOM
  - Patch management
  - Least privilege runtime

**R — Repudiation (Repúdio)**
- **Ameaça:** Ações sem auditoria de negócio
- **Descrição:** Operações críticas não têm trilha.
- **Contramedidas:**
  - Logs de negócio
  - Auditoria por evento
  - Imutabilidade de logs

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Segredos expostos
- **Descrição:** Chaves/token em env/logs ou repositório.
- **Contramedidas:**
  - Secret manager
  - Rotação
  - Redação de logs
  - CI checks

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Exaustão de recursos
- **Descrição:** CPU/memória saturadas por payload pesado.
- **Contramedidas:**
  - Rate limit
  - Limites de payload
  - Auto scaling
  - Fila assíncrona

**E — Elevation of Privilege (Elevação de privilégio)**
- **Ameaça:** Privilégios excessivos no runtime
- **Descrição:** Serviço com permissões além do necessário.
- **Contramedidas:**
  - IAM least privilege
  - Separar roles
  - Revisão de permissões

### 3.14 `cdn` (conf: 0.31)

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

### 3.15 `load_balancer` (conf: 0.26)

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

## 4) Limitações do MVP
- O detector reconhece um conjunto limitado de classes (multi-cloud genéricas).
- O mapeamento STRIDE é baseado em regras (base de conhecimento estática).
- Não inferimos fluxos/DFDs; apenas analisamos componentes detectados.

## 5) Próximos Passos
- Aumentar o dataset e refinar classes (ex.: queue, secrets manager, CI/CD).
- Detectar relações/fluxos (setas) para gerar DFD e melhorar STRIDE por fronteira de confiança.
- Integrar busca de vulnerabilidades (CWE/CVE) por tipo de componente.
