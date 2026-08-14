import os
import json
import uuid
from typing import Dict, Any
from config import DOCS_DIR

def _get_safe_path(base_dir: str, doc_id: str) -> str:
    """
    Safely join base_dir and doc_id to prevent path traversal.
    Ensures the resolved path is inside base_dir using os.path.commonpath.
    """
    abs_base = os.path.abspath(base_dir)
    # Treat the doc_id as a filename (append .json)
    filename = f"{doc_id}.json"
    path = os.path.abspath(os.path.join(abs_base, filename))

    # os.path.commonpath is robust across platforms and avoids simple startswith pitfalls
    try:
        if os.path.commonpath([abs_base, path]) != abs_base:
            raise ValueError("Invalid document ID: Path traversal detected.")
    except ValueError:
        # commonpath can raise ValueError on different-drives on Windows; treat as invalid
        raise ValueError("Invalid document ID: Path traversal detected.")
    return path

def save(doc_structure: Dict[Any, Any], custom_id: str = None) -> str:
    doc_id = custom_id if custom_id else uuid.uuid4().hex
    path = _get_safe_path(DOCS_DIR, doc_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc_structure, f, ensure_ascii=False)
    return doc_id

def load(doc_id: str) -> Dict[Any, Any]:
    try:
        path = _get_safe_path(DOCS_DIR, doc_id)
    except ValueError:
        return {}
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)