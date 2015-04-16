import logging

log = logging.getLogger('base')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

def set_handler(handler_class, args):
    handler = handler_class(*args)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    log.addHandler(handler)

def set_null_handler():
    set_handler(logging.NullHandler, [])

def set_console_handler():
    set_handler(logging.StreamHandler, [])
    
def set_file_handler(*args):
    set_handler(logging.FileHandler, args)

set_null_handler()