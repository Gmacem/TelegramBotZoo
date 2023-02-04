from pydantic import BaseModel


class TelegramBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name: bool = True
        orm_mode: bool = True


class TelegramResponse(TelegramBaseModel):
    message: str
    details: str | None
