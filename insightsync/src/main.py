#1. ROBERTA

# from transformers import pipeline
# import pdfplumber

# # 1. Load your document
# pdf_path = "/Users/rachael/Downloads/Resume_RachaelTan(2025-Updated).pdf"
# with pdfplumber.open(pdf_path) as pdf:
#     text = ""
#     for page in pdf.pages:
#         page_text = page.extract_text()
#         if page_text:  # Avoid NoneType errors
#             text += page_text + "\n"

# # 2. Try to extract just the 'Education' section (case-insensitive)
# education_section = ""
# lower_text = text.lower()
# start_keyword = "education"
# end_keywords = ["experience", "projects", "skills", "certification", "work", "achievement"]

# start_idx = lower_text.find(start_keyword)
# if start_idx != -1:
#     # Try to find the next major section header
#     end_idx = len(text)
#     for end_key in end_keywords:
#         idx = lower_text.find(end_key, start_idx + len(start_keyword))
#         if idx != -1 and idx < end_idx:
#             end_idx = idx
#     education_section = text[start_idx:end_idx].strip()
#     j

# else:
#     education_section = ""  # fallback if not found

# # Fallback: Use full text if education section wasn't found
# context = education_section if education_section else text

# print("=== Education Section Used For QA ===")
# print(context)
# print("=" * 50)

# # 3. Create the question-answering pipeline (use a strong model)
# qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# # 4. Ask your question (be specific)
# question = "What diploma did Rachael Tan achieve in the education section of the resume?"

# # 5. Run QA
# result = qa_pipeline(question=question, context=context)
# print("Best Answer:", result['answer'])


#2. BERT
# from transformers import pipeline
# import pdfplumber
# import re

# pdf_path = "/Users/rachael/Downloads/Resume_RachaelTan(2025-Updated).pdf"
# # 1. Load the PDF document as text
# with pdfplumber.open(pdf_path) as pdf:
#     text = ""
#     for page in pdf.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"

# # 2. Auto-detect sections (all-caps headers or Title Case)
# section_pattern = re.compile(r'(^[A-Z][A-Z\s]+$)', re.MULTILINE)
# matches = list(section_pattern.finditer(text))

# sections = []
# for i, match in enumerate(matches):
#     section_name = match.group(1).strip()
#     start = match.end()
#     end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
#     section_text = text[start:end].strip()
#     sections.append((section_name, section_text))

# # 3. Ask the user for a question (or set your own)
# question = input("Ask a question about the document: ")
# qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# # 4. Run QA on each section, pick the best answer
# best_answer = ""
# best_score = 0
# best_section = ""
# for section_name, section_text in sections:
#     if len(section_text.split()) < 10:  # Skip tiny sections
#         continue
#     result = qa_pipeline(question=question, context=section_text)
#     print(f"[{section_name}] Answer: {result['answer']} | Score: {result['score']:.2f}")
#     if result['score'] > best_score:
#         best_score = result['score']
#         best_answer = result['answer']
#         best_section = section_name

# print(f"\nBest Answer: {best_answer} (from section: {best_section}, score: {best_score:.2f})")


#3. Donut (naver-clova-ix/donut-base-finetuned-docvqa)
from pdf2image import convert_from_path
from transformers import DonutProcessor, VisionEncoderDecoderModel

# Convert PDF to PIL Image (no file saved)
pdf_path = "/Users/rachael/Downloads/Resume_RachaelTan(2025-Updated).pdf"
images = convert_from_path(pdf_path, dpi=300)
image = images[0]  # In memory only!

# Process with Donut directly
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")

task_prompt = "<s_docvqa><s_question>What diploma did Rachael Tan achieve?<s_answer>"
inputs = processor(image, task_prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512, early_stopping=True)
result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
print("Donut Answer:", result)

