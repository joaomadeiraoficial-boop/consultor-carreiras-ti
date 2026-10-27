"""Testes de integração de ponta a ponta, sem dependência da interface Streamlit."""
from __future__ import annotations

import json
import unittest

from base_conhecimento import carregar_base
from entrevista_etapa2 import (
    EXPERIENCIAS, IMPACTOS, OBJETIVOS, afinidades_iniciais,
    montar_relatorio,
)
from modulo_roadmap import carregar_roteiros, gerar_roadmap
from motor_ponderado import avaliar_ponderado
from painel_resultados import analisar_proximidade, tabela_ranking
from verificar_entrega import executar_verificacoes


class TestesIntegracaoFinal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = carregar_base()
        cls.roteiros = carregar_roteiros(base=cls.base)

    def test_verificacao_completa(self):
        detalhes = executar_verificacoes()
        self.assertEqual(8, len(detalhes))
        self.assertTrue(all(aprovado for _, aprovado, _ in detalhes), detalhes)

    def test_oito_componentes_integrados_independentes_da_interface(self):
        self.assertIn("trilhas", self.base)
        self.assertIn("dimensoes", self.base)
        self.assertEqual(13, len(self.base["dimensoes"]))
        self.assertEqual(10, len(self.roteiros["trilhas"]))

    def test_resultado_tem_exatamente_dez_trilhas(self):
        resultado = avaliar_ponderado(afinidades_iniciais(self.base), self.base)
        self.assertEqual(10, len(resultado.ranking))
        self.assertEqual(3, len(resultado.top3))
        self.assertEqual(10, len(tabela_ranking(resultado)))

    def test_perfil_ambiguo_e_deterministico(self):
        notas = afinidades_iniciais(self.base)
        p1 = avaliar_ponderado(notas, self.base)
        p2 = avaliar_ponderado(notas, self.base)
        self.assertEqual(p1, p2)
        self.assertTrue(analisar_proximidade(p1).diferenca >= 0)

    def test_perfil_com_diferentes_notas_muda_o_resultado(self):
        um = afinidades_iniciais(self.base)
        outro = {nome: 5 for nome in self.base["dimensoes"]}
        self.assertNotEqual(
            [c.percentual for c in avaliar_ponderado(um, self.base).ranking],
            [c.percentual for c in avaliar_ponderado(outro, self.base).ranking],
        )

    def test_lacunas_de_junior_para_todas_as_trilhas(self):
        for codigo, carreira in self.base["trilhas"].items():
            with self.subTest(carreira=codigo):
                niveis = {c["id"]: 0 for c in carreira["competencias_junior"]}
                plano = gerar_roadmap(codigo, niveis, 6, OBJETIVOS[0], self.base, self.roteiros)
                self.assertEqual(0, plano.preparo_estimado)
                self.assertEqual(len(niveis), len(plano.etapas))
                self.assertGreater(plano.total_semanas, 0)

    def test_sem_lacunas_nao_cria_estudos_artificiais(self):
        codigo = "backend"
        niveis = {c["id"]: 5 for c in self.base["trilhas"][codigo]["competencias_junior"]}
        plano = gerar_roadmap(codigo, niveis, 6, OBJETIVOS[0], self.base, self.roteiros)
        self.assertEqual(100.0, plano.preparo_estimado)
        self.assertEqual(0, plano.total_semanas)
        self.assertEqual(0, len(plano.etapas))

    def test_horas_semanais_alteram_duracao(self):
        codigo = "backend"
        niveis = {c["id"]: 0 for c in self.base["trilhas"][codigo]["competencias_junior"]}
        um = gerar_roadmap(codigo, niveis, 4, OBJETIVOS[0], self.base, self.roteiros)
        dois = gerar_roadmap(codigo, niveis, 20, OBJETIVOS[0], self.base, self.roteiros)
        self.assertGreater(um.total_semanas, dois.total_semanas)

    def test_relatorio_json_tem_roadmap_compatível_com_vencedor(self):
        notas = afinidades_iniciais(self.base)
        resultado = avaliar_ponderado(notas, self.base)
        codigo = resultado.recomendacao
        niveis = {c["id"]: 0 for c in self.base["trilhas"][codigo]["competencias_junior"]}
        plano = gerar_roadmap(codigo, niveis, 6, OBJETIVOS[0], self.base, self.roteiros)
        relatorio = montar_relatorio(
            base=self.base,
            perfil={"experiencia": EXPERIENCIAS[0], "conhecimentos": []},
            afinidades=notas,
            objetivos={"objetivo": OBJETIVOS[0], "impacto": IMPACTOS[-1], "horas_semanais": 6},
            resultado=resultado, plano=plano,
        )
        exportado = json.loads(json.dumps(relatorio, ensure_ascii=False))
        self.assertEqual(codigo, exportado["orientacao_profissional"]["carreira_id"])
        self.assertEqual(10, len(exportado["ranking"]))
        self.assertEqual(3, len(exportado["top3"]))

    def test_entrada_invalida_nao_gera_resultado(self):
        notas = afinidades_iniciais(self.base)
        notas[next(iter(notas))] = 9
        with self.assertRaises(ValueError):
            avaliar_ponderado(notas, self.base)


if __name__ == "__main__":
    unittest.main()
