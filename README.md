# Modelagem de Ameaças com IA (STRIDE)

**Projeto:** MVP de detecção supervisionada para modelagem de ameaças a partir de diagramas de arquitetura.  
**Contexto:** FIAP Software Security – validar uso de IA para identificar componentes e gerar relatório STRIDE automaticamente.

---

## 1. Objetivos do projeto

- **Interpretar automaticamente** um diagrama de arquitetura (imagem), identificando componentes (usuários, servidores, bases de dados, APIs, CDN, WAF, etc.).
- **Gerar um Relatório de Modelagem de Ameaças** baseado na metodologia **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
- **Construir/curar um dataset** de imagens de arquitetura de software e **anotar** para treino supervisionado.
- **Treinar um modelo** de detecção de objetos (YOLO) para reconhecer esses componentes.
- **Desenvolver um sistema** que, a partir dos componentes detectados, busque ameaças e contramedidas específicas (base de conhecimento STRIDE) e produza o relatório final.

---

## 2. Visão geral da arquitetura

```
[Diagramas de arquitetura]  →  [Dataset anotado]  →  [Treino YOLO]  →  [Modelo .pt]
                                                                              ↓
[Imagem nova]  →  [Detecção YOLO]  →  [Lista de componentes]  →  [Motor STRIDE]  →  [Relatório]
```

- **Preparação do dataset:** imagens de diagramas (AWS, Azure, genéricos) e/ou imagens sintéticas (grid ou fluxograma) + anotações em formato YOLO.
- **Treino:** modelo YOLO treinado com o dataset (11 classes = tipos de componente).
- **Inferência:** nova imagem → YOLO detecta caixas e classes → lista de componentes.
- **STRIDE:** cada componente é mapeado para ameaças e contramedidas na base de conhecimento → relatório em JSON e Markdown.

---

## 3. Documentação do fluxo de desenvolvimento da solução

Esta seção descreve o **fluxo utilizado para o desenvolvimento** do MVP, da coleta de dados até a geração do relatório.

### 3.1. Fase 1 — Aquisição e preparação de dados

