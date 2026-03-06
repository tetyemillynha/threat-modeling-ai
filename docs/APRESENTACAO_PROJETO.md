# Apresentação do projeto – Modelagem de Ameaças com IA (STRIDE)

Material de apoio para a apresentação em vídeo: estrutura do projeto, papel de cada arquivo, funcionamento do código e resultados.

---

## 1. Por que precisamos de uma biblioteca de imagens

Para o modelo **aprender** a reconhecer componentes em diagramas de arquitetura, ele precisa de **muitas imagens diferentes** com anotações (onde está cada componente e qual é a classe). Quanto mais variado o dataset — AWS, Azure, Google Cloud, diagramas genéricos — melhor o modelo generaliza para novas imagens.

Por isso o fluxo é:

1. **Obter imagens** de diagramas de arquitetura (sites oficiais, repositórios, screenshots).
2. **Criar as classes** (as 11 categorias: user, api_gateway, database, etc.).
3. **Anotar** cada imagem: desenhar caixas (bounding boxes) em volta de cada componente e associar à classe correta.
4. **Exportar** no formato que o YOLO entende (um arquivo `.txt` por imagem).
5. **Treinar** o modelo com esse dataset.

---

## 2. De onde vêm as imagens e como foram anotadas

### 2.1. Imagens reais (AWS e Azure)

- Foram usadas imagens de diagramas **diretamente dos sites da AWS e da Azure** (arquiteturas de referência, exemplos de documentação).
- Essas imagens são mais realistas e ajudam o modelo a reconhecer diagramas reais que o usuário vai submeter depois.

### 2.2. Anotação manual com Make Sense

