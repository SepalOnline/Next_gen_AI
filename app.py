import os, sys, json, subprocess
import streamlit as st

st.set_page_config(page_title="Hệ thống Dự đoán Cảm xúc", page_icon="🎭", layout="centered")

label_dict = {
    0: ("Tiêu cực", "😡"),
    1: ("Trung tính", "😐"),
    2: ("Tích cực", "😍")
}

st.title("🎭 Hệ thống Dự đoán Cảm xúc Văn bản")
st.markdown("**Đề tài:** Ứng dụng PhoBERT phân loại cảm xúc phản hồi (Khen/Chê/Trung tính).")
st.markdown("---")

user_input = st.text_area("✍️ Nhập văn bản cần dự đoán:", height=100,
                           placeholder="Ví dụ: Thầy dạy rất nhiệt tình nhưng slide hơi khó nhìn...")

if st.button("🚀 Dự đoán cảm xúc", use_container_width=True):
    if user_input.strip() == "":
        st.warning("⚠️ Vui lòng nhập văn bản trước khi dự đoán!")
    else:
        with st.spinner('🤖 Đang phân tích... (khoảng 10-20 giây)'):
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                predict_script = os.path.join(current_dir, "predict.py")
                
                # Gọi predict.py trong process riêng biệt hoàn toàn
                result = subprocess.run(
                    [sys.executable, predict_script, user_input],
                    capture_output=True, text=True, timeout=60,
                    cwd=current_dir
                )
                
                if result.returncode != 0:
                    st.error(f"❌ Lỗi khi dự đoán:\n{result.stderr}")
                else:
                    # Lấy dòng JSON cuối cùng trong output
                    output_lines = [l for l in result.stdout.strip().split('\n') if l.startswith('{')]
                    data = json.loads(output_lines[-1])
                    
                    predicted = data["predicted"]
                    probs = data["probs"]
                    label_name, icon = label_dict[predicted]
                    
                    st.markdown("### 📊 Kết quả dự đoán:")
                    if predicted == 2:
                        st.success(f"**{icon} {label_name}**")
                    elif predicted == 0:
                        st.error(f"**{icon} {label_name}**")
                    else:
                        st.info(f"**{icon} {label_name}**")
                    
                    st.markdown("---")
                    st.markdown("**Xác suất dự đoán của mô hình:**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("😡 **Tiêu cực**")
                        st.progress(float(probs[0]))
                        st.caption(f"{probs[0]*100:.2f}%")
                    with col2:
                        st.markdown("😐 **Trung tính**")
                        st.progress(float(probs[1]))
                        st.caption(f"{probs[1]*100:.2f}%")
                    with col3:
                        st.markdown("😍 **Tích cực**")
                        st.progress(float(probs[2]))
                        st.caption(f"{probs[2]*100:.2f}%")
                        
            except subprocess.TimeoutExpired:
                st.error("⏱️ Quá thời gian chờ! Thử lại nhé.")
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")