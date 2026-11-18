import unittest

from sistema_academico import Aluno, SistemaAcademico


class TestSistemaAcademico(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaAcademico()
        self.aluno = Aluno("Ana Souza", "2026001", 16, "2º TDS", [8, 7, 9, 8], 100, 10)
        self.sistema.cadastrar_aluno(self.aluno)

    def test_media_frequencia_e_aprovacao(self):
        self.assertEqual(self.aluno.media, 8.0)
        self.assertEqual(self.aluno.frequencia, 90.0)
        self.assertEqual(self.aluno.situacao, "Aprovado")

    def test_impede_matricula_duplicada(self):
        with self.assertRaises(ValueError):
            self.sistema.cadastrar_aluno(Aluno("Outra Pessoa", "2026001", 17, "2º TDS"))

    def test_frequencia_reprova_independente_da_media(self):
        self.sistema.registrar_frequencia("2026001", 100, 30)
        self.assertEqual(self.aluno.situacao, "Reprovado por frequência")

    def test_recuperacao_atualiza_media(self):
        aluno = Aluno("Bruno Lima", "2026002", 16, "2º TDS", [5, 5, 5, 5], 100, 0)
        self.sistema.cadastrar_aluno(aluno)
        self.assertEqual(aluno.situacao, "Recuperação")
        self.sistema.registrar_recuperacao("2026002", 9)
        self.assertEqual(aluno.media, 5.8)

    def test_ranking_decrescente(self):
        self.sistema.cadastrar_aluno(Aluno("Carlos", "2026003", 16, "2º TDS", [10, 10, 10, 10], 100, 0))
        self.assertEqual(self.sistema.ordenados_por_media()[0].nome, "Carlos")


if __name__ == "__main__":
    unittest.main()
