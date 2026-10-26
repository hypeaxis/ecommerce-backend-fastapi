# Giáo trình Đào tạo Backend Thực chiến (8 Tuần)

* **Đối tượng:** Sinh viên năm 3 – 4 ngành CNTT / Phần mềm.
* **Thời lượng:** 8 tuần, tối thiểu 12 – 15 giờ/tuần.
* **Tech Stack:** Python 3.10+, FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, Docker, Pytest.
* **Dự án thực hành xuyên suốt:** Xây dựng hệ thống Backend hoàn chỉnh cho **E-Commerce & Order Management API**.

---

## 📌 TUẦN 1: Onboarding, Git Conventions, Docker & Setup FastAPI

### 🎯 Mục tiêu:
* Hiểu văn hóa làm việc theo quy chuẩn Git chuyên nghiệp của công ty.
* Dựng môi trường phát triển độc lập bằng Docker (PostgreSQL).
* Khởi tạo dự án FastAPI đầu tiên với cấu trúc thư mục sạch và đọc cấu hình từ biến môi trường.

### ⏱️ Phân bổ thời gian (12h):
* **3h - Lý thuyết:** Đọc [Centic GitHub Conventions](git-conventions.md), tìm hiểu cơ chế hoạt động của Docker & Docker Compose cơ bản.
* **6h - Thực hành:**
  1. Tạo repository cá nhân `ecommerce-backend-fastapi` (hoặc fork template của công ty).
  2. Viết file `.gitignore` đầy đủ (loại trừ `.env`, `venv`, `__pycache__`).
  3. Viết `docker-compose.yml` để khởi chạy PostgreSQL 15+ kèm volume lưu trữ dữ liệu.
  4. Khởi tạo FastAPI app với `main.py`, sử dụng `pydantic-settings` để đọc cấu hình từ `.env`.
  5. Viết API Healthcheck: `GET /healthz` trả về trạng thái service và timestamp hiện tại.
* **3h - Tự kiểm thử & Tạo PR:** Tạo branch `feature/setup-project`, commit nguyên tử, mở PR vào `develop`.

### 📋 Tiêu chuẩn hoàn thành (Definition of Done - DoD):
- [ ] Repo có đầy đủ README hướng dẫn chạy dự án bằng lệnh.
- [ ] Chạy `docker compose up -d` khởi động Postgres thành công mà không lỗi port.
- [ ] Chạy `uvicorn app.main:app --reload` truy cập được `http://localhost:8000/docs`.
- [ ] PR tuân thủ 100% quy chuẩn Centic (không có commit dư thừa, không có file nhạy cảm).

---

## 📌 TUẦN 2: Database Modeling & Migration với SQLAlchemy 2.0 + Alembic

### 🎯 Mục tiêu:
* Nắm vững kỹ năng thiết kế lược đồ CSDL quan hệ chuẩn hóa (3NF).
* Làm quen với cú pháp hiện đại của **SQLAlchemy 2.0** (`DeclarativeBase`, `Mapped`, `mapped_column`).
* Thành thạo quy trình quản lý phiên bản cơ sở dữ liệu bằng **Alembic**.

### ⏱️ Phân bổ thời gian (12h):
* **3h - Lý thuyết:** Ôn tập thiết kế ERD, Primary Key (UUID vs Auto-increment ID), Foreign Key, Indexing, Khái niệm Database Migration.
* **6h - Thực hành:**
  1. Thiết kế ERD gồm 3 bảng:
     * `users`: `id`, `email` (unique, index), `hashed_password`, `full_name`, `role` (admin/customer), `is_active`, `created_at`, `updated_at`.
     * `categories`: `id`, `name` (unique), `description`, `created_at`.
     * `products`: `id`, `name` (index), `sku` (unique, index), `price`, `stock_quantity`, `category_id` (FK -> categories.id), `is_active`, `created_at`, `updated_at`.
  2. Khai báo các Models bằng SQLAlchemy 2.0.
  3. Khởi tạo Alembic (`alembic init alembic`), kết nối với SQLAlchemy `Base.metadata`.
  4. Sinh file migration tự động đầu tiên: `alembic revision --autogenerate -m "create users, categories, products tables"`.
  5. Thực thi migrate: `alembic upgrade head`.
* **3h - Tạo PR:** Nhánh `feature/db-modeling-alembic`.

### 📋 Tiêu chuẩn hoàn thành (DoD):
- [ ] Mở DBeaver / pgAdmin thấy đủ 3 bảng với các ràng buộc (Foreign Key, Not Null, Unique, Index).
- [ ] Thử lệnh `alembic downgrade -1` và `alembic upgrade head` đều hoạt động trơn tru không lỗi cú pháp.

---

