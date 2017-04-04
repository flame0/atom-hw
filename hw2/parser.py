from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def get_dataset(filename):
    '''
    Iterator for dataset's items
    :param filename: Path to dataset's file
    :type filename: str
    :return: Dataset's items
    :raises OSError: if has problem with file
    :raises yaml.YAMLError: if has problem with format
    :raises ValueError: if has problem with content
    '''
    with open(filename, 'rt', encoding='utf-8') as input:
        package = load(input, Loader=Loader)
        dataset = package.get('dataset')
        if not isinstance(dataset, list):
            raise ValueError('wrong format')
        yield from dataset
