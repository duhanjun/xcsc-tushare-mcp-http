## A股指数日行情

___

接口：index\_daily

描述：获取指数每日行情

限量：单次最大3000条

**输入参数**

|名称|类型|必选|描述|
|---|---|---|---|
|ts\_code|str|N|指数代码|
|trade\_date|str|N|交易日期|
|start\_date|str|N|开始日期|
|end\_date|str|N|结束日期|

**输出参数**

|名称|类型|默认显示|描述|
|---|---|---|---|
|ts\_code|str|Y|ts代码|
|trade\_date|str|Y|交易日期|
|crncy\_code|str|Y|货币代码|
|pre\_close|float|Y|昨收盘价(点)|
|open|float|Y|开盘价(点)|
|high|float|Y|最高价(点)|
|low|float|Y|最低价(点)|
|close|float|Y|收盘价(点)|
|change|float|Y|涨跌(点)|
|pct\_chg|float|Y|涨跌幅(%)|
|volume|float|Y|成交量(手)|
|amount|float|Y|成交金额(千元)|
|sec\_id|str|Y|证券ID|

**接口使用**

```python
pro = ts.pro_api()
df = pro.index_daily(trade_date="20181230",fields="ts_code,trade_date,pre_close,close,change,pct_chg")
```

**数据样例**

```
      ts_code   trade_date  pre_close  close  change  pct_chg
0  h30085.CSI   20181230      4.57  4.57      0          0
1  h30275.CSI   20181230      4.85  4.85      0          0
2  h30276.CSI   20181230      4.57  4.57      0          0
3  h30277.CSI   20181230      4.39  4.39      0          0
4  h30360.CSI   20181230       4.4   4.4      0          0
5  h30361.CSI   20181230      4.39  4.39      0          0
```