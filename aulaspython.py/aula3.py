import json
from datetime import datetime

class Finansmart:
    def __init__(self):
        self.data_file = 'finansmart_data.json'
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"registros": []}

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_record(self, record_type, value, interest_rate=None):
        record = {
            "id": len(self.data["registros"]) + 1,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": record_type,
            "value": -value if record_type == "despesa" else value,
            "interest_rate": interest_rate,
            "original_value": value if record_type == "investimento" else None
        }
        self.data["registros"].append(record)
        self.save_data()

    def read_records(self, filter_by=None, filter_value=None):
        for record in self.data["registros"]:
            if filter_by and record.get(filter_by) != filter_value:
                continue
            print(record)

    def update_record(self, record_id, new_value, new_type):
        found = False
        for record in self.data["registros"]:
            if record["id"] == record_id:
                record["value"] = -new_value if new_type == "despesa" else new_value
                record["type"] = new_type
                record["date"] = datetime.now().strftime("%Y-%m-%d")
                found = True
                break
        if not found:
            print(f"Registro com ID {record_id} não encontrado.")
        else:
            self.save_data()

    def delete_record(self, record_id):
        original_len = len(self.data["registros"])
        self.data["registros"] = [record for record in self.data["registros"] if record["id"] != record_id]
        if len(self.data["registros"]) == original_len:
            print(f"Registro com ID {record_id} não encontrado.")
        else:
            self.save_data()

def main():
    finansmart = Finansmart()

    while True:
        print("\nFinansmart - Sistema de Gerenciamento Financeiro")
        print("1. Adicionar Registro")
        print("2. Ler Registros")
        print("3. Atualizar Registro")
        print("4. Deletar Registro")
        print("5. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            tipo = input("Digite o tipo (receita/despesa/investimento): ")
            valor = float(input("Digite o valor: "))
            if tipo == "investimento":
                juros = float(input("Digite a taxa de juros (como decimal): "))
                finansmart.add_record(tipo, valor, juros)
            else:
                finansmart.add_record(tipo, valor)

        elif escolha == '2':
            finansmart.read_records()

        elif escolha == '3':
            id_registro = int(input("Digite o ID do registro a ser atualizado: "))
            novo_valor = float(input("Digite o novo valor: "))
            novo_tipo = input("Digite o novo tipo (receita/despesa/investimento): ")
            finansmart.update_record(id_registro, novo_valor, novo_tipo)

        elif escolha == '4':
            id_registro = int(input("Digite o ID do registro a ser deletado: "))
            finansmart.delete_record(id_registro)

        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
