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
    generator = '# -*- coding: utf-8 -*-\nimport sys\nt = int(sys.argv[1])\n'
    for index, test in tests:
        generator += f'if t == {index}:\n print({repr(test)}, end="")\n'
    return generator

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
        else:
            result.append(line)

    l2m = latex2markdown.LaTeX2Markdown('\n'.join(result))

    return l2m.to_markdown()
