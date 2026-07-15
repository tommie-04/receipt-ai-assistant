import streamlit as st

st.title("Receipt AI Assistant")
st.write("Upload a receipt image and let AI extract the amount and category automatically")

upload_file = st.file_uploader("Upload receipt image", type = ["jpg", "jpeg", "png"])

if upload_file is not None:
    st.image(upload_file, caption="Your upload receipt", use_container_width=True)
    st.success("Image upload successfully! Next we'll let AI read it!")