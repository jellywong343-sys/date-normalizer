# 鏃ユ湡鏍煎紡鏍囧噯鍖栧伐鍏?
[English](README.md)

缁熶竴 CSV 瀛楁涓殑澶氱鏃ユ湡鏍煎紡锛屽悓鏃朵繚鐣欐棤娉曡В鏋愮殑鍊间緵浜哄伐妫€鏌ャ€?
## 涓昏鍔熻兘

- 鏀寔 ISO銆佹枩绾裤€佺偣鍙枫€佺揣鍑戞牸寮忋€佽嫳鏂囨湀浠藉拰鏃ユ湡鏃堕棿銆?- 浣跨敤 Python `strftime` 璇硶璁剧疆杈撳嚭鏍煎紡銆?- 鍙鐩栧師瀛楁锛屼篃鍙啓鍏ユ柊鐨勬爣鍑嗗寲瀛楁銆?- 榛樿淇濈暀鏃犳晥鍊硷紝骞舵姤鍛婂搴旇鍙枫€?- 涓ユ牸妯″紡閬囧埌绗竴涓棤鏁堟棩鏈熷氨鍋滄銆?- 鍙紭鍏堟寜鈥滄棩/鏈?骞粹€濊В閲婃ā绯婃暟瀛楁棩鏈熴€?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/date-normalizer.git
cd date-normalizer
python -m pip install -e .
```

## 浣跨敤

```bash
date-normalize examples/mixed-dates.csv normalized.csv --column event_date --day-first
date-normalize input.csv output.csv --column date --output-column normalized_date
date-normalize input.csv output.csv --column date --format "%Y/%m/%d" --report invalid.json
date-normalize input.csv output.csv --column date --strict
```

鍍?`03/04/2026` 杩欐牱鐨勬棩鏈熷瓨鍦ㄦ涔夈€傞粯璁や紭鍏堟寜鈥滄湀/鏃?骞粹€濊В閲婏紱闇€瑕佲€滄棩/鏈?骞粹€濇椂浣跨敤 `--day-first`銆?
濡傛灉鐩爣鏂囦欢宸茬粡瀛樺湪锛岀▼搴忎細瑕嗙洊瀹冦€傝淇濈暀閲嶈婧愭暟鎹殑澶囦唤銆?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT

