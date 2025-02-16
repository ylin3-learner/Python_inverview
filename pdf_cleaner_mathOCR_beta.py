import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
import os
import re

# 設定 Tesseract OCR 路徑（根據實際情況修改）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 可配置的 watermark 關鍵字列表
WATERMARK_KEYWORDS = ["微信公众号", "张巍老师"]

# 可配置的數學符號關鍵字，用來檢測頁面是否包含數學公式
MATH_SYMBOLS = ["$", "∑", "∫", "√", "π", "×", "÷", "=", "+", "-", "*", "/", "^"]

def extract_page_text_pymupdf(doc, page_index):
    """從指定頁使用 PyMuPDF 提取文字"""
    page = doc[page_index]
    text = page.get_text("text").strip()
    return text

def preprocess_image(image):
    """
    影像預處理：
      1. 灰階轉換
      2. Otsu 自適應二值化
      3. 降噪處理
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
    return denoised

def remove_watermark_lines(text):
    """
    後處理：過濾掉包含 watermark 關鍵字的行
    """
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if any(keyword in line for keyword in WATERMARK_KEYWORDS) or len(line.strip()) < 3:
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def is_effective_text(text, min_words=10):
    """
    判斷提取結果是否有效：
      - 如果文字空或單詞數過少，則效果不佳
      - 或者若大部分行都是 watermark，則效果不佳
    """
    if not text:
        return False
    words = text.split()
    if len(words) < min_words:
        return False
    lines = text.splitlines()
    if not lines:
        return False
    watermark_count = sum(1 for line in lines if any(keyword in line for keyword in WATERMARK_KEYWORDS))
    if watermark_count / len(lines) > 0.5:
        return False
    return True

def extract_page_text_ocr(pdf_path, page_index):
    """
    使用 OCR 提取指定頁文字：
      1. 利用 pdf2image 轉換單頁為圖片
      2. 進行影像預處理與 Tesseract OCR 辨識
    """
    images = convert_from_path(pdf_path, dpi=300, first_page=page_index+1, last_page=page_index+1)
    if not images:
        return ""
    pil_img = images[0]
    open_cv_image = np.array(pil_img)[:, :, ::-1].copy()  # PIL -> OpenCV (BGR)
    processed_image = preprocess_image(open_cv_image)
    pil_image = Image.fromarray(processed_image)
    text = pytesseract.image_to_string(pil_image, lang='eng+chi_sim', config="--oem 3 --psm 6")
    return text.strip()

def has_math_content(text):
    """
    檢查文字中是否包含數學符號：
    如果出現的數學符號總數超過一定閾值（例如 3 個），則認定該頁包含數學公式
    """
    count = 0
    for sym in MATH_SYMBOLS:
        count += text.count(sym)
    return count >= 3

def extract_page_text_latex(pdf_path, page_index):
    """
    使用 LatexOCR（pix2tex）對指定頁圖片進行數學公式辨識，
    將數學公式轉換為 LaTeX 表達式
    """
    images = convert_from_path(pdf_path, dpi=300, first_page=page_index+1, last_page=page_index+1)
    if not images:
        return ""
    pil_img = images[0]
    from pix2tex.cli import LatexOCR
    model = LatexOCR()
    latex_text = model(pil_img)
    return latex_text.strip()

def process_page(pdf_path, doc, page_index):
    """
    處理單一頁：
      1. 優先使用 PyMuPDF 提取文字
      2. 若效果不佳則用 OCR 提取
      3. 後處理剔除 watermark 行
      4. 若檢測到數學內容，則調用 LatexOCR 進行數學公式辨識，
         並將 LaTeX 結果附加到該頁文字中
    """
    text = extract_page_text_pymupdf(doc, page_index)
    if not is_effective_text(text):
        print(f"⚠️ 第 {page_index+1} 頁 PyMuPDF 提取效果不佳，改用 OCR...")
        text = extract_page_text_ocr(pdf_path, page_index)
    else:
        print(f"✅ 第 {page_index+1} 頁 PyMuPDF 提取有效")
    text = remove_watermark_lines(text)
    
    if has_math_content(text):
        print(f"🔢 第 {page_index+1} 頁檢測到數學內容，調用 LatexOCR 進行識別...")
        math_text = extract_page_text_latex(pdf_path, page_index)
        if math_text:
            text += "\n----- LaTeX OCR 數學公式 -----\n" + math_text
    return text

def extract_pdf_text(pdf_path):
    """
    主流程：逐頁處理 PDF 並合併結果，第一頁結果會打印出來供檢查
    """
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    all_text = []
    print(f"共 {total_pages} 頁，開始逐頁處理...")
    for i in range(total_pages):
        page_text = process_page(pdf_path, doc, i)
        if i == 0:
            print("----- 第一頁辨識結果 -----")
            print(page_text)
            print("----- 第一頁辨識結果結束 -----")
        if page_text:
            all_text.append(page_text)
    combined_text = "\n".join(all_text).strip()
    return combined_text

if __name__ == "__main__":
    pdf_file = "math.pdf"  # 修改為你的 PDF 文件路徑
    extracted_text = extract_pdf_text(pdf_file)
    
    output_file = "clean_text.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    print("🎉 文字提取完成，結果已儲存至", output_file)
