"""
TUẦN 6: ORDER ROUTERS

Yêu cầu:
- POST /orders: Đặt hàng mới (yêu cầu đăng nhập, transaction)
- GET /orders/my-orders: Lịch sử đơn hàng của tôi
- GET /orders/{order_id}: Chi tiết đơn hàng
"""
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas import ApiResponse, OrderCreate, OrderResponse
from app.services.order_service import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

# TODO: Thực tập sinh tự cài đặt các endpoints đặt hàng ở Tuần 6
@router.post(
    "",
    response_model=ApiResponse[OrderResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Đặt hàng mới với Database Transaction đảm bảo ACID."""
    order = order_service.create_order(db=db, current_user=current_user, order_in=order_in)
    return ApiResponse(
        message="Tạo đơn hàng thành công",
        data=order,
    )


@router.get(
    "/my-orders",
    response_model=ApiResponse[List[OrderResponse]],
    status_code=status.HTTP_200_OK,
)
def get_my_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy danh sách lịch sử đơn hàng của người dùng hiện tại."""
    orders = order_service.get_my_orders(db=db, current_user=current_user, skip=skip, limit=limit)
    return ApiResponse(
        message="Lấy lịch sử đơn hàng thành công",
        data=orders,
    )


@router.get(
    "/{order_id}",
    response_model=ApiResponse[OrderResponse],
    status_code=status.HTTP_200_OK,
)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy thông tin chi tiết một đơn hàng kèm danh sách sản phẩm."""
    order = order_service.get_order_detail(db=db, order_id=order_id, current_user=current_user)
    return ApiResponse(
        message="Lấy chi tiết đơn hàng thành công",
        data=order,
    )
