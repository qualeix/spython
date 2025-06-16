import config
import os
import time
from utils import log


def ensure_cache_directory():
    cache_dir = config.CACHE_DIR
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        log(f"Created cache directory: {cache_dir}", "DEBUG", "cache")
    return cache_dir


def get_cache_size():
    total_size = 0
    for dirpath, _, filenames in os.walk(config.CACHE_DIR):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # Convert to MB


def purge_old_cache():
    cache_dir = config.CACHE_DIR
    current_time = time.time()
    purged_count = 0

    # Purge by age
    for root, _, files in os.walk(cache_dir):
        for name in files:
            file_path = os.path.join(root, name)
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > config.CACHE_PURGE_OLDER_THAN:
                try:
                    os.remove(file_path)
                    purged_count += 1
                except Exception as e:
                    log(f"Cache purge failed: {e}", "ERROR", "cache")

    # Purge by size (oldest first) if still over limit
    while get_cache_size() > config.MAX_CACHE_SIZE_MB:
        oldest_file = None
        oldest_time = current_time

        for root, _, files in os.walk(cache_dir):
            for name in files:
                file_path = os.path.join(root, name)
                file_time = os.path.getmtime(file_path)
                if file_time < oldest_time:
                    oldest_time = file_time
                    oldest_file = file_path

        if oldest_file:
            try:
                os.remove(oldest_file)
                purged_count += 1
            except Exception as e:
                log(f"Cache purge failed: {e}", "ERROR", "cache")
                break

    if purged_count:
        log(f"Purged {purged_count} cache items", "DEBUG", "cache")
