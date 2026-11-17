import tempfile
import unittest
from pathlib import Path
from database import BancoDados
from regras import validar_cadastro, proximo_status

class TestesSupriDesk(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = BancoDados(Path(self.temp.name) / "teste.db")

    def tearDown(self):
        self.temp.cleanup()

    def test_cadastro_e_status_inicial(self):
        setor, material, qtd, prioridade = validar_cadastro("TI", "Mouse USB", "5", "Alta")
        item_id = self.db.cadastrar(setor, material, qtd, prioridade, "17/11/2026 09:00:00")
        self.assertEqual(self.db.obter_status(item_id), "Pendente")

    def test_quantidade_zero_recusada(self):
        with self.assertRaises(ValueError):
            validar_cadastro("Administrativo", "Papel A4", "0", "Normal")

    def test_fluxo_de_atendimento(self):
        self.assertEqual(proximo_status("Pendente"), "Em atendimento")
        self.assertEqual(proximo_status("Em atendimento"), "Atendida")
        with self.assertRaises(ValueError):
            proximo_status("Atendida")

if __name__ == "__main__":
    unittest.main()
