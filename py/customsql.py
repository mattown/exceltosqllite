

custom_queries = {

'richard_table' : [

"Drop table if exists richard_data;",

"""
CREATE TABLE richard_data(
location TEXT,
region TEXT,
model TEXT,
purchase_date INTEGER,
cost NUMERIC,
source TEXT,
path TEXT);""",

"""INSERT INTO richard_data
SELECT location, region, model, purchase_date, cost, source, path from ups
UNION ALL SELECT location, region, model, purchase_date, cost, source, path from raritan_reseller
UNION ALL SELECT location, region, model, purchase_date, cost, source, path from raritan_end_user
UNION ALL SELECT location, region, model, purchase_date, cost, source, path from gso
UNION ALL SELECT location, region, model, purchase_date, cost, source, path from raritan_ww
UNION ALL SELECT location, region, model, purchase_date, cost, source, path from pdus;
"""],

'richard_query' : """
SELECT location, region, model, datetime(purchase_date, 'unixepoch'), cost, source, path from richard_data;

"""


}