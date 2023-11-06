import inspect
from typing import Any, Callable, List, Type, Union

from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from pydantic.fields import FieldInfo


class PydanticConverterUtils:
    @classmethod
    def param_maker(cls, field: FieldInfo, _type: Callable[..., FieldInfo]) -> FieldInfo:
        return cls.__fill_params(param=_type, model_field=field)

    @classmethod
    def __fill_params(cls, param: Callable[..., FieldInfo], model_field: FieldInfo) -> FieldInfo:
        return param(
            annotation=model_field.annotation,
            default=model_field.default,
            default_factory=model_field.default_factory,
            alias=model_field.alias,
            alias_priority=model_field.alias_priority,
            validation_alias=model_field.validation_alias,
            serialization_alias=model_field.serialization_alias,
            title=model_field.title,
            description=model_field.description,
            examples=model_field.examples,
            exclude=model_field.exclude,
            discriminator=model_field.discriminator,
            json_schema_extra=model_field.json_schema_extra,
            frozen=model_field.frozen,
            validate_default=model_field.validate_default,
            repr=model_field.repr,
            init_var=model_field.init_var,
            kw_only=model_field.kw_only,
            metadata=model_field.metadata,
        )

    @classmethod
    def override_signature_parameters(
        cls,
        model: Type[BaseModel],
        param_maker: Callable[[str, FieldInfo], Any],
    ) -> List[inspect.Parameter]:
        return [
            inspect.Parameter(
                name=field_name,
                kind=inspect.Parameter.POSITIONAL_ONLY,
                default=param_maker(field_name, field),
                annotation=field.annotation,
            )
            for field_name, field in model.model_fields.items()
        ]


class PydanticConverter(PydanticConverterUtils):
    @classmethod
    def reformat_model_signature(
        cls,
        model_cls: Type[BaseModel],
        _type: Any,
    ) -> Union[Type[BaseModel], Type["PydanticConverter"]]:
        """
        Adds an `query` class method to decorated models. The `query` class
        method can be used with `FastAPI` endpoints.

        Args:
            model_cls: The model class to decorate.
            _type: literal query, form, body, etc...

        Returns:
            The decorated class.
        """
        _type_var_name = str(_type.__name__).lower()

        def make_form_parameter(field_name: str, field: FieldInfo) -> Any:
            """
            Converts a field from a `Pydantic` model to the appropriate `FastAPI`
            parameter type.

            Args:
                field: The field to convert.

            Returns:
                Either the result of `Query`, if the field is not a sub-model, or
                the result of `Depends on` if it is.

            """
            field_type = field.annotation if isinstance(field.annotation, type) else type(field.annotation)

            if issubclass(field_type, BaseModel):
                # This is a sub-model.
                assert hasattr(field_type, _type_var_name), (
                    f"Sub-model class for {field_name} field must be decorated with" f" `as_form` too."
                )
                attr = getattr(field_type, _type_var_name)
                return Depends(attr)  # noqa
            else:
                return cls.param_maker(field=field, _type=_type)

        new_params = PydanticConverterUtils.override_signature_parameters(
            model=model_cls, param_maker=make_form_parameter
        )

        def _as_form(**data: Any) -> Union[BaseModel, PydanticConverter]:
            try:
                return model_cls(**data)
            except ValidationError as e:
                raise RequestValidationError(errors=e.errors())

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig  # type: ignore[attr-defined]
        _as_form.__name__ = _type_var_name.capitalize() + model_cls.__name__
        setattr(model_cls, _type_var_name, _as_form)
        return model_cls
