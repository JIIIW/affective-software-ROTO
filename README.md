# [🏆최우수상]효과적인 인재 채용을 위한 소프트웨어, ROTO
### 대량 지원서 처리의 어려움을 해소하고 기술 역량, 조직 적합성을 고려한 우수 인재를 선별함으로써 효과적인 인재 채용을 지원하고자 프로젝트를 진행했습니다.
[ROTO Project Full Story](https://www.behance.net/gallery/216485353/-ROTO)

## 🛠 Stack

![Scikit-learn](https://img.shields.io/badge/Scikit-leran-F7931E?style=for-the-badge&logo=Scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white)</br>
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0F9D58?style=for-the-badge&logo=Google&logoColor=white)
![KoNLPy](https://img.shields.io/badge/KoNLPy-cc1417?style=for-the-badge&logo=KoNLPy&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=HuggingFace&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

## Architecture

![frontend](https://github.com/user-attachments/assets/248c99da-bf88-4d86-86a3-4031c0e02f1e)
![backend](https://github.com/user-attachments/assets/967ce862-a8e2-4164-b38f-b1e3eb47817e)


## Model Workflow

![Video2Text](https://github.com/user-attachments/assets/fd8015e9-b8f2-45b5-afd0-914720f3e4c2)
![Pass Keyword](https://github.com/user-attachments/assets/7682dcc1-1a42-438b-8bd5-4be920bd0941)


## Prototype Structure

![tree](https://github.com/user-attachments/assets/79a9f84c-217a-4db8-b664-b34a4948500e)

## Prototype Execution Video
![Prototype](ROTO_ATS_Prototype.gif)

## Requirements
Python 3.10.15 환경에서 개발을 진행했습니다.

```
absl-py==2.1.0
accelerate==1.2.1
anyio==4.7.0
fastapi==0.85.0
google-auth==2.37.0
google-auth-oauthlib==0.4.6
h5py==3.12.1
huggingface-hub==0.27.0
Jinja2==3.1.5
keras==2.11.0
matplotlib==3.5.3
moviepy==1.0.3
numpy==1.26.4
opencv-python==4.6.0.66
pandas==2.2.3
pydantic==1.10.19
pydub==0.25.1
PyPDF2==3.0.1
python-docx==0.8.11
scikit-learn==1.3.0
scipy==1.15.0
tensorflow==2.11.0
torch==1.12.1+cu113
torchaudio==0.12.1+cu113
torchvision==0.13.1+cu113
transformers==4.47.1
uvicorn==0.18.3
```

## How to use Prototype
### 0. 가상환경 설정(타 패키지 간 충돌 방지를 위해 설치 권장)
- File name : **requirements.txt**

[Anaconda 환경 없을 시 다운로드](https://www.anaconda.com/download)

[anaconda prompt]
```
conda create -n [가상환경명] python=3.10.15
conda activate [가상환경명]
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu113
```
torch는 사용하는 GPU 버전에 맞춰 설치하셔야 합니다. 프로젝트에서 사용된 torch는 cu113입니다.

### Prototype 실행
```
gitclone https://github.com/JIIIW/affective-software-ROTO.git
uvicorn main:app --reload
```


## 📊 참고 모델 및 문헌
박은정, 조성준, “KoNLPy: 쉽고 간결한 한국어 정보처리 파이썬 패키지”, 제 26회 한글 및 한국어 정보처리 학술대회 논문집, 2014.

## License
이 프로젝트는 Apache License 2.0 따릅니다. 자세한 사항은 [LICENSE](https://github.com/JIIIW/affective-software-ROTO/blob/main/LICENSE) 탭을 참고해 주세요.
