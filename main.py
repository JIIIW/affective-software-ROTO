from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import logging
import PyPDF2
from app.Video2Text import Video2Text
from app.PassKeyword import preprocess_test_data, tfidf_cosine_similarity
from app.resume_analysis import initialize_model, generate_ai_response
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청 허용. 필요하면 특정 도메인으로 제한 가능.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],  # 모든 요청 헤더 허용
)

# 정적 파일 및 템플릿 설정
app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
app.mount("/images", StaticFiles(directory="templates/assets/images"), name="images")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "temp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)

# 모델 초기화
try:
    tokenizer, text_pipeline, PROMPT = initialize_model()
except Exception as e:
    raise RuntimeError(f"모델 로드에 실패했습니다: {e}")

def read_file(file_path, file_extension):
    if file_extension == ".pdf":
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return "".join(page.extract_text() for page in pdf_reader.pages)
    else:
        with open(file_path, "r", encoding="utf-8") as text_file:
            return text_file.read()

class ScoreSummary(BaseModel):
    overallGrade: str
    overallRank: int
    totalApplicants: int
    overallPercent: int
    jobGrade: str
    jobRank: int
    jobApplicants: int
    jobPercent: int
    experienceGrade: str
    experienceMatch: int
    experiencePercent: int
    skillGrade: str
    skillScore: int
    skillPercent: int

class JobFit(BaseModel):
    title: str
    percent: int

class CultureFit(BaseModel):
    percent: int

class RadarChart(BaseModel):
    imageUrl: str

class FinalSummary(BaseModel):
    overallScore: str
    jobFit: str
    cultureFit: str
    skillScore: str
    recommendation: str
    opinionText: str
    strengths: List[str]
    improvementPoint: str
    hireRecommendation: str
    hireReason: str

class AnalysisResults(BaseModel):
    applicantInfo: dict
    scoreSummary: ScoreSummary
    jobFit: List[JobFit]
    cultureFit: List[CultureFit]
    radarChart: RadarChart
    finalSummary: FinalSummary

