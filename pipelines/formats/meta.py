
def conversion(*args):
    def dec(func):
        assert not hasattr(func, 'converts_from')
        func.converts_from = args
        return func
    return dec
        
class FormatMeta(type):
    def __new__(cls, name, bases, attrs):
        assert 'convert_table' not in attrs
        attrs['convert_table'] = {}
        for base in bases:
            if hasattr(base, 'convert_table'):
                attrs['convert_table'].update(base.convert_table)
        table = {}
        for attr in attrs.itervalues():
            if hasattr(attr, 'converts_from'):
                for from_cls in attr.converts_from:
                    assert from_cls not in table
                    table[from_cls] = attr
        attrs['convert_table'].update(table)
        return super(FormatMeta, cls).__new__(cls, name, bases, attrs)
