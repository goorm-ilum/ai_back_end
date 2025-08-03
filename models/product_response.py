from pydantic import BaseModel
from typing import Optional

class ProductSummaryResponse(BaseModel):
    productId: int
    productName: str
    productDescription: str
    thumbnailImageUrl: str
    price: int
    discountPrice: int
    averageReviewStar: float
    isLiked: bool

    @classmethod
    def from_dict(cls, data: dict, is_liked: bool = False) -> 'ProductSummaryResponse':
        """
        DB 조회 결과 딕셔너리를 ProductSummaryResponse로 변환
        """
        return cls(
            productId=data.get('product_id', data.get('id', 0)),
            productName=data.get('product_name', ''),
            productDescription=data.get('description', data.get('product_description', '')),
            thumbnailImageUrl=data.get('thumbnail_image_url', ''),
            price=data.get('price', 0),
            discountPrice=data.get('discount_price', 0),
            averageReviewStar=float(data.get('average_review_star', 0.0)),
            isLiked=is_liked
        )
