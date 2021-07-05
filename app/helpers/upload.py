ALLOWED_IMG_EXTENSIONS = [
    "png",
    "jpg",
    "jpeg",
    "svg",
    "webp",
    "gif"
]


def allowed_file(filename, allowed):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed
