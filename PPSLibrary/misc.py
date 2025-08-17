import typing
import latex2markdown

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
    prefix = '# -*- coding: utf-8 -*-\nimport sys\nt = int(sys.argv[1])\n'
    generators = []
    indexes = []
    idx = []
    generator = '# -*- coding: utf-8 -*-\nimport sys\nt = int(sys.argv[1])\n'
    glen = len(generator)
    for index, test in tests:
        gtxt = f'if t == {index}:\n print({repr(test)}, end="")\n'
        if glen + len(gtxt) > 49 * 1024 * 1024:
            generators.append(generator)
            indexes.append(idx)
            idx = [index]
            generator = prefix + gtxt
            glen = len(generator)
        else:
            generator += gtxt
            idx.append(index)
            glen += len(gtxt)
    if len(idx) > 0:
        generators.append(generator)
        indexes.append(idx)
    
    return generators, indexes

def polygon_tex_to_pps_markdown(
    tex_string : str,
):
    '''
    convert polygon tex to pps markdown
    '''

    result = []
    flag = False

    for line in tex_string.split('\n'):
        if line.startswith('\\Example'):
            flag = True
        elif line.startswith('\\end{example}'):
            flag = False
            continue

        if flag: continue

        if line.startswith('\\begin{problem}'):
            result.append('# 문제')
        elif line.startswith('\\InputFile'):
            result.append('# 입력')
            result.append('')
        elif line.startswith('\\OutputFile'):
            result.append('# 출력')
            result.append('')
        elif line.startswith('\\Note'):
            result.append('# 노트')
            result.append('')
        elif line.startswith('\\end{problem}'):
            result.append('')
            break
        elif line.startswith('\\Interaction'):
            result.append('# 인터랙션')
            result.append('')
        else:
            result.append(line)

    l2m = latex2markdown.LaTeX2Markdown('\n'.join(result))

    return l2m.to_markdown()
