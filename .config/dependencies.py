import os
from pathlib import Path
import tomlkit

main_path = (Path(__file__).parent.parent)

config_path = (main_path / '.config')

with (config_path / "config.toml").open(
    mode=("rt"),
    encoding = "utf-8") \
    as fp:

    config = tomlkit.load(fp)

src_path = main_path / "src"

src_model = src_path / "model"

music_folder = src_model / config["music"]["music_folder"]

print(music_folder)





