# VacuumTubeBook

# ディレクトリ構成

各ディレクトリの中には以下のようなファイルが入っています．

* Ep-Ip_characteristic/: 真空管のEp-Ip特性のグラフ

いろいろな真空管について，低い電圧(プレート電圧最大30V)で計測した特性をグラフに描画したものです．

* LTspice/: LTspiceのモデルファイルと回路ファイル

いろいろな真空管について，実測したデータを元にして作成したLTspiceのモデルファイルと，シミュレーション用の回路ファイルを入れてあります．

* LTspice/lib: LTspiceのモデルファイル

コンピューターにインストールされているLTspiceのlib/subとlib/symの中に，MyTubeModelというフォルダをコピーすると，上記のシミュレーション用回路ファイルから読み込むことができます．

* Program/: 真空管で実測したEp，IpからLTspiceのモデルファイルを作成するプログラム

実際に自分で真空管の特性を計測して，LTspiceのモデルを作成するプログラムです．CSVデータを読み込んで，三極管のEp-Ipモデルを出力します．サンプルデータが一緒に置いてあります．

# Author

* 有村光晴

# License

* "Program/CSVtoModel_Cohen_Helie.py" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
