import typing

def compress_str(
    message : str,
    length : int = 200
):
    '''
    compress string to length
    '''
    if len(message) > length:
        return message[:length] + '...'
    return message

def make_manual_generator(
    tests : typing.List[typing.Tuple[int, str]],
):
    '''
    make manual data generator
    '''
    generator = '# -*- coding: utf-8 -*-\nimport sys\nt = int(sys.argv[1])\n'
    for index, test in tests:
        generator += f'if t == {index}:\n print({repr(test)}, end="")\n'
    return generator
