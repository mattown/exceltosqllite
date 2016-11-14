from openpyxl import load_workbook
import os, glob
import py.sql as pysql
from config import excel_config
import py.fieldutils as futil
import xlrd
import datetime


def get_data_xlsm(array_iterator, filter=None, schema=None,override_start_row=None):
    #read rows down
    output = []
    for row in array_iterator:
        c = []
        for cell in row:
            c.append(cell.value)
        output.append(c)
    return output


def get_xlsm(dir, wb, path, sheet, model_info):
    # data structs
    output = {}
    data,headers, h_idx = [], [], []
    wb=wb[sheet]
    row_num = 1
    for row in wb.rows:
        # get headers
        if row_num == model_info['header_loc']:
            cell_num =0
            for cell in row:
                val = str(cell.value).lower().strip()
                if model_info['include_all']:
                    headers.append(val)
                    h_idx.append(cell_num)
                else:
                    for field_info in model_info['fields']:
                        p_field = futil.process_field(field_info)
                        if p_field['target_field'].lower() in val:
                            headers.append(val)
                            h_idx.append(cell_num)
                cell_num+= 1
        # else
        elif row_num > model_info['header_loc']:
            cell_num,c = 0,[]
            for cell in row:
                if cell_num in h_idx:
                    c.append(cell.value)
                cell_num +=1
            data.append(c)
        row_num += 1


    output['h_idx'] = h_idx
    output['headers'] = headers
    output['table_name'] = model_info['table_name']
    output['data'] = data
    output['path'] = path
    output['source'] = os.path.basename(path)
    output['fields'] = model_info['fields']
    return output


def get_xls_val(wb, i,j,dmode, text_override=False):

    if text_override:
        return str(wb.cell_value(i,j))
    else:
        if wb.cell_type(i,j) in [0,6]: # empty
            return None
        elif wb.cell_type(i,j)==1: # Text
            return wb.cell_value(i,j)
        elif wb.cell_type(i,j)==2: # numeric float
            return wb.cell_value(i,j)
        elif wb.cell_type(i,j)==3: # date --> convert to datetime object
            t = xlrd.xldate_as_tuple(wb.cell_value(i,j), dmode)
            return datetime.datetime(t[0],t[1],t[2],t[3], t[4], t[5])
        elif wb.cell_type(i,j)==4: # boolean
            return wb.cell_value(i, j)
        else:
            print("Warning cell error  on row %i, %i cell type %s" % (i,j, wb.cell_type(i,j)))
            return None

def get_xls(dir, wb, path, sheet, model_info):
    # data structs
    output = {}
    data, headers, h_idx = [], [], []

    dmode = wb.datemode
    wb = wb.sheet_by_name(sheet)
    num_cols = wb.ncols
    num_rows = wb.nrows
    for i in range(0, num_rows):
        # get headers
        row_num = i+1
        if row_num == model_info['header_loc']:
            for j in range(0, num_cols):
                val = get_xls_val(wb, i, j,dmode, text_override=True)
                if model_info['include_all']:
                    headers.append(val)
                    h_idx.append(j)
                else:
                    for field_info in model_info['fields']:
                        p_field = futil.process_field(field_info)
                        if p_field['target_field'].lower() in val.lower():
                            headers.append(val)
                            h_idx.append(j)

        # else
        elif row_num > model_info['header_loc']:
            c= []
            for j in range(0, num_cols):
                if j in h_idx:
                    val = get_xls_val(wb, i, j, dmode)
                    c.append(val)
            data.append(c)



    output['h_idx'] = h_idx
    output['headers'] = headers
    output['table_name'] = model_info['table_name']
    output['data'] = data
    output['path'] = path
    output['source'] = os.path.basename(path)
    output['fields'] = model_info['fields']
    #print("headers", output['headers'], output['h_idx'])
    #print(output['data'])
    return output


def write_to_db(db_write_obj):
    pysql.write_obj(db_write_obj)


def load_file_to_memory_disk(dir, path):
    db_memory_objs = []# this contains a list of dictionary that has necessary info for each db table
    file_type = excel_config[dir]['file_type']
    # custom loader
    if excel_config[dir]['custom_reader']:
        custom_reader = excel_config[dir]['custom_reader']
        for key in excel_config[dir].keys():
            if key not in ['custom_reader', 'file_type']:
                print("MEMORY LOAD ATTEMPT FILE: %s CONFIG: %s SHEET CONFIG KEY: %s" % (path, dir, key))
                model_info = excel_config[dir][key]
                sheet=key
                db_memory_obj = custom_reader(dir,path,sheet, model_info)
                print("LOADED INTO MEMORY: WRITING TO DB NOW")
                write_to_db(db_memory_obj)
    #normal xls, xlsx parsers
    else:
        if file_type in ['.xlsx']:
            wb = load_workbook(path, data_only=True, read_only=True)
            for sheet in wb.get_sheet_names():
                for key in excel_config[dir].keys():
                    if key not in ['custom_reader','file_type']:
                        if key.lower() in sheet.lower():
                            print("MEMORY LOAD ATTEMPT FILE: %s CONFIG: %s SHEET CONFIG KEY: %s" % (path, dir, key))
                            model_info = excel_config[dir][key]
                            db_memory_obj = get_xlsm(dir,wb,path,sheet, model_info)
                            print("LOADED INTO MEMORY: WRITING TO DB NOW")
                            write_to_db(db_memory_obj)

        elif file_type in ['.xls']:
            wb =  xlrd.open_workbook(path, on_demand=True)
            for sheet in wb.sheet_names():
                for key in excel_config[dir].keys():
                    if key not in ['custom_reader', 'file_type']:
                        if key.lower() in sheet.lower():
                            print("MEMORY LOAD ATTEMPT FILE: %s CONFIG: %s SHEET CONFIG KEY: %s" % (path, dir, key))
                            model_info = excel_config[dir][key]
                            db_memory_obj = get_xls(dir, wb, path, sheet, model_info)
                            print("LOADED INTO MEMORY: WRITING TO DB NOW")
                            write_to_db(db_memory_obj)



def load_config(dir):
    file_type = excel_config[dir]['file_type']
    files = glob.glob(os.path.join('data',dir,'*%s' % file_type))
    for file in files:
        load_file_to_memory_disk(dir, file)

def load_all_db():
    for dir in excel_config.keys():
        load_config(dir)


def write_table_to_tab(table_name):
    print("writing %s to disk" % table_name)
    pysql.write_table(table_name)