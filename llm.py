from typing import Optional, Any
from typing_extensions import Protocol
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import PreTrainedTokenizerBase
import torch


class GenerativeModel(Protocol):
    def generate(self, *args, **kwargs): ...

MODEL_ID = "Qwen/Qwen2.5-0.5B"

_model: Optional[Any] = None
_tokenizer: Optional[PreTrainedTokenizerBase] = None


def load_llm() -> None:
    global _model, _tokenizer

    if _model is not None:
        return

    print("🔄 Carregando LLM...")

    _tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
    )
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

    encodings = _tokenizer(text, return_tensors="pt")

    generated_ids = _model.generate(
        encodings["input_ids"],
        max_new_tokens=200,
    )

    return _tokenizer.decode(
        generated_ids[0],
        skip_special_tokens=True,
    )
