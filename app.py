import os
import sys

repo_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(repo_root, "backend")
sys.path.insert(0, backend_dir)

from server import run_server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8000))
    run_server(port)
