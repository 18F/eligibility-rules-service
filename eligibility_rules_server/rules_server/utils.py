from collections import defaultdict
import json
import pprint

def relationalize(target, name='data_source', results=None, ids=None, parent_id=None, parent_name=None):
    if results is None:
        results = defaultdict(list)
    if ids is None:
        ids = defaultdict(int)
    if not isinstance(target, list):
        target = [target, ]
    for itm in target:
        row = {'id': ids[name] + 1}
        ids[name] += 1
        if parent_name:
            row[parent_name + '_id'] = parent_id
        if isinstance(itm, dict):
            for (key, val) in itm.items():
                if isinstance(val, list) or isinstance(val, dict):
                    relationalize(target=val, name=key, results=results, ids=ids, parent_id=row['id'], parent_name=name)
                else:
                    row[key] = val
        else:
            row[name] = itm
        results[name].append(row)
    return results

def sql_values(target):
    relationalized = relationalize(target)
    for (name, tbl) in relationalized.items()   :
        values = ", ".join("(%s)" % row.values() for row in tbl)
        yield """WITH %s AS (
              VALUES %s
              AS T()
            )""" % (name, values)

with open('../examples/payload1.json') as infile:
    raw = json.load(infile)
    for v in sql_values(raw):
        print(v)