## 📌 TUẦN 3: Kiến trúc 3 Tầng & CRUD Category/Product API

### 🎯 Mục tiêu:
* Áp dụng thành công kiến trúc **Layered Architecture (3-Tier)**: Router -> Service -> Repository.
* Phân định rạch ròi giữa SQLAlchemy Model và Pydantic Schema (DTO).
* Viết trọn vẹn bộ API CRUD đầu tiên chuẩn RESTful.

### ⏱️ Phân bổ thời gian (12h):
* **3h - Lý thuyết:** Đọc [Hướng dẫn Kiến trúc](architecture-guidelines.md), hiểu về Dependency Injection (`Depends`) và vòng đời của `db_session`.
* **6h - Thực hành:**
  1. Tạo `GenericRepository` (Base CRUD: get, get_multi, create, update, delete).
  2. Xây dựng Pydantic Schemas cho Product: `ProductCreate`, `ProductUpdate`, `ProductResponse`.
  3. Viết `ProductRepository` kế thừa BaseRepository.
  4. Viết `ProductService` xử lý nghiệp vụ (kiểm tra trùng mã SKU, validate giá hợp lệ).
  5. Viết Router `api/v1/endpoints/products.py`:
     * `POST /api/v1/products` (Tạo mới, trả về `201 Created`).
     * `GET /api/v1/products/{id}` (Chi tiết, trả về `200` hoặc `404`).
     * `PUT /api/v1/products/{id}` (Cập nhật).
     * `DELETE /api/v1/products/{id}` (Xóa mềm hoặc xóa cứng, trả về `204 No Content`).
* **3h - Tạo PR:** Nhánh `feature/product-crud-layered`.

### 📋 Tiêu chuẩn hoàn thành (DoD):
- [ ] Trong file router không xuất hiện bất kỳ dòng code `db.query()` hoặc `db.add()`.
- [ ] Toàn bộ response trả về đều thông qua Pydantic `response_model`.
- [ ] Test toàn bộ các API hoạt động thành công trên Swagger UI.

---

## 📌 TUẦN 4: Validation Nâng cao, Error Handling, Pagination & Filter

### 🎯 Mục tiêu:
* Kiểm soát chặt chẽ tính toàn vẹn của dữ liệu đầu vào bằng Pydantic validators.
* Xây dựng cơ chế bắt lỗi tập trung (Global Exception Handling) để trả về định dạng JSON chuẩn.
* Xây dựng API danh sách hỗ trợ phân trang (Pagination), tìm kiếm (Search) và lọc (Filter).

### ⏱️ Phân bổ thời gian (12h):
* **3h - Lý thuyết:** Các chuẩn thiết kế API Pagination (Offset-based vs Cursor-based), Custom Exception trong Python, HTTP Status Codes (400, 404, 422, 500).
* **6h - Thực hành:**
  1. Thêm validation cho Pydantic schemas:
     * Tên sản phẩm không được chỉ chứa khoảng trắng.
     * Giá bán `price > 0`, số lượng tồn kho `stock_quantity >= 0`.
  2. Viết Custom Exceptions: `AppException`, `NotFoundException`, `BadRequestException`.
  3. Đăng ký `@app.exception_handler` trong `main.py` để định dạng lỗi theo chuẩn:
     `{"success": false, "error_code": "...", "message": "...", "details": ...}`.
  4. Nâng cấp API `GET /api/v1/products`:
     * Query params: `page` (mặc định 1), `page_size` (mặc định 10, tối đa 100).
     * Filter: `category_id` (tùy chọn), `search` (tìm tương đối theo tên sản phẩm: `ILIKE %search%`).
     * Response trả về cấu trúc gồm `items`, `total`, `page`, `page_size`, `total_pages`.
* **3h - Tạo PR:** Nhánh `feature/validation-error-handling-pagination`.

### 📋 Tiêu chuẩn hoàn thành (DoD):
- [ ] Khi nhập `page_size=1000` hoặc giá trị âm, Pydantic tự bắt lỗi `422`.
- [ ] Khi tìm kiếm `id` không tồn tại, API trả về JSON chuẩn lỗi 404, không crash 500.
- [ ] Phân trang trả đúng tổng số bản ghi (`total`) và số trang tương ứng.

---

## 📌 TUẦN 5: Authentication & Phân quyền RBAC (JWT, Bcrypt, Roles)

### 🎯 Mục tiêu:
* Hiểu cơ chế Stateless Authentication với JSON Web Token (JWT).
* Nắm vững kỹ thuật băm mật khẩu một chiều (One-way hashing with Salt).
* Cài đặt cơ chế bảo vệ endpoint và phân quyền người dùng (Role-Based Access Control) qua FastAPI Dependency Injection.

