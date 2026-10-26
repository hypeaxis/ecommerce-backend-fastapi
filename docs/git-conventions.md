# Quy chuẩn Git & GitHub (Centic GitHub Conventions)

Tài liệu này tóm tắt các quy chuẩn bắt buộc khi làm việc với Git và GitHub trong quá trình thực tập, bám sát theo [Centic GitHub Conventions](https://github.com/Centic-io/centic-github-conventions).

---

## 1. Đặt tên Repository
* Tên repository viết ở dạng `kebab-case` (chữ thường, ngăn cách bằng dấu gạch ngang `-`).
* Khi tạo repo mới phải có `description` tóm tắt ngắn gọn mục đích dự án.
* Ví dụ:
  * ✅ Hợp lệ: `intern-backend-training`, `ecommerce-order-api`
  * ❌ Không hợp lệ: `InternBackendTraining`, `intern_backend_training`

---

## 2. Quy tắc Nhánh (Branching Strategy)

### 2.1. Nhánh chính (Main Branches)
* `main`: Chứa mã nguồn ổn định nhất, sẵn sàng release.
* `develop`: Nhánh tích hợp mã nguồn của tất cả các tính năng đang phát triển.
* **Quy tắc bắt buộc:** Chỉ có **Admin / Lead** mới có quyền push hoặc merge trực tiếp vào `main` và `develop`. Mọi thay đổi của thực tập sinh đều phải thông qua **Pull Request (PR)**.

### 2.2. Nhánh hỗ trợ (Supporting Branches)
Thực tập sinh tạo nhánh từ `develop` theo tiền tố sau:
* **Nhánh Feature:** `feature/<tên-tính-năng>`
  * Ví dụ: `feature/setup-docker-postgres`, `feature/user-auth-jwt`, `feature/product-crud`
* **Nhánh Bugfix/Issue:** `issue/<mã-hoặc-tên-lỗi>`
  * Ví dụ: `issue/fix-special-char-search`
* **Nhánh Hotfix:** `hotfix/<tên-lỗi>` (chỉ tạo khi sửa lỗi khẩn cấp trên `main`).

---

## 3. Quy chuẩn Commit

### 3.1. Tính nguyên tử (Atomic Commit)
* Mỗi commit **chỉ giải quyết một đơn vị công việc (meaningful-unit-of-work) duy nhất**.
* Không gộp nhiều việc không liên quan vào cùng một commit (ví dụ: vừa sửa schema database vừa sửa giao diện Swagger docs trong 1 commit là vi phạm).
* Nếu cần format code, xóa khoảng trắng thừa, tái cấu trúc (refactor), hãy dành riêng 1 commit độc lập cho việc đó.

### 3.2. Không đưa dữ liệu nhạy cảm & file rác lên Git
Thực tập sinh phải đảm bảo file `.gitignore` chứa đầy đủ:
* File biến môi trường: `.env` (chứa mật khẩu DB, secret key JWT,...). Thay vào đó, commit file `.env.example`.
* Môi trường ảo Python: `venv/`, `.venv/`, `env/`.
* Cache Python: `__pycache__/`, `*.pyc`.
* Cấu hình editor / IDE: `.vscode/`, `.idea/`.
* File hệ điều hành: `.DS_Store`, `Thumbs.db`.

> **Lưu ý:** Với Python, khi cài bất kỳ thư viện mới nào (`pip install ...`), bắt buộc phải cập nhật ngay vào `requirements.txt` trong cùng commit đó.

### 3.3. Commit Message
Commit message được viết như một văn bản rõ ràng, chuyên nghiệp:
* **Dòng đầu tiên (Summary):**
  * Dưới 72 ký tự.
  * Sử dụng **câu mệnh lệnh ở thì hiện tại** (Imperative mood).
  * Viết bằng tiếng Anh chuẩn.
  * Không kết thúc bằng dấu chấm câu.
* **Dòng thân (Body - tùy chọn):**
  * Cách dòng Summary bằng **một dòng trống**.
  * Giải thích chi tiết "Tại sao thay đổi?" nếu cần thiết.

#### Ví dụ chuẩn:
```text
Add product pagination and category filtering

- Support page and page_size query parameters
- Add category_id optional filter
- Update OpenAPI schema documentation
```

#### So sánh nhanh:
* ✅ Hợp lệ:
  * `Add user authentication endpoints`
  * `Fix crash when searching products with percent symbol`
  * `Update SQLAlchemy relationship for order items`
* ❌ Không hợp lệ:
  * `Added user authentication` (sai thì - không dùng quá khứ)
  * `I fixed the search bug` (không dùng đại từ nhân xưng)
  * `fix bug` (quá ngắn, không có ý nghĩa)
  * `update code` (vô nghĩa)

---

## 4. Quy trình Mở Pull Request (PR)

1. Trước khi mở PR, kéo code mới nhất từ `develop` về nhánh của mình và resolve conflict (nếu có):
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/<tên-nhánh>
   git merge develop
   ```
2. Đẩy nhánh lên remote:
   ```bash
   git push origin feature/<tên-nhánh>
   ```
3. Tạo PR trên GitHub hướng vào nhánh `develop`.
4. Tiêu đề PR rõ ràng, ví dụ: `[Feature] Implement User Authentication with JWT`.
5. Điền đầy đủ PR Template:
   ```markdown
   ## 📝 Mục tiêu PR
   Mô tả ngắn gọn tính năng hoặc lỗi được xử lý.

   ## 🛠️ Những thay đổi chính
   - Thêm API POST /api/v1/auth/login và POST /api/v1/auth/register
   - Bổ sung bảng users trong PostgreSQL và migration Alembic
   - Băm mật khẩu bằng bcrypt

   ## 🧪 Bằng chứng kiểm thử (Evidence)
   - [x] Pytest pass toàn bộ: (đính kèm ảnh chụp màn hình terminal)
   - [x] Swagger UI gọi thành công: (đính kèm ảnh chụp kết quả API)
   ```
6. Gán reviewer (Mentor) và đợi phản hồi. Tuyệt đối không tự ý merge khi chưa có phê duyệt (Approve).
