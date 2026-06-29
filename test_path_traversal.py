import os
from modules import doc_store

def test_path_traversal():
    malicious_id = "../../../etc/passwd"

    # Test save
    try:
        doc_store.save({"data": "test"}, custom_id=malicious_id)
        print("FAIL: Path traversal not prevented in save!")
    except ValueError as e:
        print(f"PASS: Caught ValueError in save: {e}")
    except Exception as e:
        print(f"FAIL: Unexpected exception in save: {e}")

    # Test load
    try:
        doc_store.load(malicious_id)
        print("FAIL: Path traversal not prevented in load!")
    except ValueError as e:
        print(f"PASS: Caught ValueError in load: {e}")
    except Exception as e:
        print(f"FAIL: Unexpected exception in load: {e}")

if __name__ == "__main__":
    test_path_traversal()
