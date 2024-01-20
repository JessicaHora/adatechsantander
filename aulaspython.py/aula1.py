import json
from datetime import datetime

# Nome do arquivo onde os dados serão salvos
DATA_FILE = 'finansmart_data.json'

# Carregar dados existentes ou criar nova estrutura de dados
def carregar_dados():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"registros": []}

# Salvar dados no arquivo
def salvar_dados(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Adicionar um novo registro
def adicionar_registro(tipo, valor, juros=None):
    data = carregar_dados()
    registro = {
        "id": len(data["registros"]) + 1,
        "data": datetime.now().strftime("%d/%m/%Y"),
        "tipo": tipo,
        "valor": -valor if tipo == "despesa" else valor,
        "juros": juros if tipo == "investimento" else None
    }
    data["registros"].append(registro)
    salvar_dados(data)

# Ler registros com filtro opcional
def ler_registros(filtro=None):
    data = carregar_dados()
    registros_filtrados = data["registros"]
    if filtro:
        registros_filtrados = [reg for reg in registros_filtrados if reg.get(filtro[0]) == filtro[1]]
    for reg in registros_filtrados:
        print(reg)

# Atualizar um registro existente
def atualizar_registro(id_registro, novo_valor, novo_tipo):
    data = carregar_dados()
    for reg in data["registros"]:
        if reg["id"] == id_registro:
            reg["valor"] = -novo_valor if novo_tipo == "despesa" else novo_valor
            reg["tipo"] = novo_tipo
            reg["data"] = datetime.now().strftime("%d/%m/%Y")
            break
    salvar_dados(data)

# Deletar um registro
def deletar_registro(id_registro):
    data = carregar_dados()
    data["registros"] = [reg for reg in data["registros"] if reg["id"] != id_registro]
    salvar_dados(data)

# Atualizar rendimentos de investimentos
def atualizar_rendimentos():
    data = carregar_dados()
    for reg in data["registros"]:
        if reg["tipo"] == "investimento":
            dias = (datetime.now() - datetime.strptime(reg["data"], "%d/%m/%Y")).days
            reg["valor"] = reg["valor"] * ((1 + reg["juros"]) ** dias)
    salvar_dados(data)

# Exportar relatório para um arquivo CSV ou JSON
def exportar_relatorio(tipo="json"):
    data = carregar_dados()
    if tipo == "json":
        with open('finansmart_relatorio.json', 'w') as file:
            json.dump(data, file, indent=4)
    elif tipo == "csv":
        import csv
        with open('finansmart_relatorio.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Data", "Tipo", "Valor", "Juros"])
            for reg in data["registros"]:
                writer.writerow([reg["id"], reg["data"], reg["tipo"], reg["valor"], reg.get("juros", "")])

# Função de agrupamento (exemplo: total por tipo)
def calcular_agrupamento(tipo_agrupamento):
    data = carregar_dados()
    agrupamento = {}
    for reg in data["registros"]:
        chave = reg[tipo_agrupamento]
        agrupamento[chave] = agrupamento.get(chave, 0) + reg["valor"]
    for chave, valor in agrupamento.items():
        print(f"{chave}: {valor}")

# Exemplo de uso
if __name__ == "__main__":
    # Adicionando registros
    adicionar_registro("receita", 1000)
    adicionar_registro("despesa", 500)
    adicionar_registro("investimento", 300, juros=0.05)

    # Lendo registros
    ler_registros()

    # Atualizando um registro
    atualizar_registro(1, 1500, "receita")

  # ... (continuação do código anterior)

# Deletar um registro
def deletar_registro(id_registro):
    data = carregar_dados()
    data["registros"] = [reg for reg in data["registros"] if reg["id"] != id_registro]
    salvar_dados(data)

# Atualizar rendimentos de investimentos
def atualizar_rendimentos():
    data = carregar_dados()
    for reg in data["registros"]:
        if reg["tipo"] == "investimento":
            dias = (datetime.now() - datetime.strptime(reg["data"], "%d/%m/%Y")).days
            reg["valor"] = reg["valor"] * ((1 + reg["juros"]) ** dias)
    salvar_dados(data)


# Exemplo de uso
if __name__ == "__main__":
    # Adicionando registros
    adicionar_registro("receita", 1000)
    adicionar_registro("despesa", 500)
    adicionar_registro("investimento", 300, juros=0.05)

    # Lendo registros
    ler_registros()

    # Atualizando um registro
    atualizar_registro(1, 1500, "receita")

    # Deletando um registro
    deletar_registro(2)

    # Atualizando rendimentos
    atualizar_rendimentos()

    # Lendo registros atualizados
    ler_registros()

    # Exportando relatório
    exportar_relatorio("json")
    exportar_relatorio("csv")

    # Calculando agrupamento
    calcular_agrupamento("tipo")
 