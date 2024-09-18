from pathlib import Path

from .constant import *
from .filesystem import FileSystem
from .misc import make_manual_generator, polygon_tex_to_pps_markdown
from .polygon_config import PolygonConfig

class PPSCore:
    def __init__(
        self,
        source_path : str,
        destination_path : str,
    ):
        '''
        pps core initialize function
        '''
        self.source_path = Path(source_path)
        self.destination_path = Path(destination_path)
        self.fs = FileSystem()
        self.polygon_config = PolygonConfig()

    def run(self):
        '''
        pipeline for makeing pps package from polygon package
        '''
        self.prepare() # preparing for making pps package
        self.generate_pps_config() # making config file
        self.copy_files() # copying files
        self.make_pps_custom_generator() # making pps custom generator if needed

    def prepare(self):
        '''
        preparing for making pps package
        '''
        print('Generate pps package directories\n')
        # make destination directory
        self.fs.create_directory(self.destination_path)

        # make pps package subdirectories
        self.fs.create_directory(self.destination_path / PPS_FS_STATEMENT_PATH)
        self.fs.create_directory(self.destination_path / PPS_FS_CHECKER_PATH)
        self.fs.create_directory(self.destination_path / PPS_FS_GENERATOR_PATH)
        self.fs.create_directory(self.destination_path / PPS_FS_SOLUTION_PATH)
        self.fs.create_directory(self.destination_path / PPS_FS_VALIDATOR_PATH)

        # parse polygon package config file
        self.polygon_config.parse_config_file(self.source_path / POLYGON_CONFIG_FILE_NAME)
    
    def generate_pps_config(self):
        '''
        generate pps package config file
        '''
        print('Generate pps package config file...\n')
        # generate pps package config file
        config = self.polygon_config.generate_pps_json_config()
        if self.fs.is_exists(self.destination_path / PPS_FS_CONFIG_NAME):
            self.fs.delete_file(self.destination_path / PPS_FS_CONFIG_NAME)
        self.fs.create_file(self.destination_path / PPS_FS_CONFIG_NAME)
        self.fs.set_file_data(self.destination_path / PPS_FS_CONFIG_NAME, config)

    def copy_files(self):
        '''
        copy files from polygon package to pps package
        '''
        print('Copy files from polygon package to pps package...\n')

        # copy statement files
        for statement in self.polygon_config.statements:
            src = self.source_path / statement['path']
            dest = self.destination_path / PPS_FS_STATEMENT_PATH / statement['name']
            if self.fs.is_exists(dest):
                self.fs.delete_file(dest)
            self.fs.copy_file(src, dest)

            # convert latex to markdown
            statement_tex = self.fs.get_file_data(dest)
            statement_md = polygon_tex_to_pps_markdown(statement_tex)
            self.fs.set_file_data(dest, statement_md)

        # copy checker files
        src = self.source_path / self.polygon_config.checker['path']
        dest = self.destination_path / PPS_FS_CHECKER_PATH / self.polygon_config.checker['name']
        if self.fs.is_exists(dest):
            self.fs.delete_file(dest)
        self.fs.copy_file(src, dest)

        # copy generators
        for generator in self.polygon_config.generators:
            src = self.source_path / generator['path']
            dest = self.destination_path / PPS_FS_GENERATOR_PATH / generator['name']
            if self.fs.is_exists(dest):
                self.fs.delete_file(dest)
            self.fs.copy_file(src, dest)
        
        # copy solutions
        for solution in self.polygon_config.solutions:
            src = self.source_path / solution['path']
            dest = self.destination_path / PPS_FS_SOLUTION_PATH / solution['name']
            if self.fs.is_exists(dest):
                self.fs.delete_file(dest)
            self.fs.copy_file(src, dest)
        
        # copy validators
        for validator in self.polygon_config.validators:
            src = self.source_path / validator['path']
            dest = self.destination_path / PPS_FS_VALIDATOR_PATH / validator['name']
            if self.fs.is_exists(dest):
                self.fs.delete_file(dest)
            self.fs.copy_file(src, dest)

    def make_pps_custom_generator(self):
        '''
        make pps custom generator if needed
        '''
        if self.polygon_config.generator_custom_manual_count < 1:
            print('No custom generator needed\n')
            return
        
        print('Make pps custom generator...\n')

        tests = []

        # parse manual test case
        for index, manual in enumerate(self.polygon_config.generator_custom_manuals):
            pattern = manual['input_path_pattern']
            real_index = manual['real_index']
            test_data = self.fs.get_file_data(
                self.source_path / (pattern % real_index)
            )
            tests.append((index, test_data))
            

        # make pps custom generator
        if self.fs.is_exists(self.destination_path / PPS_FS_GENERATOR_PATH / '__pps_generator.py'):
            self.fs.delete_file(self.destination_path / PPS_FS_GENERATOR_PATH / '__pps_generator.py')
        self.fs.create_file(self.destination_path / PPS_FS_GENERATOR_PATH / '__pps_generator.py')
        self.fs.set_file_data(
            self.destination_path / PPS_FS_GENERATOR_PATH / '__pps_generator.py',
            make_manual_generator(tests),
        )
