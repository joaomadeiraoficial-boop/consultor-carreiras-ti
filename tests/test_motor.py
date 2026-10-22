"""Testes unitários do motor (10 carreiras + validação + determinismo)."""
import json
import unittest
from pathlib import Path

from conhecimento import ORDEM
from motor import avaliar


PERSONAS = json.loads((Path(__file__).resolve().parents[1] / "personas.json").read_text(encoding="utf-8"))


class TesteMotor(unittest.TestCase):
    def test_dez_personas(self):
        self.assertEqual(len(PERSONAS), 10)
        for persona in PERSONAS:
            with self.subTest(persona=persona["nome"]):
                resultado = avaliar(persona["respostas"])
                self.assertEqual(resultado.recomendacao, persona["esperada"])
                self.assertGreater(resultado.ranking[0][1], 0)
                self.assertTrue(resultado.evidencias[resultado.recomendacao])

    def test_rankings_completos(self):
        resultado = avaliar(PERSONAS[0]["respostas"])
        self.assertEqual({chave for chave, _ in resultado.ranking}, set(ORDEM))
        self.assertEqual(len(resultado.ranking), 10)
        self.assertEqual(sum(item.pontos for item in resultado.evidencias["backend"]),
                         dict(resultado.ranking)["backend"])

    def test_sem_estado_entre_entrevistas(self):
        primeiro = avaliar(PERSONAS[0]["respostas"])
        avaliar(PERSONAS[1]["respostas"])
        repeticao = avaliar(PERSONAS[0]["respostas"])
        self.assertEqual(primeiro.ranking, repeticao.ranking)
        self.assertEqual(primeiro.evidencias, repeticao.evidencias)

    def test_resposta_invalida(self):
        entrada = PERSONAS[0]["respostas"].copy()
        entrada["matematica"] = "altissima"
        with self.assertRaisesRegex(ValueError, "matematica"):
            avaliar(entrada)

    def test_campo_ausente(self):
        entrada = PERSONAS[0]["respostas"].copy()
        del entrada["estilo"]
        with self.assertRaises(ValueError):
            avaliar(entrada)


if __name__ == "__main__":
    unittest.main()
