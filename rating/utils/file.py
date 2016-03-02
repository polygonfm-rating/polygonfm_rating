import django.utils.encoding


def read_uploaded_file(file):
    lines = dict()
    with file:
        for line in file:
            # TODO think of smth better
            result, s = __try_decode_m(line.strip(), "UTF-8", "cp1251")
            if result and s:
                lines[s] = None

    return lines.keys()


def __try_decode_m(s, *encodings):
    for encoding in encodings:
        result, line = __try_decode(s, encoding)
        if result:
            return True, line
    return False, s


def __try_decode(s, encoding):
    try:
        line = django.utils.encoding.force_text(s, encoding=encoding, strings_only=True)
        return True, line
    except UnicodeDecodeError:
        return False, s