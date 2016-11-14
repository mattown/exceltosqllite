def process_field(fields):
    return {
        'target_field' : str(fields[0]),
        'sql_field' : str(fields[1]),
        'field_type': str(fields[2]),
        'python_f': fields[3],
        'sql_f': fields[4]
    }