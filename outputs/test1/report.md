# Relatório de Modelagem de Ameaças (STRIDE)
**Imagem analisada:** `inputs/arch1.png`  
**Gerado em:** 2026-03-05 22:01 UTC
## 1) Resumo
- Componentes detectados: **24**
- Contagem por classe:
  - `api_gateway`: **1**
  - `app_service`: **2**
  - `cache`: **2**
  - `cdn`: **3**
  - `database`: **1**
  - `identity_auth`: **3**
  - `load_balancer`: **6**
  - `monitoring_logging`: **2**
  - `storage`: **1**
  - `user`: **3**

## 2) Componentes Detectados
| # | Classe | Confiança | Bounding Box |
|---|--------|-----------|--------------|
| 1 | `identity_auth` | 1.00 | x=987, y=244, w=86, h=85 |
| 2 | `api_gateway` | 1.00 | x=493, y=63, w=86, h=81 |
| 3 | `load_balancer` | 0.99 | x=495, y=542, w=39, h=37 |
| 4 | `monitoring_logging` | 0.99 | x=112, y=819, w=86, h=88 |
| 5 | `identity_auth` | 0.99 | x=988, y=680, w=87, h=85 |
| 6 | `app_service` | 0.99 | x=535, y=822, w=88, h=81 |
| 7 | `user` | 0.99 | x=366, y=62, w=85, h=82 |
| 8 | `identity_auth` | 0.99 | x=988, y=836, w=83, h=81 |
| 9 | `cdn` | 0.98 | x=464, y=393, w=93, h=63 |
| 10 | `database` | 0.98 | x=67, y=50, w=113, h=104 |
| 11 | `user` | 0.97 | x=648, y=62, w=84, h=83 |
| 12 | `load_balancer` | 0.97 | x=764, y=614, w=92, h=107 |
| 13 | `cache` | 0.95 | x=394, y=823, w=87, h=80 |
| 14 | `load_balancer` | 0.95 | x=761, y=821, w=91, h=109 |
| 15 | `storage` | 0.94 | x=984, y=384, w=90, h=82 |
| 16 | `load_balancer` | 0.91 | x=158, y=611, w=100, h=92 |
| 17 | `load_balancer` | 0.79 | x=469, y=613, w=91, h=90 |
| 18 | `cdn` | 0.77 | x=769, y=393, w=88, h=65 |
| 19 | `app_service` | 0.68 | x=395, y=822, w=86, h=81 |
| 20 | `cdn` | 0.63 | x=166, y=394, w=93, h=67 |
| 21 | `cache` | 0.47 | x=225, y=822, w=87, h=81 |
| 22 | `user` | 0.39 | x=495, y=538, w=42, h=41 |
| 23 | `monitoring_logging` | 0.36 | x=988, y=545, w=86, h=86 |
| 24 | `load_balancer` | 0.28 | x=784, y=750, w=43, h=41 |

## 3) Ameaças por Componente (STRIDE)

### 3.1 `identity_auth` (conf: 1.00)

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

### 3.2 `api_gateway` (conf: 1.00)

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

### 3.3 `load_balancer` (conf: 0.99)

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

### 3.4 `monitoring_logging` (conf: 0.99)

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

### 3.5 `identity_auth` (conf: 0.99)

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

### 3.6 `app_service` (conf: 0.99)

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

### 3.7 `user` (conf: 0.99)

**S — Spoofing (Falsificação de identidade)**
- **Ameaça:** Uso de credenciais comprometidas
- **Descrição:** Atacante usa credenciais roubadas para acessar o sistema.
- **Contramedidas:**
  - MFA/2FA
  - Política de senhas fortes
  - Detecção de login anômalo

**R — Repudiation (Repúdio)**
- **Ameaça:** Ações sem rastreabilidade
- **Descrição:** Usuário nega ações por falta de trilha de auditoria.
- **Contramedidas:**
  - Logs de auditoria
  - Carimbo de data/hora
  - Correlação de eventos por usuário

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Exposição via engenharia social
- **Descrição:** Vazamento de dados por phishing ou compartilhamento indevido.
- **Contramedidas:**
  - Treinamento
  - DLP onde aplicável
  - Princípio do menor privilégio

