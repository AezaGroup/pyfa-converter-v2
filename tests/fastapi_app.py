from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Form
from pydantic import BaseModel, Field

from pyfa_converter_v2 import (
    BodyDepends,
    FormDepends,
    PyFaDepends,
    QueryDepends,
)

app = FastAPI()


class TestSchema(BaseModel):
    id: Optional[int]
    title: Optional[str]
    data: Optional[List[int]]


class TestGtSchema(BaseModel):
    id: Optional[int] = Field(..., gt=0)
    title: str = Field(max_length=10)


class FormTestSchema(BaseModel):
    id: Optional[int]
    title: Optional[str]


@app.post("/test_query")
async def test_query(
    data: TestSchema = QueryDepends(TestSchema),
) -> Dict[str, Any]:
    return {"data": data}


@app.post("/test_query_gt")
async def test_query_gt(
    data: TestGtSchema = QueryDepends(TestGtSchema),
) -> Dict[str, Any]:
    return {"data": data}


@app.post("/test_body")
async def test_body(
    data: TestSchema = BodyDepends(TestSchema),
) -> Dict[str, Any]:
    return {"data": data}


@app.post("/test_form")
async def test_form(
    data: FormTestSchema = FormDepends(FormTestSchema),
) -> Dict[str, Any]:
    return {"data": data}


@app.post("/test_pyfa_form")
async def test_pyfa_form(
    data: FormTestSchema = PyFaDepends(Form, FormTestSchema),
) -> Dict[str, Any]:
    return {"data": data}
