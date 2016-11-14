import os
import py.fieldutils as futil

def basic_csv_parser(dir, path, sheet, model_info):

    # data structs
    output = {}
    data, headers, h_idx = [], [], []

    file = open(path,'r')
    row_num = 1
    for line in file:
        row =line.split(',')
        # get headers
        if row_num == model_info['header_loc']:
            cell_num = 0
            for cell in row:
                val = cell.lower()
                if model_info['include_all']:
                    headers.append(val)
                    h_idx.append(cell_num)
                else:
                    for field_info in model_info['fields']:
                        p_field = futil.process_field(field_info)
                        if p_field['target_field'].lower() in val:
                            headers.append(val)
                            h_idx.append(cell_num)
                cell_num += 1
        # else
        elif row_num > model_info['header_loc']:
            cell_num, c = 0, []
            for cell in row:
                if cell_num in h_idx:
                    c.append(cell)
                cell_num += 1
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