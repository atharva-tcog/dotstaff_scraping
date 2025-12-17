# import os
# import json

# class TextWriter:
#     def __init__(self, file_path: str):
#         self.file_path = file_path

#         # ✅ Ensure output directory exists
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     def write_job(self, job):
#         with open(self.file_path, "a", encoding="utf-8") as f:
#             f.write(str(job) + "\n\n")

#     def write_error(self, message: str):
#         with open(self.file_path, "a", encoding="utf-8") as f:
#             f.write(f"ERROR: {message}\n")

#     def write_json(self, payload: dict):
#         with open(self.file_path, "a", encoding="utf-8") as f:
#             f.write(json.dumps(payload, ensure_ascii=False))
#             f.write("\n")


import os
import json
from dataclasses import asdict

class TextWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

        # ✅ Ensure output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # -------------------------------------------------
    # WRITE JOB AS PRETTY JSON
    # -------------------------------------------------
    def write_job(self, job):
        """
        Writes JobData as formatted JSON (one job after another)
        """
        with open(self.file_path, "a", encoding="utf-8") as f:
            json.dump(
                asdict(job),          # convert dataclass → dict
                f,
                indent=4,             # ✅ multi-line
                ensure_ascii=False
            )
            f.write("\n\n")            # ✅ separation between jobs

    # -------------------------------------------------
    # WRITE ERROR
    # -------------------------------------------------
    def write_error(self, message: str):
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"ERROR: {message}\n")

    # -------------------------------------------------
    # WRITE FINAL PAYLOAD JSON
    # -------------------------------------------------
    def write_json(self, payload: dict):
        """
        Writes API-ready payload as formatted JSON
        """
        with open(self.file_path, "a", encoding="utf-8") as f:
            json.dump(
                payload,
                f,
                indent=4,             # ✅ multi-line
                ensure_ascii=False
            )
            f.write("\n\n")