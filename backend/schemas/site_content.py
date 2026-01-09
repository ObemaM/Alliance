from pydantic import BaseModel


class SiteContentResponse(BaseModel):
    id: int
    key: str
    value: str
    description: str | None

    class Config:
        from_attributes = True


class SiteContentCreate(BaseModel):
    key: str
    value: str
    description: str | None = None


class SiteContentUpdate(BaseModel):
    key: str | None = None
    value: str | None = None
    description: str | None = None
