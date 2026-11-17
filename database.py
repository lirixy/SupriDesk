import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("solicitacoes.db")

class BancoDados:
    def __init__(self, caminho=DB_PATH):
        self.caminho = str(caminho)
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.caminho)

    def criar_tabela(self):
        with self.conectar() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS solicitacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setor TEXT NOT NULL,
                    material TEXT NOT NULL,
                    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                    prioridade TEXT NOT NULL CHECK (prioridade IN ('Normal', 'Alta')),
                    status TEXT NOT NULL DEFAULT 'Pendente',
                    data_hora TEXT NOT NULL
                )
            """)

    def cadastrar(self, setor, material, quantidade, prioridade, data_hora):
        with self.conectar() as conn:
            cursor = conn.execute(
                """INSERT INTO solicitacoes
                   (setor, material, quantidade, prioridade, status, data_hora)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (setor, material, quantidade, prioridade, "Pendente", data_hora)
            )
            return cursor.lastrowid

    def listar(self, busca="", status="Todos"):
        sql = "SELECT id, setor, material, quantidade, prioridade, status, data_hora FROM solicitacoes WHERE 1=1"
        parametros = []
        if busca.strip():
            termo = f"%{busca.strip()}%"
            sql += " AND (setor LIKE ? OR material LIKE ?)"
            parametros.extend([termo, termo])
        if status != "Todos":
            sql += " AND status = ?"
            parametros.append(status)
        sql += " ORDER BY id DESC"
        with self.conectar() as conn:
            return conn.execute(sql, parametros).fetchall()

    def obter_status(self, solicitacao_id):
        with self.conectar() as conn:
            resultado = conn.execute(
                "SELECT status FROM solicitacoes WHERE id = ?", (solicitacao_id,)
            ).fetchone()
            return resultado[0] if resultado else None

    def atualizar_status(self, solicitacao_id, novo_status):
        with self.conectar() as conn:
            cursor = conn.execute(
                "UPDATE solicitacoes SET status = ? WHERE id = ?",
                (novo_status, solicitacao_id)
            )
            return cursor.rowcount > 0

    def historico_csv(self):
        with self.conectar() as conn:
            return conn.execute("""
                SELECT id, setor, material, quantidade, prioridade, status, data_hora
                FROM solicitacoes ORDER BY id
            """).fetchall()
