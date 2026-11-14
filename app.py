"""TerraSleuth Streamlit app (skeleton).  Run: streamlit run app.py

TODO(B): map (geemap/folium), cold-case presets, two-region compare,
witness (news) button, polish. This skeleton already runs the full
question -> data -> stats -> verdict loop.
"""
import plotly.graph_objects as go
import streamlit as st

from terrasleuth.data_sources import get_timeseries
from terrasleuth.stats import analyze_trend
from terrasleuth.translator import REGIONS, translate
from terrasleuth.variables import VARIABLES

st.set_page_config(page_title="TerraSleuth", page_icon="🌍", layout="wide")
st.title("🌍 TerraSleuth")
st.caption("Solve Earth's mysteries, one data point at a time.")

question = st.text_input("File a report — what do you want to investigate?",
                         "Is drought getting worse in California?")
c1, c2 = st.columns(2)
start_year = c1.number_input("From year", 2000, 2024, 2005)
end_year = c2.number_input("To year", 2001, 2025, 2024)

if st.button("Open the case 🔍"):
    plan = translate(question)
    spec = VARIABLES[plan["variable"]]
    df, note = get_timeseries(plan["variable"], plan["bbox"], int(start_year), int(end_year),
                              region_name=plan["region"])
    res = analyze_trend(df["year"], df["value"])

    st.subheader(f"Suspect: {spec['label']} — {plan['region'].title()}")
    st.info(spec["plain"] + f"  \nSource: {spec['source']}  \nData: {note}")

    fig = go.Figure()
    fig.add_scatter(x=df["date"], y=df["value"], mode="lines", name="Observed")
    st.plotly_chart(fig, use_container_width=True)

    (st.error if res.significant else st.warning)(res.verdict)
    with st.expander("Scientific evidence file (raw numbers)"):
        st.json(res.to_dict())

with st.expander("About & limitations"):
    st.write("Linear/monotonic trends only. No seasonal adjustment. "
             "Significance does not imply causation.")
