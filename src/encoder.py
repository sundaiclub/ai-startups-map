import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np

import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel


def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

class Encoder:
    def __init__(self, model_name="thenlper/gte-small"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def batch_encode(self, text_list, batch_size=32):
        encoded_list = []
        for i in range(0, len(text_list), batch_size):
            batch = text_list[i : i + batch_size]
            encoded = self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=512).to(
                self.device
            )
            with torch.no_grad():
                embeddings = self.model(**encoded)
                embeddings =  average_pool(embeddings.last_hidden_state, encoded['attention_mask'])
                encoded_list.append(embeddings.cpu().numpy())

        return np.vstack(encoded_list)

        