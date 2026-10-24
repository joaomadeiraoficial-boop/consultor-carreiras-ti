"""Testes da modelagem JSON da Etapa 2, Dia 1 (sem depender de Experta)."""
import unittest

from base_conhecimento import carregar_base, carregar_trilhas
from conhecimento import ORDEM, TRILHAS


class TesteBaseConhecimento(unittest.TestCase):
    def test_dez_trilhas(self):
        base = carregar_base()
        self.assertEqual(len(base["trilhas"]), 10)
        self.assertEqual(set(TRILHAS), set(base["trilhas"]))

    def test_todas_as_dimensoes_tem_peso(self):
        base = carregar_base()
        campos = set(base["dimensoes"])
        self.assertGreaterEqual(len(campos), 10)
        for trilha in base["trilhas"].values():
            self.assertEqual(set(trilha["pesos"]), campos)
            self.assertGreater(sum(trilha["pesos"].values()), 0)

    def test_interface_anterior_preservada(self):
        self.assertEqual(tuple(carregar_trilhas()), ORDEM)
        self.assertEqual(carregar_trilhas(), TRILHAS)
        for dados in TRILHAS.values():
            self.assertTrue(dados["nome"])
            self.assertTrue(dados["resumo"])
            self.assertTrue(dados["exemplo"])
            self.assertTrue(dados["aprender"])

    def test_lacunas_junior_modeladas(self):
        base = carregar_base()
        for trilha in base["trilhas"].values():
            self.assertGreaterEqual(len(trilha["competencias_junior"]), 3)
            for competencia in trilha["competencias_junior"]:
                self.assertIn("nivel_requerido", competencia)
                self.assertIn("nome", competencia)


if __name__ == "__main__":
    unittest.main()
