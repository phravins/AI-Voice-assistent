import os
import json
import uuid
from typing import Dict, Any
from config import DOCS_DIR

def _get_safe_path(doc_id: str) -> str:
    base_dir = os.path.abspath(DOCS_DIR)
    target_path = os.path.abspath(os.path.join(base_dir, f"{doc_id}.json"))
    if not target_path.startswith(base_dir + os.sep):
        raise ValueError("Invalid document ID: Path traversal detected.")
    return target_path

def save(doc_structure: Dict[Any, Any], custom_id: str = None) -> str:
    doc_id = custom_id if custom_id else uuid.uuid4().hex
    path = _get_safe_path(doc_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc_structure, f, ensure_ascii=False)
    return doc_id

def load(doc_id: str) -> Dict[Any, Any]:
    path = _get_safe_path(doc_id)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
