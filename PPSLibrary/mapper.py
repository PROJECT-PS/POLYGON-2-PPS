_solution_type = {
    'c.gcc':                        'c99',
    'cpp.g++11':                    'cpp11',
    'cpp.g++14':                    'cpp17',
    'cpp.g++17':                    'cpp17',
    'cpp.ms2017':                   'cpp17',
    'cpp.msys2-mingw64-9-g++17':    'cpp17',
    'cpp.gcc13-64-winlibs-g++20':   'cpp17',
    'cpp.gcc14-64-msys2-g++23':     'cpp17',
    'java21':                       'java8',
    'java11':                       'java8',
    'java8':                        'java8',
    'python.3':                     'py3',
    'python.pypy3':                 'pypy3',
    'python.pypy3-64':              'pypy3',
}

_solution_tag = {
    'main': 'MCS',
    'accepted': 'AC',
    'rejected': 'WA/TLE/MLE/FAIL',
    'time-limit-exceeded-or-accepted': 'AC/TLE',
    'wrong-answer': 'WA',
    'failed': 'FAIL',
    'memory-limit-exceeded': 'MLE',
    'presentation-error': 'WA',
    'time-limit-exceeded': 'TLE',
    'time-limit-exceeded-or-memory-limit-exceeded': 'TLE/MLE',
}

def convert_solution_type(type : str, default_value : str = ''):
    '''
    convert solution type from polygon to pps
    '''
    type = type.lower()
    if type in _solution_type:
        return _solution_type[type]
    return default_value

def convert_solution_tag(tag : str, default_value : str = ''):
    '''
    convert solution tag from polygon to pps
    '''
    tag = tag.lower()
    if tag in _solution_tag:
        return _solution_tag[tag]
    return default_value