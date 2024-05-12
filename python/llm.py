import torch
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedTokenizer,
    PreTrainedModel,
    Pipeline,
)


def setup_and_load_models() -> (PreTrainedModel, PreTrainedTokenizer, Pipeline):
    device = "cuda:0"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # load model and processors into gpu
    stt_model_id = "openai/whisper-large-v3"
    whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained(
        stt_model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
    )
    whisper_model.to(device)
    whisper_processor = AutoProcessor.from_pretrained(stt_model_id)
    llm_model_id = "microsoft/Phi-3-mini-4k-instruct"
    language_model = AutoModelForCausalLM.from_pretrained(
        llm_model_id,
        device_map="cuda",
        torch_dtype="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(llm_model_id)

    whisper_pipe = pipeline(
        "automatic-speech-recognition",
        model=whisper_model,
        tokenizer=whisper_processor.tokenizer,
        feature_extractor=whisper_processor.feature_extractor,
        max_new_tokens=128,
        torch_dtype=torch_dtype,
        device=device,
    )
    forced_decoder_ids = whisper_processor.get_decoder_prompt_ids(
        language="german", task="transcribe"
    )
    whisper_pipe.model.config.forced_decoder_ids = forced_decoder_ids
    return language_model, tokenizer, whisper_pipe


def transcribe_audio(whisper_pipeline: Pipeline, audio_path: str = "output.wav") -> str:
    whisper_result = whisper_pipeline(audio_path)
    transcribed_content = whisper_result["text"]
    return transcribed_content


def generate_new_shopping_list_item(
        language_model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        transcribed_content: str,
) -> str:
    messages = [
        {
            "role": "user",
            "content": "Act as my german Shopping assitant, called bring."
                       " Give me a one word reply which consists of the name."
                       "It is really important that your reply is only one word long and is a german word."
                       " that should be added to the shopping list: Bring, füg' Milch zur Einkaufsliste hinzu",
        },
        {"role": "assistant", "content": "Milch"},
        {"role": "user", "content": "Bring, füg' Spinat zur Einkaufsliste hinzu"},
        {"role": "assistant", "content": "Spinat"},
        {"role": "user", "content": "Brot"},
        {"role": "assistant", "content": "Brot"},
        {"role": "user", "content": "Käse auf die Einkaufsliste hinzufügen"},
        {"role": "assistant", "content": "Käse"},
        {"role": "user", "content": transcribed_content},
    ]

    pipe = pipeline(
        "text-generation",
        model=language_model,
        tokenizer=tokenizer,
    )

    generation_args = {
        "max_new_tokens": 100,
        "return_full_text": False,
        "temperature": 0.0,
        "do_sample": False,
    }

    output = pipe(messages, **generation_args)
    return output[0]["generated_text"]


if __name__ == "__main__":
    language_model, tokenizer, whisper_pipe = setup_and_load_models()
    transcribed_content = transcribe_audio(whisper_pipe, "output.wav")
    new_shopping_list_item = generate_new_shopping_list_item(
        language_model, tokenizer, transcribed_content
    )
    print(new_shopping_list_item)
