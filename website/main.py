from flask import Flask, render_template, request
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Congrats on finding the secret key! Here\'s a cookie'

@app.route('/', methods = ['POST', 'GET'])

def calculations():
    tensile_area = 3.14159
    external_shear = 3.14159

    n = 0
    dbsc = 0

    if request.method == 'POST':
        n = float(request.form.get('n'))
        dbsc = float(request.form.get('dbsc'))
        d2min = float(request.form.get('d2min'))
        D1max = float(request.form.get('D1max'))
        loe = float(request.form.get('loe'))

    if request.method == 'POST' and 'n' in request.form and 'dbsc' in request.form:
        if n == 0:
            tensile_area = 0
        elif dbsc == 0:
            tensile_area = 0
        else:
            As = (math.pi / 4) * ((dbsc - ((9 * math.sqrt(3)) / (16 * n))) ** 2)
            tensile_area = round(As,4)

    if request.method == 'POST' and 'n' in request.form and 'd2min' in request.form and 'D1max' in request.form and 'loe' in request.form:
        if n == 0:
            external_shear = 0
        else:
            ASs_min = math.pi * n * D1max * loe * ((1 / (2 * n)) + ((d2min - D1max)/math.sqrt(3)))
            external_shear = round(ASs_min, 4)

    return render_template('base.html', n = n, dbsc = dbsc, tensile_area = tensile_area, external_shear = external_shear)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug = True)
