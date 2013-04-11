from django.http import Http404

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
    )


def paginate(query_set, page, per_page=10):
    if page is None:
        page = 1
    paginator = Paginator(query_set, per_page)
    try:
        records = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        raise Http404
    return records