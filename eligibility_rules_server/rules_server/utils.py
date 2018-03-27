import json
from collections import defaultdict
from datetime import date

from django.utils.dateparse import parse_date


def relationalize(target,
                  name='data_source',
                  results=None,
                  ids=None,
                  parent_id=None,
                  parent_name=None):
    if results is None:
        results = defaultdict(list)
    if ids is None:
        ids = defaultdict(int)
    if not isinstance(target, list):
        target = [
            target,
        ]
    for itm in target:
        row = {'id': ids[name] + 1}
        ids[name] += 1
        if parent_name:
            row[parent_name + '_id'] = parent_id
        if isinstance(itm, dict):
            for (key, val) in itm.items():
                if isinstance(val, list) or isinstance(val, dict):
                    relationalize(
                        target=val,
                        name=key,
                        results=results,
                        ids=ids,
                        parent_id=row['id'],
                        parent_name=name)
                else:
                    row[key] = val
        else:
            row[name] = itm
        results[name].append(row)
    return results


def datatype_is_ok(datatype, value):
    if datatype == int:
        is_float = datatype_is_ok(float, value)
        return is_float and float(value).is_integer()
    elif datatype == bool:
        return isinstance(value, bool)
    elif datatype == date:
        try:
            result = parse_date(value)
            return bool(result)
        except TypeError:
            return False
    try:
        datatype(value)
        return True
    except (TypeError, ValueError):
        return False


def datatype(values):
    """
    Most restrictive Python type that works for all values.

    >>> data = [4, 'cows', 0.3]
    >>> datatype(data)
    <class 'str'>

    >>> data = [4, 12, 9]
    >>> datatype(data)
    <class 'int'>

    >>> data = [True, False, False]
    >>> datatype(data)
    <class 'bool'>
    """

    types = [bool, int, float, str]
    for value in values:
        while not datatype_is_ok(types[0], value):
            types.pop(0)
            if not types:
                raise TypeError('No known type for %s' % value)
    return types[0]


PY_TO_PG_DATATYPES = {
    bool: 'bool',
    int: 'integer',
    float: 'numeric',
    str: 'text',
    date: 'date',
}


def all_values_in_list_of_dicts(data):
    """
    >>> data = [{'a': 1}, {'b': 2}, {'a': 3, 'b': 4}]
    >>> dict(all_values_in_list_of_dicts(data))
    {'a': [1, 3], 'b': [2, 4]}
    """
    values = defaultdict(list)
    for row in data:
        for (key, val) in row.items():
            values[key].append(val)
    return values


def column_types(data):
    """
    For a list of dicts `data`, find PostgreSQL types

    >>> data = [{'a': 1.5}, {'b': 'cows', 'c': 2}, {'a': 3, 'b': 4}]
    >>> column_types(data)
    {'a': 'numeric', 'b': 'text', 'c': 'integer'}
    """

    result = {}
    for (key, values) in all_values_in_list_of_dicts(data).items():
        dtype = PY_TO_PG_DATATYPES.get(datatype(values))
        result[key] = dtype
    return result


def record_type(data, schema):
    """
    Generates PostgreSQL record type SQL
    """

    data_types = column_types(data)
    if schema:
        data_types.update(schema.data_types())
    return ', '.join(
        '%s %s' % (key, dtype) for (key, dtype) in data_types.items())


def sql(name, data, schema=None):

    types = record_type(data=data, schema=schema)

    return """%s AS
        (SELECT * FROM JSON_TO_RECORDSET(%%s) AS x(%s))""" % (name, types)


def values_from_json(raw, schema=None):
    relationalized = relationalize(raw, 'applicant')
    for (table_name, data) in relationalized.items():
        yield (sql(table_name, data, schema=schema), json.dumps(data))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
