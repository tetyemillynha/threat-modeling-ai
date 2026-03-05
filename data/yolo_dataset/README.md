# Dataset YOLO – Componentes de diagramas de arquitetura

Este diretório segue o formato **YOLO** para treinar um modelo de detecção de objetos que identifica componentes em diagramas (usuário, API Gateway, banco de dados, etc.). As detecções são usadas pelo motor STRIDE do projeto.

## Onde ficam as imagens?

- **data/images/** – use para guardar seus diagramas e como entrada do pipeline. Pode deixar tudo aí.
- **data/yolo_dataset/images/** – só para o **treino** do YOLO. Depois de anotar (LabelImg ou Roboflow), **copie ou mova** as imagens (e os arquivos `.txt` de labels) para `images/train` e `images/val` dentro deste diretório. Ou seja: as mesmas imagens que estão em `data/images` devem ser organizadas aqui, com train/val e labels, para o script `train_yolo.py` encontrar.

## Fluxo recomendado (MVP)

1. **Coletar ~90 diagramas** e colocar em `data/images/` (ou em qualquer pasta).
2. **Anotar** cada imagem com **LabelImg** ou **Roboflow Annotate**, desenhando caixas nos componentes.
3. **Exportar** no **formato YOLO**.
4. **Organizar** aqui: imagens em `images/train` e `images/val`, labels em `labels/train` e `labels/val` (mesmo nome da imagem no .txt).
5. **Treinar** com `python scripts/train_yolo.py`.

---

## Classes (componentes)

Use **exatamente** os nomes abaixo ao criar o projeto no LabelImg ou Roboflow. A ordem define o **class_id** (0 a 14):

| ID | Classe                  |
|----|-------------------------|
| 0  | user                    |
| 1  | api_gateway             |
| 2  | load_balancer           |
| 3  | application_server      |
| 4  | database                |
| 5  | cache                   |
| 6  | storage                 |
| 7  | cdn                     |
| 8  | waf                     |
| 9  | auth_service            |
| 10 | message_queue           |
| 11 | external_service        |
| 12 | developer_portal        |
| 13 | workflow_orchestrator   |
| 14 | other                   |

O arquivo **`classes.txt`** já contém essa lista (uma linha por classe). Use-o no LabelImg.

---

## LabelImg

1. Instale: `pip install labelImg` ou use o executável.
2. Abra LabelImg, **File → Change default saved target folder** para a pasta onde quer salvar os `.txt` (ex.: `labels/train`).
3. **Edit → Predefined classes**: carregue o conteúdo de `classes.txt` (uma classe por linha) ou digite as classes na ordem acima.
4. **View → Auto Save mode** (opcional).
5. Para cada imagem:
   - **Open Dir** → pasta com as imagens.
   - Desenhe retângulos (tecla **W**) em volta de cada componente (ícone, caixa, texto do componente).
   - Atribua a classe correta (ex.: `database`, `api_gateway`).
   - Salve (**Ctrl+S**). No modo YOLO, será gerado um `.txt` com o mesmo nome da imagem.
6. **Formato**: escolha **YOLO** (não PascalVOC).
7. Depois copie as imagens para `images/train` (ou `val`) e os `.txt` para `labels/train` (ou `val`), mantendo os nomes iguais.

---

## Roboflow Annotate

1. Crie um projeto em [Roboflow](https://roboflow.com) (ou use Roboflow Annotate local).
2. Crie as **classes** com os mesmos nomes da tabela acima (e na mesma ordem, se o export usar índice numérico).
3. Faça upload das imagens e desenhe as bounding boxes em cada componente.
4. Ao finalizar, **Export** → formato **YOLO v8** (ou YOLO Darknet).
5. Descompacte o zip no projeto. Geralmente virá com pastas `train/`, `valid/`, `data.yaml`. Ajuste para nossa estrutura:
   - Coloque as imagens em `images/train` e `images/val`.
   - Coloque os labels em `labels/train` e `labels/val`.
   - Se o `data.yaml` exportado tiver `names` em ordem diferente, substitua pelo nosso `data.yaml` para manter os IDs alinhados com o STRIDE.

---

## Estrutura esperada após preparar o dataset

```
yolo_dataset/
├── classes.txt          # lista de classes (já existe)
├── data.yaml            # configuração Ultralytics (já existe)
├── README.md             # este arquivo
├── images/
│   ├── train/           # imagens de treino (ex.: img1.png, img2.png)
│   └── val/             # imagens de validação
└── labels/
    ├── train/           # um .txt por imagem (ex.: img1.txt, img2.txt)
    └── val/
```

Cada arquivo `.txt` em `labels/` tem uma linha por objeto:

```
class_id center_x center_y width height
```

Valores normalizados entre 0 e 1 (centro e tamanho relativos à imagem).

---

## Treino

Com as pastas preenchidas:

```bash
python scripts/train_yolo.py
```

O modelo treinado será salvo em `output/yolo_models/` (ou caminho configurável). Use depois:

```bash
python scripts/run_pipeline.py data/images/seu_diagrama.png --model output/yolo_models/train/weights/best.pt -o output
```

As detecções do YOLO serão convertidas em lista de componentes e enviadas ao motor STRIDE.
