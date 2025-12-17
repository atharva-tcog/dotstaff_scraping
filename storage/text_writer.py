import os
import json

class TextWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

        # ✅ Ensure output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def write_job(self, job):
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(str(job) + "\n\n")

    def write_error(self, message: str):
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"ERROR: {message}\n")

    def write_json(self, payload: dict):
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False))
            f.write("\n")
