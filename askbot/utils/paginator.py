from django.core.paginator import Paginator, Page
from django.core import cache


class PaginatorWithCache(Paginator):

    def __init__ (self, *args, **kwargs):
        super(PaginatorWithCache, self).__init__(*args, **kwargs)
        count = cache.cache.get("paginator_count")
        if count:
            self._count = count

    def _get_count(self):
        "Returns the total number of objects, across all pages."
        if self._count is None:
            try:
                self._count = self.object_list.count()
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
            cache.cache.set("paginator_count", self._count, 300)
        return self._count
    count = property(_get_count)

    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count

        object_list = cache.cache.get("object_list")
        if not object_list:
            object_list = self.object_list[bottom:top]
            cache.cache.set("object_list", object_list, 300)
        return Page(object_list, number, self)