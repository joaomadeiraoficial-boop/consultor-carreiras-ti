"""Testes do Dia 3: validação de formulário, integração e relatório JSON.

A lógica de apresentação é testada sem depender do navegador/Streamlit.
Um teste estático verifica os pontos de integração no app.py.
"""
import ast
import json
from pathlib import Path
import unittest

from base_conhecimento import carregar_base
from entrevista_etapa2 import (
    CONHECIMENTOS, ETAPAS, EXPERIENCIAS, IMPACTOS, OBJETIVOS,
    afinidades_iniciais, montar_relatorio, validar_afinidades, validar_contexto,
)
from motor_ponderado import avaliar_ponderado


ROOT = Path(__file__).resolve().parents[1]


class TesteEntrevistaEtapa2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = carregar_base()
        cls.perfil = {
            "experiencia": EXPERIENCIAS[1],
            "conhecimentos": ["Python", "Bancos de dados"],
        }
        cls.objetivos = {
            "objetivo": OBJETIVOS[1],
            "impacto": IMPACTOS[1],
            "horas_semanais": 8,
        }

    def test_tres_etapas_e_treze_perguntas(self):
        self.assertEqual(len(ETAPAS), 3)
        self.assertEqual(len(self.base["dimensoes"]), 13)
        self.assertEqual(len(self.base["trilhas"]), 10)
        self.assertTrue(all(d["pergunta"] for d in self.base["dimensoes"].values()))

    def test_todas_as_afinidades_comecam_em_tres(self):
        respostas = afinidades_iniciais(self.base)
        self.assertEqual(set(respostas), set(self.base["dimensoes"]))
        self.assertEqual(set(respostas.values()), {3})

    def test_respostas_validas_mantem_ordem_do_json(self):
        respostas = afinidades_iniciais(self.base)
        respostas["logica"] = 5
        copia = dict(reversed(list(respostas.items())))
        validas = validar_afinidades(copia, self.base)
        self.assertEqual(validas["logica"], 5)
        self.assertEqual(list(validas), list(self.base["dimensoes"]))

    def test_rejeita_notas_invalidas(self):
        for valor in [0, 6, "3", 3.4, True, None]:
            with self.subTest(valor=valor):
                respostas = afinidades_iniciais(self.base)
                respostas["logica"] = valor
                with self.assertRaises(ValueError):
                    validar_afinidades(respostas, self.base)

    def test_rejeita_campos_faltantes_e_extras(self):
        respostas = afinidades_iniciais(self.base)
        respostas.pop("logica")
        with self.assertRaises(ValueError):
            validar_afinidades(respostas, self.base)
        respostas["logica"] = 3
        respostas["inexistente"] = 3
        with self.assertRaises(ValueError):
            validar_afinidades(respostas, self.base)

    def test_contexto_aceita_iniciante_sem_conhecimentos(self):
        validar_contexto(
            {"experiencia": EXPERIENCIAS[0], "conhecimentos": []},
            {"objetivo": OBJETIVOS[0], "impacto": IMPACTOS[-1], "horas_semanais": 1},
        )

    def test_contexto_rejeita_dados_invalidos(self):
        casos = [
            ({"experiencia": "desconhecida", "conhecimentos": []}, self.objetivos),
            ({"experiencia": EXPERIENCIAS[0], "conhecimentos": ["tecnologia-inventada"]}, self.objetivos),
            (self.perfil, {**self.objetivos, "horas_semanais": 0}),
            (self.perfil, {**self.objetivos, "horas_semanais": True}),
            (self.perfil, {**self.objetivos, "objetivo": "desconhecido"}),
            (self.perfil, {**self.objetivos, "impacto": "desconhecido"}),
        ]
        for perfil, objetivos in casos:
            with self.subTest(perfil=perfil, objetivos=objetivos):
                with self.assertRaises(ValueError):
                    validar_contexto(perfil, objetivos)

    def test_integracao_motor_top3_por_afinidades(self):
        respostas = afinidades_iniciais(self.base)
        respostas.update({
            "matematica_estatistica": 5,
            "modelagem_preditiva": 5,
            "pipelines_dados": 1,
            "logica": 4,
        })
        resultado = avaliar_ponderado(validar_afinidades(respostas, self.base), self.base)
        self.assertEqual(resultado.recomendacao, "ciencia")
        self.assertEqual(len(resultado.top3), 3)
        self.assertTrue(all(0 <= t.percentual <= 100 for t in resultado.top3))

    def test_relatorio_serializavel_com_evidencias_e_contexto(self):
        respostas = afinidades_iniciais(self.base)
        resultado = avaliar_ponderado(respostas, self.base)
        relatorio = montar_relatorio(self.base, self.perfil, respostas, self.objetivos, resultado)
        codificado = json.dumps(relatorio, ensure_ascii=False)
        restaurado = json.loads(codificado)
        self.assertEqual(len(restaurado["afinidades"]), 13)
        self.assertEqual(len(restaurado["top3"]), 3)
        self.assertEqual(len(restaurado["ranking"]), 10)
        self.assertEqual(restaurado["perfil"]["conhecimentos"], ["Python", "Bancos de dados"])
        self.assertEqual(restaurado["objetivos"]["horas_semanais"], 8)
        self.assertIn("evidencias", restaurado["top3"][0])
        self.assertIn("não são probabilidade", restaurado["aviso"])

    def test_app_contém_elementos_da_entrevista_streamlit(self):
        # Teste estrutural: execução real da interface ainda requer Streamlit e navegador.
        arvore = ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
        chamadas = {
            no.func.attr for no in ast.walk(arvore)
            if isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute)
        }
        for metodo in ("form", "slider", "selectbox", "multiselect", "bar_chart", "dataframe", "download_button", "rerun"):
            with self.subTest(metodo=metodo):
                self.assertIn(metodo, chamadas)
        self.assertIn("avaliar_ponderado", (ROOT / "app.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
