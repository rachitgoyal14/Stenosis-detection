import os

def save_file(data: bytes, filename: str, folder: str):
    path = f"storage/{folder}"
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, filename), "wb") as f:
        f.write(data)
