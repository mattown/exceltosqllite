import os
import py.dateutils as dutil
import py.customparsers as cparsers
#
#
#
#
#
#fields logic
#
#
#index 1
# name of field header
#
#index 2
# name in target table
#
#
#index 3
# TEXT
# NUMERIC
# INTEGER
# REAL
# BLOB
#
#index 4
# python normalization function
#
#index 5
# sql lite function

output_config = {
    'delimiter' : '\t',
    'null_type' : None,
    'new_line' : '\n'
}

hard_coded_fields = ['source','path']

db_dir = os.path.join(os.getcwd(),'sqllitedb','db.dat')

excel_config = {

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

    'raritan' : {

        'reseller' :{
            'table_name': 'raritan_reseller',
            'header_loc': 18,
            'include_all': False,
            'fields': [
                ['location', 'location', 'TEXT', None, None],
                ['region', 'region', 'TEXT', None, None],
                ['Contactpart', 'model', 'TEXT', None, None],
                ['purchase', 'purchase_date', 'INTEGER', dutil.datetime_to_ordinal, None],
                ['$/unit', 'cost', 'NUMERIC', None, None]
            ]},
        #,

        'end-user': {
            'table_name': 'raritan_end_user',
            'header_loc': 18,
            'include_all': False,
            'fields': [
                ['location', 'location', 'TEXT', None, None],
                ['region', 'region', 'TEXT', None, None],
                ['part', 'model', 'TEXT', None, None],
                ['purchase', 'purchase_date', 'INTEGER', dutil.datetime_to_ordinal, None],
                ['$/unit', 'cost', 'NUMERIC', None, None]
            ]},
        'custom_reader': None,
        'file_type': '.xls'

    },

    'gso' : {
        'sheet1': {
            'table_name': 'gso',
            'header_loc': 1,
            'include_all': False,
            'fields': [
                ['location', 'location', 'TEXT', None, None],
                ['region', 'region', 'TEXT', None, None],
                ['model', 'model', 'TEXT', None, None],
                ['purchase', 'purchase_date', 'INTEGER', None, None],
                ['$/unit', 'cost', 'NUMERIC', None, None]
            ]},
        'custom_reader': None,
        'file_type': '.xlsx'

    },

    'raritan_ww': {
        'devices': {
            'table_name' : 'raritan_ww',
            'header_loc': 1,
            'include_all': False,
            'fields': [
                ['location', 'location', 'TEXT', None, None],
                ['SiteName', 'region', 'TEXT', None, None],
                ['MfgProdNo', 'model', 'TEXT', None, None],
                ['Installation', 'purchase_date', 'INTEGER', dutil.raritan_ww_convert_date, None],
                ['$/unit', 'cost', 'NUMERIC', None, None]
            ]},
        'custom_reader': None,
        'file_type' : '.xlsx'

    },

    'pdus': {
        'pdus_data': {
            'table_name': 'pdus',
            'header_loc': 1,
            'include_all': False,
            'fields': [
                ['location', 'location', 'TEXT', None, None],
                ['region', 'region', 'TEXT', None, None],
                ['Model', 'model', 'TEXT', None, None],
                ['purchase_date', 'purchase_date', 'INTEGER', None, None],
                ['$/unit', 'cost', 'NUMERIC', None, None]
            ]},
        'custom_reader': cparsers.basic_csv_parser,
        'file_type': '.csv'

    }


}
