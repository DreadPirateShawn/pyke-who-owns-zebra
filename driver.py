import time
from pyke import knowledge_engine
import texttable as tt

engine = knowledge_engine.engine(__file__)

##################

CATEGORY_TYPES = ['POSITION', 'HOUSE_COLOR', 'NATIONALITY', 'PET', 'DRINK', 'SMOKE']
CATEGORY_HEADERS = ['#', 'Color', 'Nationality', 'Pet', 'Drink', 'Smoke']

def one_value_by_position(pos, category_type):
    try:
        return engine.prove_1_goal('clues.related(POSITION, %s, %s, $thing)' % (pos, category_type))[0].get('thing')
    except Exception, e:
        return "?"

def table_all_by_position():
    table = tt.Texttable()
    table.set_deco(table.HEADER)
    table.set_cols_align(['l'] * len(CATEGORY_HEADERS))
    rows = [list(CATEGORY_HEADERS)]

    with engine.prove_goal('clues.is_category(POSITION, $type)') as gen1:
        for vars, plan in gen1:
            pos = vars['type']
            rows.append( [pos,
                          one_value_by_position(pos, 'HOUSE_COLOR'),
                          one_value_by_position(pos, 'NATIONALITY'),
                          one_value_by_position(pos, 'PET'),
                          one_value_by_position(pos, 'DRINK'),
                          one_value_by_position(pos, 'SMOKE')] )

    table.add_rows(rows)
    return table.draw()

def who_owns_the_zebra():
    try:
        natl = engine.prove_1_goal('clues.related(PET, zebra, NATIONALITY, $nationality)')[0].get('nationality')
    except Exception, e:
        natl = "Unknown"
    return "== Who owns the zebra? %s ==" % natl

##################

start_time = time.time()
engine.activate('relations')
elapsed_time = round(time.time() - start_time, 2)

print ""
print who_owns_the_zebra()
print ""
print table_all_by_position()
print ""
print "Calculated in %s seconds." % elapsed_time
print ""

