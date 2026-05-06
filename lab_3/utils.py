def write_data(text: str, path: str):
    with open(path, "wb") as file:
        file.write(text)


def read_text(path: str):
    with open(path, "rb") as file:
        return file.read()


def read_encrypted(path: str):
    with open(path, "rb") as f:
        iv = f.read(16)
        c_text = f.read()
        return iv, c_text
