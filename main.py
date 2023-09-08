from urllib.parse import unquote
from typing import TypedDict

from threading import Thread
from time import sleep

import requests
import glob
import sys
import re
import os

mirrors = ["https://api.chimu.moe/v1/download/", "https://osu.direct/api/d/", "https://api.nerinyan.moe/d/"]


class Options(TypedDict):
    force_download: bool
    download_path: str
    list_path: str
    songs_path: str

def generate_queue(ids, size):
    queue = list()
    current = list()
    for id in ids:
        current.append(id)
        if len(current) == size:
            queue.append(current)
            current = list()
    if current:
        queue.append(current)
    return queue

def get_mirror(index, og_index):
    if index > len(mirrors):
        index = 0
    if index == og_index:
        return None
    return mirrors[index]


def download(og_mirror, mirror_index, path, beatmapset_id, retry=False) -> bool:
    mirror = get_mirror(mirror_index, -1 if not retry else og_mirror)
    if not mirror:
        print(f"Failed to download {beatmapset_id}!")
        return False
    r = requests.get(
        f"{mirror}{beatmapset_id}",
        allow_redirects=True,
        headers={"user-agent": "ezosudl 0.1"},
    )
    if not r.ok:
        print(f"{mirror} returned {r.status_code} for id {beatmapset_id}!")
        return download(og_mirror, mirror_index + 1, path, beatmapset_id, retry=True)
    if "content-disposition" in r.headers:
        d = r.headers["content-disposition"]
        name = re.findall("filename=(.+)", d)[0]
    else:
        name = f"{beatmapset_id}.osz"
    if name[0] == '"':
        name = name.replace('"', "")
    name = unquote(name).replace("/", "")
    with open(f"{path}/{name}", "wb") as f:
        f.write(r.content)
    print(f"downloaded {beatmapset_id}")
    sleep(0.5)
    return True


def parse_options(args) -> Options:
    options = Options(
        force_download=False,
        download_path="maps/",
        list_path="beatmaps.csv",
        songs_path=".",
    )
    for arg in args:
        if "--force_download" in arg or "-f" in arg:
            options["force_download"] = True
        elif "--download_path" in arg or "-o" in arg:
            options["download_path"] = arg.split("=")[1]
        elif "--list" in arg or "-l" in arg:
            options["list_path"] = arg.split("=")[1]
        elif "--songs-directory" in arg or "-s" in arg:
            options["songs_path"] = arg.split("=")[1]
    return options


def main():
    options = parse_options(sys.argv)
    os.makedirs(options['download_path'], exist_ok=True)
    ids = list()
    with open(options['list_path']) as f:
        for line in f.readlines():
            try:
                ids.append(int(line.split(",")[0].strip()))
            except:
                pass
    if not options['force_download']:
        for file in glob.glob(f"{options['songs_path']}/*") + glob.glob(f"{options['download_path']}/*"):
            id = 0
            try:
                id = int(file.split("/")[1].split()[0].strip())
                id = int(file.split()[0].strip())
            except:
                pass
            if id in ids:
                ids.remove(id)
    queue = generate_queue(ids, len(mirrors))
    for ids in queue:
        threads = list()
        for i in range(len(ids)):
            thread = Thread(target=download, args=(i, i, options['download_path'], ids[i]))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()