"""
TUẦN 3 & TUẦN 4: PRODUCT & CATEGORY SERVICE

Nhiệm vụ của tầng Service:
- Xử lý toàn bộ logic nghiệp vụ (kiểm tra tồn tại, validate dữ liệu, điều phối repository).
- Tuyệt đối không import Request hay Response của FastAPI vào đây.

Yêu cầu thực tập sinh tự thực hiện:
- create_category
- create_product (kiểm tra trùng SKU, kiểm tra category tồn tại)
- get_product
- list_products (phân trang và tìm kiếm)
- update_product
- delete_product (xóa mềm)
"""
import math
from typing import Optional
from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, CategoryCreate
from app.schemas.common import PageResponse
from app.repositories.product_repository import product_repo, category_repo
from app.core.exceptions import NotFoundException, BadRequestException


class ProductService:
    # TODO: Thực tập sinh tự cài đặt các phương thức nghiệp vụ ở Tuần 3 & 4
    # Tuần 3
    def create_category(self, db: Session, category_in: CategoryCreate) -> Category:
        existing_category = category_repo.get_by_name(db, category_in.name)
        if existing_category:
            raise BadRequestException(
                message=f"Danh mục '{category_in.name}' đã tồn tại",
                error_code="CATEGORY_ALREADY_EXISTS",
            )
        new_category = Category(**category_in.model_dump())
        db_obj = category_repo.create(db, new_category)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_categories(self, db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
        return category_repo.get_multi(db, skip=skip, limit=limit)

    def get_category(self, db: Session, category_id: int) -> Category:
        category = category_repo.get_by_id(db, category_id)
        if not category:
            raise NotFoundException(message=f"Không tìm thấy danh mục có ID={category_id}")
        return category

    def create_product(self, db: Session, product_in: ProductCreate) -> Product:
        category = category_repo.get_by_id(db, product_in.category_id)
        if not category:
            raise NotFoundException(message=f"Danh mục có ID={product_in.category_id} không tồn tại")

        existing_product = product_repo.get_by_sku(db, product_in.sku)
        if existing_product:
            raise BadRequestException(
                message=f"Mã SKU '{product_in.sku}' đã tồn tại",
                error_code="SKU_ALREADY_EXISTS",
            )

        new_product = Product(**product_in.model_dump())
        db_obj = product_repo.create(db, new_product)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_products(self, db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
        return product_repo.get_multi_active(db, skip=skip, limit=limit)

    def get_product(self, db: Session, product_id: int) -> Product:
        product = product_repo.get_by_id_with_category(db, product_id)
        if not product or not product.is_active:
            raise NotFoundException(message=f"Không tìm thấy sản phẩm có ID={product_id}")
        return product

    # Tuần 4: Lấy danh sách sản phẩm có phân trang, tìm kiếm và lọc theo danh mục
    def list_products(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 10,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> PageResponse[ProductResponse]:
        skip = (page - 1) * page_size
        items, total = product_repo.search_and_filter(
            db=db,
            skip=skip,
            limit=page_size,
            category_id=category_id,
            search=search,
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        return PageResponse[ProductResponse](
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def update_product(self, db: Session, product_id: int, product_in: ProductUpdate) -> Product:
        db_obj = self.get_product(db, product_id)
        update_data = product_in.model_dump(exclude_unset=True)

        if "category_id" in update_data and update_data["category_id"] is not None:
            category = category_repo.get_by_id(db, update_data["category_id"])
            if not category:
                raise NotFoundException(
                    message=f"Danh mục có ID={update_data['category_id']} không tồn tại"
                )

        if "sku" in update_data and update_data["sku"] is not None:
            new_sku = update_data["sku"].strip().upper()
            if new_sku != db_obj.sku.upper():
                if product_repo.get_by_sku(db, new_sku):
                    raise BadRequestException(
                        message=f"Mã SKU '{new_sku}' đã tồn tại",
                        error_code="SKU_ALREADY_EXISTS",
                    )
            update_data["sku"] = new_sku

        updated_obj = product_repo.update(db, db_obj, update_data)
        db.commit()
        db.refresh(updated_obj)
        return updated_obj

    def delete_product(self, db: Session, product_id: int) -> None:
        db_obj = self.get_product(db, product_id)
        product_repo.update(db, db_obj, {"is_active": False})
        db.commit()



product_service = ProductService()
