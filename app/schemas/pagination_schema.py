from pydantic import BaseModel, Field, HttpUrl
from typing import List


class Pagination(BaseModel):
    page: int = Field(..., description="Current page number.")
    per_page: int = Field(..., description="Number of items per page.")
    total_items: int = Field(..., description="Total number of items.")
    total_pages: int = Field(..., description="Total number of pages.")

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "per_page": 10,
                "total_items": 50,
                "total_pages": 5
            }
        }


class PaginationLink(BaseModel):
    rel: str
    href: HttpUrl
    method: str = "GET"


class EnhancedPagination(Pagination):
    links: List[PaginationLink] = []

    def add_link(self, rel: str, href: str):
        self.links.append(PaginationLink(rel=rel, href=href))
