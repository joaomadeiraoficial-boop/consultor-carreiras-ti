"""Testes do Dia 4: autoavaliação, gaps, roadmap e integração com relatório."""
from __future__ import annotations

import ast
import copy
import json
from pathlib import Path
import tempfile
import unittest

from base_conhecimento import carregar_base
from entrevista_etapa2 import EXPERIENCIAS, OBJETIVOS, IMPACTOS, montar_relatorio, afinidades_iniciais
from modulo_roadmap import carregar_roteiros, gerar_roadmap
from motor_ponderado import avaliar_ponderado

ROOT = Path(__file__).resolve().parents[1]


class TesteRoadmap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = carregar_base()
        cls.roteiros = carregar_roteiros(base=cls.base)

    def competencias(self, carreira):
        return self.base["trilhas"][carreira]["competencias_junior"]

    def notas(self, carreira, nota):
        return {item["id"]: nota for item in self.competencias(carreira)}

    def calcular(self, carreira, notas=None, horas=5):
        return gerar_roadmap(carreira, notas if notas is not None else self.notas(carreira, 0),
                             horas, OBJETIVOS[1], self.base, self.roteiros)

    def test_cobertura_das_dez_trilhas(self):
        self.assertEqual(len(self.roteiros["trilhas"]), 10)
        for trilha in self.base["trilhas"]:
            with self.subTest(trilha=trilha):
                plano = self.calcular(trilha)
                self.assertEqual(len(plano.avaliacoes), 3)
                self.assertEqual(len(plano.etapas), 3)
                self.assertEqual(plano.carreira_id, trilha)
                self.assertTrue(plano.certificacoes_opcionais)

    def test_nivel_zero_gera_lacunas(self):
        plano = self.calcular("backend")
        self.assertEqual(plano.preparo_estimado, 0)
        self.assertEqual([h.lacuna for h in plano.avaliacoes], [3, 3, 3])
        self.assertTrue(plano.total_semanas >= 1)

    def test_nivel_tres_alcanca_meta_autorreferida(self):
        plano = self.calcular("backend", self.notas("backend", 3))
        self.assertEqual(plano.preparo_estimado, 100)
        self.assertEqual(plano.etapas, ())
        self.assertEqual(plano.total_semanas, 0)
        self.assertIn("autoavaliação", plano.aviso)

    def test_nivel_cinco_nao_aumenta_o_indice_alem_de_cem(self):
        plano = self.calcular("qa", self.notas("qa", 5))
        self.assertEqual(plano.preparo_estimado, 100)

    def test_prioriza_maior_lacuna(self):
        habilidades = self.competencias("frontend")
        notas = {habilidades[0]["id"]: 2, habilidades[1]["id"]: 0,
                 habilidades[2]["id"]: 1}
        plano = self.calcular("frontend", notas)
        self.assertEqual(plano.etapas[0].competencia, habilidades[1]["nome"])
        self.assertEqual(plano.etapas[0].inicio_semana, 1)
        self.assertEqual(plano.etapas[1].inicio_semana,
                         plano.etapas[0].fim_semana + 1)

    def test_disponibilidade_altera_prazo_nao_conteudo(self):
        lento = self.calcular("ciencia", horas=2)
        rapido = self.calcular("ciencia", horas=20)
        self.assertGreater(lento.total_semanas, rapido.total_semanas)
        self.assertEqual([e.competencia for e in lento.etapas],
                         [e.competencia for e in rapido.etapas])

    def test_dados_de_roteiro_sao_realmente_externos(self):
        alterado = copy.deepcopy(self.roteiros)
        id_habilidade = self.competencias("backend")[0]["id"]
        alterado["trilhas"]["backend"]["competencias"][id_habilidade]["horas_por_nivel"] = 40
        padrao = self.calcular("backend", horas=5)
        custom = gerar_roadmap("backend", self.notas("backend", 0), 5,
                               OBJETIVOS[1], self.base, alterado)
        self.assertGreater(custom.total_semanas, padrao.total_semanas)

    def test_base_de_roteiro_incompleta_falha(self):
        invalido = copy.deepcopy(self.roteiros)
        del invalido["trilhas"]["qa"]
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "roteiros.json"
            caminho.write_text(json.dumps(invalido), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "dez carreiras"):
                carregar_roteiros(caminho, base=self.base)

    def test_nao_aceita_niveis_incompletos_ou_invalidos(self):
        casos = [
            {}, self.notas("mobile", 6), self.notas("mobile", -1),
            self.notas("mobile", True), self.notas("mobile", 1.0),
        ]
        for valores in casos:
            with self.subTest(valores=valores), self.assertRaises(ValueError):
                self.calcular("mobile", valores)

    def test_nao_aceita_horas_invalidas(self):
        for horas in [0, -1, 41, 3.5, True]:
            with self.subTest(horas=horas), self.assertRaises(ValueError):
                self.calcular("seguranca", horas=horas)

    def test_roadmap_aparece_no_json_de_diagnostico(self):
        afinidades = afinidades_iniciais(self.base)
        resultado = avaliar_ponderado(afinidades, self.base)
        vencedor = resultado.recomendacao
        plano = self.calcular(vencedor)
        perfil = {"experiencia": EXPERIENCIAS[1], "conhecimentos": ["Python"]}
        objetivos = {"objetivo": OBJETIVOS[1], "impacto": IMPACTOS[-1], "horas_semanais": 5}
        relatorio = montar_relatorio(self.base, perfil, afinidades, objetivos, resultado, plano=plano)
        serializado = json.loads(json.dumps(relatorio, ensure_ascii=False))
        self.assertEqual(serializado["orientacao_profissional"]["carreira_id"], vencedor)
        self.assertTrue(serializado["orientacao_profissional"]["etapas"])

    def test_relatorio_anterior_continua_compatível(self):
        afinidades = afinidades_iniciais(self.base)
        resultado = avaliar_ponderado(afinidades, self.base)
        perfil = {"experiencia": EXPERIENCIAS[0], "conhecimentos": []}
        objetivos = {"objetivo": OBJETIVOS[0], "impacto": IMPACTOS[-1], "horas_semanais": 4}
        relatorio = montar_relatorio(self.base, perfil, afinidades, objetivos, resultado)
        self.assertIsNone(relatorio["orientacao_profissional"])
        self.assertEqual(len(relatorio["top3"]), 3)

    def test_interface_integrada_tem_form_e_roadmap(self):
        texto = (ROOT / "app.py").read_text(encoding="utf-8")
        ast.parse(texto)
        self.assertIn("gerar_roadmap", texto)
        self.assertIn("etapa2_autoavaliacoes", texto)
        self.assertIn("form_lacunas_", texto)
        self.assertIn("roadmap", texto.lower())


if __name__ == "__main__":
    unittest.main()
