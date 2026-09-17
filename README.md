# 🎭 Hệ thống Dự đoán Cảm xúc Văn bản bằng PhoBERT

Ứng dụng phân loại cảm xúc phản hồi (Khen/Chê/Trung tính) sử dụng mô hình ngôn ngữ PhoBERT kết hợp với giao diện Streamlit.

## 🚀 Hướng dẫn cài đặt và chạy thử nghiệm

**1. Clone kho lưu trữ về máy:**
bash
git clone https://github.com/SepalOnline/Next_gen_AI.git
cd Next_gen_AI
**2. Tải file trọng số mô hình:**
Vì lý do giới hạn dung lượng của GitHub, file trọng số `model.safetensors` được lưu trữ riêng.
* Tải file tại đây: https://drive.google.com/file/d/1u2B7X9QxSoHXtrIkvf1_PJEIiIs2j7N0/view?usp=sharing
* Đặt file vừa tải vào đúng đường dẫn: `phobert_sentiment_model/model.safetensors`

**3. Cài đặt thư viện:**
bash
pip install -r requirements.txt
**4. Khởi chạy ứng dụng:**
bash
streamlit run app.py
