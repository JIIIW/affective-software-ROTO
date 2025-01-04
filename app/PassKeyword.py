import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from konlpy.tag import Okt

# 파일 변환: PDF -> Excel
def pdf_to_excel(pdf_path, excel_path):
    reader = PdfReader(pdf_path)
    data = [page.extract_text() for page in reader.pages]
    df = pd.DataFrame({'Content': data})
    df.to_excel(excel_path, index=False)

# 파일 변환: Word -> Excel
def word_to_excel(word_path, excel_path):
    doc = Document(word_path)
    data = [para.text for para in doc.paragraphs]
    df = pd.DataFrame({'Content': data})
    df.to_excel(excel_path, index=False)

# 테스트 데이터 전처리
def preprocess_test_data(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    temp_excel_path = "temp_output.xlsx"

    if ext == ".pdf":
        pdf_to_excel(file_path, temp_excel_path)
    elif ext == ".docx":
        word_to_excel(file_path, temp_excel_path)
    elif ext == ".xlsx":
        temp_excel_path = file_path
    else:
        raise ValueError("지원되지 않는 파일 형식입니다.")

    data = pd.read_excel(temp_excel_path)
    data_combined = data.apply(lambda row: " ".join(row.dropna().astype(str)), axis=1)
    data_combined = data_combined.replace(r"[^가-힣A-Za-z ]", "", regex=True)
    data_combined = data_combined.str.strip()
    data_combined = data_combined[data_combined != ""].reset_index(drop=True)
    return data_combined

# TF-IDF 및 코사인 유사도 계산
def tfidf_cosine_similarity(tokenized_file, test_data):
    with open(tokenized_file, 'r', encoding='utf-8') as f:
        tokenized_data = [line.strip() for line in f.readlines()]

    all_tokens = [word for line in tokenized_data for word in line.split()]
    train_word_counts = Counter(word for word in all_tokens if len(word) >= 2)

    okt = Okt()
    test_tokens = []
    for text in test_data:
        english_part = re.findall(r'[A-Za-z]+', text)
        korean_part = re.findall(r'[가-힣]+', text)

        test_tokens.extend(re.findall(r"\b\w+\b", " ".join(english_part)))
        test_tokens.extend([word for word in okt.nouns(" ".join(korean_part)) if len(word) >= 2])

    vectorizer = TfidfVectorizer(lowercase=False)
    X_train = vectorizer.fit_transform([" ".join(all_tokens)])
    X_test = vectorizer.transform([" ".join(test_tokens)])

    similarity = cosine_similarity(X_test, X_train)
    return similarity.mean()

# 파일 업로드 없이 코사인 유사도 점수 및 등급 계산
def evaluate_resume(file_path, tokenized_file):
    try:
        # 파일 전처리
        test_data = preprocess_test_data(file_path)

        # TF-IDF 및 코사인 유사도 계산
        similarity_score = tfidf_cosine_similarity(tokenized_file, test_data)

        # 점수 해석
        grade = "A" if similarity_score >= 0.6 else \
                "B" if similarity_score >= 0.4 else \
                "C" if similarity_score >= 0.2 else \
                "D" if similarity_score >= 0.1 else "E"

        return {"similarity_score": similarity_score, "grade": grade}

    except Exception as e:
        raise ValueError(f"오류 발생: {str(e)}")