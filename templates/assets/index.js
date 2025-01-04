// PDF.js 설정
const pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.15.349/pdf.worker.min.js';

// PDF 관련 변수
let pdfDoc = null; // PDF 문서 객체
let currentPage = 1; // 현재 페이지 번호
let totalPages = 0; // 총 페이지 수
let scale = 1.5; // 기본 확대/축소 비율

// DOM 요소 가져오기
const fileInput = document.getElementById('resume-upload-input'); // 파일 업로드 입력 필드
const canvas = document.getElementById('pdf-canvas'); // PDF를 렌더링할 캔버스 요소
const ctx = canvas.getContext('2d'); // 캔버스의 2D 렌더링 컨텍스트
const prevPageButton = document.getElementById('prev-page'); // 이전 페이지 버튼
const nextPageButton = document.getElementById('next-page'); // 다음 페이지 버튼
const pageInfo = document.getElementById('page-info'); // 페이지 정보 표시
const zoomInButton = document.getElementById('zoom-in'); // 확대 버튼
const zoomOutButton = document.getElementById('zoom-out'); // 축소 버튼
const loadingPopup = document.getElementById('loading-popup'); // 로딩 팝업 요소

// 허용되는 파일 형식 정의
const allowedTypes = [
    'application/pdf', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]; // PDF 및 DOCX 파일 허용

// 파일 업로드 이벤트 처리
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0]; // 업로드된 파일 가져오기
    if (!file) return;

    // 파일 형식 검사
    if (!allowedTypes.includes(file.type)) {
        alert('PDF 또는 DOCX 파일만 업로드 가능합니다.');
        return;
    }

    // PDF 파일 처리
    if (file.type === 'application/pdf') {
        const fileURL = URL.createObjectURL(file); // PDF 파일의 Blob URL 생성
        pdfjsLib.getDocument(fileURL).promise.then((pdf) => {
            pdfDoc = pdf; // PDF 문서 저장
            totalPages = pdf.numPages; // 총 페이지 수
            currentPage = 1; // 현재 페이지를 1로 초기화
            updatePageInfo(); // 페이지 정보 표시 업데이트
            renderPDFPage(currentPage); // PDF의 첫 번째 페이지 렌더링
        }).catch((error) => {
            console.error('PDF 로드 실패:', error);
        });
    } 
    // DOCX 파일 처리
    else if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        handleDOCXFile(file); // DOCX 파일 처리 함수 호출
    }
});

// 이전 페이지로 이동
prevPageButton.addEventListener('click', () => {
    if (currentPage <= 1) return; // 첫 페이지인 경우 아무 작업도 하지 않음
    currentPage -= 1;
    renderPDFPage(currentPage); // 이전 페이지 렌더링
    updatePageInfo(); // 페이지 정보 업데이트
});

// 다음 페이지로 이동
nextPageButton.addEventListener('click', () => {
    if (currentPage >= totalPages) return; // 마지막 페이지인 경우 아무 작업도 하지 않음
    currentPage += 1;
    renderPDFPage(currentPage); // 다음 페이지 렌더링
    updatePageInfo(); // 페이지 정보 업데이트
});

// 확대 버튼 클릭 이벤트
zoomInButton.addEventListener('click', () => {
    scale += 0.2; // 확대 비율 증가
    renderPDFPage(currentPage); // 현재 페이지 다시 렌더링
});

// 축소 버튼 클릭 이벤트
zoomOutButton.addEventListener('click', () => {
    if (scale <= 0.5) return; // 축소 비율이 너무 작아지는 것을 방지
    scale -= 0.2; // 확대 비율 감소
    renderPDFPage(currentPage); // 현재 페이지 다시 렌더링
});

// PDF 페이지 렌더링 함수
function renderPDFPage(pageNumber) {
    pdfDoc.getPage(pageNumber).then((page) => {
        const viewport = page.getViewport({ scale: scale }); // PDF 페이지의 스케일 설정
        canvas.width = viewport.width; // 캔버스 너비 설정
        canvas.height = viewport.height; // 캔버스 높이 설정

        const renderContext = {
            canvasContext: ctx, // 캔버스 컨텍스트 설정
            viewport: viewport  // 뷰포트 설정
        };

        page.render(renderContext).promise.then(() => {
            console.log(`Page ${pageNumber} rendered`); // 페이지 렌더링 완료 로그 출력
        });
    });
}

// 페이지 정보 업데이트 함수
function updatePageInfo() {
    pageInfo.textContent = `${currentPage} / ${totalPages}`;
}

// DOCX 파일 처리 함수
function handleDOCXFile(file) {
    const reader = new FileReader(); // FileReader 객체 생성
    reader.onload = (event) => {
        const arrayBuffer = event.target.result; // 읽어온 파일 데이터
        mammoth.convertToHtml({ arrayBuffer: arrayBuffer }) // Mammoth.js를 사용해 DOCX 파일을 HTML로 변환
            .then((result) => {
                // 변환된 HTML 내용을 미리보기 영역에 표시
                document.querySelector('.resume-preview').innerHTML = result.value;
                console.log('DOCX 내용:', result.value); // 변환된 내용을 로그로 출력
            })
            .catch((error) => {
                console.error('DOCX 변환 실패:', error); // 변환 실패 시 오류 로그 출력
            });
    };
    reader.readAsArrayBuffer(file); // DOCX 파일을 ArrayBuffer로 읽기 시작
}

// 분석 시작 버튼 이벤트 처리
document.querySelector('.analyze-btn').addEventListener('click', () => {
    // 로딩 팝업 표시
    const loadingPopup = document.getElementById('loading-popup');
    loadingPopup.style.display = 'flex'; // 로딩 팝업을 보이도록 설정

    const fileInput = document.getElementById('resume-upload-input');
    const file = fileInput.files[0]; // 업로드된 파일 가져오기

    if (file) {
        const formData = new FormData();
        formData.append("file", file);

        // 서버로 POST 요청 보내기
        fetch("http://localhost:8000/analyze_resume/", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('서버 응답 데이터:', data); // 디버깅용 데이터 확인

            // 분석 성공 시 analysis_report.html 페이지로 이동
            window.location.href = "analysis_report.html";
        })
        .catch(error => {
            console.error('분석 실패:', error.message); // 오류 로그 출력
            loadingPopup.style.display = 'none'; // 로딩 팝업 숨기기
            alert('분석에 실패했습니다.');
        });
    } else {
        alert('파일을 선택해 주세요!');
        loadingPopup.style.display = 'none'; // 로딩 팝업 숨기기
    }
});