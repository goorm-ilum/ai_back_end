import torch
from transformers import AutoModel

class KoELECTRAMultiTask(torch.nn.Module):
    def __init__(self, model_name, num_aspect_classes, num_polarity_classes):
        super().__init__()
        self.koelectra = AutoModel.from_pretrained(model_name)
        hidden_size = self.koelectra.config.hidden_size
        self.aspect_classifier = torch.nn.Linear(hidden_size, num_aspect_classes)
        self.polarity_classifier = torch.nn.Linear(hidden_size, num_polarity_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.koelectra(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.last_hidden_state[:, 0]  # [CLS] 토큰 벡터
        aspect_logits = self.aspect_classifier(pooled_output)
        polarity_logits = self.polarity_classifier(pooled_output)
        return aspect_logits, polarity_logits