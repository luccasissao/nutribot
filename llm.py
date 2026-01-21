from typing import Optional, Any
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import PreTrainedTokenizerBase
import torch

torch.set_num_threads(4)

MODEL_ID = "Qwen/Qwen2.5-0.5B"

_model: Optional[Any] = None
_tokenizer: Optional[PreTrainedTokenizerBase] = None


def load_llm() -> None:
    global _model, _tokenizer

    if _model is not None:
        return

    print("🔄 Carregando LLM...")

    _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    print("✅ Tokenizer carregado")

    _model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    print("✅ LLM carregada")


def llm_answer(text: str) -> str:
    load_llm()

    assert _model is not None
    assert _tokenizer is not None

    text = text[:2000]

    prompt = f"""Você é um assistente nutricional, que responde apenas as informações nutricionais em macronutrientes de cada alimento passado.
Usuário: {text}
Assistente:"""

    encodings = _tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
    )

    with torch.no_grad():
        generated_ids = _model.generate(
            input_ids=encodings["input_ids"],
            attention_mask=encodings["attention_mask"],
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=_tokenizer.eos_token_id,
        )

    decoded = _tokenizer.decode(
        generated_ids[0],
        skip_special_tokens=True,
    )


    return decoded.strip()