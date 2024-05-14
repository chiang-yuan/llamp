import transformers
import torch

################################################## Llama 3 ##################################################
# able to host it 
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda:1",
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": """What is the magnetic ordering of La2Sb? If there are multiple magnetic orderings, please give me the most stable one with its material id, space group, and magnetization per formula unit.
        After you reason through, please output it in the format of python dictionary below.
        
        ""magnetic_ordering"": [your answer for mass density],
        ""magnetization_per_formula_unit"": [your answer for magnetization per formula unit],
        ""material_id"": [your answer for material_id],

        Tips:
        1. don't include the calculation process, only include the answers in one sentence"""},
]

prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
)

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)
breakpoint()
print(outputs[0]["generated_text"][len(prompt):])

################################################## Mistral ##################################################
# from transformers import AutoModelForCausalLM, AutoTokenizer

# device = "cuda:6" # the device to load the model onto

# model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
# tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

# # require 30GB

# messages = [
#     {"role": "user", "content": "What is your favourite condiment?"},
#     {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
#     {"role": "user", "content": "Do you have mayonnaise recipes?"}
# ]

# encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

# model_inputs = encodeds.to(device)
# model.to(device)

# generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
# decoded = tokenizer.batch_decode(generated_ids)
# print(decoded[0])
