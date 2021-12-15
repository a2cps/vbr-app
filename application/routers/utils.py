import re
from collections import namedtuple
from typing import Any, Dict, List, NamedTuple, NoReturn, Tuple, Union

ParameterValue = Union[str, int, bool, float]
SearchParameter = namedtuple("SearchParameter", ["operator", "value"])
DEFAULT_OPERATOR = "eq"
OPERATOR_RE = re.compile("^(!\*|!|=|>=|<=|<|>|\*)|(\*)$")
# See https://tapis.readthedocs.io/en/latest/technical/pgrest.html?highlight=search#retrieving-rows-with-search-parameters
MAPPINGS = {
    "=": "eq",
    "!": "neq",
    "<": "lt",
    ">": "gt",
    "<=": "lte",
    ">=": "gte",
    "*": "like",
    "!*": "nlike",
}

__all__ = [
    "ParameterValue",
    "SearchParameter",
    "parameter_to_search_parameter",
    "parameters_to_query",
]


def parameter_to_search_parameter(param_text: ParameterValue) -> SearchParameter:
    """Transform a search parameter value into a tuple of operator/value tuple"""
    str_param_text = str(param_text)
    operator_match = OPERATOR_RE.search(str_param_text)
    if operator_match:
        operator = MAPPINGS.get(operator_match[0], "eq")
        if operator not in ("like", "nlike"):
            replacement_text = ""
        else:
            replacement_text = "%"
        for m in operator_match.groups()[1:]:
            str_param_text = OPERATOR_RE.sub(replacement_text, str_param_text)
    else:
        operator = "eq"
    return SearchParameter(operator, str_param_text)


def parameters_to_query(**kwargs) -> Dict:
    """Transforms a set of keyword arguments into a query <dict>."""
    data = {}
    for k, v in kwargs.items():
        if v is not None:
            sp = parameter_to_search_parameter(v)
            data[k] = {"operator": sp.operator, "value": sp.value}
    return data
