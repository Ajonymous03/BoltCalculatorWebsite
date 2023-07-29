from flask import Flask, render_template, request
from equationDictionary import tensile_area, min_external_shear, min_internal_shear, R_Ratio, LEr
from ASME_B11 import ASME_B11_UN_2A2B_dict

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def calculations():
    
    selected = request.form.get('threadType')

    n = 0
    dmin = 0
    dbsc = 0
    d1bsc = 0
    d2min = 0
    d2bsc = 0
    D1bsc = 0
    D1max = 0
    D2max = 0
    UTSs = 0
    UTSn = 0
    LE = 1

    if request.method == 'POST' and selected == 'none':
        n = float(request.form.get('n'))

        dmin = float(request.form.get('dmin'))

        dbsc = float(request.form.get('dbsc'))

        d1bsc = float(request.form.get('d1bsc'))

        d2min = float(request.form.get('d2min'))

        d2bsc = float(request.form.get('d2bsc'))

        D1bsc = float(request.form.get('D1bsc'))

        D1max = float(request.form.get('D1max'))

        D2max = float(request.form.get('D2max'))

        UTSs = float(request.form.get('UTSs'))

        UTSn = float(request.form.get('UTSn'))

        LE = float(request.form.get('LE'))
    else:
        n = ASME_B11_UN_2A2B_dict[selected]['n']

        dmin = ASME_B11_UN_2A2B_dict[selected]['dmin']

        dbsc = ASME_B11_UN_2A2B_dict[selected]['dbsc']
        
        d1bsc = ASME_B11_UN_2A2B_dict[selected]['d1bsc']

        d2min = ASME_B11_UN_2A2B_dict[selected]['d2min']
        
        d2bsc = ASME_B11_UN_2A2B_dict[selected]['d2bsc']

        D1bsc = ASME_B11_UN_2A2B_dict[selected]['D1bsc']

        D1max = ASME_B11_UN_2A2B_dict[selected]['D1max']

        D2max = ASME_B11_UN_2A2B_dict[selected]['D2max']

        UTSs = float(request.form.get('UTSs'))

        UTSn = float(request.form.get('UTSn'))

        LE = float(request.form.get('LE'))

    if request.method == 'POST' and n > 0 and dbsc > 0:
        As_val = round(tensile_area(n, dbsc), 4)
        As = 'The Tensile Stress Area is ' + str(As_val) + ' in\u00b2'
    else:
        As = ''

    if request.method == 'POST' and n > 0 and d2min > 0 and D1max > 0:
        ASs_val = round(min_external_shear(n, d2min, D1max, LE), 4)
        ASs = 'The Minimum External Shear Area is ' + str(ASs_val) + ' in\u00b2'
    else:
        ASs = ''

    if request.method == 'POST' and n > 0 and dmin > 0 and D2max > 0:
        ASn_val = round(min_internal_shear(n, dmin, D2max, LE), 4)
        ASn = 'The Minimum Internal Shear Area is ' + str(ASn_val) + ' in\u00b2'
    else:
        ASn = ''

    if request.method == 'POST' and n > 0 and dmin > 0 and D1bsc > 0 and D2max > 0 and UTSn > 0 and UTSs > 0 and LE > 0:
        R_val = round(R_Ratio(n, dmin, D1bsc, D2max, UTSs, UTSn, LE), 4)
        R = 'The R Ratio is ' + str(R_val)
    else:
        R = ''

    if request.method == 'POST' and n > 0 and dmin > 0 and dbsc > 0 and d1bsc > 0 and d2min > 0 and d2bsc > 0 and D1bsc \
            > 0 and D1max > 0 and D2max > 0 and UTSs > 0:
        LEr_plot = LEr(n, dmin, dbsc, d1bsc, d2min, d2bsc, D1bsc, D1max, D2max, UTSs)
    else:
        LEr_plot = ''




    return render_template('base.html', n=n, dmin=dmin, dbsc=dbsc, d1bsc=d1bsc, d2min=d2min, d2bsc=d2bsc, D1bsc=D1bsc,
                           D1max=D1max, D2max=D2max, UTSs=UTSs, UTSn=UTSn, LE=LE,
                           tensile_area=As, external_shear=ASs, internal_shear=ASn, R_Ratio=R, plot=LEr_plot)


if __name__ == '__main__':
    app.run(debug=True)

    # app.run(host="0.0.0.0", port=80, debug = True)
