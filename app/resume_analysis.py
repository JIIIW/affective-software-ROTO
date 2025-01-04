import os
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from transformers.models.auto.configuration_auto import CONFIG_MAPPING
import torch

# Llama 지원 추가
CONFIG_MAPPING.update({"llama": AutoModelForCausalLM})

def initialize_model():
    model_id = "MLP-KTLim/llama-3-Korean-Bllossom-8B"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto" if torch.cuda.is_available() else "cpu",
            low_cpu_mem_usage=True
        )
        text_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map="auto" if torch.cuda.is_available() else "cpu"
        )
        
        PROMPT = """당신은 유명한 IT 기업의 인사팀에 소속돼 있는 사람입니다.
인재 채용 면에서 매우 객관적이고, 유능합니다. 지원자의 이력서를 넣으면, 아래 척도를 기준으로
백분율 점수와 그 근거를 답변해 주세요.

1. 이 지원자는 IT 분야 직업 중 어떤 직업에 가장 적합한가요? 상위 3개 직업을 각각 적합도 백분율과 함께 답변해 주세요.
2. 이 지원자를 기술 역량, 애자일 협업 능력, 문제 해결 능력, 창의적 사고 면에서 평가해 주세요.
3. 지원자의 역량을 레이더 차트로 표현해 주세요. 12시 방향에서 시계 방향대로 기술 역량, 문제 해결 능력,
창의적 사고, 협업 능력, 커뮤니케이션 능력, 리더십 순서입니다."""
        
        return tokenizer, text_pipeline, PROMPT
    except Exception as e:
        raise RuntimeError(f"모델 로드 실패: {e}")

def generate_ai_response(instruction, tokenizer, text_pipeline, PROMPT):
    """
    Generates an AI response based on the input instruction using the preloaded model and pipeline.
    """
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": instruction}
    ]
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    outputs = text_pipeline(
        tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        ),
        max_new_tokens=2048,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9
    )
    return outputs[0]["generated_text"]
