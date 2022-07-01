def remove_nons(query):
    query_obj = {}
    for key, val in query.items():
        try:
            # if  'NoneType' not in str(type(val))
            query_obj[key] = float(val)
        except:
            pass


    return query_obj