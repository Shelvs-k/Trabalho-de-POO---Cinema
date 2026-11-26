import unittest

from filmes import (ClassificacaoIndicativa, Filme, GerenciadorFilmes,
                    FilmeDuplicadoError, FilmeNaoEncontradoError)


def novo_filme(id_filme=1, titulo="Matrix", duracao=136.0, genero="Ficção",
               sinopse="Um hacker descobre a verdade.",
               classificacao=ClassificacaoIndicativa.CATORZE_ANOS):
    return Filme(id_filme, titulo, duracao, genero, sinopse, classificacao)


class TestClassificacao(unittest.TestCase):
    def test_idade_minima_e_descricao(self):
        self.assertEqual(ClassificacaoIndicativa.LIVRE.idade_minima, 0)
        self.assertEqual(ClassificacaoIndicativa.DEZOITO_ANOS.idade_minima, 18)
        self.assertIn("18", ClassificacaoIndicativa.DEZOITO_ANOS.descricao)


class TestFilme(unittest.TestCase):
    def test_criacao_valida(self):
        f = novo_filme()
        self.assertEqual(f.id_filme, 1)
        self.assertEqual(f.titulo, "Matrix")

    def test_id_somente_leitura(self):
        with self.assertRaises(AttributeError):
            novo_filme().id_filme = 5

    def test_valores_invalidos(self):
        for kwargs in ({"id_filme": 0}, {"titulo": ""}, {"titulo": "  "},
                       {"genero": ""}, {"duracao": 0}, {"duracao": -1}):
            with self.assertRaises(ValueError, msg=str(kwargs)):
                novo_filme(**kwargs)

    def test_classificacao_tipo_errado(self):
        with self.assertRaises(TypeError):
            novo_filme(classificacao="DEZ_ANOS")
        f = novo_filme()
        with self.assertRaises(TypeError):
            f.classificacao = 14

    def test_setters_validam(self):
        f = novo_filme()
        with self.assertRaises(ValueError):
            f.duracao = 0
        f.titulo = "Matrix Reloaded"
        self.assertEqual(f.titulo, "Matrix Reloaded")

    def test_permitido_para(self):
        f = novo_filme()  # 14 anos
        self.assertTrue(f.permitido_para(14))
        self.assertTrue(f.permitido_para(30))
        self.assertFalse(f.permitido_para(13))
        with self.assertRaises(ValueError):
            f.permitido_para(-1)

    def test_exibir_detalhes(self):
        self.assertIn("Matrix", novo_filme().exibir_detalhes())


class TestGerenciador(unittest.TestCase):
    def setUp(self):
        self.g = GerenciadorFilmes()
        self.g.cadastrar_filme(novo_filme(1, "Matrix", genero="Ficção"))
        self.g.cadastrar_filme(novo_filme(2, "Matilda", genero="Infantil"))

    def test_duplicado(self):
        with self.assertRaises(FilmeDuplicadoError):
            self.g.cadastrar_filme(novo_filme(1))

    def test_buscar_por_id(self):
        self.assertEqual(self.g.buscar_por_id(2).titulo, "Matilda")
        with self.assertRaises(FilmeNaoEncontradoError):
            self.g.buscar_por_id(99)

    def test_pesquisas(self):
        self.assertEqual(len(self.g.pesquisar_por_titulo("mat")), 2)
        self.assertEqual(len(self.g.pesquisar_por_titulo("trix")), 1)
        self.assertEqual(len(self.g.pesquisar_por_genero("ficção")), 1)
        self.assertEqual(self.g.pesquisar_por_genero("Terror"), [])

    def test_listar(self):
        self.assertEqual(len(self.g.listar_filmes()), 2)


if __name__ == "__main__":
    unittest.main()
