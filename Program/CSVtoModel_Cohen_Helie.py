#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 真空管のEp-IpデータからSPICEモデルを作成
# python 3.7.3 on macOS 10.14.5

# LMFITを使う Cohen-Helieモデル
# Ip = (2/kg) max{Et, 0}^exponent
# Et = Ep/kp * log(1+exp(kp*(1/mu+(Eg+ect)/g(Ep)) ))
# g(Ep) = sqrt(kvb + Ep*Ep + evb2*Ep)

import sys,csv
import subprocess
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from lmfit import Model

# 真空管のCohen-Helieモデル関数
# 注意: 引数[Eg,Ep]は1個で与える必要がある
# 2個目以降の引数がパラメータ
def Ip(x, kG, mu, exponent, kp, kvb, kvb2, ect ):
    Eg = x[:,0]
    Ep = x[:,1]
    def PosSqrt(x):
        return np.sqrt(np.maximum(x, 0.00001))
    def PosPower(x, y):
        return np.power(np.maximum(x, 0.00001), y)
    def LogExp(x):
        return np.log(1 + np.exp(x))
    def f(Ep, kvb, kvb2):
        v = kvb + np.power(Ep, 2.0) + kvb2 * Ep
        return PosSqrt(v)
    def V(Eg, Ep, mu, kp, kvb, kvb2, ect):
        return (Ep/kp) * LogExp(kp*(1/mu + (Eg+ect)/f(Ep, kvb, kvb2)))
    return 1000.0 /kG * PosPower( V(Eg, Ep, mu, kp, kvb, kvb2, ect),
                                  exponent)

