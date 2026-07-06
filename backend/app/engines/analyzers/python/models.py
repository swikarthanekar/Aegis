from pydantic import BaseModel


class CallInfo(BaseModel):
    caller: str
    callee: str
    line: int


class FunctionInfo(BaseModel):
    name: str
    line: int
    is_async: bool
    arguments: list[str]


class ClassInfo(BaseModel):
    name: str
    line: int


class PythonAnalysis(BaseModel):
    language: str = "Python"
    imports: list[str]
    classes: list[ClassInfo]
    functions: list[FunctionInfo]
    calls: list[CallInfo]