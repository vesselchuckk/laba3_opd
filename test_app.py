import unittest
from app import app, solve_quadratic

class TestQuadraticEquationSolver(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента Flask"""
        self.app = app.test_client()
        self.app.testing = True

    def test_solve_quadratic_valid_roots(self):
        """Тест решения уравнения с двумя действительными корнями"""
        roots, error = solve_quadratic(1, -3, 2)  # x² - 3x + 2 = 0
        self.assertCountEqual(roots, [2.0, 1.0])  # Независимо от порядка
        self.assertEqual(error, "")

    def test_solve_quadratic_one_root(self):
        """Тест решения уравнения с одним действительным корнем"""
        roots, error = solve_quadratic(1, -4, 4)  # x² - 4x + 4 = 0
        self.assertEqual(roots, [2.0])
        self.assertEqual(error, "")

    def test_solve_quadratic_no_roots(self):
        """Тест решения уравнения без действительных корней"""
        roots, error = solve_quadratic(1, 2, 5)  # x² + 2x + 5 = 0
        self.assertEqual(roots, [])
        self.assertEqual(error, "Уравнение не имеет действительных корней")

    def test_solve_quadratic_invalid_a(self):
        """Тест с нулевым коэффициентом a"""
        roots, error = solve_quadratic(0, 2, 3)  # 0x² + 2x + 3 = 0
        self.assertIsNone(roots)
        self.assertEqual(error, "Ошибка: Коэффициент 'a' не может быть нулем")

    def test_solve_quadratic_non_numeric(self):
        """Тест с нечисловыми коэффициентами"""
        roots, error = solve_quadratic("a", "b", "c")
        self.assertIsNone(roots)
        self.assertEqual(error, "Ошибка: Все коэффициенты должны быть числами")

    def test_index_page_get(self):
        """Тест GET-запроса к главной странице"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Решение квадратных уравнений', response.data.decode('utf-8'))

    def test_index_page_post_valid(self):
        """Тест POST-запроса с валидными данными"""
        response = self.app.post('/', data={
            'a': 1,
            'b': -5,
            'c': 6
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Корни уравнения: x₁ = 3.0, x₂ = 2.0', response.data.decode('utf-8'))

    def test_index_page_post_invalid_a(self):
        """Тест POST-запроса с нулевым коэффициентом a"""
        response = self.app.post('/', data={
            'a': 0,
            'b': 2,
            'c': 3
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ошибка: Коэффициент &#39;a&#39; не может быть нулем", response.data.decode('utf-8'))

    def test_index_page_post_no_roots(self):
        """Тест POST-запроса с уравнением без корней"""
        response = self.app.post('/', data={
            'a': 1,
            'b': 2,
            'c': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Уравнение не имеет действительных корней', response.data.decode('utf-8'))

    def test_index_page_post_one_root(self):
        """Тест POST-запроса с уравнением с одним корнем"""
        response = self.app.post('/', data={
            'a': 1,
            'b': -6,
            'c': 9
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Уравнение имеет один корень: x = 3.0', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

