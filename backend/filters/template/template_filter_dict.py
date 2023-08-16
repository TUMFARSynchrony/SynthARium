from filters.filter_dict import FilterDict


# Add or delete this, depending on filters needs
class TemplateFilterDict(FilterDict):
    """TypedDict for template filter.

    Attributes
    ----------
    type : str
        filter type (unique identifier / name)
    id : str
        Filter id.  Empty string if adding a new filter.  Read only for client.
    size : int
        Example value for template
    """

    direction: str
    size: int
