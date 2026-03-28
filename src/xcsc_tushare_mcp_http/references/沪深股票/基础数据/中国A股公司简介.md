## 中国A股公司简介

___

接口：stock\_company

描述：获取上市公司基础信息

限量：单次最大10000条

**输入参数**

|名称|类型|必选|描述|
|---|---|---|---|
|ts\_code|str|N|TS代码|

**输出参数**

|名称|类型|默认显示|描述|
|---|---|---|---|
|ts\_code|str|Y|TS代码|
|province|str|Y|省份|
|city|str|Y|城市|
|chairman|str|Y|法人代表|
|president|str|Y|总经理|
|bd\_secretary|str|Y|董事会秘书|
|reg\_capital|int|Y|注册资本(万元)|
|found\_date|str|Y|成立日期|
|chinese\_introduction|str|Y|公司中文简介|
|comp\_type|str|Y|公司类型|
|website|str|Y|主页|
|email|str|Y|电子邮箱|
|office|str|Y|办公地址|
|ann\_date|str|Y|公告日期|
|country|str|Y|国籍|
|business\_scope|None|Y|经营范围|
|company\_type|str|Y|公司类别|
|total\_employees|int|Y|员工总数(人)|
|main\_business|str|Y|主要产品及业务|

**接口示例**

```python
pro = ts.pro_api()

#或者
#pro = ts.pro_api('your token')

df = pro.stock_company(ts_code='000001.SZ,000002.SZ', fields='ts_code,province,city,chairman,president,bd_secretary')
```

**数据示例**

```
        ts_code province city chairman president bd_secretary
0  000001.SZ      广东省  深圳市      谢永林       胡跃飞           周强
1  000002.SZ      广东省  深圳市       郁亮       祝九胜           朱旭
```