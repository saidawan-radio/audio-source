import json
from pathlib import Path

SOURCE_DIR="file-sources"
COLLECTION_FILE_NAME = "source.json"

COLLECTION_FORM = {
    "audio_info" : {},
    
    "general_info": {
    "total_duration": 0,
    "last_downloaded_internal_id": 0
    }
}

def load_json(file) -> dict:
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        return data
    
def dump_json(file, data:dict):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def create_and_fill_if_empty(file_path: str, default_data: dict):
    path = Path(file_path)

    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create/fill file if missing or empty
    if not path.exists() or path.stat().st_size <= 3:
        with path.open("w") as f:
            json.dump(default_data, f, indent=2)

        print(f"Created/updated {path} with data")

    print(f"{path} already has content")

def apend_data(collection:dict, data:dict):
    collection["audio_info"].update(data["audio_info"])

create_and_fill_if_empty(COLLECTION_FILE_NAME, COLLECTION_FORM)
collection = load_json(COLLECTION_FILE_NAME)

dir = Path(SOURCE_DIR)




for file in dir.iterdir():
    if file.is_file():
        print(file)
        data = load_json(file)
        apend_data(collection, data)


total_duration = 0
last_downloaded_internal_id = 0

for audio in collection["audio_info"].values():
    total_duration += audio["duration"]
    last_downloaded_internal_id = max(last_downloaded_internal_id, int(audio["id"]))
    
collection["general_info"]["total_duration"] = total_duration
collection["general_info"]["last_downloaded_internal_id"] = last_downloaded_internal_id

dump_json(COLLECTION_FILE_NAME, collection)

print("total duration:", total_duration)
print("last internal id:", last_downloaded_internal_id)