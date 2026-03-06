# Roteiro para vídeo de 15 minutos – Modelagem de Ameaças com IA (STRIDE)

**Duração total alvo:** ~15 min  
**Objetivo:** Explicar o problema, a estrutura do projeto, o papel de cada parte do código, como o modelo aprende, e por fim mostrar os resultados (relatórios e o que o modelo concluiu).

**Material de apoio detalhado:** [docs/APRESENTACAO_PROJETO.md](APRESENTACAO_PROJETO.md) — use para consulta durante a gravação.

---

## Cronograma sugerido

| Trecho | Tempo | Conteúdo |
|--------|--------|----------|
| 1. Abertura e contexto | 0:00 – 1:20 | Apresentação, FIAP Software Security, objetivo (modelagem de ameaças com IA, STRIDE) |
| 2. Problema e necessidade de dados | 1:20 – 2:30 | Por que precisa de biblioteca de imagens variadas; criar classes e anotar |
| 3. De onde vieram as imagens e anotação manual | 2:30 – 4:00 | Imagens da AWS/Azure; Make Sense; anotação manual (caixas + classes); export YOLO |
| 4. Script de geração automática e outros scripts | 4:00 – 6:00 | Ícones AWS/GCP/Azure; `generate_synthetic_dataset.py` (mostrar o script); move, split, rename, train |
| 5. Estrutura: imagens de treino e labels | 6:00 – 6:50 | data/labeled (train/val), um .txt por imagem, formato YOLO, architectures.yaml |
| 6. Como o modelo aprende e o que tem em runs/ | 6:50 – 8:30 | YOLO, treino vs val; mostrar runs/ (confusion matrix, curvas, best.pt, results.csv) |
| 7. Código: detect, stride_engine, report e dependências | 8:30 – 10:30 | Para que serve cada um em src/; por que Ultralytics, Pillow, OpenCV, Jinja2 |
| 8. Demo: gerar relatório | 10:30 – 12:00 | Rodar main.py com imagem de inputs/; mostrar outputs/ |
| 9. Resultados: o que cada arquivo significa e o que o modelo concluiu | 12:00 – 14:00 | detections.json, stride_report.json, report.md; “o que o modelo concluiu da arquitetura” |
| 10. Fechamento | 14:00 – 15:00 | Limitações, próximos passos, link do GitHub |

---

## Roteiro por bloco (o que falar / mostrar)

### 1. Abertura e contexto (0:00 – 1:20)

- Apresente-se: projeto para a FIAP Software Security.
- “O objetivo era validar a viabilidade de usar **Inteligência Artificial** para fazer **modelagem de ameaças automaticamente** a partir de um **diagrama de arquitetura em imagem**, usando a metodologia **STRIDE**.”
- Escopo: **MVP** com detecção supervisionada — o modelo precisa aprender com exemplos anotados.

---

### 2. Problema e necessidade de dados (1:20 – 2:30)

- “Para o modelo **interpretar** diagramas e **identificar componentes** (usuário, API Gateway, banco de dados, CDN, WAF, etc.), é necessário uma **biblioteca de imagens de arquitetura diferentes**, para ele generalizar bem.”
- “Isso exige **criar as classes** (as 11 categorias que a gente definiu) e **anotar** cada imagem: dizer onde está cada componente e qual é a classe. Só com isso o YOLO consegue aprender.”

---

### 3. De onde vieram as imagens e anotação manual (2:30 – 4:00)

- “Para facilitar, peguei imagens de arquitetura **diretamente nos sites da AWS e da Azure** (diagramas de referência, documentação).”
- “Fiz as **anotações para o YOLO** usando o **Make Sense** (makesense.ai). Em cada imagem, fui em **cada componente** e fiz as anotações **de forma manual**: desenhei a caixa em volta do componente e escolhi a classe (user, api_gateway, database, etc.). No final exportei no formato YOLO, que gera um arquivo `.txt` por imagem.”
- “Como anotar tudo à mão não é suficiente para agilizar e ter bastante dado, usei também uma **biblioteca de ícones** de arquitetura (AWS, Google Cloud, Azure) e **criei um script** que gera imagens anotadas automaticamente — aí mostro esse script.”

---

### 4. Script de geração automática e outros scripts (4:00 – 6:00)

- Abrir **`scripts/generate_synthetic_dataset.py`**.
- Explicar em poucas palavras: “O script usa a pasta `data/icon_dataset/`, onde cada subpasta é uma classe (api_gateway, database, etc.) com ícones em PNG. Ele monta imagens sintéticas (fundo branco, grade), cola ícones aleatórios, calcula a bounding box no formato YOLO e salva a imagem e o `.txt` em `data/labeled`.” Mostrar as partes principais (ex.: descoberta de classes, geração da imagem, `to_yolo_bbox`, gravação em `train`).
- “Os **outros scripts** que precisei criar: **move_yolo_dataset_to_labeled** — move imagens/labels de outra pasta para `data/labeled` e renomeia tudo com o mesmo padrão (ex.: yolo_0001). **split_train_val** — tira uns 10% dos pares de train e manda para val, para o YOLO ter conjunto de validação. **rename_raw_images** — renomeia imagens em data/raw para um padrão sequencial. **train_yolo** — roda o treino usando o `data/architectures.yaml`.”

---

