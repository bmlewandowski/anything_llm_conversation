import traceback
import sys
from pathlib import Path

# Ensure repository root is on sys.path so package imports work when running this script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import custom_components.anything_llm_conversation.conversation as m
    print('Imported OK:', m)
except Exception:
    traceback.print_exc()
