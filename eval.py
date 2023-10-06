import torch
from model import Llama
from dataset import Dataset


def create_question(sample):
    INTRO_BLURB = 'Below is an instruction that describes a task. Write a response that appropriately completes the request.'
    INSTRUCTION_KEY = '### Instruction:'
    INPUT_KEY = 'Input:'
    RESPONSE_KEY = '### Response:'

    blurb = INTRO_BLURB
    instruction = f'{INSTRUCTION_KEY}\n{sample["instruction"]}'
    input_context = f'{INPUT_KEY}\n{sample["context"]}' if sample['context'] else None
    response = f'{RESPONSE_KEY}'

    parts = [part for part in [blurb, instruction,
                               input_context, response] if part]

    formatted_prompt = '\n\n'.join(parts)

    return formatted_prompt


if __name__ == '__main__':
    llama = Llama()
    dataset = Dataset('databricks/databricks-dolly-15k', llama.max_length)
    question_index = 0
    question_instance = dataset.dataset[question_index]

    question = create_question(question_instance)
    original_response = llama.ask_model(question)

    llama = Llama.load_pretrained_model('llama_adapter')
    lora_response = llama.ask_model(question)

    dash_line = f'\n{"-" * 80}\n'
    display_list = ['QUESTION', question,
                    'RESPONSE', question_instance['response'],
                    'ORIGINAL LLAMA 2', original_response,
                    'LORA LLAMA 2', lora_response]

    print()
    print(dash_line.join(display_list))
