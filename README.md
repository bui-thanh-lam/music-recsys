# music-recsys
Folder db:
- Chứa file backup .sql cho db của app mình (tạm thời dùng cách này trong thời gian Nam đẩy lên host)
- File repository.py: Viết các query cần thiết vào đây
- File dbconfig: Config kết nối với db (mọi người tự điền đường dẫn trong máy mình, add vào .gitignore)

Folder apis: (import db.repository)
- recommenders: Chứa các thuật toán gợi ý (WMF, cold-start...)
- search: Chứa các thuật toán search
- ...

Lưu ý chung:
- Thống nhất với nhau về cách trả về, khuôn dạng dữ liệu
- Dùng virtualenv. Nếu cần cài thêm thư viện gì, nhớ pip freeze > requirements.txt để mọi người pull về thì cài theo. Không push cả venv lên repo này


# Khuôn dạng dữ liệu
