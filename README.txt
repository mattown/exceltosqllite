This is a generic Excel --> Sqllite loader

TOC

1. Install notes
2. Usage
 a) context
 b) config excel
 c) run
3. Contact


1.) Install notes

Requirments

Python 3.x

# python dependencies
openpyxl
xlrd

2.) Usage

a) Context

Before we explain the usage of this we need to make a couple of assumptions.
We always assume that there is a header in the excel for what files we want,
it doesn't have to be located at the top per se but we have to specify in the config on what row it is.


Directory explanation

data/   excel files go in here
output/  any custom queries on the sqllite db and their output go here
sqllitedb/   this is where the database is stored
config.py   This is the file we edit to config what field combinations we want to extract from the excel files -->db


b) config excel

To configure an excel file we have to put excel files in the data directory. For each directory we add to the data direcotry
we have to add a corresponding entry in the config.py, you must put it in the excel_config dictionary with the following format

You can also add as many excel files you want into one directory, but the application will apply that config to all files in the
directory.

Format:

    '<dir name>' : {
        '<sheet name>' : {
            'table_name': <<tablename>>,
            'header_loc' : <<header location>>,
            'include_all' : <<includeall>>,
            'fields' : [
            <<field arrays>>....



            ]},
        'custom_reader': <<custom_reader>>,
        'file_type': '<<extension>>'

    },

<dir name> = directory name of excel files for given sheet configs
<sheet name> = sheet name of excel file(s) to look for, is a regex
<<tablename>> = Table name of the converted data in sqllitedb
<<header location>> = location of row in excel file where header is located
<<includeall>> = true/false whether to specify all fields or add a custom one defined in fields, when true it will add all fields as TEXT in db
<<field arrays>>. = when includeall is false, this is where we want to specify what custom header-->db selection we want, add arrays here with the following format
    [<header field name in excel file>, <field name for db table>, <db data type (TEXT/NuMERIC/INT/REAL/BLOB)>, <custom python function to transform, ie. dates>, <custom db function to apply on load>]
<<custom_reader>> = in rare cases where we don't want to use pyexcel or xlrd we can specify a special one here
<<extension>> = extension to scan for in directory, i.e. .xls or .xlsx

Example:

    'ups' : {
        'sheet1' : {
            'table_name': 'ups',
            'header_loc' : 1,
            'include_all' : False,
            'fields' : [
                ['location', 'location', 'TEXT',None, None],
                ['region','region', 'TEXT', None, None],
                ['model','model', 'TEXT', None, None],
                ['purchase date','purchase_date', 'INTEGER',dutil.datetime_to_ordinal, None],
                ['$/unit', 'cost', 'NUMERIC', None, None]

            ]},
        'custom_reader': None,
        'file_type': '.xlsx'

    },



c) run

Once the config file is complete and the excel files are in place you only need to run

python3 run.py

and it will load everything into the db and then prompt you to a sql console!


3) Contact
Author: mattown@gmail.com