@app.get("/index.html", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/analysis_report.html", response_class=HTMLResponse)
async def analysis_report(request: Request):
    return templates.TemplateResponse("analysis_report.html", {"request": request})


# 로그 설정
logging.basicConfig(level=logging.INFO)

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        # 파일 크기 제한 (5MB)
        MAX_FILE_SIZE = 5 * 1024 * 1024
        file_size = file.file.seek(0, os.SEEK_END)
        file.file.seek(0)
        logging.info(f"파일 크기: {file_size} bytes")
        if file_size > MAX_FILE_SIZE:
            logging.error("파일 크기 초과")
            return JSONResponse(status_code=400, content={"message": "File size exceeds 5MB limit."})

        # 파일 형식 확인
        logging.info(f"파일 형식: {file.content_type}")
        if file.content_type not in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            logging.error("잘못된 파일 형식")
            return JSONResponse(status_code=400, content={"message": "Invalid file type. Only PDF and DOCX are allowed."})

        # 파일 저장
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # 업로드 디렉터리 생성
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        logging.info(f"파일 저장 위치: {file_location}")
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # 분석 결과 반환 (샘플 데이터)
        logging.info("파일 분석 성공")
        result = {
            "job_fit_score": 85,
            "tech_fit": "전문 기술에 매우 적합",
            "job_fit_graph_url": "https://example.com/job_fit_graph.png",
            "tech_fit_graph_url": "https://example.com/tech_fit_graph.png"
        }
        return result
    except Exception as e:
        logging.error(f"파일 처리 중 오류 발생: {e}")
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file."})

@app.get("/api/get_analysis_results", response_model=AnalysisResults)
async def get_analysis_results():
    return {
        "applicantInfo": {
            "name": "홍길동",
            "recommendation": "매우 추천",
            "id": "hong_gildong@roto.ai",
            "position": "데이터 분석가",
            "location": "서울"
        },
        "scoreSummary": {
            "overallGrade": "A",
            "overallRank": 25,
            "totalApplicants": 5000,
            "overallPercent": 5,
            "jobGrade": "A",
            "jobRank": 7,
            "jobApplicants": 1000,
            "jobPercent": 3,
            "experienceGrade": "A",
            "experienceMatch": 90,
            "experiencePercent": 10,
            "skillGrade": "A",
            "skillScore": 85,
            "skillPercent": 5
        },
        "jobFit": [
            {"title": "데이터 분석가", "percent": 80},
            {"title": "소프트웨어 개발자", "percent": 70},
            {"title": "프로젝트 매니저", "percent": 60}
        ],
        "cultureFit": [
            {"title": "기술 역량", "percent": 90},
            {"title": "애자일 협업 능력", "percent": 85},
            {"title": "문제 해결 능력", "percent": 80},
            {"title": "창의적 사고", "percent": 75}
        ],
        "radarChart": {
            "imageUrl": "images/applicant_radar_chart_fixed.png"
        },
        "finalSummary": {
            "overallScore": "88점",
            "jobFit": "90%",
            "cultureFit": "85%",
            "skillScore": "85점",
            "recommendation": "매우 추천",
            "opinionText": "지원자는 문제 해결 능력과 협업 능력이 매우 뛰어나며, 기술 역량과 창의적 사고에서도 높은 점수를 받았습니다. 리더십에서는 개선 여지가 있습니다.",
            "strengths": [
                "데이터 분석 및 문제 해결 능력",
                "애자일 협업 능력",
                "창의적 사고"
            ],
            "improvementPoint": "리더십 경험 부족",
            "hireRecommendation": "매우 추천",
            "hireReason": "데이터 분석가와 소프트웨어 개발자 직무에 높은 적합성을 보임"
        }
    }

@app.get("/api/download_report")
async def download_report():
    file_path = "path/to/generated/report.pdf"
    return FileResponse(file_path, media_type='application/pdf', filename="analysis_report.pdf")

@app.get("/applicant-info", response_model=dict)
async def applicant_info():
    return {
        "name": "홍길동",
        "recommendation": "매우 추천",
        "id": "hong_gildong@roto.ai",
        "position": "데이터 분석가",
        "location": "서울"
    }

@app.get("/score-summary", response_model=dict)
async def score_summary():
    return {
        "overallGrade": "A",
        "overallRank": 25,
        "totalApplicants": 5000,
        "overallPercent": 5,
        "jobGrade": "A",
        "jobRank": 7,
        "jobApplicants": 1000,
        "jobPercent": 3,
        "experienceGrade": "A",
        "experienceMatch": 90,
        "experiencePercent": 10,
        "skillGrade": "A",
        "skillScore": 85,
        "skillPercent": 5
    }

@app.get("/job-fit", response_model=list)
async def job_fit():
    return [
        {"title": "데이터 분석가", "percent": 80},
        {"title": "소프트웨어 개발자", "percent": 70},
        {"title": "프로젝트 매니저", "percent": 60}
    ]

@app.get("/culture-fit", response_model=list)
async def culture_fit():
    return [
        {"title": "기술 역량", "percent": 90},
        {"title": "애자일 협업 능력", "percent": 85},
        {"title": "문제 해결 능력", "percent": 80},
        {"title": "창의적 사고", "percent": 75}
    ]

@app.get("/radar-chart", response_model=dict)
async def radar_chart():
    return {
        "imageUrl": "images/applicant_radar_chart_fixed.png"
    }

@app.get("/final-summary", response_model=dict)
async def final_summary():
    return {
        "overallScore": "88점",
        "jobFit": "90%",
        "cultureFit": "85%",
        "skillScore": "85점",
        "recommendation": "매우 추천",
        "opinionText": "지원자는 문제 해결 능력과 협업 능력이 매우 뛰어나며, 기술 역량과 창의적 사고에서도 높은 점수를 받았습니다. 리더십에서는 개선 여지가 있습니다.",
        "strengths": [
            "데이터 분석 및 문제 해결 능력",
            "애자일 협업 능력",
            "창의적 사고"
        ],
        "improvementPoint": "리더십 경험 부족",
        "hireRecommendation": "매우 추천",
        "hireReason": "데이터 분석가와 소프트웨어 개발자 직무에 높은 적합성을 보임"
    }
    
@app.get("/download-report")
async def download_report():
    # 웹상의 파일 URL
    file_url = "http://127.0.0.1:8000/analysis_report.html"
    return {"file_url": file_url}