import pytest
from bs4 import BeautifulSoup
from app import app, solve_quadratic


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_no_real_roots(client):
    # данные с отрицательным дискриминантом
    response = client.post('/', data={
        'a': 1,
        'b': 2,
        'c': 3
    })

    # парсим ответ
    soup = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    # ищем блок результатов
    result_div = soup.find('div', class_='result')

    # проверям что результат существует
    assert result_div is not None
    assert 'Уравнение не имеет действительных корней' in result_div.text.strip()


def test_zero_a(client):
    # данные с a=0
    response = client.post('/', data={
        'a': 0,
        'b': 2,
        'c': 3
    })

    # парсим ответ
    soup = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    # ищем блок с ошибкой
    error_div = soup.find('div', class_='error')

    # првоеряем что блок существует
    assert error_div is not None
    assert 'Коэффициент \'a\' не может быть нулем' in error_div.text.strip()

