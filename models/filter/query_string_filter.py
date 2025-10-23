from models.filter.base_filter import Filter
from boolean_query_parser import parse_query, apply_query


class QueryStringFilter(Filter):
    def __init__(self, qs):
        self.qs = qs
        self.query = parse_query(qs)

    def infer(self, document) -> bool:
        return apply_query(self.query, document.text)