- Ferramenta: **[Make Sense](https://makesense.ai)** (gratuita, no navegador).
- Processo:
  1. Upload das imagens de arquitetura.
  2. Definição das **11 classes** (com os nomes exatos: `user`, `api_gateway`, `monitoring_logging`, etc.).
  3. Em **cada imagem**, para **cada componente** visível: desenhar um retângulo em volta (bounding box) e escolher a classe.
  4. Exportar no formato **YOLO** → gera um arquivo `.txt` por imagem.

- Cada `.txt` contém linhas no formato:  
  `class_id x_center y_center width height`  
  (valores normalizados entre 0 e 1, relativos à largura/altura da imagem).

- Como anotar tudo à mão em muitas imagens é demorado, foi criada uma forma de **gerar mais dados automaticamente** (ver abaixo).

### 2.3. Geração automática com ícones (script de dataset sintético)

- Foi usada uma **biblioteca de ícones** de arquitetura (AWS, Google Cloud, Azure) disponível em `data/icon_dataset/`.
- Cada **pasta** dentro de `data/icon_dataset/` é uma **classe** (ex.: `api_gateway`, `database`, `identity_auth`) e contém vários PNGs de ícones daquele componente.
- O script **`scripts/generate_synthetic_dataset.py`** faz o seguinte:
  - Cria imagens “sintéticas” (ex.: 1024×768) com fundo branco.
  - Distribui ícones em uma grade (ex.: 3×2 células).
  - Em cada imagem, sorteia quantos componentes mostrar (ex.: 3 a 6), escolhe ícones aleatórios por classe, posiciona nas células e redimensiona.
  - Para cada ícone colado, calcula a **bounding box** no formato YOLO (centro e tamanho normalizados).
  - Salva a imagem em `data/labeled/images/train/` e o arquivo de labels em `data/labeled/labels/train/` com o mesmo nome base (ex.: `syn_0000.png` e `syn_0000.txt`).

- Assim é possível **gerar centenas de imagens anotadas automaticamente**, sem desenhar caixas à mão, o que acelera muito a montagem do dataset.

**Trecho relevante do script (ideia):**

- Descobre as classes a partir das pastas em `data/icon_dataset/` que tenham pelo menos um `.png`.
- Para cada imagem sintética: cria um fundo, sorteia posições na grade, cola ícones com `PIL`, calcula bbox normalizada e grava o `.txt` em formato YOLO.

### 2.4. Outros scripts que foram necessários

| Script | Função |
|--------|--------|
| **`scripts/move_yolo_dataset_to_labeled.py`** | Quando as imagens e labels estavam em `data/yolo_dataset/` (ex.: vindas do Make Sense em outra estrutura), esse script **move** tudo para `data/labeled/` e **renomeia** os pares para um padrão único (ex.: `yolo_0001.png` e `yolo_0001.txt`), mantendo train/val. Assim o YOLO encontra sempre um `.txt` com o mesmo nome da imagem. |
| **`scripts/split_train_val.py`** | Após colocar muitas imagens em `data/labeled/images/train` (e labels em `labels/train`), esse script **move cerca de 10%** dos pares (imagem + `.txt`) para `images/val` e `labels/val`. O treino usa train para aprender e val para avaliar (métricas, early stopping, etc.). |
| **`scripts/rename_raw_images.py`** | Renomeia imagens em `data/raw/` para um padrão sequencial (ex.: `arch_0.png`, `arch_1.png`), útil para organizar imagens baixadas antes de anotar. |
| **`scripts/train_yolo.py`** | Roda o treino do YOLO usando `data/architectures.yaml`; salva os pesos em `runs/detect/train/` (ou train2, train3…). |

---

## 3. Imagens de treino vs. labels

- **Imagens de treino:** ficam em `data/labeled/images/train/` (e validação em `images/val/`). Formatos típicos: PNG, JPG.
- **Labels:** ficam em `data/labeled/labels/train/` (e `labels/val/`). Um arquivo **`.txt` por imagem**, com **o mesmo nome base** (ex.: `arch_0001.png` → `arch_0001.txt`).
- Cada linha do `.txt` é um objeto na imagem:  
  `class_id x_center y_center width height`  
  (todos em relação à largura/altura da imagem, entre 0 e 1).
- O arquivo **`data/architectures.yaml`** diz ao YOLO onde estão as pastas e qual índice corresponde a qual classe (0: user, 1: api_gateway, …, 10: identity_auth).

---

## 4. Como o modelo funciona e o que aparece em `runs/`

- O modelo é um **YOLO** (Ultralytics YOLOv8): rede de detecção de objetos que, em cada região da imagem, prevê “aqui tem um objeto da classe X com confiança Y e caixa (x,y,w,h)”.
- **Aprendizado:** no treino, o modelo vê muitas imagens com labels; ajusta os pesos para minimizar o erro entre as caixas previstas e as caixas anotadas e entre as classes previstas e as reais. A validação (`val`) não é usada para atualizar pesos, só para medir desempenho.
- **Saída do treino em `runs/detect/train/` (ou train2, …):**
  - **`weights/best.pt`** e **`last.pt`**: pesos do modelo (use `best.pt` para inferência).
  - **`results.csv`**: métricas por época (loss, mAP, etc.).
  - **`confusion_matrix_normalized.png`**: matriz de confusão (quais classes o modelo confunde).
  - **`BoxPR_curve.png`** / **`BoxF1_curve.png`**: curvas Precision-Recall e F1 por classe.
  - **`labels.jpg`**: exemplos de imagens com as caixas anotadas (visualização do dataset).
  - **`args.yaml`**: hiperparâmetros e caminhos usados no treino.

Na apresentação, vale mostrar essas figuras e o `results.csv` para explicar como o modelo aprendeu e onde ele acerta ou erra mais.

---

## 5. Para que serve cada arquivo em `src/`

| Arquivo | Função |
|---------|--------|
| **`src/detect.py`** | Contém a função **`run_detection(image_path, model_path, conf)`**. Carrega o modelo YOLO a partir do `.pt`, roda a predição na imagem e retorna uma **lista de detecções**: cada item tem `class`, `confidence` e `bbox` (x, y, w, h em pixels). É a ponte entre “imagem + modelo” e “lista de componentes” que o resto do pipeline usa. |
| **`src/stride_engine.py`** | Contém a **base de conhecimento STRIDE** por tipo de componente. Para cada classe (user, api_gateway, database, etc.) há uma lista de **ThreatItem** (ameaça S, T, R, I, D ou E com título, descrição e contramedidas). A função **`build_stride_report(detections)`** recebe a lista de detecções e, para cada componente, busca as ameaças daquela classe e monta um dicionário com resumo (total, contagem por classe) e a lista de componentes com suas ameaças e contramedidas. Ou seja: “traduz” componentes detectados em relatório STRIDE. |
| **`src/report.py`** | Contém **`to_markdown(image_path, detections, stride_data)`**. Gera o texto do **relatório em Markdown**: cabeçalho, resumo, tabela de componentes detectados, seção “Ameaças por componente (STRIDE)” para cada um, limitações do MVP e próximos passos. O `main.py` chama essa função e grava o resultado em `outputs/report.md`. |
| **`utils.py`** | No repositório atual **não existe** `src/utils.py`; o pipeline usa apenas `detect.py`, `stride_engine.py` e `report.py`. Se no futuro forem extraídas funções auxiliares (ex.: leitura de config, formatação), podem ir em um `utils.py`. |

---

## 6. Por que usei Ultralytics, Jinja2, Pillow, OpenCV etc.

| Dependência | Uso no projeto |
|-------------|-----------------|
| **ultralytics** | Biblioteca que implementa o YOLO (treino e inferência). Fornece a API `YOLO(model_path)` e `model.predict()`, além do comando de treino. É o núcleo da detecção de componentes. |
| **opencv-python** | Usado **indiretamente** pelo Ultralytics para leitura de imagens e pré-processamento. Não é chamado diretamente no nosso código, mas o YOLO depende dele. |
| **Pillow (PIL)** | Usado nos **scripts de dataset**: `generate_synthetic_dataset.py` (criar imagens, colar ícones, salvar PNG) e `rename_raw_images.py` (abrir/redimensionar/salvar imagens ao renomear ou converter formato). |
| **jinja2** | Dependência do **Ultralytics** (templates para relatórios/logs). Não é usada diretamente no nosso código. |
| **pydantic** | Usado pelo Ultralytics para validação de configurações e parâmetros. Não é usada diretamente no nosso código. |

Resumindo: **Ultralytics** é a base do modelo; **Pillow** é a base da geração/renomeação de imagens nos scripts; **OpenCV, Jinja2 e Pydantic** vêm como dependências do ecossistema Ultralytics.

---

## 7. Resultados: o que cada saída significa e o que o modelo “concluiu”

Após treinar e rodar **`main.py`** com uma imagem de arquitetura (ex.: em `inputs/`), a pasta **`outputs/`** contém:

### 7.1. `detections.json`

- Lista de **todos os componentes detectados** na imagem.
- Cada item tem:
  - **`class`**: tipo do componente (user, api_gateway, database, etc.).
  - **`confidence`**: confiança do modelo (0 a 1).
  - **`bbox`**: posição da caixa na imagem (x, y, w, h em pixels).
- **O que isso significa:** “O modelo concluiu que nesta imagem existem N componentes, nesses locais e com essas classes e confianças.”

### 7.2. `stride_report.json`

- **Resumo:** total de componentes e contagem por classe.
- **Para cada componente:** lista de ameaças STRIDE (S, T, R, I, D, E) com título, descrição e contramedidas, conforme a base de conhecimento em `stride_engine.py`.
- **O que isso significa:** “Para cada componente que o modelo encontrou, o sistema buscou as ameaças e contramedidas cadastradas para aquela classe e montou o relatório estruturado.”

### 7.3. `report.md`

- Relatório em **Markdown** para leitura humana:
  - Imagem analisada e data.
  - Resumo (quantos componentes, contagem por classe).
  - Tabela de componentes (classe, confiança, bbox).
  - Para cada componente: ameaças STRIDE com descrição e contramedidas.
  - Limitações do MVP e próximos passos.
- **O que isso significa:** “Conclusão final em texto: a arquitetura analisada contém estes componentes e, para cada um, estes são os riscos STRIDE e as recomendações de mitigação.”

Na apresentação, vale mostrar **uma imagem de `inputs/`**, rodar o `main.py`, e em seguida abrir o **`report.md`** (e, se quiser, um trecho do `detections.json` e do `stride_report.json`) explicando que aquilo é o “diagnóstico” que o modelo e o motor STRIDE produziram para aquela arquitetura.

---

## 8. Ordem sugerida na apresentação

1. Contexto e objetivo (modelagem de ameaças com IA, STRIDE).
2. Necessidade de um dataset variado → imagens da AWS/Azure + anotação manual (Make Sense) + geração automática com ícones (mostrar `generate_synthetic_dataset.py` e os outros scripts).
3. Estrutura de dados: imagens de treino vs. labels, `data/architectures.yaml`.
4. Como o modelo aprende (YOLO, treino/val) e o que aparece em `runs/` (curvas, matriz de confusão, `best.pt`).
5. Papel de cada arquivo em `src/` (detect, stride_engine, report) e das dependências (Ultralytics, Pillow, etc.).
6. Demo: rodar `main.py` com uma imagem de `inputs/`.
7. Resultados: explicar o que é `detections.json`, `stride_report.json` e `report.md` e o que o modelo “concluiu” sobre as arquiteturas analisadas.

Para o roteiro cronometrado do vídeo de 15 min, use o arquivo **`docs/ROTEIRO_VIDEO_15MIN.md`**, que foi ajustado para seguir essa narrativa.
