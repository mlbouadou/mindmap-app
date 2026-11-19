
import random
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch import nn
from torch.utils.data import Dataset, DataLoader

from gesture import GestureCNN


classes = ["triangle", "circle", "rectangle", "equal", "not_equal"]
folder = Path(__file__).parent


class ShapeDataset(Dataset):
    def __init__(self, samples):
        self.samples = samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        path, label = self.samples[i]

        with Image.open(path) as img:
            image = np.array(img.convert("L"), dtype=np.float32) / 255

        return torch.from_numpy(image).unsqueeze(0), label


def load_data():
    random_gen = random.Random(42)
    train, val, test = [], [], []

    for label, name in enumerate(classes):
        images = sorted((folder / "data/training" / name).glob("*.png"))
        random_gen.shuffle(images)

        if len(images) < 10:
            raise ValueError(f"Not enough images in {name}")

        a = int(len(images) * 0.7)
        b = int(len(images) * 0.85)

        train += [(p, label) for p in images[:a]]
        val += [(p, label) for p in images[a:b]]
        test += [(p, label) for p in images[b:]]

    return train, val, test


def evaluate(model, loader, device):
    model.eval()
    correct = total = 0

    with torch.no_grad():
        for x, y in loader:
            predictions = model(x.to(device)).argmax(1)
            correct += (predictions == y.to(device)).sum().item()
            total += len(y)

    return correct / total


if __name__ == "__main__":
    torch.manual_seed(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    train, val, _ = load_data()
    train_loader = DataLoader(ShapeDataset(train), batch_size=64, shuffle=True)
    val_loader = DataLoader(ShapeDataset(val), batch_size=64)

    model = GestureCNN(5).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    best = 0

    for epoch in range(15):
        model.train()
        total_loss = 0

        for x, y in train_loader:
            x, y = x.to(device), y.to(device)

            optimizer.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(y)

        accuracy = evaluate(model, val_loader, device)
        print(f"Epoch {epoch+1}: loss={total_loss/len(train):.4f}, val={accuracy:.2%}")

        if accuracy > best:
            best = accuracy
            torch.save(model.state_dict(), folder / "gesture_model.pt")
