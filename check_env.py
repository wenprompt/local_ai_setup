# check_env.py

import sys
import os

try:
    import pydantic

    print("✅ Pydantic was successfully imported.")
    print("\n--- Pydantic Location ---")
    print(pydantic.__file__)

except ImportError:
    print("❌ FAILED to import Pydantic.")

print("\n--- Python Interpreter Being Used by VS Code ---")
print(sys.executable)

print("\n--- sys.path (where this interpreter looks for modules) ---")
for path in sys.path:
    print(path)
