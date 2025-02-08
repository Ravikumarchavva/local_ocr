from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelInference:
    def __init__(self, model_name):
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def predict(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors='pt')
        output = self.model.generate(input_ids, max_length=50, num_return_sequences=3)
        return self.tokenizer.batch_decode(output, skip_special_tokens=True)