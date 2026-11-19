
import torch
from torch.utils.data import DataLoader

from gesture import GestureCNN
from train import classes, folder, ShapeDataset, load_data, evaluate


device = "cuda" if torch.cuda.is_available() else "cpu"

_, _, test = load_data()
loader = DataLoader(ShapeDataset(test), batch_size=64)

model = GestureCNN(len(classes)).to(device)
model.load_state_dict(
    torch.load(folder / "gesture_model.pt", map_location=device, weights_only=True)
)

accuracy = evaluate(model, loader, device)
print(f"Test accuracy: {accuracy:.2%}")
