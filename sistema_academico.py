"""Sistema Inteligente de Gestão Acadêmica.

Aplicação de console para cadastro, notas, frequência, relatórios e recuperação.
"""
from dataclasses import dataclass, field
from typing import Optional

MEDIA_APROVACAO = 7.0
MEDIA_RECUPERACAO = 5.0
FREQUENCIA_MINIMA = 75.0


@dataclass
class Aluno:
    nome: str
    matricula: str
    idade: int
    turma: str
    notas: list[float] = field(default_factory=list)
    aulas_ministradas: int = 0
    faltas: int = 0
    nota_recuperacao: Optional[float] = None

    @property
    def media(self) -> float:
        notas = self.notas + ([self.nota_recuperacao] if self.nota_recuperacao is not None else [])
        return sum(notas) / len(notas) if notas else 0.0

    @property
    def frequencia(self) -> float:
        if self.aulas_ministradas <= 0:
            return 0.0
        presencas = self.aulas_ministradas - self.faltas
        return max(0.0, min(100.0, presencas / self.aulas_ministradas * 100))

    @property
    def situacao(self) -> str:
        if self.frequencia < FREQUENCIA_MINIMA:
            return "Reprovado por frequência"
        if self.media >= MEDIA_APROVACAO:
            return "Aprovado"
        if self.media >= MEDIA_RECUPERACAO:
            return "Recuperação"
        return "Reprovado"

    def inconsistencias(self) -> list[str]:
        problemas = []
        if len(self.notas) != 4:
            problemas.append("deve possuir exatamente quatro notas")
        if self.aulas_ministradas <= 0:
            problemas.append("aulas ministradas deve ser maior que zero")
        if self.faltas < 0 or self.faltas > self.aulas_ministradas:
            problemas.append("quantidade de faltas inválida")
        if any(n < 0 or n > 10 for n in self.notas):
            problemas.append("há nota fora do intervalo de 0 a 10")
        return problemas


class SistemaAcademico:
    def __init__(self) -> None:
        self.alunos: dict[str, Aluno] = {}

    def cadastrar_aluno(self, aluno: Aluno) -> None:
        self._validar_aluno(aluno)
        if aluno.matricula in self.alunos:
            raise ValueError("A matrícula já está cadastrada.")
        self.alunos[aluno.matricula] = aluno

    @staticmethod
    def _validar_aluno(aluno: Aluno) -> None:
        if not aluno.nome.strip():
            raise ValueError("O nome não pode ficar vazio.")
        if not aluno.matricula.strip():
            raise ValueError("A matrícula não pode ficar vazia.")
        if aluno.idade <= 0:
            raise ValueError("A idade deve ser maior que zero.")
        if len(aluno.notas) not in (0, 4):
            raise ValueError("O aluno deve possuir zero ou quatro notas.")
        if any(n < 0 or n > 10 for n in aluno.notas):
            raise ValueError("As notas devem estar entre 0 e 10.")
        if aluno.aulas_ministradas < 0 or aluno.faltas < 0:
            raise ValueError("Aulas e faltas não podem ser negativas.")
        if aluno.aulas_ministradas and aluno.faltas > aluno.aulas_ministradas:
            raise ValueError("Faltas não podem superar aulas ministradas.")

    def buscar(self, matricula: str) -> Aluno:
        try:
            return self.alunos[matricula]
        except KeyError as exc:
            raise ValueError("Aluno não encontrado.") from exc

    def registrar_notas(self, matricula: str, notas: list[float]) -> None:
        if len(notas) != 4 or any(n < 0 or n > 10 for n in notas):
            raise ValueError("Informe exatamente quatro notas entre 0 e 10.")
        self.buscar(matricula).notas = notas

    def registrar_frequencia(self, matricula: str, aulas: int, faltas: int) -> None:
        if aulas <= 0 or faltas < 0 or faltas > aulas:
            raise ValueError("Informe aulas > 0 e faltas entre 0 e aulas.")
        aluno = self.buscar(matricula)
        aluno.aulas_ministradas, aluno.faltas = aulas, faltas

    def registrar_recuperacao(self, matricula: str, nota: float) -> None:
        if nota < 0 or nota > 10:
            raise ValueError("A nota de recuperação deve estar entre 0 e 10.")
        aluno = self.buscar(matricula)
        if aluno.situacao != "Recuperação":
            raise ValueError("Somente alunos em recuperação podem receber nova nota.")
        aluno.nota_recuperacao = nota

    def ordenados_por_media(self) -> list[Aluno]:
        return sorted(self.alunos.values(), key=lambda a: (-a.media, a.nome.lower()))

    def relatorio(self) -> dict:
        alunos = list(self.alunos.values())
        contagem = {"Aprovado": 0, "Reprovado": 0, "Recuperação": 0, "Reprovado por frequência": 0}
        for aluno in alunos:
            contagem[aluno.situacao] += 1
        return {
            "total": len(alunos),
            "media_turma": sum(a.media for a in alunos) / len(alunos) if alunos else 0.0,
            "maior_media": max(alunos, key=lambda a: a.media) if alunos else None,
            "menor_media": min(alunos, key=lambda a: a.media) if alunos else None,
            "contagem": contagem,
            "baixa_frequencia": [a for a in alunos if a.frequencia < FREQUENCIA_MINIMA],
            "top_3": self.ordenados_por_media()[:3],
            "inconsistencias": {a.matricula: a.inconsistencias() for a in alunos if a.inconsistencias()},
        }


