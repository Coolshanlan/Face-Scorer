from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, utils
import torch.utils.model_zoo as model_zoo
from PIL import Image


class TrainDataloader(Dataset):
    def __init__(self, imagepaths, labels, transformer):
        self.imagepathlist = imagepaths
        self.labellist = labels
        self.transformer = transformer

    def loadimage(self, imagepath):
        img = Image.open(imagepath)
        img = self.transformer(img)
        return img

    def __getitem__(self, index):
        imp = self.imagepathlist[index]
        img = self.loadimage(imp)
        label = self.labellist[index]
        return img, label

    def __len__(self):
        return len(self.imagepathlist)
