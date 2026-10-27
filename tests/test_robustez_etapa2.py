"""Dia 5: casos-limite, consistência matemática e apresentação do resultado."""
from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import replace
from math import isfinite
from pathlib import Path
import random
import unittest

from base_conhecimento import carregar_base
from motor_ponderado import avaliar_ponderado
from painel_resultados import (
    analisar_proximidade,
    tabela_composicao_top3,
    tabela_ranking,
    pesos_destaque_top3,
)

RAIZ = Path(__file__).resolve().parents[1]


class TesteRobustezEtapa2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = carregar_base()
        cls.dim = tuple(cls.base["dimensoes"])

    def perfil(self, nota=3, **trocas):
        respostas = dict.fromkeys(self.dim, nota)
        respostas.update(trocas)
        return respostas

    def test_extremo_tudo_um_fica_em_zero_sem_crash(self):
        resultado = avaliar_ponderado(self.perfil(1), self.base)
        self.assertEqual(len(resultado.ranking), 10)
        self.assertTrue(all(x.percentual == 0 for x in resultado.ranking))
        self.assertTrue(analisar_proximidade(resultado).empate)

    def test_extremo_tudo_cinco_respeita_teto_de_cem(self):
        resultado = avaliar_ponderado(self.perfil(5), self.base)
        self.assertTrue(all(x.percentual == 100 for x in resultado.ranking))
        self.assertTrue(analisar_proximidade(resultado).empate)

    def test_perfil_ambiguo_web_e_mobile_tem_top3_estavel(self):
        perfil = self.perfil(3, logica=5, design_ux=5, mobile=5,
                            bancos_dados=5, testes_qualidade=4)
        primeiro = avaliar_ponderado(perfil, self.base)
        segundo = avaliar_ponderado(perfil, self.base)
        self.assertEqual(primeiro, segundo)
        self.assertEqual(len({x.identificador for x in primeiro.top3}), 3)
        self.assertEqual(primeiro.top3, primeiro.ranking[:3])

    def test_rankings_permanecem_ordenados_em_cem_perfis(self):
        rng = random.Random(20261026)
        for indice in range(100):
            with self.subTest(perfil=indice):
                respostas = {codigo: rng.randint(1, 5) for codigo in self.dim}
                resultado = avaliar_ponderado(respostas, self.base)
                self.assertEqual(len(resultado.ranking), 10)
                self.assertEqual(len(set(x.identificador for x in resultado.ranking)), 10)
                self.assertTrue(all(isfinite(x.percentual) and 0 <= x.percentual <= 100
                                    for x in resultado.ranking))
                self.assertEqual([x.percentual for x in resultado.ranking],
                                 sorted([x.percentual for x in resultado.ranking], reverse=True))

    def test_criterio_de_empate_e_deterministico(self):
        perfil = self.perfil(1)
        primeira = avaliar_ponderado(perfil, self.base)
        segunda = avaliar_ponderado(perfil, self.base)
        self.assertEqual([x.identificador for x in primeira.ranking],
                         [x.identificador for x in segunda.ranking])
        self.assertIn("empate", primeira.criterio_desempate.lower())

    def test_aviso_de_empate_exato(self):
        resultado = avaliar_ponderado(self.perfil(1), self.base)
        aviso = analisar_proximidade(resultado)
        self.assertEqual(aviso.diferenca, 0)
        self.assertTrue(aviso.empate)
        self.assertTrue(aviso.muito_proximas)
        self.assertIn("Empate", aviso.mensagem)

    def test_aviso_de_resultado_proximo(self):
        resultado = avaliar_ponderado(self.perfil(3), self.base)
        a, b, *restante = resultado.ranking
        # Dados sintéticos usados APENAS para testar os limiares de apresentação.
        ranking = (replace(a, percentual=70.0), replace(b, percentual=66.5), *restante)
        sintetico = replace(resultado, ranking=ranking, top3=ranking[:3])
        aviso = analisar_proximidade(sintetico)
        self.assertFalse(aviso.empate)
        self.assertTrue(aviso.muito_proximas)
        self.assertEqual(aviso.diferenca, 3.5)

    def test_aviso_de_resultado_distante(self):
        resultado = avaliar_ponderado(self.perfil(3), self.base)
        a, b, *restante = resultado.ranking
        ranking = (replace(a, percentual=80), replace(b, percentual=60), *restante)
        sintetico = replace(resultado, ranking=ranking, top3=ranking[:3])
        aviso = analisar_proximidade(sintetico)
        self.assertFalse(aviso.muito_proximas)
        self.assertEqual(aviso.diferenca, 20)
        self.assertIn("heurística", aviso.mensagem)

    def test_limiar_invalido_nao_e_aceito(self):
        resultado = avaliar_ponderado(self.perfil(3), self.base)
        for ruim in (-1, 101, float("nan"), float("inf"), True, "5", None):
            with self.subTest(limiar=ruim), self.assertRaises(ValueError):
                analisar_proximidade(resultado, ruim)

    def test_tabela_ranking_e_identica_ao_motor(self):
        resultado = avaliar_ponderado(self.perfil(3), self.base)
        linhas = tabela_ranking(resultado)
        self.assertEqual(len(linhas), 10)
        self.assertEqual([x["Posição"] for x in linhas], list(range(1, 11)))
        self.assertEqual([x["Compatibilidade (%)"] for x in linhas],
                         [x.percentual for x in resultado.ranking])

    def test_tabela_composicao_confere_com_calculo(self):
        respostas = self.perfil(2, matematica_estatistica=5,
                               modelagem_preditiva=5, pipelines_dados=1)
        resultado = avaliar_ponderado(respostas, self.base)
        linhas = tabela_composicao_top3(resultado)
        self.assertEqual(len(linhas), 3)
        for linha, trilha in zip(linhas, resultado.top3):
            bruto = (linha["Base (p.p.)"] + linha["Bônus (p.p.)"]
                     + linha["Penalidades (p.p.)"])
            esperado = min(100.0, max(0.0, bruto))
            self.assertAlmostEqual(linha["Resultado (%)"], esperado, delta=0.03)
            self.assertEqual(linha["Penalidades (p.p.)"], -trilha.penalidade)

    def test_pesos_do_painel_vem_do_json(self):
        resultado = avaliar_ponderado(self.perfil(3), self.base)
        linhas = pesos_destaque_top3(resultado, self.base)
        self.assertEqual(len(linhas), 6)
        nomes = [x.nome for x in resultado.top3]
        self.assertEqual(list(linhas[0]), ["Afinidade", *nomes])
        titulo_para_codigo = {info["titulo"]: cod for cod, info in self.base["dimensoes"].items()}
        for linha in linhas:
            codigo = titulo_para_codigo[linha["Afinidade"]]
            for trilha in resultado.top3:
                self.assertEqual(linha[trilha.nome],
                                 self.base["trilhas"][trilha.identificador]["pesos"][codigo])

    def test_alterar_peso_no_json_muda_o_painel(self):
        resultado = avaliar_ponderado(self.perfil(3), self.base)
        original = pesos_destaque_top3(resultado, self.base, len(self.dim))
        alterada = deepcopy(self.base)
        primeira = resultado.top3[0]
        codigo = self.dim[0]
        alterada["trilhas"][primeira.identificador]["pesos"][codigo] += 1
        mudado = pesos_destaque_top3(resultado, alterada, len(self.dim))
        titulo = self.base["dimensoes"][codigo]["titulo"]
        valor_antigo = next(x[primeira.nome] for x in original if x["Afinidade"] == titulo)
        valor_novo = next(x[primeira.nome] for x in mudado if x["Afinidade"] == titulo)
        self.assertEqual(valor_novo, valor_antigo + 1)

    def test_quantidade_de_afinidades_invalida(self):
        resultado = avaliar_ponderado(self.perfil(3), self.base)
        for invalida in (0, -1, 1.5, True, "6"):
            with self.subTest(valor=invalida), self.assertRaises(ValueError):
                pesos_destaque_top3(resultado, self.base, invalida)

    def test_interface_esta_integrada_e_sintaxe_correta(self):
        codigo = (RAIZ / "app.py").read_text(encoding="utf-8")
        ast.parse(codigo)
        for trecho in ("analisar_proximidade", "tabela_ranking", "tabela_composicao_top3",
                       "pesos_destaque_top3", "horizontal=True"):
            self.assertIn(trecho, codigo)
        self.assertIn("gerar_roadmap", codigo)


if __name__ == "__main__":
    unittest.main()
