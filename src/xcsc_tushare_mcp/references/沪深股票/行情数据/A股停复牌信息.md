## A股停复牌信息

___

接口：suspend

描述：获取股票每日停复牌信息

限量：单次最大10000条

**输入参数**

|名称|类型|必选|描述|
|---|---|---|---|
|ts\_code|str|N|ts代码|
|suspend\_date|str|N|停牌日期|
|resume\_date|str|N|复牌日期|

**输出参数**

|名称|类型|默认显示|描述|
|---|---|---|---|
|ts\_code|str|Y|ts代码|
|suspend\_date|str|Y|停牌日期|
|suspend\_type|int|Y|停牌类型代码|
|resump\_date|str|Y|复牌日期|
|change\_reason|str|Y|停牌原因|
|suspend\_time|str|Y|停复牌时间|
|change\_reason\_type|int|Y|停牌原因代码|

**接口用法**

```python

pro = ts.pro_api()
df = pro.suspend(ts_code='600848.SH', fields='ts_code,suspend_date,suspend_type,resump_date')
```

**数据样例**

```
       ts_code suspend_date  suspend_type resump_date
0    600848.SH     20140505     444016000        None
1    600848.SH     20140506     444003000        None
2    600848.SH     20140507     444016000        None
3    600848.SH     20140508     444016000        None
4    600848.SH     20140509     444016000        None
..         ...          ...           ...         ...
310  600848.SH     20180927     444016000        None
311  600848.SH     20180928     444016000        None
312  600848.SH     20181008     444016000        None
313  600848.SH     20181009     444016000    20181010
314  600848.SH     20190327     444016000    20190328
```