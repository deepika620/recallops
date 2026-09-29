import streamlit as st

import store
import charts
from theme import inject_css, hero_banner, label, kpi_card

inject_css()

hero_banner("Incident Dashboard", "Every incident, broken down by time, category, severity, and outcome.")

incidents = store.load_incidents()
df = charts.to_df(incidents)
feedback = store.load_feedback()

# ---------------------------------------------------------------- KPI row
helpful = sum(1 for f in feedback if f["worked"])
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    kpi_card("Total incidents", len(df))
with k2:
    kpi_card("Avg. time to resolve", f"{df['mttr_minutes'].mean():.0f} min")
with k3:
    kpi_card("Top category", df["category"].mode().iloc[0])
with k4:
    kpi_card("Fixed first try", f"{df['first_try'].mean() * 100:.0f}%")
with k5:
    kpi_card("Fix feedback", f"{helpful}/{len(feedback)} helpful" if feedback else "None yet")

st.write("")

# ---------------------------------------------------------------- date range details
label("Coverage period")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Earliest incident", df["date"].min().strftime("%b %d, %Y"))
c2.metric("Latest incident", df["date"].max().strftime("%b %d, %Y"))
c3.metric("Years covered", df["date"].dt.year.nunique())
c4.metric("Months covered", df["date"].dt.to_period("M").nunique())

st.write("")

# ---------------------------------------------------------------- charts
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(charts.monthly_chart(df), theme=None, config={"displayModeBar": False})
with c2:
    st.plotly_chart(charts.weekday_chart(df), theme=None, config={"displayModeBar": False})

c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(charts.category_chart(df), theme=None, config={"displayModeBar": False})
with c4:
    st.plotly_chart(charts.mttr_chart(df), theme=None, config={"displayModeBar": False})

c3b, c4b = st.columns(2)
with c3b:
    st.plotly_chart(charts.mttr_trend_chart(df), theme=None, config={"displayModeBar": False})
with c4b:
    st.plotly_chart(charts.category_severity_chart(df), theme=None, config={"displayModeBar": False})

c5, c6 = st.columns(2)
with c5:
    st.plotly_chart(charts.severity_chart(df), theme=None, config={"displayModeBar": False})
with c6:
    st.plotly_chart(charts.attempts_chart(df), theme=None, config={"displayModeBar": False})

st.plotly_chart(charts.timeline_chart(df), theme=None, config={"displayModeBar": False})

# ---------------------------------------------------------------- detailed table
label("All incidents — full detail")
table = charts.table_df(incidents).copy()
table["year"] = charts.to_df(incidents)["date"].dt.year
table["month"] = charts.to_df(incidents)["date"].dt.strftime("%B")
table["day_of_week"] = charts.to_df(incidents)["date"].dt.day_name()
cols = ["id", "service", "severity", "category", "date", "year", "month",
        "day_of_week", "mttr_minutes", "symptom", "root_cause", "fix", "failed_attempts"]
st.dataframe(table[cols], use_container_width=True)

st.download_button("Download full data as CSV", table[cols].to_csv(index=False),
                   file_name="recallops_full_detail.csv", mime="text/csv",
                   icon=":material/download:")