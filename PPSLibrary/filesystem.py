import os
import typing
import shutil
import threading

from pathlib import Path
from .error import (
    PPSFileNotFoundError,
    PPSFileExistsError,
)

def thread_safe(fn):
    '''
    make function thread safe
    '''
    def f(self, *args, **kwargs):
        with self.semaphore:
            return fn(self, *args, **kwargs)
    return f

class FileSystem:
    '''
    custom file system class
    '''
    def __init__(self):
        self.semaphore = threading.BoundedSemaphore(1)

    @thread_safe
    def create_directory(
        self,
        dir_path: typing.Union[str, Path],
    ):
        '''
        create directory
        '''
        dir_path = Path(dir_path).resolve()
        dir_path.mkdir(parents=True, exist_ok=True)
    
    @thread_safe
    def create_file(
        self,
        file_path: typing.Union[str, Path],
    ):
        '''
        create empty file
        '''
        file_path = Path(file_path).resolve()
        if file_path.exists() and file_path.is_file():
            raise PPSFileExistsError
        file_path.touch()
    
    @thread_safe
    def copy_file(
        self,
        sourcePath : typing.Union[str, Path],
        destinationPath : typing.Union[str, Path],
    ):
        '''
        copy file from source to destination
        '''
        sourcePath = Path(sourcePath).resolve()
        destinationPath = Path(destinationPath).resolve()
        if not sourcePath.exists() or not sourcePath.is_file():
            raise PPSFileNotFoundError
        if destinationPath.exists() and destinationPath.is_file():
            raise PPSFileExistsError
        shutil.copyfile(sourcePath, destinationPath)
    
    @thread_safe
    def get_file_data(
        self,
        file_path: typing.Union[str, Path],
    ):
        '''
        get file data from path
        '''
        file_path = Path(file_path).resolve()
        if not file_path.exists() or not file_path.is_file():
            raise PPSFileNotFoundError
        with open(file_path, 'r') as f:
            return f.read()
        
    @thread_safe
    def set_file_data(
        self,
        file_path: typing.Union[str, Path],
        data: str,
    ):
        '''
        set file data from path
        '''
        file_path = Path(file_path).resolve()
        if not file_path.exists() or not file_path.is_file():
            raise PPSFileNotFoundError
        with open(file_path, 'w') as f:
            return f.write(data)
    
    @thread_safe
    def delete_file(
        self,
        file_path: typing.Union[str, Path],
    ):
        '''
        delete file from path
        '''
        file_path = Path(file_path).resolve()
        if not file_path.exists() or not file_path.is_file():
            raise PPSFileNotFoundError
        os.remove(file_path)

    @thread_safe
    def delete_directory(
        self,
        dir_path: typing.Union[str, Path],
    ):
        '''
        delete directory from path
        '''
        dir_path = Path(dir_path).resolve()
        if not dir_path.exists() or not dir_path.is_dir():
            raise PPSFileNotFoundError
        shutil.rmtree(dir_path)
    
    @thread_safe
    def is_exists(
        self,
        path: typing.Union[str, Path],
    ):
        '''
        check if path exists
        '''
        path = Path(path).resolve()
        return path.exists()
    
    @staticmethod
    def get_basepath(
        file_path: typing.Union[str, Path],
    ):
        '''
        get base path of file
        '''
        file_path = Path(file_path).resolve()
        return file_path.parent
    
    @staticmethod
    def get_filename(
        file_path: typing.Union[str, Path],
    ):
        '''
        get filename from path
        '''
        file_path = Path(file_path)
        return file_path.name
    
    @staticmethod
    def remove_extension(
        filename: str,
    ):
        '''
        remove extension from filename
        '''
        return '.'.join(filename.split('.')[:-1])