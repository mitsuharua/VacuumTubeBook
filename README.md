# 真空管アンプ製作 LTspiceでシミュレーション サポートページ
<img src="https://github.com/mitsuharua/VacuumTubeBook/blob/main/book_cover.png" title="Vacuum Tube BOOK" width="450" height="635">

# このページについて

このページは，書籍<a href="https://www.ohmsha.co.jp/book/9784274228780/" target="_blank">「真空管アンプ製作 LTspiceでシミュレーション」</a>のサポートページです．

本書では，12Vという電圧の制限を課して真空管アンプを製作します．通常使われる200Vから400Vという高い電圧を使用した真空管アンプと比べ，部品を安価に抑えられ，感電の危険をなくし，配線を間違えたときの部品の損傷もある程度防げます．

本書では，20〜30V程度で真空管の特性を実測したデータを基に作成したSPICEモデルを用いて，回路設計を行なっています．実測したモデルに基づいたEp-Ip特性とSPICEモデルを，このサイトで公開しています．

# ファイルのダウンロード方法

右上にある緑色の「Code」というボタンをマウスでクリックすると，メニューが開きます．一番下にある「Download ZIP」をクリックすると，全てのファイルがzipファイルにアーカイブされて手元のパソコンにダウンロードされます．

# ディレクトリ構成

各ディレクトリの中には以下のようなファイルが入っています．

* Ep-Ip_characteristic/: 真空管のEp-Ip特性のグラフ

いろいろな真空管について，低い電圧(プレート電圧最大30V)で計測した特性をグラフに描画したものです．

* LTspice/: LTspiceのモデルファイルと回路ファイル

いろいろな真空管について，実測したデータを元にして作成したLTspiceのモデルファイルと，シミュレーション用の回路ファイルを入れてあります．

* LTspice/lib: LTspiceのモデルファイル

コンピューターにインストールされているLTspiceのライブラリフォルダlib/subとlib/symの中に，フォルダlib/subの中のMyTubeModelと，フォルダlib/symの中のMyTubeModelをそれぞれコピーすると，上記のシミュレーション用回路ファイルから読み込むことができます．

* Program/: 真空管で実測したEp，IpからLTspiceのモデルファイルを作成するプログラム

実際に自分で真空管の特性を計測して，LTspiceのモデルを作成するプログラムです．CSVデータを読み込んで，三極管のEp-Ipモデルを出力します．サンプルデータが一緒に置いてあります．

# Author

* 有村光晴

# License

* "Program/CSVtoModel_Cohen_Helie.py" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
