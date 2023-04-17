# システム要件

```txt
python = >=3.9, <3.11
poetry = ^1.2.2
```

# 仮想環境の作成

```bash
poetry install
poetry shell
```

# D-Wave: 手順

1. a D-Wave Leap のアカウントを作成<br>
https://cloud.dwavesys.com/leap/login/
2. Dashborad にあるAPI Token をメモ<br>
configの `d-wave_credential_example.yml` を `d-wave_credential.yml` に変更し，TOKEN にAPI TOKEN を貼り付ける

# 定式化
問題設定は以下の論文を参考<br>
[Applying Quantum Annealing for Shift Scheduling Problem for Call Centers](https://www.jstage.jst.go.jp/article/ijnc/13/1/13_2/_pdf/-char/ja)
## 定数
- $A$ : 作業員の集合
  - {作業員1, …, 作業員a}
- $D$ : スケジュール対象日の集合
  - {1日, …, d日}
- $T$ : 1日のターム（午前，午後，夕方など）の集合
  - {ターム1, ..., タームt}
- $S_{dt}$ : $d$ 日のターム $t$ に必要なブース数
- $R_{a}$ : 作業員 $a$ の希望割り当てシフト数
- $G_{ga} \in \{0, 1\}$ : グループ $g$ に作業員 $a$ が所属しているかいないかのバイナリ定数
- $r_{adt} \in \{0, 1\}$ : 作業員 $a$ が $d$ 日のターム $t$ へ割り当て可能かを表すバイナリ定数

## 変数
- $x_{adt} \in \{0, 1\}$ : 作業員 $a$ が $d$ 日のターム $t$ に割り振られたか


## 制約条件
- 作業員が希望していないターム( $r_{adt}=0$ )にはシフトを割り振らない
$r_{adt} = 0$ の場合，以下を満たす
```math
\forall a\in A, \forall d\in D, \forall t\in T :  x_{adt} = 0
```
- 同じグループに割り振られた作業員全員が同じシフトに割り振られる
```math
\forall a\in A, \forall d\in D, \forall g : \sum_{a} x_{adt} * G_{ga} = \sum_{a}G_{ga}
```

## 目的関数
- 希望ブース数と割り当てられる作業員数が近い
```math
\sum_{dt}(\sum_{a}x_{adt} - S_{dt})
```
- 実際に割り当てる作業員数と希望シフト数の差が近い
```math
\sum_{a}(\sum_{dt}x_{adt} - R_{a})
```


# 実行
## ペナルティ係数の Ratio を決める
SQAで実行すると 10分 程度かかる．`graph/coeff_ratio.png` にヒートマップが出力される
```bash
python src/decide_ratio.py
```

## ペナルティ係数の base を決める
SQAで実行すると 1分 程度かかる．`graph/coeff_base.png` に実行可能確率とエネルギー図が出力される．
```bash
python src/decide_base.py
```

## スケジュールを算出
`graph/schedule.png` にスケジュールが出力される
```bash
python src/optimize.py
```