# パラメータをファイルから読み込む
# 全て文字列で読み込まれる
def ReadParamFiles(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        # param1, 初期値, 最小値, 最大値
        # param2, 初期値, 最小値, 最大値
        # ...
        return [row for row in reader]

# データをフィッティングする
# Levenberg-Marquardt法を用いた非線形最小二乗法
def FittingData(xlist, ylist, data, paramsList):
    xarray = np.array(xlist)
    yarray = np.array(ylist)
    datamatrix = np.array(data)
    xarrayf = xarray.astype(np.float32)
    yarrayf = yarray.astype(np.float32)
    datamatrixf = datamatrix.astype(np.float32)
    #print('x:\n{}'.format(xarrayf))
    #print('y:\n{}'.format(yarrayf))
    #print('data:\n{}'.format(datamatrixf))

    x_array, y_array = np.meshgrid(xarrayf, yarrayf)
    #print('x_array:\n{}'.format(x_array))
    #print('y_array:\n{}'.format(y_array))
    xy_array = np.array(list(zip(x_array.flatten(),
                                 y_array.flatten())))
    z_array = datamatrixf.flatten()
    #print('xy:\n{}'.format(xy_array))
    #print('z:\n{}'.format(z_array))

    #print("parameter:\n{}".format(paramsList))
    model = Model(Ip)
    for p in paramsList:
        model.set_param_hint(p[0],
                             value=float(p[1]),
                             min=float(p[2]),
                             max=float(p[3]))
        print('{}: value={}, min={}, max={}'.format(
            p[0], float(p[1]), float(p[2]), float(p[3]) ))
    params = model.make_params()

    #print('data for fit:\n{}'.format(z_array))
    #print('x for fit:\n{}'.format(xy_array))
    result = model.fit(z_array,
                       x=xy_array,
                       params=params)
    # overall report
    print('fit report============================')
    print(result.fit_report())
    # fitted parameters
    print('estimated parameters===========================')
    fitted_params = result.best_values
    print(fitted_params)
    for v in fitted_params:
        print("key: {}, values: {}".format(v, fitted_params[v]))
    # fitted data
    print('fitted data==========================')
    fitted_data = result.best_fit.reshape([len(yarrayf),
                                           len(xarrayf)])
    #print('fitted data:\n{}'.format(fitted_data))
    return (xarrayf, yarrayf, datamatrixf,
            fitted_params, fitted_data)

# オリジナルデータのグラフの出力EpIp2次元
def OutputOriginalDataGraphEpIp2D(xarrayf, yarrayf, datamatrixf,
                            titleStr, fileNameStr):
    #ディスプレイに表示せずファイルに出力するだけの場合の設定
    matplotlib.use('pdf')
    # 測定データのプロット
    measured_data = datamatrixf.T
    plt.rcParams['font.size'] = 10
    plt.xlabel('Ep(V)')
    plt.ylabel('Ip(mA)')
    plt.xlim(xmax=20)
    #plt.ylim(ymax=1.0)
    plt.title(titleStr)
    # xlabelは20個に押さえる
    if (len(yarrayf) > 10):
        skip = len(yarrayf) // 20
        xticklist = yarrayf[::skip]
    else:
        xticklist = yarrayf
    #print("xtics: {}".format(xticklist))
    plt.xticks(xticklist)
    # 格子線を描画
    plt.grid(b=None, which='major', axis='both')
    # 実測データを折れ線でプロット
    line_styles = ["-", "--", ":", "-."]
    for eg in range(xarrayf.size):
        plt.plot(yarrayf,
                 measured_data[eg],
                 marker="+",
                 color='black',
                 linestyle=line_styles[eg % len(line_styles)],
                 linewidth=0.5 * (eg // len(line_styles) + 1),
                 label="Eg={:.2f}".format(xarrayf[eg]))
    # 凡例の表示
    plt.legend(bbox_to_anchor=(1.05, 1),
               loc='upper left', borderaxespad=0)
    # PDFファイルに出力
    fileName = fileNameStr + '_Original.pdf'
    plt.savefig(fileName, bbox_inches='tight', format='pdf')
    # 現在まで描画した画面を削除
    plt.clf()

# オリジナルデータのグラフの出力EpIp2次元(最大1mA)
def OutputOriginalDataGraphEpIp2D1mA(xarrayf, yarrayf, datamatrixf,
                            titleStr, fileNameStr):
    #ディスプレイに表示せずファイルに出力するだけの場合の設定
    matplotlib.use('pdf')
    # 測定データのプロット
    measured_data = datamatrixf.T
    plt.rcParams['font.size'] = 10
    plt.xlabel('Ep(V)')
    plt.ylabel('Ip(mA)')
    plt.xlim(xmax=20)
    plt.ylim(ymax=1.0)
    plt.title(titleStr)
    # xlabelは20個に押さえる
    if (len(yarrayf) > 10):
        skip = len(yarrayf) // 20
        xticklist = yarrayf[::skip]
    else:
        xticklist = yarrayf
    #print("xtics: {}".format(xticklist))
    plt.xticks(xticklist)
    # 格子線を描画
    plt.grid(b=None, which='major', axis='both')
    # 実測データを折れ線でプロット
    line_styles = ["-", "--", ":", "-."]
    for eg in range(xarrayf.size):
        plt.plot(yarrayf,
                 measured_data[eg],
                 marker="+",
                 color='black',
                 linestyle=line_styles[eg % len(line_styles)],
                 linewidth=0.5 * (eg // len(line_styles) + 1),
                 label="Eg={:.2f}".format(xarrayf[eg]))
    # 凡例の表示
    plt.legend(bbox_to_anchor=(1.05, 1),
               loc='upper left', borderaxespad=0)
    # PDFファイルに出力
    fileName = fileNameStr + '_Original1mA.pdf'
    plt.savefig(fileName, bbox_inches='tight', format='pdf')
    # 現在まで描画した画面を削除
    plt.clf()

# オリジナルデータのグラフの出力EpEgIp3次元
def OutputOriginalDataGraphEpEgIp3D(xarrayf, yarrayf, datamatrixf,
                                    titleStr, fileNameStr):
    #ディスプレイに表示せずファイルに出力するだけの場合の設定
    matplotlib.use('pdf')
    # 測定データのプロット
    zarrayf = datamatrixf
    X = np.ravel(xarrayf)
    Y = np.ravel(yarrayf)
    XY = np.array([[x for x in X] for y in Y])
    X, Y = np.meshgrid(X, Y)
    Z = np.reshape(zarrayf, np.shape(XY))
    #print( "X: {}".format(X) )
    #print( "Y: {}".format(Y) )
    #print( "X,Y: {}".format(X,Y) )
    #print( "Z: {}".format(Z) )
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Eg(V)')
    ax.set_ylabel('Ep(V)')
    ax.set_zlabel('Ip(mA)')
    ax.set_title(titleStr)
    # 格子線を描画
    ax.plot_wireframe(X, Y, Z, color='black')
    # PDFファイルに出力
    fileName = fileNameStr + '_Original3D.pdf'
    plt.savefig(fileName, bbox_inches='tight', format='pdf')
    # 現在まで描画した画面を削除
    plt.clf()

# モデルにfitしたグラフの出力
def DisplayFittedGraph(xarrayf, yarrayf, datamatrixf, fitted_data,
              titleStr, fileNameStr):
    #ディスプレイに表示する場合
    #matplotlib.use('MacOSX')
    # 測定データのプロット
    measured_data = datamatrixf.T
    plt.rcParams['font.size'] = 10
    plt.xlabel('Ep(V)')
    plt.ylabel('Ip(mA)')
    plt.xlim(xmax=20)
    plt.ylim(ymax=1.0)
    plt.title(titleStr)
    # xlabelは20個に押さえる
    if (len(yarrayf) > 10):
        skip = len(yarrayf) // 20
        xticklist = yarrayf[::skip]
    else:
        xticklist = yarrayf
    #print("xtics: {}".format(xticklist))
    plt.xticks(xticklist)
    # 格子線を描画
    plt.grid(b=None, which='major', axis='both')
    # 実測データは点のみプロット
    for eg in range(xarrayf.size):
        plt.plot(yarrayf,
                 measured_data[eg],
                 marker="+",
                 linewidth=0,
                 color='black')

    # フィッティングしたグラフを折れ線でプロット
    data_for_each_eg = fitted_data.T
    line_styles = ["-", "--", ":", "-."]
    for eg in range(xarrayf.size):
        plt.plot(yarrayf,
                 data_for_each_eg[eg],
                 color='black',
                 linestyle=line_styles[eg % len(line_styles)],
                 linewidth=0.5 * (eg // len(line_styles) + 1),
                 label="Eg={:.2f}".format(xarrayf[eg]))
    # 凡例の表示
    plt.legend(bbox_to_anchor=(1.05, 1),
               loc='upper left', borderaxespad=0)
    # PDFファイルに出力
    fileName = fileNameStr + '_Cohen.pdf'
    plt.savefig(fileName, bbox_inches='tight', format='pdf')
    # 表示 (注:macOS用) PDFファイルはopenするだけでPreviewが開いてくれる．
    #cmdline = ["/usr/bin/env", "open", fileName]
    #print("cmdline: {}".format(cmdline))
    #subprocess.run(cmdline)
    # プログラム内部で表示する
    # このウィンドウを閉じるとプログラム終了
    #plt.show()

# csvファイルから実測データを読み込む
def GeneratePlotData(csvFileName, tubeNameStr):
    with open(csvFileName) as f:
        reader = csv.reader(f)
        csvData = [row for row in reader]
        # 0行目:メーカー,型番,ピン配置
        # 1行目:'三極管'/'五極管'/'ビーム管',
        #       'ヒーター',電圧,電流,'直流'/'交流'
        # 2行目:'三極管接続'/'五極管接続'/'UL接続',Eg2設定
        # 3行目:'','Eg'
        # 4行目:'','Ip(mA)',Eg(0),Eg(1),...
        # 5行目:'Ep',Ep(0),Ip,...
        # 6行目以降:'',Ep(1),Ip,...

        # 転置を使うためnumpyで配列を操作
        csvMatrix = np.array(csvData)
        csvMatrixTr = csvMatrix.T
        #print(csvMatrix)
        #print(csvMatrixTr)
        # データを取り出した後，文字列からfloat32に変換
        # 現時点では各行が各Ep固定でEgを変化させたときのIp
        EgLabelsData = csvMatrix[4][2:].astype(np.float32)
        EpLabelsData = csvMatrixTr[1][5:].astype(np.float32)
        IpData = csvMatrix[5:,2:].astype(np.float32)
        #print('Eg:{}'.format(EgLabelsData))
        #print('Ep:{}'.format(EpLabelsData))
        #print('Ip:{}'.format(IpData))
        tubeNameArray=tubeNameStr.split('_')
        tubeName=tubeNameArray[0]
        Eg2Setting=tubeNameArray[1]
        titleStr=tubeName
        fileNameStr=tubeName + '_' + Eg2Setting
        #FittingData(EgLabelsData, EpLabelsData, IpData)
        return (EgLabelsData, EpLabelsData, IpData, titleStr,
                fileNameStr, tubeName)

def OutputLTspiceModel(fileNameStr, tubeNameStr, fittedParams):
    fileName = fileNameStr + "_Cohen.sub"
    print("Output LTspice model to the file {}".format(fileName))
    with open(fileName, "w") as f:
        f.write(".SUBCKT {} 1 2 3; P G K\n".format(tubeNameStr))
        f.write("+ PARAMS:\n")
        for v in fittedParams:
            f.write("+ {}={}".format(v, fittedParams[v]))
            f.write(" ; from model fit\n")
        f.write("+ CGA=??? CGK=??? CAK=??? ; from datasheet\n")
        f.write("+ RGI=2000\n")
        f.write('''
* Plate Current
E1  6 0 VALUE={SQRT(kvb+V(1,3)*V(1,3)+kvb2*V(1,3))}
E2  7 0 VALUE={V(1,3)/kp*LOG(1+EXP(kp*(1/mu+(V(2,3)+ect)/V(6))))}
RE1 7 0 1G
G1  1 3 VALUE={PWR(URAMP(V(7)),exponent)/kG}
RCP 1 3 1G
D3  5 3 DX    ; for Grid Current
R2  2 5 {RGI} ; for Grid Current
* CAPS
CGK 2 3 {CGK} ; Cathode-Grid
CGA 2 1 {CGA} ; Grid-Anode(Plate)
CAK 1 3 {CAK} ; Anode(Plate)-Cathode
* REGS
RF1 1 0 1G
RF2 2 0 1G
RF3 3 0 1G
.MODEL DX D(IS=1N RS=1 CJO=10PF TT=1N) ; diode for grid current
.ENDS
''')
        f.close()
##------
if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print('{} '.format(args[0])
              + 'TubeName_Setting.csv '
              + 'TubeName_param.csv')
        sys.exit()
    # 拡張子".csv"を除く
    # "TubeName_Setting"
    tubeNameStr = args[1][0:-4]
    # csvファイルからデータを取り出す
    (EgData, EpData, IpData, titleStr,
     fileNameStr, tubeName) = GeneratePlotData(args[1], tubeNameStr)
    # パラメータファイルからパラメータのリストと初期値を取り出す
    ParamsList = ReadParamFiles(args[2])
    # フィッティング
    (xarrayf, yarrayf, datamatrixf, fittedParams,
     fittedData) = FittingData(EgData, EpData, IpData, ParamsList)
    # LTspiceモデルを出力
    OutputLTspiceModel(fileNameStr, tubeName, fittedParams)
    # グラフを出力
    OutputOriginalDataGraphEpIp2D(xarrayf, yarrayf, datamatrixf,
                                  titleStr, fileNameStr)
    OutputOriginalDataGraphEpIp2D1mA(xarrayf, yarrayf, datamatrixf,
                                     titleStr, fileNameStr)
    OutputOriginalDataGraphEpEgIp3D(xarrayf, yarrayf, datamatrixf,
                                    titleStr, fileNameStr)
    DisplayFittedGraph(xarrayf, yarrayf, datamatrixf,
              fittedData, titleStr, fileNameStr)
    # グラフ画面を閉じると終了
# EOF