### 5. Estrutura: imagens de treino e labels (6:00 – 6:50)

- Mostrar a estrutura de **`data/labeled`**: `images/train`, `images/val`, `labels/train`, `labels/val`.
- “As **imagens de treino** ficam em `images/train` (e val em `images/val`). Os **labels** ficam em `labels/train` e `labels/val`: **um arquivo `.txt` por imagem**, com **o mesmo nome base** (ex.: syn_0000.png e syn_0000.txt). Cada linha do `.txt` é um objeto: class_id, centro x/y e largura/altura normalizados (formato YOLO). O `data/architectures.yaml` diz onde estão essas pastas e qual número é qual classe.”

---

### 6. Como o modelo aprende e o que tem em runs/ (6:50 – 8:30)

- “O modelo é um **YOLO** (Ultralytics): rede de detecção de objetos. O **aprendizado** acontece no treino: ele vê as imagens com as caixas anotadas e ajusta os pesos para acertar cada vez mais. A pasta **val** não é usada para atualizar pesos, só para **avaliar** (métricas, evitar overfitting).”
- Abrir a pasta **`runs/detect/train/`** (ou train2): “Aqui ficam os resultados do treino. **weights/best.pt** é o modelo que a gente usa depois. **results.csv** tem as métricas por época. **confusion_matrix_normalized.png** mostra onde o modelo confunde classes. **BoxPR_curve** e **BoxF1_curve** mostram precisão e recall por classe. **labels.jpg** é uma amostra visual do dataset. Tudo isso ajuda a entender como o modelo aprendeu.”

---

### 7. Código: detect, stride_engine, report e dependências (8:30 – 10:30)

- **`src/detect.py`**: “Aqui fica a função que **carrega o modelo YOLO** e **roda a predição** na imagem. Ela devolve a lista de componentes detectados: classe, confiança e posição da caixa (bbox). É a ponte entre ‘imagem + modelo’ e o resto do pipeline.”
- **`src/stride_engine.py`**: “Aqui está a **base de conhecimento STRIDE**: para cada tipo de componente (user, api_gateway, database, etc.) temos as ameaças S, T, R, I, D, E com descrição e contramedidas. A função **build_stride_report** recebe as detecções e, para cada componente, busca essas ameaças e monta o relatório estruturado.”
- **`src/report.py`**: “Gera o **relatório em Markdown**: resumo, tabela de componentes, e para cada um as ameaças STRIDE e contramedidas. O main.py chama isso e grava o `report.md`.”
- “No projeto atual **não tem utils.py**; o fluxo usa só esses três arquivos em src/.”
- **Dependências:** “**Ultralytics** é a biblioteca do YOLO — treino e inferência. **Pillow** usei nos scripts de dataset (gerar imagens sintéticas, renomear/redimensionar). **OpenCV** e **Jinja2** vêm como dependência do Ultralytics (leitura de imagem, relatórios internos). **Pydantic** também é do ecossistema Ultralytics (validação de config).”

---

### 8. Demo: gerar relatório (10:30 – 12:00)

- Terminal na **raiz do projeto**. Rodar:
  ```bash
  python main.py --image inputs/arch1.png --model runs/detect/train/weights/best.pt --outdir outputs
  ```
  (Ajustar nome da imagem e caminho do modelo se for train2, etc.)
- Mostrar a mensagem de sucesso e a pasta **outputs/**: “Ficam três arquivos: detections.json, stride_report.json e report.md.”

---

### 9. Resultados: o que cada arquivo significa e o que o modelo concluiu (12:00 – 14:00)

- **detections.json:** “É a **lista bruta** do que o modelo detectou: cada componente com classe, confiança e posição da caixa. Ou seja: **o que o modelo concluiu que existe na imagem** — quantos componentes, de que tipo e onde.”
- **stride_report.json:** “O sistema pegou cada componente detectado e **buscou na base STRIDE** as ameaças e contramedidas daquela classe. Aqui está o **resumo** (total, contagem por classe) e **cada componente** com suas ameaças S, T, R, I, D, E.”
- **report.md:** Abrir no editor ou em preview. “É o **relatório final para o usuário**: resumo, tabela de detecções e, para cada componente, as ameaças e as contramedidas em texto. **O que o modelo concluiu das arquiteturas que pedi para ele analisar** está aqui: quais componentes ele enxergou na imagem e quais riscos STRIDE e recomendações se aplicam a cada um.”

---

### 10. Fechamento (14:00 – 15:00)

- “Limitações do MVP: 11 classes fixas; STRIDE é por regras estáticas; não detectamos fluxos/setas. Próximos passos: mais dataset, mais classes, detecção de relações, integração com CWE/CVE.”
- “Documentação do fluxo e detalhes da apresentação estão em **docs/** no repositório.”
- Mostrar ou dizer o **link do GitHub**. Agradecer e encerrar.

---

## Dicas para gravação

- Tenha **uma imagem em inputs/** que o modelo reconheça bem para a demo.
- Deixe **APRESENTACAO_PROJETO.md** aberto para consulta (estrutura, scripts, libs, resultados).
- Use um cronômetro para não estourar 15 min; se precisar cortar, reduza um pouco o bloco 4 (scripts) ou 7 (código/dependências), mantendo **dataset → treino → runs/ → demo → resultados**.
