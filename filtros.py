def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **dados):
    if cidade:
        return {
            'cidade': cidade,
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset }

consulta_sem_cidade = """SELECT * FROM hoteis \
                WHERE (estrelas >= ? AND estrelas <= ?) \
                AND (diaria >= ? AND diaria <= ?) \
                LIMIT ? OFFSET ?"""

consulta_com_cidade = """SELECT * FROM hoteis \
                WHERE cidade = ? \
                AND (estrelas >= ? AND estrelas <= ?) \
                AND (diaria >= ? AND diaria <= ?) \
                LIMIT ? OFFSET ?"""