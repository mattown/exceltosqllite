import py.exceletl as exceletl
import sqlite3
import config, sys
import py.customsql as csql

print("starting up loading all data into db")
exceletl.load_all_db()


conn = sqlite3.connect(config.db_dir)
c = conn.cursor()
# run richards custom job
for query in csql.custom_queries['richard_table']:
    c.execute(query)
conn.commit()
exceletl.write_table_to_tab('richard_data')



kill_switch = True

while kill_switch:
    response = input("Please enter your query\n")
    if 'q' in response.lower().strip():
        kill_switch =False
    else:
        try:
            for row in c.execute(response):
                print(row)
        except:
            print("Unexpected error:", sys.exc_info()[0])
conn.close()