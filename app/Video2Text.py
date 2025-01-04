from transformers import logging
logging.set_verbosity_error()

import os
import torch
import torchaudio
import soundfile as sf
from jiwer import wer, cer
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from moviepy.editor import VideoFileClip

# 영상 파일을 오디오로 변환하는 함수
def video_to_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, codec='pcm_s16le')

    print(f"오디오 파일이 생성되었습니다: {audio_path}")

# 오디오를 텍스트로 변환하는 함수
def audio_to_text(audio_path, model, processor, device, torch_dtype):
    # 오디오 파일 로드
    waveform, sample_rate = sf.read(audio_path)

    # Whisper 모델에서 사용할 16,000Hz로 샘플링 레이트 변환
    if sample_rate != 16000:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)
        sample_rate = 16000

    # 입력 데이터 준비
    inputs = processor(waveform.squeeze(), sampling_rate=sample_rate, return_tensors="pt").to(device)
    processor.feature_extractor.language = "ko"
    inputs["input_features"] = inputs["input_features"].to(dtype=torch_dtype)

    # 모델 추론
    with torch.no_grad():
        generated_tokens = model.generate(inputs["input_features"])

    # 텍스트 변환
    transcription = processor.batch_decode(generated_tokens, skip_special_tokens=True)
    print("Transcription:", transcription[0])
    return transcription[0]

# 정확도 평가 함수
def evaluate_transcription(transcription, true_label):
    # WER (Word Error Rate) 계산
    wer_value = wer(true_label, transcription)

    # CER (Character Error Rate) 계산
    cer_value = cer(true_label, transcription)

    return wer_value, cer_value

# 결과 저장 함수
def save_results(file_name, transcription, wer_value, cer_value):
    # 결과 저장
    text_path = f"./output/{file_name}.txt"
    os.makedirs(os.path.dirname(text_path), exist_ok=True)

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(f"Transcription: {transcription}\n")
        f.write(f"Word Error Rate (WER): {wer_value}\n")
        f.write(f"Character Error Rate (CER): {cer_value}\n")

    print(f"변환된 텍스트와 정확도 정보가 저장되었습니다: {text_path}")

# 메인 함수
def Video2Text():
    # 파일 경로 설정
    video_path = "./audio/ckmk_a_rnd_f_e_21038.wav"
    audio_dir = "./audio"
    os.makedirs(audio_dir, exist_ok=True)

    file_name, _ = os.path.splitext(os.path.basename(video_path))
    audio_path = f"{audio_dir}/{file_name}.wav"

    # 영상 파일을 오디오로 변환
    # 지원되는 파일 확장자 리스트
    VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv')
    AUDIO_EXTENSIONS = ('.aiff', '.au', '.avr', '.caf', '.flac', '.htk',
                        '.svx', '.mat4', '.mat5', '.mpc', '.mp3', '.ogg',
                        '.paf', '.pvf', '.wav')

    # 영상 파일을 오디오로 변환
    if video_path.lower().endswith(VIDEO_EXTENSIONS):
        print("영상 파일을 감지했습니다. 오디오로 변환합니다.")
        video_to_audio(video_path, audio_path)
    elif video_path.lower().endswith(AUDIO_EXTENSIONS):
        print("오디오 파일을 감지했습니다. 변환을 시작합니다.")
    else:
        print("지원되지 않는 파일 형식입니다. 파일 형식을 확인해 주세요.")

    # 장치 및 데이터 타입 설정
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Whisper 모델 로드
    processor = AutoProcessor.from_pretrained("openai/whisper-large-v3-turbo")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3-turbo")
    model.half()
    model.to(device)

    # 오디오를 텍스트로 변환
    transcription = audio_to_text(audio_path, model, processor, device, torch_dtype)

    # 실제 라벨
    true_label = "이 직무를 수행하기 위해서 저의 강점은 커뮤니케이션이 잘 된다는 겁니다.\
    특히 타 팀과 협업해야 되는 업무에 있어서 저는 타 팀과 충분한 커뮤니케이션을\
    통해서 최고의 효율을 끌어 올릴 수 있습니다.\
    그러므로 저의 장점은 커뮤니케이션이 충분히 잘 된다는 것입니다."

    # 정확도 평가
    wer_value, cer_value = evaluate_transcription(transcription, true_label)

    # 결과 저장
    save_results(file_name, transcription, wer_value, cer_value)

if __name__ == "__main__":
    Video2Text()