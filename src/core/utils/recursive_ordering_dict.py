def sort_complete_dict(data):
    # 1. Diccionarios: Ordenamos por llaves (Ascendente por defecto)
    if isinstance(data, dict):
        return {
            k: sort_complete_dict(v) 
            for k, v in sorted(data.items())
        }
    
    elif isinstance(data, list):
        if not data:
            return []
        if isinstance(data[0], dict):
            sorted_list = sorted(data, key=lambda x: str(x.get('nombre', '')).upper())
            return [sort_complete_dict(i) for i in sorted_list]
        
        else:
            try:
                return sorted([sort_complete_dict(i) for i in data])
            except TypeError:
                return sorted([sort_complete_dict(i) for i in data], key=str)

    return data