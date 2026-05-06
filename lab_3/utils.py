def write_data(text: bytes, path: str):
    """
    Записывает данные в файл

    Аргументы:
        text: исходный текст
        path: путь для сохранения текста
    """
    with open(path, "wb") as file:
        file.write(text)


def read_text(path: str):
    """
    Считывает текст из файла

    Аргумент:
        path: путь к файлу
    """
    with open(path, "rb") as file:
        return file.read()


def read_encrypted(path: str):
    """
    Считывает зашифрованные данные

    Аргументы:
        path: путь к файлу
    """
    with open(path, "rb") as f:
        iv = f.read(16)
        c_text = f.read()
        return iv, c_text