| Etapa | Descrição | Ferramentas/Scripts |
|-------|-----------|----------------------|
| **Imagens brutas** | Diagramas reais (AWS, Azure, draw.io etc.) são colocados em `data/raw`. | — |
| **Padronização de nomes** | Imagens em `data/raw` são renomeadas para `arch_0.png`, `arch_1.png`, … (e SVGs convertidos para PNG se necessário). | `scripts/rename_raw_images.py` |
| **Ícones por classe** | Para dataset sintético, ícones PNG por classe ficam em `data/icon_dataset/<classe>/`. | — |
| **Geração sintética (grid)** | Geração de imagens com ícones em grid e anotações YOLO (prefixo `syn_`). | `scripts/generate_synthetic_dataset.py` |
| **Geração sintética (fluxograma)** | Geração de imagens em formato de fluxograma com camadas e setas (prefixo `flow_`). | `scripts/generate_flowchart_dataset.py` |
| **Anotação manual** | Imagens reais são anotadas com bounding boxes e labels (11 classes) em ferramentas como [Make Sense](https://makesense.ai) ou [Roboflow](https://roboflow.com). Export em formato **YOLO** (um `.txt` por imagem: `class_id x_center y_center width height` normalizados 0–1). | Make Sense / Roboflow |
| **Organização** | Pares imagem + `.txt` devem estar em `data/labeled/images/train` e `data/labeled/labels/train` (mesmo nome base, ex.: `arch_0001.png` e `arch_0001.txt`). | — |
| **Divisão train/val** | Cerca de 10% dos pares em `train` é movido para `images/val` e `labels/val` para validação do treino. | `scripts/split_train_val.py` |

### 3.2. Fase 2 — Configuração do dataset (YOLO)

- **Arquivo:** `data/architectures.yaml`
- Define: `path: data/labeled`, `train: images/train`, `val: images/val`, e o mapeamento `names: {0: user, 1: api_gateway, …}`.
- O treino e a inferência usam esse mapeamento (índice → nome da classe). A ordem das classes deve ser **exatamente** a das 11 classes listadas na seção 5.

### 3.3. Fase 3 — Treino do modelo

- **Comando (na raiz do projeto):**
  ```bash
  python scripts/train_yolo.py
  python scripts/train_yolo.py --epochs 100 --model yolov8n.pt   # opcional
  ```
- O script usa `data/architectures.yaml`, treina com Ultralytics YOLO e salva em `runs/detect/train/` (ou `train2`, `train3`, … se já existir).
- **Saída:** `runs/detect/train*/weights/best.pt` (e `last.pt`).

### 3.4. Fase 4 — Pipeline de inferência e relatório

- **Comando (na raiz do projeto):**
  ```bash
  python main.py \
    --image inputs/arch1.png \
    --model runs/detect/train/weights/best.pt \
    --outdir outputs
  ```
- **Fluxo interno:**
  1. **`src/detect.run_detection()`:** carrega o modelo YOLO, executa `predict()` na imagem, retorna lista de dicionários `{class, confidence, bbox}` (bbox em pixels: x, y, w, h).
  2. **`src/stride_engine.build_stride_report()`:** para cada componente detectado, consulta a base STRIDE (por nome da classe) e monta a lista de ameaças (S, T, R, I, D, E) com título, descrição e contramedidas.
  3. **`main.py`:** grava `outputs/detections.json`, `outputs/stride_report.json` e chama `src/report.to_markdown()` para gerar `outputs/report.md`.

### 3.5. Entregáveis e avaliação

- **Arquivos de saída:** `detections.json` (lista de componentes com classe, confiança e bbox), `stride_report.json` (resumo + ameaças STRIDE por componente), `report.md` (relatório em Markdown).
- **Avaliação:** utilizar as imagens na pasta **`inputs/`** para avaliar o sistema; rodar `main.py` para cada imagem com o `best.pt` do último treino e inspecionar `outputs/report.md` e `outputs/stride_report.json`.

---

## 4. Estrutura do repositório

```
threat-modeling-ai/
├── main.py                 # Ponto de entrada: imagem + modelo → relatório
├── requirements.txt
├── data/
│   ├── architectures.yaml  # Config do dataset YOLO (path, train/val, nomes das 11 classes)
│   ├── labeled/            # Dataset para treino
│   │   ├── images/train/   # Imagens de treino
│   │   ├── images/val/     # Imagens de validação
│   │   ├── labels/train/   # Labels YOLO (.txt) – um por imagem, mesmo nome base
│   │   └── labels/val/
│   ├── icon_dataset/       # Ícones por classe (geração de dataset sintético)
│   ├── raw/                # Imagens brutas (diagramas) antes de renomear/organizar
│   └── knowledge_base/    # (opcional) Vulnerabilidades CWE/CVE
├── src/
│   ├── detect.py           # run_detection(): carrega YOLO, prediz, retorna lista de componentes
│   ├── stride_engine.py    # Base STRIDE por classe + build_stride_report()
│   └── report.py           # to_markdown(): gera report.md a partir de detecções + STRIDE
├── scripts/
│   ├── train_yolo.py       # Treina o modelo (data/architectures.yaml → runs/detect/train*/)
│   ├── split_train_val.py  # Move ~10% de train para val (rebalanceia dataset)
│   ├── generate_synthetic_dataset.py  # Gera imagens sintéticas em grid (syn_*)
│   ├── generate_flowchart_dataset.py  # Gera imagens em formato fluxograma (flow_*)
│   └── rename_raw_images.py           # Renomeia imagens em data/raw (arch_0.png, ...)
├── inputs/                 # Imagens de teste para avaliação (ex.: arch1.png)
├── outputs/                # Saída do pipeline: detections.json, stride_report.json, report.md
└── runs/detect/train*/     # Saída do treino: weights/best.pt, métricas, gráficos
```

---

## 5. Classes do modelo (11 componentes)

As classes devem ser **exatamente** estas (com underscore), para coincidir com o motor STRIDE e com `data/architectures.yaml`:

| Índice | Classe             | Exemplo em diagramas                    |
|--------|--------------------|-----------------------------------------|
| 0      | user               | Usuários, pessoas                       |
| 1      | api_gateway        | API Gateway, API Management            |
| 2      | app_service        | App Service, Logic Apps, VMs, ECS      |
| 3      | database           | RDS, SQL, bancos de dados               |
| 4      | storage            | S3, Blob, EFS, armazenamento de arquivos|
| 5      | waf_firewall       | WAF, Firewall, AWS Shield              |
| 6      | cdn                | CloudFront, Front Door, CDN            |
| 7      | load_balancer      | ALB, Load Balancer                     |
| 8      | cache              | ElastiCache, Redis, cache              |
| 9      | monitoring_logging | CloudWatch, CloudTrail, monitoramento  |
| 10     | identity_auth      | IAM, Entra ID, autenticação            |

---

## 6. Funcionalidades e scripts — resumo

| Script | Função |
|--------|--------|
| **main.py** | Recebe `--image`, `--model`, `--outdir`; executa detecção → STRIDE → gera `detections.json`, `stride_report.json`, `report.md`. |
| **src/detect.py** | `run_detection(image_path, model_path, conf)` → lista de `{class, confidence, bbox}`. |
| **src/stride_engine.py** | Base de conhecimento STRIDE por classe; `build_stride_report(detections)` → `{summary, components}` com ameaças e contramedidas. |
| **src/report.py** | `to_markdown(image_path, detections, stride_data)` → string Markdown do relatório. |
| **scripts/train_yolo.py** | Treina YOLO com `data/architectures.yaml`; argumentos opcionais: `--epochs`, `--model`, `--imgsz`. |
| **scripts/split_train_val.py** | Move ~10% dos pares (imagem + label) de train para val; `--ratio`, `--seed` opcionais. |
| **scripts/generate_synthetic_dataset.py** | Gera imagens sintéticas em grid a partir de `data/icon_dataset`, com labels YOLO em `data/labeled`. |
| **scripts/generate_flowchart_dataset.py** | Gera imagens em formato fluxograma (camadas + setas) com anotações YOLO; `--count`, `--out-size` opcionais. |
| **scripts/rename_raw_images.py** | Renomeia imagens em `data/raw` para `arch_0.png`, …; converte SVG→PNG se `cairosvg` estiver instalado; `--dir`, `--dry-run` opcionais. |

---

## 7. Conteúdo do relatório gerado

- **detections.json:** lista de componentes com `class`, `confidence` e `bbox` (x, y, w, h em pixels).
- **stride_report.json:** `summary` (total_components, by_class) + `components` (para cada um: class, confidence, bbox, lista `stride` com code, label, title, description, mitigations).
- **report.md:** relatório em Markdown com resumo, tabela de detecções, seção “Ameaças por componente (STRIDE)”, limitações do MVP e próximos passos.

---

## 8. Tecnologias utilizadas

- **Python 3**
- **Ultralytics YOLO** (YOLOv8): detecção de objetos.
- **Dataset:** formato YOLO (bounding boxes normalizadas).
- **Metodologia:** STRIDE; base de conhecimento codificada em `src/stride_engine.py` (ameaças e contramedidas por tipo de componente).
- **Pillow:** manipulação de imagens nos scripts de dataset sintético.
- **Opcional:** cairosvg para conversão SVG→PNG em `rename_raw_images.py`.

---

## 9. Limitações do MVP

- Conjunto fixo de 11 classes; diagramas com outros símbolos podem não ser reconhecidos.
- STRIDE é baseado em regras estáticas (por classe), sem inferência de fluxos ou DFD.
- Não há detecção de setas/relações; a análise é por componente, não por fronteira de confiança entre atores.

---

## 10. Referências rápidas

- **Treino:** `python scripts/train_yolo.py [--epochs N] [--model yolov8n.pt]`
- **Relatório:** `python main.py --image <caminho_imagem> --model runs/detect/train/weights/best.pt --outdir outputs`
- **Split train/val:** `python scripts/split_train_val.py [--ratio 0.10]`
- **Classes:** seção 5 ou `data/architectures.yaml`.

---

## 11. Autor

**Stefhany Santos**

Projeto desenvolvido para o **Hackaton - Fase 5**  
**FIAP** — Pós-Graduação em Inteligência Artificial

---

## 12. Referências

- **STRIDE** — Metodologia de modelagem de ameaças (Microsoft Security).
- **Ultralytics YOLO** — [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) — Detecção de objetos (YOLOv8).
