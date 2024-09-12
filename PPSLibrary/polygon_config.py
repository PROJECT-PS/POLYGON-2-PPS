import json
import typing
import xml.etree.ElementTree as ET

from pathlib import Path

from .constant import *
from .error import (
    PPSPolygonConfigParseError,
)
from .misc import (
    compress_str,
)
from .mapper import (
    convert_solution_tag,
    convert_solution_type,
)
from .filesystem import (
    FileSystem,
)

class PolygonConfig:
    def __init__(self):
        self.problem_title = ''
        self.input_path_pattern = ''
        self.output_path_pattern = ''
        self.time_limit = POLYGON_CONFIG_DEFAULT_TIME_LIMIT
        self.memory_limit = POLYGON_CONFIG_DEFAULT_MEMORY_LIMIT
        self.test_count = POLYGON_CONFIG_DEFAULT_TEST_COUNT
        self.generator_custom_manual_count = 0
        self.test_count = 0
        self.generator_custom_manuals = []
        self.statements = []
        self.tests = []
        self.groups = []
        self.executables = []
        self.checker = {}
        self.validators = []
        self.solutions = []
        self.generators = []
    
    def generate_pps_json_config(self):
        '''
        generate pps json config
        '''
        config = {
            'problem_title': self.problem_title,
            'problem_type': 'stdio',
            'checker': self.checker['name'],
            'checker_language': self.checker['type'],
            'validator': self.validators[0]['name'] if len(self.validators) > 0 else '',
            'validator_language': self.validators[0]['type'] if len(self.validators) > 0 else '',
            'subtask': True if len(self.groups) > 0 else False,
            'limits': {
                'time': self.time_limit,
                'memory': self.memory_limit,
                'factor': {},
            },
            'enable_language': [],
            'statements': [
                {
                    'name': statement['name'],
                    'label': statement['language'],
                } for statement in self.statements
            ],
            'solutions': [
                {
                    'name': solution['name'],
                    'language': solution['type'],
                    'type': solution['tag'],
                } for solution in self.solutions
            ],
            'generators': [
                {
                    'name': generator['name'],
                    'language': generator['type'],
                    'alias': FileSystem.remove_extension(generator['name']),
                } for generator in self.generators
            ] + [
                {
                    'name': '__pps_generator.py',
                    'language': 'py3',
                    'alias': '__pps_generator',
                },
            ],
            'subtask_group': [
                {
                    'name': group['name'],
                    'description': group['description'],
                    'score': group['score'],
                } for group in self.groups
            ],
            'genscript': [
                {
                    'script': test['genscript'],
                    'subtask_group': test['subtask_group'],
                    'description': test['description'],
                    'is_example': test['is_example'],
                    'only_deploy': False,
                } for test in self.tests
            ],
            'versions': {
                'config': 1,
                'repository': 1,
            },
        }
        return json.dumps(config, ensure_ascii=False, indent=4)

    def parse_config_file(
        self,
        config_file_path : typing.Union[str, Path],
    ):
        '''
        parse polygon config file for pps package
        '''
        print('Parsing polygon config file...\n')
        tree = ET.parse(config_file_path)
        root = tree.getroot()
        
        def recursive_find(path : str):
            '''
            find xml element recursively
            '''
            spt = path.split('.')
            node = root
            for word in spt:
                node = node.find(word)
                if node is None:
                    return None
            return node
        def parse(node, default_value):
            '''
            parse xml element to string
            '''
            if node is None:
                return default_value
            return node.text
        
        # parse polygon config file

        # parse problem title & language
        node = recursive_find(POLYGON_CONFIG_PROBLEM_TITLE)
        if node is not None:
            attrib = node.attrib
            self.problem_title = attrib.get('value', '')

        # parse time limit
        node = recursive_find(POLYGON_CONFIG_TIME_LIMIT)
        self.time_limit = int(parse(node, POLYGON_CONFIG_DEFAULT_TIME_LIMIT))

        # parse memory limit
        node = recursive_find(POLYGON_CONFIG_MEMORY_LIMIT)
        self.memory_limit = int(parse(node, POLYGON_CONFIG_DEFAULT_MEMORY_LIMIT))

        # parse test count
        node = recursive_find(POLYGON_CONFIG_TEST_COUNT)
        self.test_count = int(parse(node, POLYGON_CONFIG_DEFAULT_TEST_COUNT))

        # parse input path pattern
        node = recursive_find(POLYGON_CONFIG_INPUT_PATH_PATTERN)
        self.input_path_pattern = parse(node, '')

        # parse output path pattern
        node = recursive_find(POLYGON_CONFIG_OUTPUT_PATH_PATTERN)
        self.output_path_pattern = parse(node, '')

        # parse statements
        node = recursive_find(POLYGON_CONFIG_STATEMENTS)
        if node is not None:
            lang_map = {
                "korean": "한국어",
                "english": "English"
            }

            # parse statement
            for statement in node.findall(POLYGON_CONFIG_STATEMENT):
                attrib = statement.attrib
                # skip not tex statement
                if attrib.get('type', '') != POLYGON_CONFIG_STATEMENT_TEX_TYPE: continue
                self.statements.append({
                    'path': attrib.get('path', ''),
                    'name': FileSystem.get_filename(attrib.get('path', '')),
                    'type': attrib.get('type', ''),
                    'language': attrib.get('language', ''),
                })
                if self.statements[-1]['name'].endswith('.tex'): # change extension to md
                    self.statements[-1]['name'] = FileSystem.remove_extension(self.statements[-1]['name']) + '.md'
                if self.statements[-1]['language'] in lang_map: # change language to pps language
                    self.statements[-1]['language'] = lang_map[self.statements[-1]['language']]

        # parse tests
        used_generator = {}
        node = recursive_find(POLYGON_CONFIG_TESTS)
        if node is not None:
            # parse test
            test_index = 0
            for test in node.findall(POLYGON_CONFIG_TEST):
                testObj = {}
                method = test.attrib.get(POLYGON_CONFIG_GENERATOR_METHOD)
                testObj['is_example'] = bool(test.attrib.get(POLYGON_CONFIG_GENERATOR_IS_EXAMPLE, False))
                testObj['description'] = str(test.attrib.get(POLYGON_CONFIG_GENERATOR_DESCRIPTION, ''))
                testObj['subtask_group'] = str(test.attrib.get(POLYGON_CONFIG_TEST_GROUP, ''))
                if method == POLYGON_CONFIG_GENERATOR_METHOD_MANUAL: # data generated from manually
                    testObj['genscript'] = POLYGON_CONFIG_PPS_CUSTROM_MANUAL_GENERATOR + ' ' + str(self.generator_custom_manual_count)
                    testObj['test_index'] = test_index
                    self.generator_custom_manuals.append(testObj)
                    self.generator_custom_manual_count += 1
                elif method == POLYGON_CONFIG_GENERATOR_METHOD_GENERATED: # data generated from generator
                    testObj['genscript'] = test.attrib.get(POLYGON_CONFIG_GENERATOR_GENSCRIPT, '')
                    used_generator[testObj['genscript'].split(' ')[0]] = True
                else: # unknown method
                    raise PPSPolygonConfigParseError('Unknown Generator Method')
                self.tests.append(testObj)
                test_index += 1
        else: # no tests
            raise PPSPolygonConfigParseError('No Tests')
        
        # parse groups
        node = recursive_find(POLYGON_CONFIG_GROUPS)
        if node is not None:
            # parse group
            for group in node.findall(POLYGON_CONFIG_GROUP):
                groupObj = {}
                groupObj['name'] = str(group.attrib.get('name', ''))
                groupObj['description'] = ''
                groupObj['score'] = 0
                self.groups.append(groupObj)

        # parse executables
        node = recursive_find(POLYGON_CONFIG_EXECUTABLES)
        if node is not None:
            # parse executable
            for executable in node.findall(POLYGON_CONFIG_EXECUTABLE):
                attrib = executable.find(POLYGON_CONFIG_EXECUTABLE_SOURCE).attrib
                execObj = {}
                execObj['path'] = attrib.get('path', '')
                execObj['name'] = FileSystem.get_filename(attrib.get('path', ''))
                execObj['alias'] = FileSystem.remove_extension(execObj['name'])
                execObj['type'] = convert_solution_type(attrib.get('type', ''))
                self.executables.append(execObj)
                if execObj['alias'] in used_generator:
                    self.generators.append(execObj)
        
        # parse checker
        node = recursive_find(POLYGON_CONFIG_CHECKER)
        attrib = node.attrib
        self.checker = {
            'path': attrib.get('path', ''),
            'name': FileSystem.get_filename(attrib.get('path', '')),
            'type': convert_solution_type(attrib.get('type', '')),
        }

        # parse validators
        node = recursive_find(POLYGON_CONFIG_VALIDATORS)
        if node is not None:
            # parse validator
            for validator in node.findall(POLYGON_CONFIG_VALIDATOR):
                attrib = validator.find(POLYGON_CONFIG_VALIDATOR_SOURCE).attrib
                validObj = {}
                validObj['path'] = attrib.get('path', '')
                validObj['name'] = FileSystem.get_filename(attrib.get('path', ''))
                validObj['type'] = convert_solution_type(attrib.get('type', ''))
                self.validators.append(validObj)
        
        # parse solutions
        node = recursive_find(POLYGON_CONFIG_SOLUTIONS)
        if node is not None:
            # parse solution
            for solution in node.findall(POLYGON_CONFIG_SOLUTION):
                attrib = solution.find(POLYGON_CONFIG_SOLUTION_SOURCE).attrib
                solObj = {}
                solObj['tag'] = convert_solution_tag(solution.attrib.get('tag', ''))
                solObj['path'] = attrib.get('path', '')
                solObj['name'] = FileSystem.get_filename(attrib.get('path', ''))
                solObj['type'] = convert_solution_type(attrib.get('type', ''))
                self.solutions.append(solObj)

        print('[PARSED] problem title:', self.problem_title)
        print('[PARSED] time limit:', self.time_limit)
        print('[PARSED] memory limit:', self.memory_limit, '- MiB:', self.memory_limit / 1024 / 1024)
        print('[PARSED] test count:', self.test_count)
        print('[PARSED] generator custom manual count:', self.generator_custom_manual_count)
        print('[PARSED] statements:', compress_str(str(self.statements)))
        print('[PARSED] generator custom manuals:', compress_str(str(self.generator_custom_manuals)))
        print('[PARSED] tests:', compress_str(str(self.tests)))
        print('[PARSED] groups:', compress_str(str(self.groups)))
        print('[PARSED] executables:', compress_str(str(self.executables)))
        print('[PARSED] checker:', compress_str(str(self.checker)))
        print('[PARSED] validators:', compress_str(str(self.validators)))
        print('[PARSED] solutions:', compress_str(str(self.solutions)))
        print('[PARSED] generators:', compress_str(str(self.generators)))
        print()