### ⏱️ Phân bổ thời gian (12h):
* **3h - Lý thuyết:** Cơ chế hoạt động của JWT (Header, Payload, Signature), Access Token vs Refresh Token, Nguyên lý băm mật khẩu (Bcrypt/Argon2).
* **6h - Thực hành:**
  1. Cài đặt thư viện: `passlib[bcrypt]`, `python-jose[cryptography]`.
  2. Viết module `core/security.py`: hàm hash mật khẩu, verify mật khẩu, tạo access token có thời hạn (ví dụ: 60 phút).
  3. Viết API xác thực trong `api/v1/endpoints/auth.py`:
     * `POST /api/v1/auth/register`: Đăng ký tài khoản khách hàng mới.
     * `POST /api/v1/auth/login`: Xác thực email/password, trả về Bearer JWT token.
  4. Viết Dependency `get_current_user`: giải mã JWT từ header `Authorization: Bearer <token>`, tìm user trong DB.
  5. Viết Permission Dependency `require_roles(["admin"])`:
     * Áp dụng để bảo vệ các API thay đổi dữ liệu sản phẩm (`POST`, `PUT`, `DELETE /api/v1/products` chỉ admin mới được gọi; khách hàng thường chỉ được xem `GET`).
* **3h - Tạo PR:** Nhánh `feature/auth-jwt-rbac`.

### 📋 Tiêu chuẩn hoàn thành (DoD):
- [ ] Mật khẩu trong PostgreSQL được băm dạng `$2b$...`, không thể đọc được mật khẩu gốc.
- [ ] Đăng nhập đúng trả về Token; đăng nhập sai trả về `401 Unauthorized`.
- [ ] Dùng tài khoản role `customer` gọi API tạo sản phẩm sẽ nhận mã lỗi `403 Forbidden`.

---

## 📌 TUẦN 6: Quan hệ Dữ liệu Nâng cao & Database Transaction (Order API)

### 🎯 Mục tiêu:
* Nắm vững nguyên lý ACID của cơ sở dữ liệu quan hệ.
* Hiểu rủi ro mất mát dữ liệu nếu không dùng Database Transaction.
* Xây dựng nghiệp vụ phức tạp: Đặt hàng, tính tổng tiền, kiểm tra và trừ tồn kho tự động.

### ⏱️ Phân bổ thời gian (12h):
* **3h - Lý thuyết:** Tính chất ACID (Atomicity, Consistency, Isolation, Durability), Vấn đề N+1 Query trong ORM và kỹ thuật Eager Loading (`joinedload`/`selectinload`).
* **6h - Thực hành:**
  1. Tạo Models và Alembic migration cho 2 bảng:
     * `orders`: `id`, `user_id`, `total_amount`, `status` (PENDING, PAID, CANCELLED), `created_at`.
     * `order_items`: `id`, `order_id`, `product_id`, `quantity`, `unit_price`.
  2. Viết Schema `OrderCreate`: nhận danh sách `items: [{"product_id": 1, "quantity": 2}, ...]`.
  3. Viết nghiệp vụ tạo đơn hàng trong `OrderService` bọc trong **1 Transaction duy nhất**:
     * Duyệt qua từng sản phẩm: kiểm tra sản phẩm có tồn tại và còn đủ số lượng không.
     * Trừ `stock_quantity` của sản phẩm tương ứng.
     * Tính tổng tiền dựa trên giá hiện tại của sản phẩm trong DB (không tin giá client gửi lên).
     * Tạo bản ghi `order` và danh sách `order_items`.
     * Gọi `db.commit()` nếu tất cả thành công. Nếu bất kỳ sản phẩm nào thiếu hàng, lập tức `db.rollback()` và ném lỗi `BadRequestException`.
  4. Viết API:
     * `POST /api/v1/orders`: Đặt hàng (Customer).
     * `GET /api/v1/orders/my-orders`: Xem lịch sử đơn hàng của chính user đang đăng nhập.
* **3h - Tạo PR:** Nhánh `feature/order-management-transaction`.

### 📋 Tiêu chuẩn hoàn thành (DoD):
- [ ] Test trường hợp đặt 2 món đồ: món 1 còn hàng, món 2 hết hàng -> Verify trong DB món 1 **không bị trừ tồn kho** (Transaction rollback thành công).
- [ ] API lấy chi tiết đơn hàng load kèm toàn bộ `order_items` chỉ bằng 1 hoặc 2 query tối ưu, không bị N+1.

---

## 📌 TUẦN 7: Pytest (Unit/Integration Test) & Dockerize Toàn bộ Ứng dụng

