from typing import Any, Callable, Type, TypeVar

from fastapi import Body, Depends, Form, Query
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .main import PydanticConverter

_T = TypeVar("_T", bound=BaseModel)


def _generate(model: Type[_T], _type: Callable[..., FieldInfo]) -> _T:
    obj = PydanticConverter.reformat_model_signature(model_cls=model, _type=_type)
    attr = getattr(obj, str(_type.__name__).lower())
    return Depends(attr)


def PyFaDepends(type_: Callable[..., Any], model_type: Type[_T]) -> _T:
    """Convert a Pydantic model to FastAPI parameters.

    Args:
        type_: The type of the parameter. Example: `Query`, `Form`, `Body`.
        model_type: The model class to convert.

    Returns:
        The converted model.

    Example:
        >>> from fastapi import Query
        >>> @app.post("/test")
        ... def test(
        ...     data: ExampleModel = PyFaDepends(Query, ExampleModel)
        ... ) -> Dict[str, Any]:
        ...     return {"data": data}
    """
    return _generate(model=model_type, _type=type_)


def FormDepends(model_type: Type[_T]) -> _T:
    """Convert a Pydantic model to FastAPI Form parameters.

    Args:
        model_type: The model class to convert.

    Returns:
        The converted model.

    Example:
        >>> @app.post("/test")
        ... def test(
        ...     data: ExampleModel = FormDepends(ExampleModel)
        ... ) -> Dict[str, Any]:
        ...     return {"data": data}
    """
    return _generate(model=model_type, _type=Form)


def BodyDepends(model_type: Type[_T]) -> _T:
    """Convert a Pydantic model to FastAPI Body parameters.

    Args:
        model_type: The model class to convert.

    Returns:
        The converted model.

    Example:
        >>> @app.post("/test")
        ... def test(
        ...     data: ExampleModel = BodyDepends(ExampleModel)
        ... ) -> Dict[str, Any]:
        ...     return {"data": data}
    """
    return _generate(model=model_type, _type=Body)


def QueryDepends(model_type: Type[_T]) -> _T:
    """Convert a Pydantic model to FastAPI Query parameters.

    Args:
        model_type: The model class to convert.

    Returns:
        The converted model.

    Example:
        >>> @app.post("/test")
        ... def test(
        ...     data: ExampleModel = QueryDepends(ExampleModel)
        ... ) -> Dict[str, Any]:
        ...     return {"data": data}
    """
    return _generate(model=model_type, _type=Query)
