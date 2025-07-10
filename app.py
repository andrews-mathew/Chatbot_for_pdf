import streamlit as st
import fitz  # PyMuPDF
from docx import Document
import ollama
import mimetypes

# ---------- Helper Functions ----------

def extract_text_from_pdf(uploaded_file):
    try:
        uploaded_file.seek(0)  # Reset stream
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        return text.strip()
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")
        return ""

def extract_text_from_docx(uploaded_file):
    try:
        uploaded_file.seek(0)
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        st.error(f"❌ Error reading DOCX: {e}")
        return ""

def ask_llm(prompt, context):
    full_prompt = f"Answer the following question based only on the context below:\n\nContext:\n{context}\n\nQuestion:\n{prompt}"
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"❌ LLM error: {e}"

# ---------- Streamlit UI ----------

st.set_page_config(page_title="📄 Local LLM Doc Chatbot", layout="wide")
st.title("📄 Chat with Your Document using Local LLM")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    file_type, _ = mimetypes.guess_type(uploaded_file.name)
    st.write(f"📁 **Uploaded:** `{uploaded_file.name}` | `{file_type}`")

    with st.spinner("🔍 Extracting content..."):
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format.")
            text = ""

    if text:
        st.success("✅ Document content loaded!")

        query = st.text_input("💬 Ask a question about the document:")
        if query:
            with st.spinner("🤖 Thinking..."):
                answer = ask_llm(query, text[:4000])  # Limit context for local models
                st.markdown(f"**🧠 Answer:** {answer}")
    else:
        st.warning("⚠️ Could not extract any content from the file.")
else:
    st.info("📂 Please upload a `.pdf` or `.docx` file to get started.")
