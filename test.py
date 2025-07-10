import fitz  # this comes from pymupdf

doc = fitz.open("chatbot ollama/CV unit 3.pdf")  # Use your file path here
print(f"Loaded {len(doc)} pages.")
