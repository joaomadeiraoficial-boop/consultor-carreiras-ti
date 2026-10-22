"""Motor baseado em regras SE-ENTÃO, com encadeamento para frente (Experta)."""
from __future__ import annotations

# Experta 1.9.4 depende de frozendict 1.2, que usa collections.Mapping.
# Compatibilidade para Python >= 3.10 (sem alterar arquivos do pacote instalado).
import collections
import collections.abc
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping

from dataclasses import dataclass
from experta import Fact, KnowledgeEngine, Rule, P
from conhecimento import ORDEM, TRILHAS, VALIDOS


class Perfil(Fact):
    """Fatos fornecidos na entrevista."""


@dataclass(frozen=True)
class RegraDisparada:
    codigo: str
    pontos: int
    motivo: str


@dataclass
class Resultado:
    recomendacao: str
    ranking: list[tuple[str, int]]
    evidencias: dict[str, list[RegraDisparada]]
    criterio_desempate: str


class ConsultorCarreiras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.pontos = {carreira: 0 for carreira in ORDEM}
        self.evidencias = {carreira: [] for carreira in ORDEM}

    def registrar(self, carreira: str, codigo: str, pontos: int, motivo: str):
        self.pontos[carreira] += pontos
        self.evidencias[carreira].append(RegraDisparada(codigo, pontos, motivo))

    @Rule(Perfil(atividade='backend'))
    def regra_01(self):
        self.registrar('backend', 'R01', 3, 'Você prefere tarefas cotidianas ligadas a Desenvolvimento Back-end.')

    @Rule(Perfil(atividade='backend', entrega='funcionalidades'))
    def regra_02(self):
        self.registrar('backend', 'R02', 8, 'Sua atividade favorita combina com o resultado típico de Desenvolvimento Back-end.')

    @Rule(Perfil(atividade='backend', ferramenta=P(lambda valor: valor in ('python', 'sql'))))
    def regra_03(self):
        self.registrar('backend', 'R03', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Desenvolvimento Back-end.')

    @Rule(Perfil(entrega='funcionalidades', estilo='programar'))
    def regra_04(self):
        self.registrar('backend', 'R04', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Desenvolvimento Back-end.')

    @Rule(Perfil(atividade='frontend'))
    def regra_05(self):
        self.registrar('frontend', 'R05', 3, 'Você prefere tarefas cotidianas ligadas a Desenvolvimento Front-end & UI/UX.')

    @Rule(Perfil(atividade='frontend', entrega='experiencia'))
    def regra_06(self):
        self.registrar('frontend', 'R06', 8, 'Sua atividade favorita combina com o resultado típico de Desenvolvimento Front-end & UI/UX.')

    @Rule(Perfil(atividade='frontend', ferramenta=P(lambda valor: valor in ('javascript', 'design'))))
    def regra_07(self):
        self.registrar('frontend', 'R07', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Desenvolvimento Front-end & UI/UX.')

    @Rule(Perfil(entrega='experiencia', estilo='criar'))
    def regra_08(self):
        self.registrar('frontend', 'R08', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Desenvolvimento Front-end & UI/UX.')

    @Rule(Perfil(atividade='ciencia'))
    def regra_09(self):
        self.registrar('ciencia', 'R09', 3, 'Você prefere tarefas cotidianas ligadas a Ciência de Dados e Machine Learning.')

    @Rule(Perfil(atividade='ciencia', entrega='previsoes'))
    def regra_10(self):
        self.registrar('ciencia', 'R10', 8, 'Sua atividade favorita combina com o resultado típico de Ciência de Dados e Machine Learning.')

    @Rule(Perfil(atividade='ciencia', ferramenta=P(lambda valor: valor in ('python', 'sql'))))
    def regra_11(self):
        self.registrar('ciencia', 'R11', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Ciência de Dados e Machine Learning.')

    @Rule(Perfil(entrega='previsoes', estilo='analisar'))
    def regra_12(self):
        self.registrar('ciencia', 'R12', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Ciência de Dados e Machine Learning.')

    @Rule(Perfil(atividade='engenharia'))
    def regra_13(self):
        self.registrar('engenharia', 'R13', 3, 'Você prefere tarefas cotidianas ligadas a Engenharia de Dados.')

    @Rule(Perfil(atividade='engenharia', entrega='dados'))
    def regra_14(self):
        self.registrar('engenharia', 'R14', 8, 'Sua atividade favorita combina com o resultado típico de Engenharia de Dados.')

    @Rule(Perfil(atividade='engenharia', ferramenta=P(lambda valor: valor in ('sql', 'python'))))
    def regra_15(self):
        self.registrar('engenharia', 'R15', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Engenharia de Dados.')

    @Rule(Perfil(entrega='dados', estilo='estruturar'))
    def regra_16(self):
        self.registrar('engenharia', 'R16', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Engenharia de Dados.')

    @Rule(Perfil(atividade='seguranca'))
    def regra_17(self):
        self.registrar('seguranca', 'R17', 3, 'Você prefere tarefas cotidianas ligadas a Cibersegurança (Security / Pentesting).')

    @Rule(Perfil(atividade='seguranca', entrega='protecao'))
    def regra_18(self):
        self.registrar('seguranca', 'R18', 8, 'Sua atividade favorita combina com o resultado típico de Cibersegurança (Security / Pentesting).')

    @Rule(Perfil(atividade='seguranca', ferramenta=P(lambda valor: valor in ('linux', 'python'))))
    def regra_19(self):
        self.registrar('seguranca', 'R19', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Cibersegurança (Security / Pentesting).')

    @Rule(Perfil(entrega='protecao', estilo='investigar'))
    def regra_20(self):
        self.registrar('seguranca', 'R20', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Cibersegurança (Security / Pentesting).')

    @Rule(Perfil(atividade='devops'))
    def regra_21(self):
        self.registrar('devops', 'R21', 3, 'Você prefere tarefas cotidianas ligadas a DevOps & SRE.')

    @Rule(Perfil(atividade='devops', entrega='entrega_continua'))
    def regra_22(self):
        self.registrar('devops', 'R22', 8, 'Sua atividade favorita combina com o resultado típico de DevOps & SRE.')

    @Rule(Perfil(atividade='devops', ferramenta=P(lambda valor: valor in ('linux', 'cloud'))))
    def regra_23(self):
        self.registrar('devops', 'R23', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para DevOps & SRE.')

    @Rule(Perfil(entrega='entrega_continua', estilo='automatizar'))
    def regra_24(self):
        self.registrar('devops', 'R24', 5, 'O modo de trabalho escolhido ajuda a entregar valor em DevOps & SRE.')

    @Rule(Perfil(atividade='cloud'))
    def regra_25(self):
        self.registrar('cloud', 'R25', 3, 'Você prefere tarefas cotidianas ligadas a Computação em Nuvem (Cloud Architecture).')

    @Rule(Perfil(atividade='cloud', entrega='escala'))
    def regra_26(self):
        self.registrar('cloud', 'R26', 8, 'Sua atividade favorita combina com o resultado típico de Computação em Nuvem (Cloud Architecture).')

    @Rule(Perfil(atividade='cloud', ferramenta=P(lambda valor: valor in ('cloud', 'linux'))))
    def regra_27(self):
        self.registrar('cloud', 'R27', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Computação em Nuvem (Cloud Architecture).')

    @Rule(Perfil(entrega='escala', estilo='operar'))
    def regra_28(self):
        self.registrar('cloud', 'R28', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Computação em Nuvem (Cloud Architecture).')

    @Rule(Perfil(atividade='mobile'))
    def regra_29(self):
        self.registrar('mobile', 'R29', 3, 'Você prefere tarefas cotidianas ligadas a Desenvolvimento Mobile.')

    @Rule(Perfil(atividade='mobile', entrega='aplicativos'))
    def regra_30(self):
        self.registrar('mobile', 'R30', 8, 'Sua atividade favorita combina com o resultado típico de Desenvolvimento Mobile.')

    @Rule(Perfil(atividade='mobile', ferramenta=P(lambda valor: valor in ('mobile', 'javascript'))))
    def regra_31(self):
        self.registrar('mobile', 'R31', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Desenvolvimento Mobile.')

    @Rule(Perfil(entrega='aplicativos', estilo='programar'))
    def regra_32(self):
        self.registrar('mobile', 'R32', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Desenvolvimento Mobile.')

    @Rule(Perfil(atividade='qa'))
    def regra_33(self):
        self.registrar('qa', 'R33', 3, 'Você prefere tarefas cotidianas ligadas a Engenharia de Qualidade e Testes (QA).')

    @Rule(Perfil(atividade='qa', entrega='qualidade'))
    def regra_34(self):
        self.registrar('qa', 'R34', 8, 'Sua atividade favorita combina com o resultado típico de Engenharia de Qualidade e Testes (QA).')

    @Rule(Perfil(atividade='qa', ferramenta=P(lambda valor: valor in ('testes', 'python'))))
    def regra_35(self):
        self.registrar('qa', 'R35', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Engenharia de Qualidade e Testes (QA).')

    @Rule(Perfil(entrega='qualidade', estilo='testar'))
    def regra_36(self):
        self.registrar('qa', 'R36', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Engenharia de Qualidade e Testes (QA).')

    @Rule(Perfil(atividade='produto'))
    def regra_37(self):
        self.registrar('produto', 'R37', 3, 'Você prefere tarefas cotidianas ligadas a Gestão de Produtos (Product Management).')

    @Rule(Perfil(atividade='produto', entrega='negocio'))
    def regra_38(self):
        self.registrar('produto', 'R38', 8, 'Sua atividade favorita combina com o resultado típico de Gestão de Produtos (Product Management).')

    @Rule(Perfil(atividade='produto', ferramenta=P(lambda valor: valor in ('gestao', 'design'))))
    def regra_39(self):
        self.registrar('produto', 'R39', 4, 'Suas ferramentas têm aplicação direta na atividade escolhida para Gestão de Produtos (Product Management).')

    @Rule(Perfil(entrega='negocio', estilo='coordenar'))
    def regra_40(self):
        self.registrar('produto', 'R40', 5, 'O modo de trabalho escolhido ajuda a entregar valor em Gestão de Produtos (Product Management).')

    @Rule(Perfil(atividade='ciencia', matematica='alta'))
    def regra_41(self):
        self.registrar('ciencia', 'R41', 3, 'Afinidade matemática alta favorece modelagem estatística e preditiva.')

    @Rule(Perfil(atividade='engenharia', entrega='dados', estilo='estruturar'))
    def regra_42(self):
        self.registrar('engenharia', 'R42', 3, 'Seu foco é construir e organizar fluxos de dados, mais do que prever resultados.')

    @Rule(Perfil(atividade='devops', entrega='entrega_continua', estilo='automatizar'))
    def regra_43(self):
        self.registrar('devops', 'R43', 2, 'Automação de entrega e confiabilidade apontam para DevOps/SRE.')

    @Rule(Perfil(atividade='cloud', entrega='escala', estilo='operar'))
    def regra_44(self):
        self.registrar('cloud', 'R44', 2, 'Arquitetura escalável e operação de infraestrutura apontam para Cloud.')

    @Rule(Perfil(entrega='qualidade', ferramenta='testes', estilo='testar'))
    def regra_45(self):
        self.registrar('qa', 'R45', 2, 'Ferramentas e rotina de testes reforçam qualidade de software.')

    @Rule(Perfil(entrega='negocio', ferramenta='gestao', estilo='coordenar'))
    def regra_46(self):
        self.registrar('produto', 'R46', 2, 'Priorização e coordenação orientadas a negócio reforçam Gestão de Produtos.')


def avaliar(respostas: dict[str, str]) -> Resultado:
    """Valida as opções, dispara regras e classifica as trilhas sem probabilidades fictícias."""
    if set(respostas) != set(VALIDOS):
        raise ValueError("Campos da entrevista ausentes ou inesperados.")
    for campo, resposta in respostas.items():
        if resposta not in VALIDOS[campo]:
            raise ValueError(f"Resposta inválida no campo: {campo}.")

    motor = ConsultorCarreiras()
    motor.reset()
    motor.declare(Perfil(**respostas))
    motor.run()

    # Critérios transparentes: pontos, quantidade de evidências, atividade,
    # entrega; a ordem de exibição fixa somente em empate total.
    atividade = respostas["atividade"]
    entrega = respostas["entrega"]
    valor_por_trilha = {
        "backend":"funcionalidades", "frontend":"experiencia", "ciencia":"previsoes",
        "engenharia":"dados", "seguranca":"protecao", "devops":"entrega_continua",
        "cloud":"escala", "mobile":"aplicativos", "qa":"qualidade", "produto":"negocio"
    }
    ranking = sorted(
        motor.pontos.items(),
        key=lambda item: (
            -item[1],
            -len(motor.evidencias[item[0]]),
            -int(item[0] == atividade),
            -int(valor_por_trilha[item[0]] == entrega),
            ORDEM.index(item[0]),
        ),
    )
    primeiro = ranking[0]
    empatados = [id_ for id_, pontos in ranking if pontos == primeiro[1]]
    criterio = (
        "Não houve empate na pontuação."
        if len(empatados) == 1 else
        "Houve empate em pontos; foram usados, nesta ordem: número de regras, "
        "afinidade diária, entrega preferida e ordem fixa das trilhas."
    )
    for lista in motor.evidencias.values():
        lista.sort(key=lambda regra: regra.codigo)
    return Resultado(primeiro[0], ranking, motor.evidencias, criterio)