### 🎯 Mục tiêu:
* Hình thành thói quen viết kiểm thử tự động (Automated Testing) trước khi giao sản phẩm.
* Sử dụng `TestClient` và `pytest` để kiểm thử API endpoints.
* Đóng gói toàn bộ ứng dụng bằng `Dockerfile` và cấu hình `docker-compose.yml` để 1 lệnh khởi chạy toàn bộ hệ thống.

### ⏱️ Phân bổ thời gian (12h):
* **3h - Lý thuyết:** Kim tự tháp kiểm thử (Test Pyramid), Pytest fixtures, Multi-stage build trong Docker.
* **6h - Thực hành:**
  1. Cấu hình Pytest trong thư mục `tests/`:
     * Tạo `conftest.py` thiết lập Database test riêng biệt (hoặc SQLite in-memory).
     * Viết fixture tạo tài khoản test, fixture sinh token đăng nhập của admin và customer.
  2. Viết các test suites:
     * `test_auth.py`: Test đăng ký thành công, đăng ký trùng email, đăng nhập sai pass.
     * `test_products.py`: Test tạo sản phẩm bằng tài khoản admin (thành công) và customer (bị 403).
     * `test_orders.py`: Test đặt hàng trừ kho và test rollback khi hết hàng.
  3. Viết `Dockerfile` tối ưu (multi-stage build, non-root user).
  4. Cập nhật `docker-compose.yml`:
     * Service `db`: PostgreSQL.
     * Service `api`: Build từ Dockerfile, tự động chạy `alembic upgrade head` rồi start `uvicorn`.
* **3h - Tạo PR:** Nhánh `feature/testing-and-dockerization`.

### 📋 Tiêu chuẩn hoàn thành (DoD):
- [ ] Chạy lệnh `pytest` ở máy local: Tất cả bài test đều màu xanh (PASS 100%).
- [ ] Clone repo sang một thư mục trống khác, chỉ cần gõ `docker compose up --build` là ứng dụng tự migrate DB và phục vụ API sẵn sàng.

---

## 📌 TUẦN 8: Mock Onboarding Sprint (Nghiệm thu & Sẵn sàng gia nhập dự án)

### 🎯 Mục tiêu:
* Đóng vai một kỹ sư Backend chính thức trong một Sprint thật: tự đọc yêu cầu (User Story / Bug Report), tự ước lượng thời gian (estimate), tự code và bảo vệ sản phẩm trước Tech Lead.

### ⏱️ Phân bổ thời gian (12h):
Mentor giao 2 nhiệm vụ độc lập mô phỏng thực tế:

#### Task 1 (Feature Task - 7h):
* **Yêu cầu:** Khách hàng yêu cầu thêm tính năng thống kê báo cáo cho Admin.
* **Đặc tả API:** `GET /api/v1/analytics/dashboard` (Chỉ Admin có quyền gọi).
* **Dữ liệu trả về:**
  * Tổng số khách hàng đăng ký (`total_customers`).
  * Tổng số đơn hàng đã hoàn thành (`total_orders`).
  * Tổng doanh thu (`total_revenue`).
  * Top 5 sản phẩm bán chạy nhất.
* **Yêu cầu kỹ thuật:** Viết câu truy vấn tổng hợp (Aggregation: `COUNT`, `SUM`, `GROUP BY`) tối ưu bằng SQLAlchemy, không load toàn bộ dữ liệu lên Python rồi tính bằng vòng lặp `for`.

#### Task 2 (Bug Fix Task - 3h):
* **Báo cáo lỗi (Issue):** Khách hàng báo lỗi khi tìm kiếm sản phẩm chứa các ký tự đặc biệt như dấu `%`, `_` hoặc dấu nháy `'`, hệ thống bị lỗi cú pháp SQL hoặc trả về toàn bộ dữ liệu sai mong muốn.
* **Nhiệm vụ:** Tìm hiểu nguyên nhân (SQL Injection rủi ro hoặc lỗi escape ký tự wildcard trong câu lệnh `ILIKE`), sửa lỗi trong Repository và bổ sung ít nhất 1 test case trong `tests/test_products.py` để phòng ngừa tái phát.

#### Bàn giao & Nghiệm thu (2h):
* Mở 2 Pull Request tương ứng cho từng task theo đúng quy chuẩn Centic.
* Chuẩn bị slide hoặc kịch bản trình bày tóm tắt toàn bộ thành quả 8 tuần trong buổi Checkpoint cuối cùng.

### 📋 Tiêu chuẩn tốt nghiệp chương trình đào tạo:
- [ ] Toàn bộ 8 Pull Request trong 8 tuần đều được review và merge vào nhánh `develop`.
- [ ] Hoàn thành cả 2 task của Tuần 8 đúng hạn.
- [ ] Trả lời tốt buổi Vấn đáp Tổng kết (Final Sign-off) cùng Mentor.
