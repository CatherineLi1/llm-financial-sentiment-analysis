# # Code from Kaggle: Downloads the latest version
# import kagglehub
# path = kagglehub.dataset_download("jeet2016/us-financial-news-articles")
# print("Path to dataset files:", path)


# Assume downloaded from Kaggle, read archive.zip file
# archive.zip >>
'''
2018_01_112b52537b67659ad3609a234388c50a
2018_02_112b52537b67659ad3609a234388c50a
2018_03_112b52537b67659ad3609a234388c50a
2018_04_112b52537b67659ad3609a234388c50a
2018_05_112b52537b67659ad3609a234388c50a
'''
import zipfile
import random
import shutil
from pathlib import Path

random.seed(42)

zip_path = Path("archive.zip")
source_folder = "2018_05_112b52537b67659ad3609a234388c50a"
train_dir = Path("data/training/2018_05")
test_dir = Path("data/testing/2018_05")

train_dir.mkdir(parents=True, exist_ok=True)
test_dir.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as z:
    json_files = sorted([
        f for f in z.namelist()
        if f.startswith(source_folder + "/") and f.endswith(".json")
    ])

    block_size = 10

    train_files = []
    test_files = []

    for i in range(0, len(json_files), block_size):
        block = json_files[i:i + block_size]
        random.shuffle(block)

        split_idx = int(len(block) * 0.8)

        train_files.extend(block[:split_idx])
        test_files.extend(block[split_idx:])

    for file in train_files:
        filename = Path(file).name
        with z.open(file) as src, open(train_dir / filename, "wb") as dst:
            shutil.copyfileobj(src, dst)

    for file in test_files:
        filename = Path(file).name
        with z.open(file) as src, open(test_dir / filename, "wb") as dst:
            shutil.copyfileobj(src, dst)

print("Done.")
print(f"Total JSON files: {len(json_files)}")
print(f"Training files: {len(train_files)}")
print(f"Testing files: {len(test_files)}")

print("\nTraining timeline:")
print(Path(sorted(train_files)[0]).name, "->", Path(sorted(train_files)[-1]).name)

print("\nTesting timeline:")
print(Path(sorted(test_files)[0]).name, "->", Path(sorted(test_files)[-1]).name)