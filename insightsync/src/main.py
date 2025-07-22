from transformers import pipeline
import pdfplumber

# 1. Load your document
pdf_path = "/Users/rachael/Downloads/Resume_RachaelTan(2025-Updated).pdf"
with pdfplumber.open(pdf_path) as pdf:
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:  # Avoid NoneType errors
            text += page_text + "\n"

# 2. Try to extract just the 'Education' section (case-insensitive)
education_section = ""
lower_text = text.lower()
start_keyword = "education"
end_keywords = ["experience", "projects", "skills", "certification", "work", "achievement"]

start_idx = lower_text.find(start_keyword)
if start_idx != -1:
    # Try to find the next major section header
    end_idx = len(text)
    for end_key in end_keywords:
        idx = lower_text.find(end_key, start_idx + len(start_keyword))
        if idx != -1 and idx < end_idx:
            end_idx = idx
    education_section = text[start_idx:end_idx].strip()
else:
    education_section = ""  # fallback if not found

# Fallback: Use full text if education section wasn't found
context = education_section if education_section else text

print("=== Education Section Used For QA ===")
print(context)
print("=" * 50)

# 3. Create the question-answering pipeline (use a strong model)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# 4. Ask your question (be specific)
question = "What diploma did Rachael Tan achieve in the education section of the resume?"

# 5. Run QA
result = qa_pipeline(question=question, context=context)
print("Best Answer:", result['answer'])


