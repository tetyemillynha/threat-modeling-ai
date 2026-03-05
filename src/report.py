from __future__ import annotations
from typing import Dict, Any, List
from datetime import datetime

def _fmt_bbox(bbox: Dict[str, float] | None) -> str:
    if not bbox:
        return "-"
    return f"x={bbox['x']:.0f}, y={bbox['y']:.0f}, w={bbox['w']:.0f}, h={bbox['h']:.0f}"

def to_markdown(image_path: str, detections: List[dict], stride_data: Dict[str, Any]) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(f"# Relatório de Modelagem de Ameaças (STRIDE)\n")
    lines.append(f"**Imagem analisada:** `{image_path}`  \n")
    lines.append(f"**Gerado em:** {now}\n")

    lines.append("## 1) Resumo\n")
    lines.append(f"- Componentes detectados: **{stride_data['summary']['total_components']}**\n")
    lines.append("- Contagem por classe:\n")
    for k, v in sorted(stride_data["summary"]["by_class"].items()):
        lines.append(f"  - `{k}`: **{v}**\n")

    lines.append("\n## 2) Componentes Detectados\n")
    lines.append("| # | Classe | Confiança | Bounding Box |\n")
    lines.append("|---|--------|-----------|--------------|\n")
    for i, d in enumerate(detections, start=1):
        lines.append(f"| {i} | `{d['class']}` | {d['confidence']:.2f} | {_fmt_bbox(d.get('bbox'))} |\n")

    lines.append("\n## 3) Ameaças por Componente (STRIDE)\n")
    for i, comp in enumerate(stride_data["components"], start=1):
        lines.append(f"\n### 3.{i} `{comp['class']}` (conf: {comp['confidence']:.2f})\n")
        if not comp["stride"]:
            lines.append("- *(Sem regras STRIDE cadastradas para esta classe no MVP.)*\n")
            continue

        for t in comp["stride"]:
            lines.append(f"\n**{t['code']} — {t['label']}**\n")
            lines.append(f"- **Ameaça:** {t['title']}\n")
            lines.append(f"- **Descrição:** {t['description']}\n")
            lines.append(f"- **Contramedidas:**\n")
            for m in t["mitigations"]:
                lines.append(f"  - {m}\n")

    lines.append("\n## 4) Limitações do MVP\n")
    lines.append("- O detector reconhece um conjunto limitado de classes (multi-cloud genéricas).\n")
    lines.append("- O mapeamento STRIDE é baseado em regras (base de conhecimento estática).\n")
    lines.append("- Não inferimos fluxos/DFDs; apenas analisamos componentes detectados.\n")

    lines.append("\n## 5) Próximos Passos\n")
    lines.append("- Aumentar o dataset e refinar classes (ex.: queue, secrets manager, CI/CD).\n")
    lines.append("- Detectar relações/fluxos (setas) para gerar DFD e melhorar STRIDE por fronteira de confiança.\n")
    lines.append("- Integrar busca de vulnerabilidades (CWE/CVE) por tipo de componente.\n")

    return "".join(lines)