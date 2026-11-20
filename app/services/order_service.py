"""
TUẦN 6: ORDER SERVICE (DATABASE TRANSACTION & ACID)

Nhiệm vụ trọng tâm:
- create_order: bọc trong 1 Transaction duy nhất!
  1. Kiểm tra tồn kho của từng sản phẩm.
  2. Trừ stock_quantity của sản phẩm.
  3. Tính tổng tiền dựa trên giá trong DB (không tin giá client gửi).
  4. Lưu order và order_items.
  5. Nếu bất kỳ sản phẩm nào thiếu hàng -> rollback toàn bộ!
"""
from decimal import Decimal
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User, UserRole
from app.models.product import Product
from app.schemas.order import OrderCreate
from app.repositories.order_repository import order_repo
from app.repositories.product_repository import product_repo
from app.core.exceptions import BadRequestException, NotFoundException, ForbiddenException


class OrderService:
    # TODO: Thực tập sinh tự cài đặt nghiệp vụ đặt hàng và transaction ở Tuần 6
    def create_order(
        self, db: Session, current_user: User, order_in: OrderCreate
    ) -> Order:
        """
        Tạo đơn hàng mới với Database Transaction đảm bảo tính ACID:
        - Khóa dòng sản phẩm (with_for_update) chống race condition.
        - Trừ tồn kho và tính tổng tiền trực tiếp từ giá sản phẩm trong DB.
        - Nếu bất kỳ sản phẩm nào không đủ tồn kho -> rollback toàn bộ.
        """
        total_amount = Decimal("0.00")
        order_items: List[OrderItem] = []

        try:
            for item_in in order_in.items:
                # 1. Khóa dòng kiểm tra sản phẩm
                stmt = select(Product).where(Product.id == item_in.product_id).with_for_update()
                product = db.scalar(stmt)

                if not product or not product.is_active:
                    db.rollback()
                    raise NotFoundException(
                        message=f"Sản phẩm với ID {item_in.product_id} không tồn tại hoặc đã ngừng kinh doanh"
                    )

                # 2. Kiểm tra tồn kho
                if product.stock_quantity < item_in.quantity:
                    db.rollback()
                    raise BadRequestException(
                        message=f"Sản phẩm '{product.name}' không đủ số lượng tồn kho (còn {product.stock_quantity}, yêu cầu {item_in.quantity})",
                        error_code="INSUFFICIENT_STOCK",
                    )

                # 3. Trừ số lượng tồn kho
                product.stock_quantity -= item_in.quantity

                # 4. Tính giá tiền từ database
                line_total = product.price * item_in.quantity
                total_amount += line_total

                # 5. Khởi tạo OrderItem
                order_items.append(
                    OrderItem(
                        product_id=product.id,
                        quantity=item_in.quantity,
                        unit_price=product.price,
                    )
                )

            # 6. Tạo đơn hàng Order
            new_order = Order(
                user_id=current_user.id,
                total_amount=total_amount,
                status=OrderStatus.PENDING,
                items=order_items,
            )
            db.add(new_order)
            db.flush()

            # 7. Commit duy nhất một lần chốt transaction
            db.commit()

            # 8. Tải lại đầy đủ items qua repository
            order_detail = order_repo.get_by_id_with_items(db, id=new_order.id)
            if not order_detail:
                raise NotFoundException(message=f"Không tìm thấy đơn hàng vừa tạo với ID {new_order.id}")
            return order_detail

        except (BadRequestException, NotFoundException, ForbiddenException):
            db.rollback()
            raise
        except Exception:
            db.rollback()
            raise

    def get_my_orders(
        self, db: Session, current_user: User, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """Lấy danh sách đơn hàng của người dùng đang đăng nhập."""
        return order_repo.get_by_user_id(db, user_id=current_user.id, skip=skip, limit=limit)

    def get_order_detail(
        self, db: Session, order_id: int, current_user: User
    ) -> Order:
        """
        Lấy chi tiết đơn hàng kèm danh sách items.
        Kiểm tra quyền sở hữu: chỉ chủ đơn hàng hoặc Admin mới được xem.
        """
        order = order_repo.get_by_id_with_items(db, id=order_id)
        if not order:
            raise NotFoundException(message=f"Không tìm thấy đơn hàng với ID {order_id}")

        if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
            raise ForbiddenException(message="Bạn không có quyền xem chi tiết đơn hàng này")

        return order


order_service = OrderService()
