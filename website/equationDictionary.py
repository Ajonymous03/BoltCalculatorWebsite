from math import pi, sqrt
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def tensile_area(n, dbsc):
    As = (pi / 4) * ((dbsc - ((9 * sqrt(3)) / (16 * n))) ** 2)
    return As


def As_ISO(n, d1bsc, d2bsc):
    H = sqrt(3) / (2 * n)
    d3 = d1bsc - (H / 6)
    As = (pi / 4) * ((d2bsc + d3) / 2) ** 2
    return As


def ASb_ISO(n, d2bsc, D1bsc):
    ASb = n * pi * D1bsc * ((1 / (2 * n)) + ((d2bsc - D1bsc) / sqrt(3)))
    return ASb


def ASn_ISO(n, dbsc, d2bsc):
    ASn = n * pi * dbsc * ((1 / (2 * n)) + ((dbsc - d2bsc) / sqrt(3)))
    return ASn


def min_external_shear(n, d2min, D1max, LE):
    ASs_min = pi * n * LE * D1max * ((1 / (2 * n)) + ((1 / sqrt(3)) * (d2min - D1max)))
    return ASs_min


def max_external_shear(D1bsc, LE):
    ASs_max = pi * D1bsc * 0.75 * LE
    return ASs_max


def min_internal_shear(n, dmin, D2max, LE):
    ASn_min = pi * n * LE * dmin * ((1 / (2 * n)) + ((1 / sqrt(3)) * (dmin - D2max)))
    return ASn_min


def R_Ratio(n, dmin, D1bsc, D2max, UTSs, UTSn, LE):
    R1 = (max_external_shear(D1bsc, LE)) / (min_internal_shear(n, dmin, D2max, LE))
    R2 = (UTSn) / (UTSs)
    return (R1 / R2)


def Rs_Ratio(n, dbsc, d2bsc, D1bsc, UTSs, UTSn):
    Rs = (UTSn * ASn_ISO(n, dbsc, d2bsc)) / (UTSs * ASb_ISO(n, d2bsc, D1bsc))
    return Rs


def C2_ISO(n, dbsc, d2bsc, D1bsc, UTSs, UTSn):
    R = Rs_Ratio(n, dbsc, d2bsc, D1bsc, UTSs, UTSn)
    if R <= 1:
        C2 = 0.897
    else:
        C2 = 5.594 - 13.682 * R + 14.107 * R ** 2 - 6.057 * R ** 3 + 0.9353 * R ** 4
    return C2


def C3_ISO(n, dbsc, d2bsc, D1bsc, UTSs, UTSn):
    R = Rs_Ratio(n, dbsc, d2bsc, D1bsc, UTSs, UTSn)
    if R >= 1:
        C3 = 0.897
    else:
        C3 = 0.728 + 1.769 * R - 2.896 * R ** 2 + 1.296 * R ** 3
    return C3


def LEr_FEDSTD_13(n, dbsc, d2bsc):
    As = tensile_area(n, dbsc)
    LEr = (4 * As) / (pi * d2bsc)
    return LEr


def LEr_FEDSTD_14(n, dbsc, d2min, D1max):
    As = tensile_area(n, dbsc)
    LE = 1
    ASs = min_external_shear(n, d2min, D1max, 1)
    LEr = 2 * As / ASs
    return LEr


def LEr_FEDSTD_15(n, dbsc, D1bsc):
    As = tensile_area(n, dbsc)
    LE = 1
    LEr = 2 * As / max_external_shear(D1bsc, 1)
    return LEr


def LEr_FEDSTD_16(n, dmin, dbsc, D1bsc, D2max, UTSs, UTSn):
    LEr = LEr_FEDSTD_15(n, dbsc, D1bsc) * R_Ratio(n, dmin, D1bsc, D2max, UTSs, UTSn, 1)
    return LEr


def LEr_FEDSTD(n, dmin, dbsc, d2min, d2bsc, D1bsc, D1max, D2max, UTSs, UTSn):
    R = R_Ratio(n, dmin, D1bsc, D2max, UTSs, UTSn, 1) 
    if R < 0.95:
        LEr = LEr_FEDSTD_14(n, dbsc, d2min, D1max)
    else:
        LEr_13 = LEr_FEDSTD_13(n, dbsc, d2bsc)
        LEr_16 = LEr_FEDSTD_16(n, dmin, dbsc, D1bsc, D2max, UTSs, UTSn)
        LEr = max(LEr_13, LEr_16)
    return LEr


def LEr_ISO16224(n, dbsc, d1bsc, d2bsc, D1bsc, UTSs, UTSn):
    LEr1 = As_ISO(n, d1bsc, d2bsc) / (0.6 * ASb_ISO(n, d2bsc, D1bsc) * C2_ISO(n, dbsc, d2bsc, D1bsc, UTSs, UTSn)) 
    LEr2 = (As_ISO(n, d1bsc, d2bsc) * UTSs) / (0.6 * UTSn * ASn_ISO(n, dbsc, d2bsc) * C3_ISO(n, dbsc, d2bsc, D1bsc, UTSs, UTSn)) 
    LEr = max(LEr1, LEr2) 
    return LEr


def LEr(n, dmin, dbsc, d1bsc, d2min, d2bsc, D1bsc, D1max, D2max, UTSs):
     UTSn_list = np.linspace(50000, 200000, 2000)
     fig = Figure()
     FigureCanvas(fig)

     LEr_FED = []
     LEr_ISO = []

     for UTSn in UTSn_list:
          LEr_FED.append(LEr_FEDSTD(n, dmin, dbsc, d2min, d2bsc, D1bsc, D1max, D2max, UTSs, UTSn))
          LEr_ISO.append(LEr_ISO16224(n, dbsc, d1bsc, d2bsc, D1bsc, UTSs, UTSn))

     ax = fig.subplots(1)
     ax.plot(UTSn_list, LEr_FED, label = 'FED-STD-H28/2B')
     ax.plot(UTSn_list, LEr_ISO, label = 'ISO 16224')
     ax.set_xlabel('Strength of Internally Threaded Part (psi)')
     ax.set_ylabel('Length of Engagement Required')
     ax.legend()
     
     img = io.StringIO()
     fig.savefig(img, format = 'svg')
     svg_img = '<svg' + img.getvalue().split('<svg')[1]
     return svg_img
