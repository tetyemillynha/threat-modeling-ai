# Modelagem de Ameaças com IA (STRIDE)

**Projeto:** MVP de detecção supervisionada para modelagem de ameaças a partir de diagramas de arquitetura.  
**Contexto:** FIAP Software Security – validar uso de IA para identificar componentes e gerar relatório STRIDE automaticamente.

## 1. Objetivos do projeto

- **Interpretar automaticamente** um diagrama de arquitetura (imagem), identificando componentes (usuários, servidores, bases de dados, APIs, CDN, WAF, etc.).
- **Gerar um Relatório de Modelagem de Ameaças** baseado na metodologia **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
- **Construir/curar um dataset** de imagens de arquitetura de software e **anotar** para treino supervisionado.
- **Treinar um modelo** de detecção de objetos (YOLO) para reconhecer esses componentes.
- **Desenvolver um sistema** que, a partir dos componentes detectados, busque ameaças e contramedidas específicas (base de conhecimento STRIDE) e produza o relatório final.

---

## 2. Visão geral do fluxo

```
[Diagramas de arquitetura]  →  [Dataset anotado]  →  [Treino YOLO]  →  [Modelo .pt]
                                                                              ↓
[Imagem nova]  →  [Detecção YOLO]  →  [Lista de componentes]  →  [Motor STRIDE]  →  [Relatório]
```

1. **Preparação do dataset:** imagens de diagramas (AWS, Azure, genéricos) + anotações em formato YOLO.
2. **Treino:** modelo YOLO treinado com o dataset (classes = tipos de componente).
3. **Inferência:** nova imagem → YOLO detecta caixas e classes → lista de componentes.
4. **STRIDE:** cada componente é mapeado para ameaças e contramedidas na base de conhecimento → relatório em JSON e Markdown.

---

