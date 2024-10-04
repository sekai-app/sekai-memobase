from dataclasses import dataclass
from typing import TypeVar, Optional, Type
from pydantic import ValidationError
from .response import CODE, BaseResponse
from ..utils import LOG


T = TypeVar("T", bound=BaseResponse)


@dataclass
class Promise:
    __data: Optional[dict]
    __errcode: CODE = CODE.SUCCESS
    __errmsg: str = ""

    @classmethod
    def from_error(cls, errcode: CODE, errmsg: str):
        assert errmsg is not None, "Error Message can't be None!"
        assert errcode in CODE, f"Invalid Error Code: {errcode}"
        return cls(None, errcode, errmsg)

    def ok(self) -> bool:
        return self.__errcode == CODE.SUCCESS

    def to_response(self, ResponseModel: Type[T]) -> T:
        try:
            return ResponseModel(
                data=self.__data,
                errno=self.__errcode,
                errmsg=self.__errmsg,
            )
        except ValidationError as e:
            LOG.error(f"Error while parsing response: {e}")
            return ResponseModel(
                data=None,
                errno=CODE.INTERNAL_SERVER_ERROR,
                errmsg=str(e),
            )
