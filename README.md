# audio-source

`audio-source` is a small metadata aggregation utility. It downloads JSON documents from URLs listed in `sources-url`, stores those source files locally, merges their `audio_info` records, and writes the combined catalogue to `source.json`.

Repository: https://github.com/saidawan-radio/audio-source

## Files

| File | Purpose |
|---|---|
| `sources-url` | One source URL per line. |
| `fetch_source.sh` | Downloads each URL into `file-sources/sourceNN.json`, then runs the collector. |
| `colector.py` | Merges each source file's `audio_info` into the combined JSON and calculates aggregate fields. |
| `source.json` | Combined catalogue output. |
| `.github/workflows/` | GitHub Actions automation, if configured in the current branch. |

## Processing flow

1. `fetch_source.sh` creates the `file-sources/` directory.
2. It reads `sources-url` line by line and downloads each non-empty URL using `curl`.
3. Downloaded documents are named `source01.json`, `source02.json`, and so on.
4. The script runs `python3 ./colector.py`.
5. The collector merges each source's `audio_info` map into `source.json`.
6. It calculates `general_info.total_duration` and `general_info.last_downloaded_internal_id`.

## Expected JSON shape

The source documents are expected to contain an `audio_info` object. Each audio record should include at least a numeric-like `id` and a numeric `duration`, because the collector sums durations and finds the highest ID.

## Run locally

Requirements: Bash, `curl`, and Python 3.

```bash
chmod +x fetch_source.sh
./fetch_source.sh
```

Check that every URL in `sources-url` is reachable and returns valid JSON. The collector expects each downloaded file to have the expected schema.

## Relationship to the radio

This repository is a **metadata aggregation layer**, distinct from `audio-data`'s Telegram metadata fetching and from the `pocketXX` repositories that store media. Its `source.json` can serve as a merged index for other parts of the project when its URL is configured as a source.

## Notes

- The repository name and script use the spelling `colector.py`; retain that filename unless the workflow and shell script are updated together.
- The current collector updates records by key, so if two input sources contain the same `audio_info` key, the later source processed can overwrite the earlier value.
- Validate downloaded JSON before committing it; a failed HTTP download can otherwise leave an invalid source file.
