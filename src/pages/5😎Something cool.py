

import pandas as pd
import numpy as np

from streamlit_extras.colored_header import colored_header
from streamlit_extras.customize_running import center_running
import time
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.echo_expander import echo_expander
from streamlit_extras.grid import grid

import streamlit as st
import dotenv
dotenv.load_dotenv()




# echo_expander结合了st.echo和st.expander，可以在expander中显示/隐藏代码
with echo_expander():

    st.markdown(
        """
        This component is a combination of `st.echo` and `st.expander`.
        The code inside the `with echo_expander()` block will be executed,
        and the code can be shown/hidden behind an expander
        """
    )



with echo_expander(code_location="below", label="Simple Dataframe example"):

    df = pd.DataFrame(
        [[1, 2, 3, 4, 5], [11, 12, 13, 14, 15]],
        columns=("A", "B", "C", "D", "E"),
    )
    st.dataframe(df)





colored_header(
    label="My New Pretty Colored Header",
    description="文献综述分析系统",
    color_name="violet-70",
)

# click = st.button("Observe where the 🏃‍♂️ running widget is now!")
# if click:
#     center_running()
#     time.sleep(2)


random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

my_grid = grid(2, [2, 4, 1], 1, 4, vertical_align="bottom")

# Row 1:
my_grid.dataframe(random_df, use_container_width=True)
my_grid.line_chart(random_df, use_container_width=True)
# Row 2:
my_grid.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
my_grid.text_input("Your name")
my_grid.button("Send", use_container_width=True)
# Row 3:
my_grid.text_area("Your message", height=40)
# Row 4:
my_grid.button("Example 1", use_container_width=True)
my_grid.button("Example 2", use_container_width=True)
my_grid.button("Example 3", use_container_width=True)
my_grid.button("Example 4", use_container_width=True)
# Row 5 (uses the spec from row 1):
with my_grid.expander("Show Filters", expanded=True):
    st.slider("Filter by Age", 0, 100, 50)
    st.slider("Filter by Height", 0.0, 2.0, 1.0)
    st.slider("Filter by Weight", 0.0, 100.0, 50.0)
my_grid.dataframe(random_df, use_container_width=True)
