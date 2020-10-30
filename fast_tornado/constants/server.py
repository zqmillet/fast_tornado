DOCUMENT_SCHEMA = '''
type: dict
properties:
    description:
        type: str
    methods:
        type: list
        items:
            type: str
            enumeration: [get, post, patch, options, delete, put]
        minimum_length: 1
    api_path:
        type: str
    arguments:
        type: list
        items:
            type: dict
            properties:
                type:
                    type: str
                from:
                    type: str
                    enumeration: [query, path, body, header, entire_body]
    return:
        type: dict
        properties:
            type:
                type: str
'''
