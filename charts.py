import pandas as pd
import plotly.express as px

SEV = {"SEV-1": "#ef4444", "SEV-2": "#f59e0b", "SEV-3": "#3b82f6"}
PALETTE = ["#6366f1", "#8b5cf6", "#22d3ee", "#22c55e",
           "#f59e0b", "#ef4444", "#ec4899", "#14b8a6"]


def _style(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color="#cbd5e1", size=13),
        margin=dict(l=10, r=10, t=56, b=10),
        legend_title_text="",
        title_font_size=16,
        title_font_color="#f1f5f9",
        title_x=0.0,
        colorway=PALETTE,
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,.06)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,.06)", zeroline=False)
    return fig


def to_df(incidents):
    df = pd.DataFrame(incidents)
    df["date"] = pd.to_datetime(df["date"])
    df["n_failed"] = df["failed_attempts"].apply(len)
    df["first_try"] = df["n_failed"] == 0
    return df


def table_df(incidents):
    df = pd.DataFrame(incidents).drop(columns=["keywords"])
    df["failed_attempts"] = df["failed_attempts"].apply(lambda x: "; ".join(x) or "-")
    return df


def category_chart(df):
    counts = df.groupby("category").size().reset_index(name="incidents")
    counts = counts.sort_values("incidents")
    fig = px.bar(counts, x="incidents", y="category", orientation="h",
                 title="Incidents by category")
    fig.update_traces(marker_color="#6366f1")
    return _style(fig)


def mttr_chart(df):
    fig = px.bar(df.sort_values("mttr_minutes"), x="mttr_minutes", y="service",
                 color="severity", orientation="h", color_discrete_map=SEV,
                 title="Time to resolve (minutes)")
    return _style(fig)


def severity_chart(df):
    fig = px.pie(df, names="severity", hole=0.6, color="severity",
                 color_discrete_map=SEV, title="Severity mix")
    return _style(fig)


def timeline_chart(df):
    fig = px.scatter(df, x="date", y="mttr_minutes", color="severity",
                     size="mttr_minutes", size_max=30, hover_name="service",
                     color_discrete_map=SEV,
                     title="Incidents over time (bubble = time to resolve)")
    return _style(fig)


def attempts_chart(df):
    labels = df["first_try"].map({True: "Fixed on first attempt",
                                  False: "Needed more than one attempt"})
    fig = px.pie(
        names=labels, hole=0.6, title="First-attempt success",
        color=labels,
        color_discrete_map={
            "Fixed on first attempt": "#22c55e",
            "Needed more than one attempt": "#64748b",
        },
    )
    return _style(fig)


def compare_chart(df, inc):
    others = df[(df["category"] == inc["category"]) & (df["id"] != inc["id"])]

    labels = ["This incident"]
    values = [inc["mttr_minutes"]]
    colors = ["#8b5cf6"]

    if len(others) > 0:
        labels.append(f"Avg. other {inc['category']}")
        values.append(others["mttr_minutes"].mean())
        colors.append("#6366f1")

    labels.append("Avg. all incidents")
    values.append(df["mttr_minutes"].mean())
    colors.append("#64748b")

    fig = px.bar(
        x=labels, y=values, color=labels,
        color_discrete_sequence=colors,
        labels={"x": "", "y": "minutes"},
        text_auto=".0f",
        title="Time to resolve vs averages",
    )
    fig.update_layout(showlegend=False)
    return _style(fig)


def monthly_chart(df):
    d = df.copy()
    d["month"] = d["date"].dt.strftime("%b %Y")
    d["month_sort"] = d["date"].dt.to_period("M")
    counts = d.groupby(["month", "month_sort"]).size().reset_index(name="incidents")
    counts = counts.sort_values("month_sort")
    fig = px.bar(counts, x="month", y="incidents", title="Incidents by month")
    fig.update_traces(marker_color="#8b5cf6")
    return _style(fig)


def weekday_chart(df):
    d = df.copy()
    d["weekday"] = d["date"].dt.day_name()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = d.groupby("weekday").size().reindex(order, fill_value=0).reset_index(name="incidents")
    fig = px.bar(counts, x="weekday", y="incidents", title="Incidents by day of week")
    fig.update_traces(marker_color="#22d3ee")
    return _style(fig)


def mttr_trend_chart(df):
    """Average resolution time over each month — shows whether the team is getting faster."""
    d = df.copy()
    d["month"] = d["date"].dt.strftime("%b %Y")
    d["month_sort"] = d["date"].dt.to_period("M")
    trend = d.groupby(["month", "month_sort"])["mttr_minutes"].mean().reset_index()
    trend = trend.sort_values("month_sort")
    fig = px.line(trend, x="month", y="mttr_minutes", markers=True,
                  title="Avg. resolution time trend")
    fig.update_traces(line_color="#22c55e", marker_color="#22c55e")
    return _style(fig)


def category_severity_chart(df):
    """Stacked bar: which categories carry the most critical (SEV-1) incidents."""
    counts = df.groupby(["category", "severity"]).size().reset_index(name="incidents")
    fig = px.bar(counts, x="category", y="incidents", color="severity",
                 color_discrete_map=SEV, title="Category vs severity",
                 barmode="stack")
    return _style(fig)