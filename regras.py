from datetime import datetime

TRANSICOES = {
    "Pendente": "Em atendimento",
    "Em atendimento": "Atendida"
}

def validar_cadastro(setor, material, quantidade, prioridade):
    if not setor.strip():
        raise ValueError("Informe o setor.")
    if not material.strip():
        raise ValueError("Informe o material.")
    try:
        qtd = int(quantidade)
    except (TypeError, ValueError):
        raise ValueError("A quantidade deve ser um número inteiro.")
    if qtd <= 0:
        raise ValueError("A quantidade deve ser um inteiro positivo.")
    if prioridade not in ("Normal", "Alta"):
        raise ValueError("Selecione uma prioridade válida.")
    return setor.strip(), material.strip(), qtd, prioridade

def proximo_status(status_atual):
    if status_atual not in TRANSICOES:
        raise ValueError("Esta solicitação já foi atendida ou possui status inválido.")
    return TRANSICOES[status_atual]

def data_hora_atual():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
