import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from torch.nn import CrossEntropyLoss
from transformers import AdamW, get_linear_schedule_with_warmup

class StyleClassificationDataset(Dataset):
    def __init__(self, texts, styles, tokenizer, max_length):
        self.encodings = tokenizer(texts, truncation=True, padding='max_length', max_length=max_length, return_tensors='pt')
        self.labels = styles

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
max_length = 128

dataset = StyleClassificationDataset(texts, styles, tokenizer, max_length)

model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_styles)

train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
optimizer = AdamW(model.parameters(), lr=2e-5)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_loader))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        inputs = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**inputs)
        loss = CrossEntropyLoss()(outputs.logits, inputs['labels'])
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

    print(f"Epoch {epoch + 1} - Avg. Loss: {total_loss / len(train_loader)}")