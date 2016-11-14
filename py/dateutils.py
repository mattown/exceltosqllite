import datetime
def datetime_to_ordinal(dt_obj):
    try:
        return int(dt_obj.strftime("%s"))
    except:
        return None


def raritan_ww_convert_date(str):
    str = str.replace("  ", " ").replace("  "," ")
    date_object = datetime.datetime.strptime(str, '%b %d %Y %I:%M%p')
    i = datetime_to_ordinal(date_object)

    return i


#s ='Oct  7 2014  6:17PM'
#print(raritan_ww_convert_date(s))