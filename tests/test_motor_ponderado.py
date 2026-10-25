"""Testes do motor ponderado da Etapa 2 (independentes de Streamlit/Experta)."""
from copy import deepcopy
import unittest

from base_conhecimento import carregar_base
from motor_ponderado import avaliar_ponderado


class TesteMotorPonderado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = carregar_base()
        cls.dimensoes = tuple(cls.base["dimensoes"])

    def perfil(self, valor=1, **substituicoes):
        respostas = dict.fromkeys(self.dimensoes, valor)
        respostas.update(substituicoes)
        return respostas

    def test_retorna_dez_trilhas_e_top3(self):
        resultado = avaliar_ponderado(self.perfil(3))
        self.assertEqual(len(resultado.ranking), 10)
        self.assertEqual(len(resultado.top3), 3)
        self.assertEqual(len(set(item.identificador for item in resultado.ranking)), 10)
        self.assertEqual(resultado.top3, resultado.ranking[:3])
        self.assertTrue(all(0 <= item.percentual <= 100 for item in resultado.ranking))

    def test_extremos_de_afinidade(self):
        baixa = avaliar_ponderado(self.perfil(1))
        alta = avaliar_ponderado(self.perfil(5))
        self.assertTrue(all(item.percentual == 0 for item in baixa.ranking))
        self.assertTrue(all(item.percentual == 100 for item in alta.ranking))

    def test_dez_perfis_sinteticos_reconhecem_as_dez_trilhas(self):
        """Cada carreira deve vencer num perfil focado em seus pesos essenciais."""
        for identificador, trilha in self.base["trilhas"].items():
            with self.subTest(trilha=identificador):
                respostas = {
                    dimensao: (5 if peso >= 4 else 3 if peso >= 3 else 1)
                    for dimensao, peso in trilha["pesos"].items()
                }
                self.assertEqual(avaliar_ponderado(respostas).recomendacao, identificador)

    def test_diferencia_ciencia_de_engenharia(self):
        ciencia = self.perfil(2, logica=4, matematica_estatistica=5,
                              modelagem_preditiva=5, pipelines_dados=1, bancos_dados=3)
        engenharia = self.perfil(2, logica=4, pipelines_dados=5,
                                  bancos_dados=5, automacao=4, modelagem_preditiva=1)
        self.assertEqual(avaliar_ponderado(ciencia).recomendacao, "ciencia")
        self.assertEqual(avaliar_ponderado(engenharia).recomendacao, "engenharia")

    def test_diferencia_devops_de_cloud(self):
        devops = self.perfil(2, logica=4, automacao=5, nuvem=4,
                             testes_qualidade=5, bancos_dados=2)
        cloud = self.perfil(2, nuvem=5, automacao=2, logica=3,
                           seguranca=3, comunicacao=3)
        self.assertEqual(avaliar_ponderado(devops).recomendacao, "devops")
        self.assertEqual(avaliar_ponderado(cloud).recomendacao, "cloud")

    def test_criterio_essencial_baixo_provoca_penalidade(self):
        perfil = self.perfil(3, matematica_estatistica=1)
        item = next(x for x in avaliar_ponderado(perfil).ranking if x.identificador == "ciencia")
        self.assertGreater(item.penalidade, 0)
        self.assertTrue(any(e.tipo == "penalidade" for e in item.evidencias))

    def test_regras_de_contraste_ativadas_e_explicadas(self):
        perfil = self.perfil(2, matematica_estatistica=5, modelagem_preditiva=5, pipelines_dados=1)
        item = next(x for x in avaliar_ponderado(perfil).ranking if x.identificador == "ciencia")
        self.assertGreater(item.bonus, 0)
        self.assertTrue(any(e.codigo == "A01" for e in item.evidencias))

    def test_regra_externa_controla_resultados(self):
        perfil = self.perfil(2, matematica_estatistica=5, modelagem_preditiva=5, pipelines_dados=1)
        normal = avaliar_ponderado(perfil, self.base)
        alterada = deepcopy(self.base)
        alterada["regras_ajuste"][0]["pontos"] = 0
        mudado = avaliar_ponderado(perfil, alterada)
        normal_ciencia = next(x for x in normal.ranking if x.identificador == "ciencia")
        mudado_ciencia = next(x for x in mudado.ranking if x.identificador == "ciencia")
        self.assertEqual(round(normal_ciencia.percentual - mudado_ciencia.percentual, 2), 5)

    def test_rejeita_valores_invalidos(self):
        for invalido in (0, 6, 3.5, "3", True, None):
            with self.subTest(invalido=invalido):
                entrada = self.perfil(3, logica=invalido)
                with self.assertRaises(ValueError):
                    avaliar_ponderado(entrada)
        with self.assertRaises(ValueError):
            avaliar_ponderado({"logica": 3})
        with self.assertRaises(ValueError):
            avaliar_ponderado(self.perfil(3, campo_inexistente=5))

    def test_deterministico_com_perfil_ambiguo(self):
        perfil = self.perfil(3, logica=5, design_ux=5, mobile=5,
                             bancos_dados=5, testes_qualidade=4)
        a = avaliar_ponderado(perfil)
        b = avaliar_ponderado(perfil)
        self.assertEqual(a, b)
        self.assertEqual(len(a.top3), 3)
        self.assertEqual(sorted([x.percentual for x in a.ranking], reverse=True),
                         [x.percentual for x in a.ranking])


if __name__ == "__main__":
    unittest.main()
