"""
"""
import decimal
import json

from os import makedirs, path
from functools import partial


class DecimalEncoder(json.JSONEncoder):

    #def __init__(self, *args, **kwargs):
    #    super(DecimalEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        decoder = super(DecimalEncoder, self).default
        decoder = str if isinstance(obj, decimal.Decimal) else decoder
        return decoder(obj)


def dump_docs(left, right, outdir='.', **kwargs):
    """Dump two JSON objects so that then can be compared

    When dealing with large objects it can be difficult to see the difference
    between two similar versions.  This utility method helps prepare those
    docs to be compared.

    The output files will be named `left.json` and `right.json`, respectively,
    in the `outdir` that you specify.  If you wish to control the file names
    you can provide a mapping to the filenames to be used.

    >>> dump_docs(doc1, doc2, filenames={'left': 'one.json', right: 'two.json'})

    If you specify create=True, then the method will create outdir if it does
    not already exist.  Setting overwrite=True will overwrite files if they
    already exist.  Both of these are set to False by default and will raise
    an exception.

    >>> dump_docs(doc1, doc2, outdir='/tmp/project/component', create=True)
    """
    # Get user specified configuration or defaults
    create = kwargs.pop('create', False)
    user_provided_filenames = kwargs.pop('filenames', {})
    decimal_data_handler = kwargs.pop('decimal', {})
    encoder = decimal_data_handler.get('encoder', DecimalEncoder)
    precision = decimal_data_handler.get('precision', 0)
    decimal.getcontext().prec = precision
    common_kwargs = dict(
        indent=2, sort_keys=True, separators=(',', ': '), cls=encoder,
    )

    # Prepare output location
    filenames = {'left': 'left.json', 'right': 'right.json'}
    filenames.update(user_provided_filenames)
    if not path.isdir(outdir) and not create:
        raise IOError("No such file or directory: '%s'", outdir)
    elif not path.isdir(outdir) and create:
        os.makedirs(outdir)

    outfile = partial(path.join, path.abspath(outdir))
    with open(outfile(filenames['left']), 'w') as fp:
        json.dump(left, fp, **common_kwargs)
    with open(outfile(filenames['right']), 'w') as fp:
        json.dump(right, fp, **common_kwargs)

