from models.filter.base_filter import Filter
from boolean_query_parser import parse_query, apply_query

class QueryStringFilter(Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qs = ''
        self.query = parse_query('test')
    

    def infer(self, string) -> bool:
        return apply_query(self.query,string)

    # specific replacement for train
    def set_qs(self,qs):
        self.qs = qs
        self.query = parse_query(qs)

