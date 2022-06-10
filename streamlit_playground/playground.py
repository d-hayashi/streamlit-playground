"""Streamlit Playground.

How to run?:

```shell
$ cd streamlit_playground
$ poetry run streamlit run playground.py

```

"""

import base64
import glob
import os
from io import BytesIO

import numpy as np
import pandas as pd
from pydtk.io.reader import BaseFileReader
from PIL import Image
import srt
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode


st.set_page_config(page_title="Video caption search", layout="wide")
st.title("Video caption search")


DATA_DIR = "../sample"

df = pd.DataFrame()
video_placeholder = st.empty()
video_info_placeholder = st.empty()

# ---


@st.cache
def load_files(dir: str):
    """Load str files in dir.

    Args:
        dir (str): directory path.

    Returns:
        data [dict]: a list of dicts.

    """
    print("loading data")
    res = []
    for file in glob.iglob(f"{dir}/*.srt"):
        filename = os.path.splitext(os.path.basename(file))[0]
        video_file = os.path.splitext(file)[0] + ".mp4"

        if not os.path.exists(video_file):
            continue

        # load video
        reader = BaseFileReader()
        v_timestamps, v_data, _ = reader.read(metadata=dict(path=video_file))

        # load srt
        with open(file, 'r') as f:
            data = f.read()
        for sub in srt.parse(data):
            time = sub.start.total_seconds()
            v_idx = np.argmin(np.abs(v_timestamps - time))
            thumbnail = Image.fromarray(v_data[v_idx][:, :, ::-1])
            thumbnail = thumbnail.resize((int(thumbnail.size[0] / thumbnail.size[1] * 200), 200))
            ofs = BytesIO()
            thumbnail.save(ofs, format="png")
            thumbnail = ofs.getvalue()

            res.append({
                "filename": filename,
                "start_time": time,
                "subtitle": sub.content.replace("\n", ""),
                "thumbnail": base64.b64encode(thumbnail).decode()
            })

    return res


def show_video(info: dict):
    with open(os.path.join(os.path.join(DATA_DIR, info["filename"] + ".mp4")), 'rb') as video_file:
        video_bytes = video_file.read()
        video_placeholder.video(video_bytes, start_time=int(info["start_time"]))
        video_info_placeholder.text(info["subtitle"])


data = load_files(DATA_DIR)

search_text = st.text_input('Search:', '')

df = pd.DataFrame.from_records(data)
df = df[df["subtitle"].str.contains(search_text, case=False)]
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="single")
gb.configure_grid_options(rowHeight=200)

image_nation = JsCode(
    """
    function (params) {
        var element = document.createElement("span");
        var imageElement = document.createElement("img");

        if (params.data.thumbnail) {
            imageElement.src = "data:image/png;base64," + params.data.thumbnail;
            imageElement.height="200";
        } else {
            imageElement.src = "";
        }
        element.appendChild(imageElement);
        return element;
    }
    """
)
gb.configure_column('thumbnail', cellRenderer=image_nation)


grid_options = gb.build()
grid = AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=800
)
selected_rows = grid["selected_rows"]


if len(selected_rows) > 0:
    show_video(selected_rows[0])
