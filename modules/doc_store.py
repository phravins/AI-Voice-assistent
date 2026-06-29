import os
import json
import uuid
from typing import Dict, Any
from config import DOCS_DIR

def _safe_path(base_dir: str, doc_id: str) -> str:
    """Safely join base_dir and doc_id to prevent path traversal."""
    abs_base = os.path.abspath(base_dir)
    # Ensure doc_id is treated as a filename, not an absolute path
    # If doc_id starts with /, os.path.join(DOCS_DIR, doc_id) will discard DOCS_DIR
    # We use os.path.basename to get only the filename if we want to be very strict,
    # but the requirement says "verify the resolved path starts with the expected base directory".
    path = os.path.abspath(os.path.join(abs_base, f"{doc_id}.json"))
    if not path.startswith(abs_base + os.sep):
        raise ValueError("Invalid document ID")
    return path

def save(doc_structure: Dict[Any, Any], custom_id: str = None) -> str:
    doc_id = custom_id if custom_id else uuid.uuid4().hex
    path = _safe_path(DOCS_DIR, doc_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc_structure, f, ensure_ascii=False)
    return doc_id

def load(doc_id: str) -> Dict[Any, Any]:
    try:
        path = _safe_path(DOCS_DIR, doc_id)
    except ValueError:
        return {}

    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
