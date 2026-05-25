import math


def paginate_query(query, page=1, limit=20):
    page = max(page, 1)
    limit = max(limit, 1)
    total = query.count()
    total_pages = math.ceil(total / limit) if total > 0 else 0
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()
    return {
        'data': items,
        'meta': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': total_pages,
        },
    }