### 3.8 `identity_auth` (conf: 0.99)

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

### 3.9 `cdn` (conf: 0.98)

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

### 3.10 `database` (conf: 0.98)

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

### 3.11 `user` (conf: 0.97)

**S — Spoofing (Falsificação de identidade)**
- **Ameaça:** Uso de credenciais comprometidas
- **Descrição:** Atacante usa credenciais roubadas para acessar o sistema.
- **Contramedidas:**
  - MFA/2FA
  - Política de senhas fortes
  - Detecção de login anômalo

**R — Repudiation (Repúdio)**
- **Ameaça:** Ações sem rastreabilidade
- **Descrição:** Usuário nega ações por falta de trilha de auditoria.
- **Contramedidas:**
  - Logs de auditoria
  - Carimbo de data/hora
  - Correlação de eventos por usuário

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Exposição via engenharia social
- **Descrição:** Vazamento de dados por phishing ou compartilhamento indevido.
- **Contramedidas:**
  - Treinamento
  - DLP onde aplicável
  - Princípio do menor privilégio

### 3.12 `load_balancer` (conf: 0.97)

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

### 3.13 `cache` (conf: 0.95)

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Cache poisoning / dados sensíveis
- **Descrição:** Dados errados/sensíveis podem vazar pelo cache.
- **Contramedidas:**
  - Chaves de cache bem definidas
  - Evitar cache de PII
  - TTL adequado

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Eviction / cache stampede
- **Descrição:** Explosão de misses causa sobrecarga no backend.
- **Contramedidas:**
  - TTL com jitter
  - Locking/Singleflight
  - Warmup

**E — Elevation of Privilege (Elevação de privilégio)**
- **Ameaça:** Acesso administrativo ao cache
- **Descrição:** Painéis/portas abertas permitem controle do cache.
- **Contramedidas:**
  - Rede privada
  - Auth
  - Segurança por grupo/NSG

### 3.14 `load_balancer` (conf: 0.95)

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

### 3.15 `storage` (conf: 0.94)

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

### 3.16 `load_balancer` (conf: 0.91)

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

### 3.17 `load_balancer` (conf: 0.79)

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

### 3.18 `cdn` (conf: 0.77)

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

### 3.19 `app_service` (conf: 0.68)

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

### 3.20 `cdn` (conf: 0.63)

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

### 3.21 `cache` (conf: 0.47)

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Cache poisoning / dados sensíveis
- **Descrição:** Dados errados/sensíveis podem vazar pelo cache.
- **Contramedidas:**
  - Chaves de cache bem definidas
  - Evitar cache de PII
  - TTL adequado

**D — Denial of Service (Negação de serviço)**
- **Ameaça:** Eviction / cache stampede
- **Descrição:** Explosão de misses causa sobrecarga no backend.
- **Contramedidas:**
  - TTL com jitter
  - Locking/Singleflight
  - Warmup

**E — Elevation of Privilege (Elevação de privilégio)**
- **Ameaça:** Acesso administrativo ao cache
- **Descrição:** Painéis/portas abertas permitem controle do cache.
- **Contramedidas:**
  - Rede privada
  - Auth
  - Segurança por grupo/NSG

### 3.22 `user` (conf: 0.39)

**S — Spoofing (Falsificação de identidade)**
- **Ameaça:** Uso de credenciais comprometidas
- **Descrição:** Atacante usa credenciais roubadas para acessar o sistema.
- **Contramedidas:**
  - MFA/2FA
  - Política de senhas fortes
  - Detecção de login anômalo

**R — Repudiation (Repúdio)**
- **Ameaça:** Ações sem rastreabilidade
- **Descrição:** Usuário nega ações por falta de trilha de auditoria.
- **Contramedidas:**
  - Logs de auditoria
  - Carimbo de data/hora
  - Correlação de eventos por usuário

**I — Information Disclosure (Exposição de informação)**
- **Ameaça:** Exposição via engenharia social
- **Descrição:** Vazamento de dados por phishing ou compartilhamento indevido.
- **Contramedidas:**
  - Treinamento
  - DLP onde aplicável
  - Princípio do menor privilégio

### 3.23 `monitoring_logging` (conf: 0.36)

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

### 3.24 `load_balancer` (conf: 0.28)

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
