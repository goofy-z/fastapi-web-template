class EnumTypeMeta(type):
    """
    使用metaclass来使继承的枚举类具有新的特征
        几个概念：
           属性： 定义枚举类的属性
           值：   枚举类属性的value
           说明： 这个枚举值的中文解释
        用法：
            class MyTest(EnumType):
                TestPeople = ("goofy", "a handsome guy")
            print(MyTest.TestPeople) 值 goofy
            print(MyTest.values) {属性:值} 字典
            print(MyTest.labels) {属性:说明} 字典
            print(MyTest.value_label)  {值:说明} 字典
        注意：
            切记不要在代码中通过_values或其它属性改变枚举类定义的属性和值，虽然程序允许。
    """

    def __new__(cls, name, bases, attrs):
        _values = {}  # {属性:值}
        _labels = {}  # {属性:说明}
        _value_label = {}  # {值:说明}

        for k, v in attrs.items():
            # 遇到私有属性跳过
            if k.startswith("__"):
                continue
            if isinstance(v, (tuple, list)) and len(v) == 2:
                _values[k] = v[0]
                _labels[k] = v[1]
                _value_label[v[0]] = v[1]
            elif isinstance(v, dict) and "label" in v and "value" in v:
                _values[k] = v["value"]
                _labels[k] = v["label"]
                _value_label[v["value"]] = v["label"]
            else:
                _values[k] = k
                _labels[k] = v
                _value_label[v] = None
        # 通过元类生成类对象时，传入_values，将类属性的值改写
        obj = type.__new__(cls, name, bases, _values)
        obj._values = _values
        obj._labels = _labels
        obj._value_label = _value_label
        return obj

    @property
    def values(self):
        return self._values

    @property
    def labels(self):
        return self._labels

    @property
    def value_label(self):
        return self._value_label

    def __eq__(self, other):
        print(123)
        if isinstance(other, str):
            return other == self.__str__()
        else:
            return hash(id(self)) == hash(id(other))


class EnumType(metaclass=EnumTypeMeta):
    pass
