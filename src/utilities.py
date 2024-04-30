def extract_text_from_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        python_code = f.read()
        return python_code
