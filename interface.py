import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from database import BancoDados
from regras import validar_cadastro, proximo_status, data_hora_atual

class SupriDeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SupriDesk | Gestão de Solicitações")
        self.root.geometry("1050x650")
        self.root.minsize(850, 550)
        self.db = BancoDados()
        self._configurar_estilo()
        self._montar_interface()
        self.atualizar_tabela()

    def _configurar_estilo(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Title.TLabel", font=("Arial", 20, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 10))

    def _montar_interface(self):
        principal = ttk.Frame(self.root, padding=18)
        principal.pack(fill="both", expand=True)

        topo = ttk.Frame(principal)
        topo.pack(fill="x", pady=(0, 14))
        ttk.Label(topo, text="SupriDesk", style="Title.TLabel").pack(anchor="w")
        ttk.Label(topo, text="Sistema de gestão de solicitações internas", style="Subtitle.TLabel").pack(anchor="w")

        cadastro = ttk.LabelFrame(principal, text="Nova solicitação", padding=12)
        cadastro.pack(fill="x", pady=(0, 12))

        self.setor_var = tk.StringVar()
        self.material_var = tk.StringVar()
        self.quantidade_var = tk.StringVar()
        self.prioridade_var = tk.StringVar(value="Normal")

        campos = [
            ("Setor", self.setor_var, 20),
            ("Material", self.material_var, 25),
            ("Quantidade", self.quantidade_var, 12),
        ]
        for coluna, (rotulo, variavel, largura) in enumerate(campos):
            ttk.Label(cadastro, text=rotulo).grid(row=0, column=coluna, sticky="w", padx=5, pady=(0, 4))
            ttk.Entry(cadastro, textvariable=variavel, width=largura).grid(row=1, column=coluna, sticky="ew", padx=5)
        ttk.Label(cadastro, text="Prioridade").grid(row=0, column=3, sticky="w", padx=5, pady=(0, 4))
        ttk.Combobox(cadastro, textvariable=self.prioridade_var, values=("Normal", "Alta"),
                     state="readonly", width=13).grid(row=1, column=3, sticky="ew", padx=5)
        ttk.Button(cadastro, text="Cadastrar solicitação", command=self.cadastrar).grid(
            row=1, column=4, padx=8, sticky="ew")
        for i in range(5):
            cadastro.columnconfigure(i, weight=1 if i < 4 else 0)

        filtros = ttk.LabelFrame(principal, text="Pesquisa e filtros", padding=10)
        filtros.pack(fill="x", pady=(0, 12))
        self.busca_var = tk.StringVar()
        self.status_filtro_var = tk.StringVar(value="Todos")
        ttk.Label(filtros, text="Buscar por setor ou material:").pack(side="left", padx=(0, 6))
        busca = ttk.Entry(filtros, textvariable=self.busca_var, width=28)
        busca.pack(side="left", padx=(0, 12))
        busca.bind("<Return>", lambda event: self.atualizar_tabela())
        ttk.Label(filtros, text="Status:").pack(side="left", padx=(0, 6))
        combo = ttk.Combobox(filtros, textvariable=self.status_filtro_var,
                             values=("Todos", "Pendente", "Em atendimento", "Atendida"),
                             state="readonly", width=18)
        combo.pack(side="left", padx=(0, 8))
        combo.bind("<<ComboboxSelected>>", lambda event: self.atualizar_tabela())
        ttk.Button(filtros, text="Pesquisar", command=self.atualizar_tabela).pack(side="left", padx=3)
        ttk.Button(filtros, text="Limpar filtros", command=self.limpar_filtros).pack(side="left", padx=3)

        tabela_frame = ttk.Frame(principal)
        tabela_frame.pack(fill="both", expand=True)
        colunas = ("id", "setor", "material", "quantidade", "prioridade", "status", "data_hora")
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", selectmode="browse")
        titulos = {
            "id": "ID", "setor": "Setor", "material": "Material",
            "quantidade": "Qtd.", "prioridade": "Prioridade",
            "status": "Status", "data_hora": "Data/Hora"
        }
        larguras = {"id": 55, "setor": 130, "material": 180, "quantidade": 65,
                    "prioridade": 90, "status": 140, "data_hora": 155}
        for coluna in colunas:
            self.tabela.heading(coluna, text=titulos[coluna])
            self.tabela.column(coluna, width=larguras[coluna], anchor="center")
        barra = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        acoes = ttk.Frame(principal)
        acoes.pack(fill="x", pady=(12, 0))
        ttk.Button(acoes, text="Iniciar atendimento", command=lambda: self.alterar_status("Em atendimento")).pack(side="left", padx=(0, 8))
        ttk.Button(acoes, text="Marcar como atendida", command=lambda: self.alterar_status("Atendida")).pack(side="left", padx=8)
        ttk.Button(acoes, text="Atualizar tabela", command=self.atualizar_tabela).pack(side="left", padx=8)
        ttk.Button(acoes, text="Exportar histórico CSV", command=self.exportar_csv).pack(side="right")

        self.rodape_var = tk.StringVar(value="Pronto.")
        ttk.Label(principal, textvariable=self.rodape_var).pack(anchor="w", pady=(8, 0))

    def cadastrar(self):
        try:
            setor, material, quantidade, prioridade = validar_cadastro(
                self.setor_var.get(), self.material_var.get(),
                self.quantidade_var.get(), self.prioridade_var.get()
            )
            novo_id = self.db.cadastrar(setor, material, quantidade, prioridade, data_hora_atual())
            self.setor_var.set("")
            self.material_var.set("")
            self.quantidade_var.set("")
            self.prioridade_var.set("Normal")
            self.busca_var.set("")
            self.status_filtro_var.set("Todos")
            self.atualizar_tabela()
            self.rodape_var.set(f"Solicitação #{novo_id} cadastrada com sucesso.")
            messagebox.showinfo("Sucesso", f"Solicitação #{novo_id} cadastrada como Pendente.")
        except ValueError as erro:
            messagebox.showwarning("Dados inválidos", str(erro))
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível cadastrar: {erro}")

    def selecionar_id(self):
        selecionados = self.tabela.selection()
        if not selecionados:
            messagebox.showwarning("Atenção", "Selecione uma solicitação na tabela.")
            return None
        valores = self.tabela.item(selecionados[0], "values")
        return int(valores[0])

    def alterar_status(self, status_solicitado):
        solicitacao_id = self.selecionar_id()
        if solicitacao_id is None:
            return
        status_atual = self.db.obter_status(solicitacao_id)
        try:
            proximo = proximo_status(status_atual)
            if proximo != status_solicitado:
                messagebox.showwarning(
                    "Transição inválida",
                    f"O próximo status permitido é '{proximo}'. Status atual: '{status_atual}'."
                )
                return
            self.db.atualizar_status(solicitacao_id, proximo)
            self.atualizar_tabela()
            self.rodape_var.set(f"Solicitação #{solicitacao_id}: {proximo}.")
        except ValueError as erro:
            messagebox.showwarning("Ação não permitida", str(erro))

    def atualizar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        registros = self.db.listar(self.busca_var.get(), self.status_filtro_var.get())
        for registro in registros:
            self.tabela.insert("", "end", values=registro)
        self.rodape_var.set(f"{len(registros)} solicitação(ões) exibida(s).")

    def limpar_filtros(self):
        self.busca_var.set("")
        self.status_filtro_var.set("Todos")
        self.atualizar_tabela()

    def exportar_csv(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar histórico de solicitações",
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")],
            initialfile="historico_supridesk.csv"
        )
        if not caminho:
            return
        registros = self.db.historico_csv()
        try:
            with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.writer(arquivo, delimiter=";")
                escritor.writerow(["ID", "Setor", "Material", "Quantidade", "Prioridade", "Status", "Data/Hora"])
                escritor.writerows(registros)
            messagebox.showinfo("Exportação concluída", f"Histórico exportado para:\n{caminho}")
        except OSError as erro:
            messagebox.showerror("Erro", f"Não foi possível exportar o CSV: {erro}")
