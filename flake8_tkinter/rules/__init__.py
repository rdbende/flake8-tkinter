from pathlib import Path

for module in Path(__file__).parent.glob("*.py"):
    if module != "__init__.py":
        __import__(f"{__package__}.{module.stem}")
