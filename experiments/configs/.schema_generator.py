import inspect
import json
import importlib
from pathlib import Path
from typing import Any, get_type_hints, Union, get_origin, get_args

# Map stages to their module paths
MODULES = {
    "processor": "models.processor",
    "classifier": "models.classifier",
}


# -------- Utility functions --------


def python_type_to_json_type(annotation: Any) -> str:
    """Map Python types to JSON Schema types."""
    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin in (list, tuple, set):
        return "array"

    if origin is Union:
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return python_type_to_json_type(non_none_args[0])

    if annotation is str:
        return "string"
    if annotation is int:
        return "integer"
    if annotation is float:
        return "number"
    if annotation is bool:
        return "boolean"

    return "string"


def class_to_schema(cls: type) -> dict:
    """
    Generate JSON Schema for a class with mutually exclusive options:
    - file
    - constructor parameters exposed at top level
    """
    sig = inspect.signature(cls.__init__)
    hints = get_type_hints(cls.__init__)

    param_props = {}
    required_params = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue

        annotation = hints.get(name, Any)
        param_props[name] = {"type": python_type_to_json_type(annotation)}

        if param.default is inspect._empty:
            required_params.append(name)

    constructor_schema = {
        "type": "object",
        "properties": param_props,
        "required": required_params,
        "additionalProperties": False,
    }

    return {
        "type": "object",
        "description": (cls.__doc__ or "").strip(),
        "oneOf": [
            {
                "type": "object",
                "properties": {
                    "file": {"type": "string"},
                },
                "required": ["file"],
                "additionalProperties": False,
            },
            constructor_schema,
        ],
    }


def load_module_classes(module_path: str):
    """Load all classes defined in the module."""
    mod = importlib.import_module(module_path)
    return {
        name: cls
        for name, cls in inspect.getmembers(mod, inspect.isclass)
    }


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
                "oneOf": [
                    {
                        "properties": {
                            "file": {
                                "type": "string",
                                "description": "Path to input file.",
                            }
                        },
                        "required": ["file"],
                        "additionalProperties": False,
                    },
                    {
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL query to fetch data.",
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False,
                    },
                ],
            },
        },
        "required": ["data", "processor", "classifier"],
        "additionalProperties": False,
        "dependencies": {
            "processor": ["data"],
            "classifier": ["processor"],
        },
    }

    for stage, module_path in MODULES.items():
        classes = load_module_classes(module_path)
        if not classes:
            continue

        one_of = []
        for name, cls in classes.items():
            one_of.append(
                {
                    "type": "object",
                    "properties": {
                        name: class_to_schema(cls),
                    },
                    "required": [name],
                    "additionalProperties": False,
                }
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

