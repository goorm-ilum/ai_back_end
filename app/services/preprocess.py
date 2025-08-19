import re
import os
import kss

MIN_LEN = 5  # 최소 문장 길이 기준

# 제거할 감탄사/의성어 리스트
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCLAMATION_FILE = os.path.join(BASE_DIR, "../db/exclamations.txt")

with open(EXCLAMATION_FILE, "r", encoding="utf-8") as f:
    EXCLAMATIONS = [line.strip() for line in f if line.strip()]
    
def clean_sentence(sentence):
    # 1) 감탄사 제거
    for excl in EXCLAMATIONS:
        sentence = sentence.replace(excl, "")
    
    # 2) 이모지 제거
    sentence = re.sub(r"[\U00010000-\U0010ffff]", "", sentence)
    
    # 3) 특수문자 제거 (한글, 숫자, 영어 제외)
    sentence = re.sub(r"[^가-힣0-9a-zA-Z\s\.\?\!]", "", sentence)
    
    # 4) 공백 정리
    sentence = re.sub(r"\s+", " ", sentence).strip()
    
    return sentence

def split_and_merge_sentences(text):
    """
    1) KSS로 문장 단위 분리
    2) 짧은 문장은 주변 문장과 병합
    3) 불용어/이모지 제거
    """
    sentences = kss.split_sentences(text)
    merged_sentences = []
    buffer = ""

    for s in sentences:
        s = clean_sentence(s)  # 전처리 적용
        if not s:  # 빈 문자열이면 스킵
            continue

        if len(s) < MIN_LEN:
            buffer += " " + s if buffer else s
        else:
            if buffer:
                merged_sentences.append(buffer + " " + s)
                buffer = ""
            else:
                merged_sentences.append(s)

    if buffer:  # 마지막 버퍼 처리
        merged_sentences.append(buffer)

    return merged_sentences
