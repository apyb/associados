

def get_all_field_names(model):
    return [f.name for f in model._meta.get_fields()]


def response_string(response):
    """Converte o conteúdo de um HTTPResponse para String"""
    return response.content.decode(response.charset)
