document.addEventListener("DOMContentLoaded", () => {
    /**
     * 지원자 정보 가져오기
     * 지원자 이름, 추천 상태, ID, 지원 직무, 응시 지역 등 정보를 백엔드에서 가져와 DOM에 반영합니다.
     */
    async function fetchApplicantInfo() {
        try {
            // 백엔드에서 지원자 정보 API 호출
            const response = await fetch("http://127.0.0.1:8000/applicant-info");

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // JSON 형식의 데이터 파싱
            const data = await response.json();

            // DOM 요소에 데이터를 업데이트
            document.getElementById("applicantName").textContent = data.name || "이름 없음"; // 지원자 이름 예: "홍길동"
            document.getElementById("recommendation").textContent = data.recommendation || "추천 상태 없음"; // 추천 상태 예: "매우 추천"
            document.getElementById("applicantId").textContent = data.id || "ID 없음"; // 지원자 ID 예: "hong_dev@company.com"
            document.getElementById("applicantPosition").textContent = data.position || "직무 없음"; // 지원 직무 예: "백엔드 개발자"
            document.getElementById("applicantLocation").textContent = data.location || "지역 없음"; // 응시 지역 예: "서울"
        } catch (error) {
            console.error("Error fetching applicant info:", error);

            // // 에러 발생 시 기본값 표시
            // document.getElementById("applicantName").textContent = "데이터 로드 실패";
            // document.getElementById("recommendation").textContent = "알 수 없음";
            // document.getElementById("applicantId").textContent = "ID 불러오기 실패";
            // document.getElementById("applicantPosition").textContent = "직무 불러오기 실패";
            // document.getElementById("applicantLocation").textContent = "지역 불러오기 실패";
        }
    }

    /**
     * 종합 점수 분포 가져오기
     * 종합 점수, 전체 등급, 직무 적합도, 기술 역량 등의 데이터를 백엔드에서 가져와 DOM에 반영합니다.
     * 점수 분포 차트를 이미지로 추가합니다.
     */
    async function fetchScoreSummary() {
        try {
            // 백엔드에서 종합 점수 데이터 API 호출
            const response = await fetch("http://127.0.0.1:8000/score-summary");

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // JSON 데이터 파싱
            const data = await response.json();

            // DOM 요소에 데이터 업데이트
            document.getElementById("allGrade").textContent = data.overallGrade || "N/A"; // 전체 등급 예: "A"
            document.getElementById("allRank").textContent = `${data.overallRank || "-"}등/${data.totalApplicants || "-"}명`; // 전체 랭킹 예: "1등/100명"
            document.getElementById("allPercent").textContent = `상위 ${data.overallPercent || "-"}%`; // 상위 퍼센트 예: "상위 1%"

            document.getElementById("jobGrade").textContent = data.jobGrade || "N/A"; // 직무 등급 예: "A"
            document.getElementById("jobRank").textContent = `${data.jobRank || "-"}등/${data.jobApplicants || "-"}명`; // 직무 랭킹 예: "1등/20명"
            document.getElementById("jobPercent").textContent = `상위 ${data.jobPercent || "-"}%`; // 직무 퍼센트 예: "상위 5%"

            document.getElementById("experienceGrade").textContent = data.experienceGrade || "N/A"; // 경력 적합도 예: "A"
            document.getElementById("experienceMatch").textContent = `${data.experienceMatch || "-"}% 적합도`; // 경력 퍼센트 예: "85% 적합도"
            document.getElementById("experiencePercent").textContent = `상위 ${data.experiencePercent || "-"}%`; // 상위 퍼센트 예: "상위 10%"

            document.getElementById("skillGrade").textContent = data.skillGrade || "N/A"; // 기술 역량 예: "B"
            document.getElementById("skillScore").textContent = `${data.skillScore || "-"}점/100점`; // 점수 예: "75점/100점"
            document.getElementById("skillPercent").textContent = `상위 ${data.skillPercent || "-"}%`; // 상위 퍼센트 예: "상위 20%"

        } catch (error) {
            console.error("Error fetching score summary:", error);

            // // 에러 발생 시 기본값 표시
            // document.getElementById("allGrade").textContent = "데이터 없음";
            // document.getElementById("allRank").textContent = "데이터 없음";
            // document.getElementById("allPercent").textContent = "데이터 없음";
        }
    }

    /**
     * 직무 적합도 데이터 가져오기
     * 직무 별 적합도를 진행률과 점수로 DOM에 반영합니다.
     */
    async function fetchJobFitData() {
        try {
            // 백엔드에서 직무 적합도 API 호출
            const response = await fetch("http://127.0.0.1:8000/job-fit");

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const jobFitItems = document.querySelectorAll(".job-fit-container > .job-fit-item");

            // 데이터 순회하며 DOM 업데이트
            data.forEach((item, index) => {
                if (jobFitItems[index]) {
                    const title = jobFitItems[index].querySelector(".job-title");
                    const progress = jobFitItems[index].querySelector(".progress");
                    const score = jobFitItems[index].querySelector(".job-score");

                    title.textContent = item.title || "직무 정보 없음"; // 예: "백엔드 개발"
                    progress.style.width = `${item.percent || 0}%`; // 예: "90%"
                    score.textContent = `${item.percent || 0}%`; // 예: "90%"
                }
            });
        } catch (error) {
            console.error("Error fetching job fit data:", error);
        }
    }


/**
 * 조직 문화 적합도 데이터 가져오기
 */
async function fetchCultureFitData() {
    try {
        // 조직 문화 적합도 데이터를 API로 가져오기
        const response = await fetch("http://127.0.0.1:8000/culture-fit");

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // DOM 요소 가져오기 (조직 문화 적합도 컨테이너)
        const cultureFitContainer = document.querySelector(".analysis-box2 .job-fit-container2");
        const cultureFitItems = cultureFitContainer.querySelectorAll(".job-fit-item2");

        if (!data || !Array.isArray(data) || data.length === 0) {
            console.error("No culture fit data available.");
            return;
        }

        // 데이터 순회하며 DOM 업데이트
        data.forEach((item, index) => {
            if (cultureFitItems[index]) {
                const title = cultureFitItems[index].querySelector(".job-title2");
                const progress = cultureFitItems[index].querySelector(".progress2");
                const score = cultureFitItems[index].querySelector(".job-score2");

                // 데이터 적용
                title.textContent = item.title || "항목 없음";
                progress.style.width = `${item.percent || 0}%`;
                score.textContent = `${item.percent || 0}%`;
            } else {
                console.warn(`No matching DOM element for index ${index}`);
            }
        });
    } catch (error) {
        console.error("Error fetching culture fit data:", error);
    }
}

/**
 * 조직 문화 적합도 데이터 가져오기 (가상 데이터 테스트)
 */
// function updateCultureFitProgress() {
//     // 가상 데이터
//     const cultureFitData = [
//         { title: "기술 역량", percent: 85 },
//         { title: "애자일 협업 능력", percent: 75 },
//         { title: "문제 해결 능력", percent: 90 },
//         { title: "창의적 사고", percent: 80 }
//     ];

//     // 조직 문화 적합도 DOM 요소 가져오기
//     const progressItems = document.querySelectorAll(".job-fit-container2 .job-fit-item2");

//     // 데이터 순회하며 진행 바 업데이트
//     cultureFitData.forEach((item, index) => {
//         if (progressItems[index]) {
//             const title = progressItems[index].querySelector(".job-title2");
//             const progress = progressItems[index].querySelector(".progress2");
//             const score = progressItems[index].querySelector(".job-score2");

//             // 데이터 적용
//             title.textContent = item.title || "항목 없음";
//             progress.style.width = `${item.percent || 0}%`;
//             score.textContent = `${item.percent || 0}%`;
//         } else {
//             console.warn(`No matching DOM element found for index ${index}`);
//         }
//     });
// }

// // 실행
// updateCultureFitProgress();


    /**
     * 역량 분석 차트 가져오기
     * 백엔드에서 제공하는 차트 이미지를 DOM에 추가합니다.
     */
    async function fetchRadarChart() {
        try {
            // 백엔드에서 역량 분석 차트 데이터 API 호출
            const response = await fetch("http://127.0.0.1:8000/radar-chart");

            // HTTP 에러 처리
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // JSON 데이터 파싱
            const data = await response.json();

            // DOM 요소 가져오기 (차트 이미지 태그)
            const radarChartImage = document.getElementById("radarChartImage");

            // 차트 이미지 업데이트
            if (data.imageUrl) {
                radarChartImage.src = data.imageUrl; // 백엔드에서 제공된 이미지 URL
                radarChartImage.alt = "역량 분석 차트"; // 이미지 대체 텍스트
            } else {
                radarChartImage.src = ""; // 이미지가 없을 때 기본값
                radarChartImage.alt = "차트 이미지 없음"; // 기본 대체 텍스트
            }
        } catch (error) {
            // 에러 처리 (콘솔 출력 및 기본값 적용)
            console.error("Error fetching radar chart:", error);
            const radarChartImage = document.getElementById("radarChartImage");
            radarChartImage.src = ""; // 기본값으로 초기화
            radarChartImage.alt = "차트를 로드하는 데 실패했습니다."; // 실패 메시지
        }
    }

    /**
     * 결론 및 최종 의견 데이터 가져오기
     * 결론 데이터를 DOM에 반영하며, 주요 강점과 보완점을 동적으로 추가합니다.
     */
    async function fetchFinalSummary() {
        try {
            // 백엔드에서 결론 및 최종 의견 데이터를 API로 가져오기
            const response = await fetch("http://127.0.0.1:8000/final-summary");

            // HTTP 에러 처리
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // JSON 데이터 파싱
            const data = await response.json();

            // DOM 요소에 데이터 반영
            document.getElementById("finalOverallScore").textContent = data.overallScore || "N/A"; // 종합 점수 예: "88점"
            document.getElementById("finalJobFit").textContent = data.jobFit || "N/A"; // 직무 적합도 예: "90%"
            document.getElementById("finalCultureFit").textContent = data.cultureFit || "N/A"; // 조직 문화 적합도 예: "85%"
            document.getElementById("finalSkillScore").textContent = data.skillScore || "N/A"; // 기술 점수 예: "85점"
            document.getElementById("finalRecommendation").textContent = data.recommendation || "N/A"; // 추천 상태 예: "매우 추천"

            document.getElementById("finalOpinionText").textContent = data.opinionText || "의견 없음"; // 최종 의견

            // 주요 강점 리스트 업데이트
            const strengthsList = document.getElementById("strengthsList");
            strengthsList.innerHTML = ""; // 기존 리스트 초기화
            (data.strengths || []).forEach((strength) => {
                const li = document.createElement("li");
                li.textContent = strength; // 강점 예: "문제 해결 능력"
                strengthsList.appendChild(li);
            });

            // 보완점 업데이트
            document.getElementById("improvementPoint").textContent = data.improvementPoint || "보완점 없음"; // 보완점 예: "창의적 사고 부족"

            // 채용 추천 및 이유 업데이트
            document.getElementById("finalHireRecommendation").textContent = data.hireRecommendation || "N/A"; // 채용 추천 예: "매우 추천"
            document.getElementById("finalHireReason").textContent = data.hireReason || "이유 없음"; // 이유 예: "팀워크와 기술 능력이 탁월함"
        } catch (error) {
            // 에러 처리 (콘솔 출력)
            console.error("Error fetching final summary:", error);
        }
    }

    /**
     * 보고서 다운로드 버튼 클릭 이벤트
     * 보고서를 백엔드에서 다운로드합니다.
     */
    document.getElementById("downloadButton").addEventListener("click", async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/download-report", { method: "GET" });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const downloadLink = document.createElement("a");
            downloadLink.href = downloadUrl;
            downloadLink.download = "Insight_Report.pdf"; // 다운로드 파일 이름
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        } catch (error) {
            console.error("Error downloading the report:", error);
            alert("보고서를 다운로드하는 데 실패했습니다.");
        }
    });

    // 데이터 가져오기 실행
    fetchApplicantInfo();
    fetchScoreSummary();
    fetchJobFitData();
    fetchCultureFitData();
    fetchRadarChart();
    fetchFinalSummary();
});

