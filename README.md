# music-recsys
Folder db:
- Chứa file backup .sql cho db
- File repository.py: Viết các query cần thiết vào đây
- File ConnectDatabase đã điền đầy đủ thông tin host, có thể kết nối và chạy luôn, không cần chỉnh sửa sang local.
    Nhưng tốc độ có lẽ hơi chậm một chút, muốn nhanh thì dùng local sẽ nhanh hơn.

Folder apis: (import db.repository)
- recommenders: Chứa các thuật toán gợi ý (WMF, cold-start...)
- search: Chứa các thuật toán search
- ...

Lưu ý chung:
- Thống nhất với nhau về cách trả về, khuôn dạng dữ liệu
- Dùng virtualenv. Nếu cần cài thêm thư viện gì, nhớ pip freeze > requirements.txt để mọi người pull về thì cài theo. Không push cả venv lên repo này

# Khuôn dạng dữ liệu
