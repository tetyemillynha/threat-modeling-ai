# Dataset a partir de ícones (AWS / Azure)

Em vez de anotar diagramas completos à mão, você pode usar os **ícones oficiais** da AWS e da Azure para gerar o dataset YOLO automaticamente.

## 1. Baixar os ícones

- **AWS:** https://aws.amazon.com/architecture/icons/  
  Faça download do kit (PNG). Procure ícones como: Amazon RDS, CloudFront, Elastic Load Balancing, WAF, S3, ElastiCache, etc.

- **Azure:** https://learn.microsoft.com/en-us/azure/architecture/icons/  
  Ícones em SVG/PNG: API Management, Logic Apps, Microsoft Entra, Storage, etc.

## 2. Mapear ícones para as nossas classes

Crie **uma pasta por classe** dentro de `data/icon_dataset/` com o **nome exato** da classe (igual ao `data/yolo_dataset/classes.txt`). Coloque dentro os PNG que representam aquela classe.

| Nossa classe            | Exemplos de ícones AWS / Azure |
|-------------------------|--------------------------------|
| **user**                | Ícone de usuário/pessoas (AWS ou genérico). |
| **api_gateway**         | API Gateway (AWS), API Management (Azure). |
| **load_balancer**       | Elastic Load Balancing (AWS), Load Balancer (Azure). |
| **application_server**  | EC2, computação, “Application” (AWS/Azure). |
| **database**            | Amazon RDS, DynamoDB (AWS); SQL Database, Cosmos DB (Azure). |
| **cache**               | ElastiCache (AWS), Cache for Redis (Azure). |
| **storage**             | S3, EFS (AWS); Blob Storage, File Storage (Azure). |
| **cdn**                 | CloudFront (AWS), Azure CDN. |
| **waf**                 | AWS WAF; Azure WAF (se existir ícone). |
| **auth_service**        | Cognito (AWS), Microsoft Entra (Azure). |
| **message_queue**       | SQS, SNS (AWS); Service Bus, Event Hubs (Azure). |
| **external_service**    | “Generic” / “External” ou ícone de nuvem genérico. |
| **developer_portal**    | Developer portal (Azure API Management). |
| **workflow_orchestrator** | Step Functions (AWS), Logic Apps (Azure). |
| **other**               | Shield, CloudWatch, Backup, KMS, etc. |

Exemplo de estrutura depois de baixar e organizar:

```
data/icon_dataset/
  user/           <- 1 ou mais PNG de ícone de usuário
  database/       <- RDS, DynamoDB, etc.
  cdn/            <- CloudFront
  waf/            <- WAF
  load_balancer/  <- ELB
  application_server/
  cache/          <- ElastiCache
  storage/        <- S3, EFS
  api_gateway/
  auth_service/   <- Entra, Cognito
  workflow_orchestrator/  <- Logic Apps, Step Functions
  developer_portal/
  message_queue/
  external_service/
  other/
```

Não é obrigatório ter as 15 pastas; pode começar com as que você tiver ícones (ex.: user, database, load_balancer, application_server, cache, storage, cdn, waf, other).

## 3. Gerar o dataset YOLO

Com as pastas preenchidas:

```bash
python scripts/build_dataset_from_icons.py
```

O script:
- Lê cada PNG em cada pasta (nome da pasta = classe).
- Gera uma imagem 640x640 com o ícone centralizado em fundo cinza.
- Gera o `.txt` no formato YOLO (uma caixa por ícone).
- Separa automaticamente parte para **train** e parte para **val** (evita erro de “val vazio”).
- Escreve em `data/yolo_dataset/images/train`, `images/val`, `labels/train`, `labels/val`.

Opções:
- `--icons-dir DIR` – pasta onde estão as subpastas por classe (default: `data/icon_dataset`).
- `--out-dir DIR` – raiz do dataset YOLO (default: `data/yolo_dataset`).
- `--val-ratio 0.1` – 10% das imagens viram validação.

## 4. Treinar

```bash
python scripts/train_yolo.py --epochs 50
```

Depois use o modelo como antes:

```bash
python scripts/run_pipeline.py data/images/diagrama.png --model output/yolo_models/train/weights/best.pt -o output
```

## 5. Dica

Você pode **misturar** os dois tipos de dado:
- Imagens geradas a partir de ícones (script acima).
- Alguns diagramas reais anotados à mão (Make Sense / Roboflow).

Assim o modelo vê tanto ícones isolados quanto diagramas completos e tende a generalizar melhor.
