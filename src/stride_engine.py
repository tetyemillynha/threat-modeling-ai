from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Literal

Stride = Literal["S", "T", "R", "I", "D", "E"]

STRIDE_LABELS: Dict[Stride, str] = {
    "S": "Spoofing (Falsificação de identidade)",
    "T": "Tampering (Adulteração)",
    "R": "Repudiation (Repúdio)",
    "I": "Information Disclosure (Exposição de informação)",
    "D": "Denial of Service (Negação de serviço)",
    "E": "Elevation of Privilege (Elevação de privilégio)",
}

@dataclass
class ThreatItem:
    stride: Stride
    title: str
    description: str
    mitigations: List[str]

KB: Dict[str, List[ThreatItem]] = {
    "user": [
        ThreatItem("S", "Uso de credenciais comprometidas",
                   "Atacante usa credenciais roubadas para acessar o sistema.",
                   ["MFA/2FA", "Política de senhas fortes", "Detecção de login anômalo"]),
        ThreatItem("R", "Ações sem rastreabilidade",
                   "Usuário nega ações por falta de trilha de auditoria.",
                   ["Logs de auditoria", "Carimbo de data/hora", "Correlação de eventos por usuário"]),
        ThreatItem("I", "Exposição via engenharia social",
                   "Vazamento de dados por phishing ou compartilhamento indevido.",
                   ["Treinamento", "DLP onde aplicável", "Princípio do menor privilégio"]),
    ],
    
}