def ler_float(mensagem: str, minimo: float | None = None, maximo: float | None = None) -> float:
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
                raise ValueError
            return valor
        except ValueError:
            print("Entrada inválida. Tente novamente.")


def ler_int(mensagem: str, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                raise ValueError
            return valor
        except ValueError:
            print("Entrada inválida. Tente novamente.")


def exibir_aluno(aluno: Aluno) -> None:
    print(f"\n{aluno.nome} | Matrícula: {aluno.matricula} | {aluno.idade} anos | Turma: {aluno.turma}")
    print(f"Notas: {', '.join(f'{n:.1f}' for n in aluno.notas) or 'não registradas'} | Média: {aluno.media:.2f}")
    print(f"Frequência: {aluno.frequencia:.2f}% | Situação: {aluno.situacao}")
    if aluno.nota_recuperacao is not None:
        print(f"Nota de recuperação: {aluno.nota_recuperacao:.1f}")


def executar_menu() -> None:
    sistema = SistemaAcademico()
    while True:
        print("\n=== SISTEMA INTELIGENTE DE GESTÃO ACADÊMICA ===")
        print("1. Cadastrar aluno\n2. Registrar notas\n3. Registrar frequência\n4. Consultar aluno")
        print("5. Relatórios\n6. Registrar recuperação\n7. Ranking\n0. Encerrar")
        opcao = input("Escolha: ").strip()
        try:
            if opcao == "1":
                aluno = Aluno(input("Nome completo: "), input("Matrícula: "), ler_int("Idade: ", 1), input("Turma: "))
                sistema.cadastrar_aluno(aluno); print("Aluno cadastrado com sucesso.")
            elif opcao == "2":
                matricula = input("Matrícula: ")
                sistema.registrar_notas(matricula, [ler_float(f"Nota {i}/4: ", 0, 10) for i in range(1, 5)])
                print("Notas registradas.")
            elif opcao == "3":
                sistema.registrar_frequencia(input("Matrícula: "), ler_int("Aulas ministradas: ", 1), ler_int("Faltas: ", 0)); print("Frequência registrada.")
            elif opcao == "4":
                exibir_aluno(sistema.buscar(input("Matrícula: ")))
            elif opcao == "5":
                r = sistema.relatorio(); print(f"Total: {r['total']} | Média da turma: {r['media_turma']:.2f}")
                print("Situações:", r["contagem"])
                print("Baixa frequência:", ", ".join(a.nome for a in r["baixa_frequencia"]) or "nenhum")
            elif opcao == "6":
                sistema.registrar_recuperacao(input("Matrícula: "), ler_float("Nova nota: ", 0, 10)); print("Recuperação registrada.")
            elif opcao == "7":
                for posicao, aluno in enumerate(sistema.ordenados_por_media(), 1): print(f"{posicao}. {aluno.nome} — {aluno.media:.2f}")
            elif opcao == "0":
                print("Sistema encerrado."); break
            else: print("Opção inválida.")
        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    executar_menu()
