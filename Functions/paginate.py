def paginate(objects, page):
    start = 0
    if page:
        page = int(page)
    else:
        page = 1
    start = (page - 1) * 9
    page = 9 * page
    len_ = len(objects)

    if len_ > page:
        objects = objects[start:page]

    elif page > len_ > 10:
        objects = objects[len_ - 9:]
    return objects
