class PPSError(Exception):
    pass

class PPSFileNotFoundError(PPSError):
    pass

class PPSFileExistsError(PPSError):
    pass

class PPSPolygonConfigParseError(PPSError):
    pass