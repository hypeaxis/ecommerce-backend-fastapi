# E-Commerce API (Starter Template Dành Cho Thực Tập Sinh)

Chào mừng bạn đến với chương trình đào tạo Thực tập sinh Backend! Đây là repository khởi đầu trọn gói dành cho bạn.

---

## 📚 TÀI LIỆU QUAN TRỌNG (BẮT BUỘC ĐỌC TRƯỚC KHI CODE)

Toàn bộ giáo trình và quy chuẩn kỹ thuật đã được đóng gói sẵn trong thư mục `docs/`:
1. 📖 **[docs/curriculum.md](docs/curriculum.md):** Giáo trình chi tiết nhiệm vụ từng tuần (từ Tuần 1 đến Tuần 8).
2. 🌿 **[docs/git-conventions.md](docs/git-conventions.md):** Quy chuẩn Git bắt buộc (cách đặt tên nhánh, commit nguyên tử, template PR).
3. 🏛️ **[docs/architecture-guidelines.md](docs/architecture-guidelines.md):** Hướng dẫn Kiến trúc 3 tầng (Router -> Service -> Repository) và chuẩn RESTful API.

---

## 🛠️ Hướng dẫn Bắt đầu (Tuần 1)

### 1. Khởi tạo Git cá nhân
Sau khi nhận thư mục này, hãy khởi tạo Git trên máy của bạn và push lên GitHub cá nhân:
```bash
git init
git add .
git commit -m "Initialize starter project"
```

### 2. Cấu hình biến môi trường
Tạo file `.env` từ file mẫu:
```bash
cp .env.example .env
```

### 3. Khởi chạy PostgreSQL qua Docker Compose
```bash
docker compose up -d db
```

### 4. Tạo môi trường ảo Python và cài đặt thư viện
```bash
# Tạo virtualenv
python -m venv venv

# Kích hoạt trên Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Kích hoạt trên Linux/MacOS:
source venv/bin/activate

# Cài đặt dependencies:
pip install -r requirements.txt
```

### 5. Khởi chạy Server phát triển
```bash
uvicorn app.main:app --reload --port 8000
```
Truy cập tài liệu Swagger UI tại: [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Chạy kiểm thử tự động
```bash
pytest
```

---

## 📋 Tóm tắt Nhiệm vụ 8 Tuần

* **Tuần 1:** Setup môi trường, chạy Docker, tạo branch `feature/setup-project`, mở PR đầu tiên.
* **Tuần 2:** Thiết kế models trong `app/models/` và sinh migration bằng Alembic (`alembic revision --autogenerate`).
* **Tuần 3 & 4:** Viết Schemas, Repository, Service và Router cho `Category` và `Product` theo kiến trúc 3 tầng.
* **Tuần 5:** Xây dựng module xác thực Authentication (JWT, Bcrypt) trong `app/services/user_service.py` và bảo vệ API bằng `Depends`.
* **Tuần 6:** Viết tính năng đặt hàng `Order` với Database Transaction đảm bảo ACID trong `app/services/order_service.py`.
* **Tuần 7:** Viết Unit/Integration Test trong thư mục `tests/` và đóng gói Dockerfile hoàn chỉnh.
* **Tuần 8:** Nhận task Mock Sprint và nghiệm thu tốt nghiệp.
