def write_data(text: bytes, path: str):
    """
    Записывает данные в файл

    Аргументы:
        text: исходный текст
        path: путь для сохранения текста
    """
    try:
        with open(path, "wb") as file:
            file.write(text)
    except PermissionError:
        print(f"Недостаточно прав для сохранения файла {path}")
        exit(100)
    except Exception as e:
        print(e)
        exit(100)


def read_text(path: str):
    """
    Считывает текст из файла

    Аргумент:
        path: путь к файлу
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except PermissionError:
        print(f"Недостаточно прав для чтения файла {path}")
        exit(100)
    except FileNotFoundError:
        print(f"Не найден файл {path}")
        exit(100)
    except Exception as e:
        print(e)
        exit(100)


def read_encrypted(path: str):
    """
    Считывает зашифрованные данные

    Аргументы:
        path: путь к файлу
    """
    try:
        with open(path, "rb") as f:
            iv = f.read(16)
            c_text = f.read()
            return iv, c_text
    except PermissionError:
        print(f"Недостаточно прав для чтения файла {path}")
        exit(100)
    except FileNotFoundError:
        print(f"Не найден файл {path}")
        exit(100)
    except Exception as e:
        print(e)
        exit(100)
