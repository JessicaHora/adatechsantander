import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

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
        records = []
        for record in self.data["registros"]:
            if filter_by and record.get(filter_by) != filter_value:
                continue
            records.append(record)
        return records

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
            return False
        else:
            self.save_data()
            return True

    def delete_record(self, record_id):
        original_len = len(self.data["registros"])
        self.data["registros"] = [record for record in self.data["registros"] if record["id"] != record_id]
        if len(self.data["registros"]) == original_len:
            return False
        else:
            self.save_data()
            return True

class FinansmartApp:
    def __init__(self, master):
        self.finansmart = Finansmart()
        self.master = master
        master.title("Finansmart - Sistema de Gerenciamento Financeiro")

        tk.Button(master, text="Adicionar Registro", command=self.add_record).pack()
        tk.Button(master, text="Ler Registros", command=self.read_records).pack()
        tk.Button(master, text="Atualizar Registro", command=self.update_record).pack()
        tk.Button(master, text="Deletar Registro", command=self.delete_record).pack()
        tk.Button(master, text="Sair", command=master.quit).pack()

    def add_record(self):
        tipo = simpledialog.askstring("Input", "Digite o tipo (receita/despesa/investimento):", parent=self.master)
        valor = simpledialog.askfloat("Input", "Digite o valor:", parent=self.master)
        if tipo == "investimento":
            juros = simpledialog.askfloat("Input", "Digite a taxa de juros (como decimal):", parent=self.master)
            self.finansmart.add_record(tipo, valor, juros)
        else:
            self.finansmart.add_record(tipo, valor)
        messagebox.showinfo("Info", "Registro adicionado com sucesso!")

    def read_records(self):
        records = self.finansmart.read_records()
        records_str = '\n'.join([str(record) for record in records])
        messagebox.showinfo("Registros", records_str)

    def update_record(self):
        id_registro = simpledialog.askinteger("Input", "Digite o ID do registro a ser atualizado:", parent=self.master)
        novo_valor = simpledialog.askfloat("Input", "Digite o novo valor:", parent=self.master)
        novo_tipo = simpledialog.askstring("Input", "Digite o novo tipo (receita/despesa/investimento):", parent=self.master)
        success = self.finansmart.update_record(id_registro, novo_valor, novo_tipo)
        if success:
            messagebox.showinfo("Info", "Registro atualizado com sucesso!")
        else:
            messagebox.showwarning("Warning", "Registro com ID não encontrado.")

    def delete_record(self):
        id_registro = simpledialog.askinteger("Input", "Digite o ID do registro a ser deletado:", parent=self.master)
        success = self.finansmart.delete_record(id_registro)
        if success:
            messagebox.showinfo("Info", "Registro deletado com sucesso!")
        else:
            messagebox.showwarning("Warning", "Registro com ID não encontrado.")

def main():
    root = tk.Tk()
    app = FinansmartApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
