## Estrutura sugerida do repositório (organizada e explicável)

threat-modeling-ai/
  README.md
  requirements.txt

  data/
    raw/                 # imagens coletadas
    labeled/             # dataset YOLO (images + labels)
    architectures.yaml   # config do YOLO

  src/
    detect.py            # roda YOLO e retorna componentes
    stride_engine.py     # regras STRIDE + mitigations
    report.py            # gera Markdown/HTML
    utils.py

  inputs/
    arch1.png
    arch2.png

  outputs/
    (gerado)
  
  main.py

## Classes do dataset

user
identity_auth (AWS IAM / Azure Entra)
api_gateway (Amazon API Gateway / Azure API Management)
waf_firewall (AWS WAF / Azure WAF/Firewall)
cdn (CloudFront / Azure Front Door)
load_balancer (ALB / Azure Load Balancer)
app_service (EC2/ECS/EKS/ASG / App Service/VM/AKS)
database (RDS/Aurora / Azure SQL)
cache (ElastiCache / Azure Cache for Redis)
storage (S3/EFS / Blob/File Storage)