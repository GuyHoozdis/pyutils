from six import iteritems

# !!!: I'm still working on this idea, it's not fully realized yet.
# The goals are:
# - Turn a dict (or loaded JSON data) into an object with attribute access,
#   instead of item access, semantics.
# - Turn a mutable data structure into an immutable one.
#   - Did I see a freeze module - or maybe that was in React
#   - Does FrozenDict exist?
#   - Would implmeneting a collections.Mapping interface, implementing the
#     attribute access there, be a better approach.
#
# Current Issues:
# - For deeply nested objects, it ends up being the original object that is
#   modified; that is, the nested object nested in the original data structure
#   is modified.  The root object was not modified.
# - The handler/dispatch pattern I love wasn't working as well as I expected. I
#   broke it out for some easier debugging, but I feel like that is an
#   indication that the it is a bad pattern for this scenario.
def freeze_document(document):
    """Convert a dict object into a namedtuple object with attributes
    """
    def list_handler(document):
        return [freeze_document(element) for element in document]

    def dict_handler(document):
        sorted_elements = sorted(iteritems(document))
        for attribute, subdocument in sorted_elements:
            document[attribute] = freeze_document(subdocument)
        return namedtuple(
            'FrozenDocument',
            [element[0] for element in sorted_elements]
        )(**document)

    import operator, collections
    ifaces = operator.attrgetter('MutableMapping', 'MutableSequence')
    if not isinstance(document, ifaces(collections)):
        return document

    # TODO: Collapse this again, or replace with a pattern that is more
    # appropriate.
    dispatch = {
        list: list_handler,
        dict: dict_handler,
        VenueCustomerDocument: dict_handler,
    }
    handler = dispatch[type(document)]
    result = handler(document)
    return result



