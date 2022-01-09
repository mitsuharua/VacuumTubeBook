# fittingプログラム

このディレクトリには，三極真空管のEp-Ip特性を実測したデータに対して，Cohen-Helieモデルを当てはめて，LTspiceのモデルデータを出力するプログラムと，サンプルファイルが入っています．

# このディレクトリにあるファイル

* README.md: このファイル
* CSVtoModel_Cohen_Helie.py: Python3による変換プログラム
* 6J1_Eg2=Ep.csv: 三極管結合でEg1とEpを決めてIpを実測したデータ
* 6J1_params_Cohen.csv: モデルフィッティングする際のパラメータの初期化ファイル

# プログラムの実行方法

python3 CSVtoModel_Cohen_Helie.py 6J1_Eg2=Ep.csv 6J1_params_Cohen.csv

# 出力ファイル

