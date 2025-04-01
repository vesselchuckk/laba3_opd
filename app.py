from flask import Flask, render_template, request

app = Flask(__name__)

def solve_quadratic(a, b, c):
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except ValueError:
        return None, "Ошибка: Все коэффициенты должны быть числами"

    if a == 0:
        return None, "Ошибка: Коэффициент 'a' не может быть нулем"

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return [], "Уравнение не имеет действительных корней"
    elif discriminant == 0:
        root = -b / (2 * a)
        return [round(root, 2)], ""
    else:
        root1 = (-b + discriminant ** 0.5) / (2 * a)
        root2 = (-b - discriminant ** 0.5) / (2 * a)
        return [round(root1, 2), round(root2, 2)], ""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')

        roots, error = solve_quadratic(a, b, c)
        return render_template('index.html',
                               a=a, b=b, c=c,
                               roots=roots,
                               error=error)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)