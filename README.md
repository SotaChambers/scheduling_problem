# system requirements

```txt
python = >=3.9, <3.11
poetry = ^1.2.2
```

# Creating a virtual environment

```bash
poetry install
poetry shell
```

# D-Wave: Procedure

1. Create a D-Wave Leap account
https://cloud.dwavesys.com/leap/login/
2. Note your API Token in Dashborad

# formulation

## Constant
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

## Variable
- $x_{adt} \in \{0, 1\}$ : 作業員 $a$ が $d$ 日のターム $t$ に割り振られたか


## Constraint
- 作業員が希望していないターム( $r_{adt}=0$ )にはシフトを割り振らない
$r_{adt} = 0$ の場合，以下を満たす
```math
\forall a\in A, \forall d\in D, \forall t\in T :  x_{adt} = 0
```
- 同じグループに割り振られた作業員全員が同じシフトに割り振られる
```math
\forall a\in A, \forall d\in D, \forall g : \sum_{a} x_{adt} * G_{ga} = \sum_{a}G_{ga}
```

## Objective Function
- 希望ブース数と割り当てられる作業員数が近い
```math
\sum_{dt}(\sum_{a}x_{adt} - S_{dt})
```
- 実際に割り当てる作業員数と希望シフト数の差が近い
```math
\sum_{a}(\sum_{dt}x_{adt} - R_{a})
```


実行
ratio: 10分程度
base: 1分程度
opt: 2sくらい