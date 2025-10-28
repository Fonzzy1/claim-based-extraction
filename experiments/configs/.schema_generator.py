import inspect
import json
import importlib
from pathlib import Path
from typing import Any, get_type_hints, Optional

# Map stages to their module paths
MODULES = {
    "filter": "models.filter",
    "elementfilter": "models.filter",  # Shares same class set
    "extractor": "models.extractor",
    "deconstructor": "models.deconstructor",
}

# -------- Utility functions --------


def python_type_to_json_type(annotation: Any) -> str:
    """Map Python types to JSON Schema types."""
    origin = getattr(annotation, "__origin__", None)
    if origin in (list, tuple, set):
        return "array"
    if annotation in (str, Optional[str]):
        return "string"
    if annotation in (int, Optional[int]):
        return "integer"
    if annotation in (float, Optional[float]):
        return "number"
    if annotation in (bool, Optional[bool]):
        return "boolean"
    return "string"


def class_to_schema(cls: type) -> dict:
    """
    Generate JSON Schema for a class with mutually exclusive options:
    - file
    - drive
    - constructor parameters exposed at top level
    """
    sig = inspect.signature(cls.__init__)
    hints = get_type_hints(cls.__init__)
    
    # Build schema for constructor parameters (skip self)
    param_props = {}
    required_params = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        annotation = hints.get(name, Any)
        param_props[name] = {"type": python_type_to_json_type(annotation)}
        if param.default is inspect._empty:
            required_params.append(name)
    
    # Schemas for the three mutually exclusive options
    return {
        "type": "object",
        "description": (cls.__doc__ or "").strip(),
        "anyOf": [
            {"required": ["file"], "properties": {"file": {"type": "string"}}},
            {"required": ["drive"], "properties": {"drive": {"type": "string"}}},
            {"required": required_params, "properties": param_props} if param_props else {}
        ]
    }


def load_module_classes(module_path: str):
    """Load all classes defined in the module (ignores imported ones)."""
    mod = importlib.import_module(module_path)
    return {name: cls for name, cls in inspect.getmembers(mod, inspect.isclass)}


# -------- Schema generator --------


def generate_pipeline_schema():
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Auto-generated Media Pipeline Schema",
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "description": "Data source configuration.",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to input file.",
                    },
                    "query": {
                        "type": "string",
                        "description": "SQL query to fetch data.",
                    },
                },
            },
            "processor": {
                "type": "object",
                "description": "Fixed text processor configuration.",
                "properties": {
                    "context_size": {
                        "type": "integer",
                        "description": "Number of surrounding sentences to include as context.",
                    },
                    "sentence_splitting_function": {
                        "type": "string",
                        "description": "Python function used for sentence tokenization.",
                    },
                },
            },
        },
        "additionalProperties": False,
        "dependencies": {
            "filter": ["data"],
            "processor": ["filter"],
            "elementfilter": ["processor"],
            "extractor": ["elementfilter"],
            "deconstructor": ["extractor"],
        },
    }

    # Dynamically build schema for filter, elementfilter, extractor, deconstructor
    for stage, module_path in MODULES.items():
        classes = load_module_classes(module_path)
        if not classes:
            continue

        one_of = []
        for name, cls in classes.items():
            one_of.append(
                {"properties": {name: class_to_schema(cls)}, "required": [name]}
            )

        schema["properties"][stage] = {
            "type": "object",
            "description": f"{stage.capitalize()} stage configuration.",
            "oneOf": one_of,
        }

    return schema


if __name__ == "__main__":
    schema = generate_pipeline_schema()
    Path("./experiments/configs/.schema.json").write_text(
        json.dumps(schema, indent=2)
    )