## 3. Estrutura do repositório

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
│   ├── icon_dataset/       # Ícones por classe (opcional: geração de dataset sintético)
│   └── knowledge_base/     # (opcional) Vulnerabilidades CWE/CVE
├── src/
│   ├── detect.py           # run_detection(): carrega YOLO, prediz, retorna lista de componentes
│   ├── stride_engine.py    # Base STRIDE por classe + build_stride_report()
│   └── report.py           # to_markdown(): gera report.md a partir de detecções + STRIDE
├── scripts/
│   ├── train_yolo.py       # Treina o modelo (data/architectures.yaml → runs/detect/train*/)
│   ├── move_yolo_dataset_to_labeled.py  # Move imagens/labels de yolo_dataset → labeled + renomeia
│   ├── split_train_val.py  # Move ~10% de train para val (syn_* ou similar)
│   ├── generate_synthetic_dataset.py    # Gera imagens sintéticas a partir de icon_dataset
│   └── rename_raw_images.py             # Renomeia imagens em data/raw (arch_0.png, ...)
├── inputs/                 # Imagens de teste (ex.: arch1.png)
├── outputs/                # Saída do pipeline: detections.json, stride_report.json, report.md
└── runs/detect/train*/     # Saída do treino: weights/best.pt
```

---

## 4. Classes do modelo (11 componentes)

As classes devem ser **exatamente** estas (com underscore), para bater com o motor STRIDE e com `data/architectures.yaml`:

| Índice | Classe             | Exemplo em diagramas                    |
|--------|--------------------|-----------------------------------------|
| 0      | user               | Usuários, pessoas                       |
| 1      | api_gateway        | API Gateway, API Management            |
| 2      | app_service        | App Service, Logic Apps, VMs, ECS       |
| 3      | database           | RDS, SQL, bancos de dados               |
| 4      | storage            | S3, Blob, EFS, armazenamento de arquivos|
| 5      | waf_firewall       | WAF, Firewall, AWS Shield               |
| 6      | cdn                | CloudFront, Front Door, CDN             |
| 7      | load_balancer      | ALB, Load Balancer                      |
| 8      | cache              | ElastiCache, Redis, cache               |
| 9      | monitoring_logging | CloudWatch, CloudTrail, monitoramento   |
| 10     | identity_auth      | IAM, Entra ID, autenticação             |

---

## 5. Fluxo detalhado

### 5.1. Dataset e anotação

- **Fontes de imagens:** diagramas reais (AWS, Azure) em `data/raw` ou `data/images`; opcionalmente imagens sintéticas geradas por `scripts/generate_synthetic_dataset.py` a partir de `data/icon_dataset`.
- **Ferramenta de anotação:** [Make Sense](https://makesense.ai) ou [Roboflow](https://roboflow.com). Upload das imagens, desenho de bounding boxes, tags com os **11 nomes exatos** (ex.: `api_gateway`, `monitoring_logging`).
- **Export:** formato **YOLO** (um `.txt` por imagem: `class_id x_center y_center width height` normalizados 0–1).
- **Organização:** pares imagem + `.txt` em `data/labeled/images/train` e `labels/train` (e opcionalmente `val`). Mesmo nome base (ex.: `arch_0001.png` e `arch_0001.txt`).
- **Scripts auxiliares:**
  - `move_yolo_dataset_to_labeled.py`: move de `data/yolo_dataset` para `data/labeled` e renomeia para padrão único (ex.: `yolo_0001.png`).
  - `split_train_val.py`: separa ~10% dos pares para `images/val` e `labels/val`.

### 5.2. Configuração do dataset (YOLO)

- **Arquivo:** `data/architectures.yaml`
- Define: `path: data/labeled`, `train: images/train`, `val: images/val`, e o mapeamento `names: {0: user, 1: api_gateway, ...}`.
- O treino e a inferência usam esse mapeamento (índice → nome da classe).

### 5.3. Treino do modelo

- **Comando:** na raiz do projeto:
  ```bash
  python scripts/train_yolo.py
  python scripts/train_yolo.py --epochs 100 --model yolov8n.pt  # opcional
  ```
- O script usa `data/architectures.yaml`, treina com Ultralytics YOLO e salva em `runs/detect/train/` (ou `train2`, `train3`, … se já existir).
- **Saída:** `runs/detect/train*/weights/best.pt` (e `last.pt`).

### 5.4. Geração do relatório (inferência + STRIDE)

- **Comando:** na raiz do projeto:
  ```bash
  python main.py \
  --image inputs/arch1.png \
  --model runs/detect/train/weights/best.pt \
  --outdir outputs
  ```
- **Fluxo interno:**
  1. **`src/detect.run_detection()`:** carrega o modelo YOLO, roda `predict()` na imagem, retorna lista de dicionários `{class, confidence, bbox}`.
  2. **`src/stride_engine.build_stride_report()`:** para cada componente detectado, consulta a base STRIDE (por nome da classe) e monta a lista de ameaças (S, T, R, I, D, E) com título, descrição e contramedidas.
  3. **`main.py`:** grava `outputs/detections.json`, `outputs/stride_report.json` e chama `src/report.to_markdown()` para gerar `outputs/report.md`.

### 5.5. Conteúdo do relatório

- **detections.json:** lista de componentes com classe, confiança e bbox (x, y, w, h).
- **stride_report.json:** resumo (total, contagem por classe) + para cada componente as ameaças STRIDE e contramedidas.
- **report.md:** relatório em Markdown com resumo, tabela de detecções, seção “Ameaças por componente (STRIDE)”, limitações do MVP e próximos passos.

---

## 6. Avaliação (entregáveis)

- **Arquiteturas de teste:** conforme enunciado, utilizar as imagens na pasta **`inputs/`** para avaliar o sistema.
- **Comando sugerido:** rodar `main.py` para cada imagem em `inputs/` com o `best.pt` do último treino e inspecionar `outputs/report.md` e `outputs/stride_report.json`.

---

## 7. Tecnologias utilizadas

- **Python 3**
- **Ultralytics YOLO** (YOLOv8): detecção de objetos.
- **Dataset:** formato YOLO (bounding boxes normalizadas).
- **Metodologia:** STRIDE; base de conhecimento codificada em `src/stride_engine.py` (ameaças e contramedidas por tipo de componente).

---

## 8. Limitações do MVP

- Conjunto fixo de 11 classes; diagramas com outros símbolos podem não ser reconhecidos.
- STRIDE é baseado em regras estáticas (por classe), sem inferência de fluxos ou DFD.
- Não há detecção de setas/relações; a análise é por componente, não por fronteira de confiança entre atores.

---

## 9. Referências rápidas

- **Treino:** `python scripts/train_yolo.py [--epochs N]`
- **Relatório:** `python main.py --image <caminho_imagem> --model runs/detect/train/weights/best.pt --outdir outputs`
- **Classes:** ver seção 4 ou `data/architectures.yaml`.
