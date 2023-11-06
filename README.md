# pyfa-converter-v2

Allows you to convert Pydantic models for FastAPI param models - query, form, header, cookie, body, etc.

The project is originally written by dotX12 at [dotX12/pyfa-converter](https://github.com/dotX12/pyfa-converter),
but it doesn't support Pydantic v2, so we made a fork of the project with some changes:

- Added support for pydantic v2
- Added tests
- Re-licensed the code to LGPL 3.0
- Added mypy, flake8, isort checks
- Removed dead code

The project may be archived if the original package author upgrades to Pydantic v2
([dotX12/pyfa-converter#25](https://github.com/dotX12/pyfa-converter/issues/25)).

Currently, the library does not fully reflect the requirements in OpenAPI (e.g. gt parameter will be required, but this will not be specified in FastAPI docs).

## How to install?

`pip install pyfa_converter_v2`

## How to simplify your life?

```python3
from fastapi import FastAPI
from pydantic import BaseModel

from pyfa_converter_v2 import QueryDepends

app = FastAPI()

class ArticleSchema(BaseModel):
    title: str
    content: str

@app.post("/article")
async def create_article(article: ArticleSchema = QueryDepends(ArticleSchema)):
    return {"id": 1, "title": article.title, "content": article.content}
```

Available converters: `QueryDepends`, `BodyDepends`, `FormDepends`. You can add new types via `PyFaDepends`.

## Credits

[![aeza logo](https://w3s.link/ipfs/bafybeibdusnw63pr4a6otvtl6eqrydw7vi7l2r6q5p4woyltthmiipj77u/logo.png)](https://aeza.net/?utm_source=github&utm_medium=banner&utm_campaign=open-source&utm_id=pyfa-converter-v2)

This project is brought to you by the **⭐ [Aeza.net](https://aeza.net/?utm_source=github&utm_medium=hyperlink&utm_campaign=open-source&utm_id=pyfa-converter-v2) hosting provider team**.
