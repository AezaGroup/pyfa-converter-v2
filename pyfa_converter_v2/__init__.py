"""Pydantic model to FastAPI Depends() converter.

This library provides a way to convert Pydantic models to FastAPI to use
it in FastAPI endpoints and remove code duplication.

You can learn more about it here: https://github.com/AezaGroup/pyfa-converter-v2

Example:
    >>> @app.post("/test")
    ... def test(
    ...     data: ExampleModel = PyFaDepends(Query, ExampleModel)
    ... ) -> Dict[str, Any]:
    ...     return {"data": data}
"""

from .depends import BodyDepends, FormDepends, PyFaDepends, QueryDepends

__all__ = (
    "QueryDepends",
    "BodyDepends",
    "FormDepends",
    "PyFaDepends",
)
