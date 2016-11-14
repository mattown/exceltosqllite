import sqlite3, os
from config import db_dir, hard_coded_fields, output_config
import py.fieldutils as futil

sql_statements = {
    'drop_table' : 'DROP TABLE IF EXISTS %s',
    'create_table': 'CREATE TABLE %s(%s);',
    'insert_table': 'INSERT INTO %s VALUES (%s)'
}

def add_py_function(item, function):
    if function ==None:
        return item
    else:
        return function(item)

def write_obj(write_obj):

    #connect to db
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()

    # Drop table
    cmd = sql_statements['drop_table'] % write_obj['table_name']
    c.execute(cmd)

    #create table
    create_statement =[]
    for f in write_obj['fields']:
        field_info = futil.process_field(f)
        create_statement.append('%s %s' % (field_info['sql_field'], field_info['field_type']) )
    #hard coded fields
    for item in hard_coded_fields:
        create_statement.append('%s TEXT' % item)

    cmd = sql_statements['create_table'] % (str(write_obj['table_name']), ', '.join(create_statement))
    c.execute(cmd)

    # load table
    cleaned_data = []
    for row in write_obj['data']:
        col = []
        for f in write_obj['fields']:
            field_info = futil.process_field(f)
            val = None
            for i in range(0,len(write_obj['headers'])):
                if field_info['target_field'].lower() in write_obj['headers'][i].lower():
                    val = add_py_function(row[i], field_info['python_f'])
            col.append(val)
        #hard coded fields
        for item in hard_coded_fields:
            col.append(write_obj[item])

        cleaned_data.append(tuple(col))

    cmd = sql_statements['insert_table'] % (write_obj['table_name'], ','.join(['?'] * (len(write_obj['fields'])+len(hard_coded_fields)) ))
    c.executemany(cmd, cleaned_data)
    conn.commit()
    conn.close()
    print("CREATED TABLE %s " % write_obj['table_name'])

def print_table(name):
    conn = sqlite3.connect(db_dir)
    cmd = 'select * from %s' % name
    c = conn.cursor()
    for row in c.execute(cmd):
        print(row)
    conn.close()


def write_table(name):
    conn = sqlite3.connect(db_dir)

    cmd = 'select * from %s' % name
    c = conn.cursor()
    f = open('output/%s.tsv'% name,'w')
    data = c.execute(cmd)
    names = [description[0] for description in c.description]
    f.write(output_config['delimiter'].join(names) + output_config['new_line'])
    for row in data:
        l = []
        for item in row:
            l.append( str(item) )
        f.write(output_config['delimiter'].join(l)+output_config['new_line'])
    f.close()
    conn.close()