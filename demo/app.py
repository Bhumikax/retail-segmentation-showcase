
from html import escape
from pathlib import Path
from textwrap import dedent

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

st.set_page_config(
    page_title="RETAIL / REFRAMED",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# VISUAL IDENTITY
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --ink: #11130f;
        --panel: #191c17;
        --panel-soft: #20241e;
        --paper: #e9ebdf;
        --muted: #999f91;
        --line: #343a30;
        --acid: #d5fa62;
        --coral: #ff866d;
        --white: #f5f6ef;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: var(--ink);
        color: var(--paper);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1440px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }

    [data-testid="stSidebar"] {
        background: var(--panel);
    }

    /* General text */
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--white) !important;
        letter-spacing: -0.045em;
    }

    p, li, label {
        color: var(--paper);
    }

    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
    }

    /* Hide Streamlit's default chrome */
    #MainMenu, footer {
        visibility: hidden;
    }

    /* Navigation */
    div[data-testid="stRadio"] > div {
        gap: 0.45rem;
    }

    div[data-testid="stRadio"] label {
        background: var(--panel);
        border: 1px solid var(--line);
        padding: 0.55rem 1rem;
        border-radius: 3px;
        transition: 0.2s ease;
    }

    div[data-testid="stRadio"] label:hover {
        border-color: var(--acid);
    }

    div[data-testid="stRadio"] label p {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: var(--paper);
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background: var(--panel);
        border-color: var(--line);
        color: var(--white);
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 5px;
        overflow: hidden;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 5px;
        padding: 1.1rem;
    }

    [data-testid="stMetricLabel"] p {
        color: var(--muted) !important;
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    [data-testid="stMetricValue"] {
        color: var(--acid) !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Buttons */
    .stButton button {
        background: var(--acid);
        color: var(--ink);
        border: none;
        border-radius: 3px;
        font-weight: 700;
    }

    .stButton button:hover {
        background: var(--white);
        color: var(--ink);
        border: none;
    }

    /* Dividers */
    hr {
        border-color: var(--line);
        margin: 2rem 0;
    }

    /* Editorial components */
    .eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--acid);
        margin-bottom: 0.8rem;
    }

    .masthead {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0 1.2rem 0;
        border-bottom: 1px solid var(--line);
        margin-bottom: 2.5rem;
    }

    .brand {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        color: var(--white);
    }

    .brand span {
        color: var(--acid);
    }

    .mast-meta {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        color: var(--muted);
        letter-spacing: 0.08em;
        text-align: right;
    }

    .hero {
        padding: 2.5rem 0 2rem 0;
    }

    .hero-kicker {
        font-family: 'DM Mono', monospace;
        color: var(--acid);
        font-size: 0.76rem;
        letter-spacing: 0.17em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(3.5rem, 9vw, 8.4rem);
        line-height: 0.91;
        font-weight: 700;
        letter-spacing: -0.085em;
        color: var(--white);
        margin: 0;
    }

    .hero-title .accent {
        color: var(--acid);
    }

    .hero-bottom {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: 2rem;
        margin-top: 2.5rem;
    }

    .hero-description {
        max-width: 510px;
        font-size: 1.05rem;
        line-height: 1.7;
        color: var(--muted);
    }

    .hero-index {
        font-family: 'DM Mono', monospace;
        color: var(--muted);
        font-size: 0.72rem;
        text-align: right;
        line-height: 1.8;
    }

    .hero-index strong {
        color: var(--acid);
        font-size: 1.3rem;
        font-weight: 500;
    }

    .stat-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        border-top: 1px solid var(--line);
        border-bottom: 1px solid var(--line);
        margin: 2.5rem 0;
    }

    .stat-cell {
        padding: 1.5rem 1.2rem 1.5rem 0;
        border-right: 1px solid var(--line);
    }

    .stat-cell:not(:first-child) {
        padding-left: 1.2rem;
    }

    .stat-cell:last-child {
        border-right: none;
    }

    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--acid);
        font-size: clamp(1.7rem, 3vw, 2.8rem);
        font-weight: 600;
        letter-spacing: -0.07em;
    }

    .stat-label {
        font-family: 'DM Mono', monospace;
        color: var(--muted);
        text-transform: uppercase;
        font-size: 0.65rem;
        letter-spacing: 0.1em;
        margin-top: 0.4rem;
    }

    .section-heading {
        display: flex;
        align-items: baseline;
        gap: 1rem;
        margin: 3.5rem 0 1.3rem 0;
        border-bottom: 1px solid var(--line);
        padding-bottom: 0.9rem;
    }

    .section-number {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: var(--acid);
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--white);
        letter-spacing: -0.05em;
    }

    .section-subtitle {
        font-size: 0.9rem;
        color: var(--muted);
        margin: 0.5rem 0 1.5rem 0;
        line-height: 1.6;
    }

    .story-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 5px;
        padding: 1.4rem;
        height: 100%;
    }

    .story-card.highlight {
        border-color: var(--acid);
    }

    .card-label {
        font-family: 'DM Mono', monospace;
        color: var(--muted);
        font-size: 0.68rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .card-number {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--acid);
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: -0.07em;
        line-height: 1.1;
    }

    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--white);
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0.6rem 0;
    }

    .card-copy {
        color: var(--muted);
        font-size: 0.85rem;
        line-height: 1.6;
    }

    .pull-quote {
        border-left: 3px solid var(--acid);
        padding: 0.8rem 1.2rem;
        margin: 1.5rem 0;
        color: var(--white);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        line-height: 1.4;
    }

    .pull-quote span {
        color: var(--acid);
    }

    .segment-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 5px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }

    .segment-top {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: flex-start;
    }

    .segment-name {
        color: var(--white);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
    }

    .segment-id {
        color: var(--acid);
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
    }

    .segment-share {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--acid);
        font-size: 1.5rem;
        font-weight: 600;
    }

    .segment-bar {
        height: 5px;
        background: #343a30;
        margin: 1rem 0;
        border-radius: 10px;
        overflow: hidden;
    }

    .segment-fill {
        height: 100%;
        background: var(--acid);
        border-radius: 10px;
    }

    .segment-meta {
        display: flex;
        justify-content: space-between;
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
    }

    .method-row {
        display: grid;
        grid-template-columns: 90px 1fr;
        gap: 1rem;
        padding: 1rem 0;
        border-bottom: 1px solid var(--line);
    }

    .method-index {
        color: var(--acid);
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
    }

    .method-title {
        color: var(--white);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }

    .method-copy {
        color: var(--muted);
        font-size: 0.85rem;
        line-height: 1.6;
    }

    .footer {
        border-top: 1px solid var(--line);
        margin-top: 4rem;
        padding-top: 1.5rem;
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.04em;
    }

    .footer strong {
        color: var(--acid);
        font-weight: 500;
    }

    @media (max-width: 700px) {
        .stat-strip {
            grid-template-columns: repeat(2, 1fr);
        }

        .stat-cell:nth-child(2) {
            border-right: none;
        }

        .stat-cell:nth-child(3) {
            border-top: 1px solid var(--line);
            padding-left: 0;
        }

        .stat-cell:nth-child(4) {
            border-top: 1px solid var(--line);
        }

        .hero-bottom {
            display: block;
        }

        .hero-index {
            text-align: left;
            margin-top: 1.5rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA LOADING AND VALIDATION
# ============================================================

@st.cache_data
def load_report(filename: str) -> pd.DataFrame:
    path = REPORTS / filename

    if not path.is_file():
        raise FileNotFoundError(
            f"Required report not found: {filename}"
        )

    return pd.read_csv(path)


try:
    cleaning = load_report("cleaning_report.csv")
    evaluation = load_report("cluster_evaluation.csv")
    profiles = load_report("segment_profiles.csv")
    preprocessing = load_report("preprocessing_sensitivity.csv")
    bootstrap = load_report("sensitivity_analysis.csv")

except (FileNotFoundError, pd.errors.ParserError) as exc:
    st.error(f"Unable to load aggregate reports: {exc}")
    st.stop()


required_columns = {
    "cleaning_report.csv": {
        "stage", "rule", "rows_removed", "rows_remaining"
    },
    "cluster_evaluation.csv": {
        "n_clusters", "silhouette_score",
        "calinski_harabasz_score", "davies_bouldin_score",
        "inertia", "min_cluster_size", "max_cluster_size",
    },
    "segment_profiles.csv": {
        "Cluster", "segment_name", "customer_count",
        "recency_mean", "recency_median",
        "frequency_mean", "frequency_median",
        "monetary_mean", "monetary_median",
    },
    "preprocessing_sensitivity.csv": {
        "configuration", "scaling", "n_clusters",
        "silhouette_score", "calinski_harabasz_score",
        "davies_bouldin_score", "inertia",
        "min_cluster_size", "max_cluster_size",
    },
    "sensitivity_analysis.csv": {
        "random_state", "reference_cluster",
        "candidate_cluster", "profile_distance",
    },
}

loaded_reports = {
    "cleaning_report.csv": cleaning,
    "cluster_evaluation.csv": evaluation,
    "segment_profiles.csv": profiles,
    "preprocessing_sensitivity.csv": preprocessing,
    "sensitivity_analysis.csv": bootstrap,
}


for filename, required in required_columns.items():
    missing = required - set(loaded_reports[filename].columns)

    if missing:
        st.error(
            f"{filename} is missing expected columns: "
            f"{sorted(missing)}"
        )
        st.stop()


# Privacy guard: only aggregate reports are allowed.
blocked_columns = {
    "CustomerID", "InvoiceNo", "InvoiceDate", "StockCode",
    "Description", "Quantity", "UnitPrice", "Revenue",
}

for filename, frame in loaded_reports.items():
    exposed = blocked_columns.intersection(frame.columns)

    if exposed:
        st.error(
            f"Privacy validation failed for {filename}. "
            f"Unexpected columns: {sorted(exposed)}"
        )
        st.stop()


# Normalize numerical fields.
numeric_columns = {
    "cleaning_report.csv": [
        "rows_removed", "rows_remaining"
    ],
    "cluster_evaluation.csv": [
        "n_clusters", "silhouette_score",
        "calinski_harabasz_score", "davies_bouldin_score",
        "inertia", "min_cluster_size", "max_cluster_size",
    ],
    "segment_profiles.csv": [
        "Cluster", "customer_count",
        "recency_mean", "recency_median",
        "frequency_mean", "frequency_median",
        "monetary_mean", "monetary_median",
    ],
    "preprocessing_sensitivity.csv": [
        "n_clusters", "silhouette_score",
        "calinski_harabasz_score", "davies_bouldin_score",
        "inertia", "min_cluster_size", "max_cluster_size",
    ],
    "sensitivity_analysis.csv": [
        "random_state", "reference_cluster",
        "candidate_cluster", "profile_distance",
    ],
}

for filename, columns in numeric_columns.items():
    frame = loaded_reports[filename]

    for column in columns:
        frame[column] = pd.to_numeric(
            frame[column],
            errors="raise",
        )


if cleaning.empty or profiles.empty or evaluation.empty:
    st.error("One or more required reports contain no data.")
    st.stop()


# ============================================================
# DERIVED VALUES
# ============================================================

total_raw = int(cleaning.iloc[0]["rows_remaining"])
total_clean = int(cleaning.iloc[-1]["rows_remaining"])
total_customers = int(profiles["customer_count"].sum())

retained_pct = (
    total_clean / total_raw * 100
    if total_raw > 0 else 0
)

profile_view = profiles.sort_values("Cluster").copy()

profile_view["share_pct"] = (
    profile_view["customer_count"]
    / total_customers * 100
)

smallest = profile_view.loc[
    profile_view["customer_count"].idxmin()
]

largest = profile_view.loc[
    profile_view["customer_count"].idxmax()
]

baseline = evaluation.loc[
    evaluation["n_clusters"] == 4
]

baseline_silhouette = (
    float(baseline.iloc[0]["silhouette_score"])
    if not baseline.empty else None
)


# ============================================================
# REUSABLE HTML HELPERS
# ============================================================

def section_heading(number: str, title: str) -> None:
    st.markdown(
        f"""
        <div class="section-heading">
            <span class="section-number">{escape(number)}</span>
            <span class="section-title">{escape(title)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def story_card(
    label: str,
    number: str,
    title: str,
    copy: str,
    highlight: bool = False,
) -> None:
    card_class = "story-card highlight" if highlight else "story-card"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="card-label">{escape(label)}</div>
            <div class="card-number">{escape(number)}</div>
            <div class="card-title">{escape(title)}</div>
            <div class="card-copy">{escape(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def segment_card(row: pd.Series) -> None:
    name = escape(str(row["segment_name"]))
    cluster = int(row["Cluster"])
    count = int(row["customer_count"])
    share = float(row["share_pct"])

    width = max(0, min(100, share))

    st.markdown(
        f"""
        <div class="segment-card">
            <div class="segment-top">
                <div>
                    <div class="segment-id">PROFILE / {cluster:02d}</div>
                    <div class="segment-name">{name}</div>
                </div>
                <div class="segment-share">{share:.1f}%</div>
            </div>
            <div class="segment-bar">
                <div class="segment-fill" style="width:{width:.2f}%"></div>
            </div>
            <div class="segment-meta">
                <span>{count:,} CUSTOMERS</span>
                <span>OF RFM POPULATION</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MASTHEAD
# ============================================================

st.markdown(
    """
    <div class="masthead">
        <div class="brand">RETAIL <span>/</span> REFRAMED</div>
        <div class="mast-meta">
            AN APPLIED AI & DATA STUDY<br>
            ONLINE RETAIL · 2010—2011
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

pages = [
    "THE BIG PICTURE",
    "THE SEGMENTS",
    "THE MODEL",
    "THE STRESS TEST",
    "THE FINE PRINT",
]

selected_page = st.radio(
    "Explore the study",
    pages,
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()


# ============================================================
# PAGE 1 — THE BIG PICTURE
# ============================================================

if selected_page == "THE BIG PICTURE":

    st.markdown(
        dedent(
            """
            <div class="hero">
                <div class="hero-kicker">
                    A STUDY IN CUSTOMER BEHAVIOUR · 01 / 05
                </div>
                <div class="hero-title">
                    BEHIND<br>
                    THE <span class="accent">PURCHASE.</span>
                </div>
                <div class="hero-bottom">
                    <div class="hero-description">
                        Every transaction leaves a pattern.
                        We used Recency, Frequency and Monetary
                        behaviour to uncover four distinct views
                        of retail purchasing — and tested how
                        much those patterns hold up.
                    </div>
                    <div class="hero-index">
                        DATASET<br>
                        <strong>UCI / 352</strong><br>
                        DOI: 10.24432/C5BW33
                    </div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="stat-strip">
            <div class="stat-cell">
                <div class="stat-value">{total_raw:,}</div>
                <div class="stat-label">Raw transactions</div>
            </div>
            <div class="stat-cell">
                <div class="stat-value">{total_clean:,}</div>
                <div class="stat-label">After cleaning</div>
            </div>
            <div class="stat-cell">
                <div class="stat-value">{total_customers:,}</div>
                <div class="stat-label">RFM profiles</div>
            </div>
            <div class="stat-cell">
                <div class="stat-value">04</div>
                <div class="stat-label">Selected clusters</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("01", "First, make the data usable.")

    st.markdown(
        """
        <div class="section-subtitle">
            Before looking for patterns, we need to understand
            what went into the analysis — and what did not.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.25, 0.75], gap="large")

    with left:
        st.markdown("##### THE CLEANING JOURNEY")

        cleaning_chart = cleaning[
            ["rule", "rows_remaining"]
        ].copy()

        cleaning_chart = cleaning_chart.rename(
            columns={
                "rule": "Cleaning stage",
                "rows_remaining": "Rows remaining",
            }
        )

        st.line_chart(
            cleaning_chart,
            x="Cleaning stage",
            y="Rows remaining",
            color="#d5fa62",
            width="stretch",
        )

    with right:
        story_card(
            "DATA RETENTION",
            f"{retained_pct:.1f}%",
            "Transactions retained",
            (
                f"{total_clean:,} of {total_raw:,} rows remained "
                "after the documented cleaning process."
            ),
            highlight=True,
        )

        st.markdown("")

        st.markdown(
            """
            <div class="card-copy">
                Cleaning covered cancellations, invalid quantities,
                missing customer identifiers, duplicate rows,
                invalid dates or prices, and extreme transaction lines.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    section_heading("02", "What are we actually measuring?")

    a, b, c = st.columns(3, gap="medium")

    with a:
        story_card(
            "R",
            "RECENCY",
            "When did they last buy?",
            "Days since the most recent transaction. Lower values mean a more recent purchase.",
        )

    with b:
        story_card(
            "F",
            "FREQUENCY",
            "How often did they buy?",
            "Number of distinct invoices. Higher values indicate more frequent purchasing.",
        )

    with c:
        story_card(
            "M",
            "MONETARY",
            "How much did they spend?",
            "Total transaction revenue. Values are measured in the source currency, GBP.",
        )

    st.markdown(
        """
        <div class="pull-quote">
            The goal isn't to find the <span>highest score.</span>
            It's to find patterns that are meaningful, interpretable,
            and honest about their limitations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("03", "The analytical route")

    method_items = [
        ("01", "Prepare", "Clean and validate the transaction data."),
        ("02", "Transform", "Build customer-level RFM features."),
        ("03", "Segment", "Apply StandardScaler and K-Means."),
        ("04", "Evaluate", "Compare candidate cluster counts."),
        ("05", "Challenge", "Test scaling sensitivity and bootstrap stability."),
    ]

    for number, title, copy in method_items:
        st.markdown(
            f"""
            <div class="method-row">
                <div class="method-index">{number}</div>
                <div>
                    <div class="method-title">{title}</div>
                    <div class="method-copy">{copy}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE 2 — THE SEGMENTS
# ============================================================

elif selected_page == "THE SEGMENTS":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">THE CUSTOMER LANDSCAPE · 02 / 05</div>
            <div class="hero-title">
                FOUR WAYS<br>
                TO <span class="accent">PURCHASE.</span>
            </div>
            <div class="hero-bottom">
                <div class="hero-description">
                    The selected baseline separates the RFM population
                    into four aggregate purchasing profiles.
                    These are behavioural patterns in historical
                    transaction data — not fixed customer identities.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("01", "The distribution")

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown("##### HOW THE POPULATION IS DIVIDED")

        for _, row in profile_view.iterrows():
            segment_card(row)

    with right:
        st.markdown("##### THE LARGEST PROFILE")

        story_card(
            "MOST COMMON",
            f"{largest['share_pct']:.1f}%",
            str(largest["segment_name"]),
            (
                f"{int(largest['customer_count']):,} profiles "
                "belong to this segment. It represents the largest "
                "share of the RFM population."
            ),
            highlight=True,
        )

        st.markdown("")

        st.markdown("##### THE SMALLEST PROFILE")

        story_card(
            "INTERPRET WITH CAUTION",
            f"{int(smallest['customer_count']):,}",
            str(smallest["segment_name"]),
            (
                f"This segment accounts for {smallest['share_pct']:.2f}% "
                "of the population. Its small size makes its profile "
                "more sensitive to changes in the data."
            ),
        )

    st.divider()

    section_heading("02", "Explore a profile")

    selected_cluster = st.selectbox(
        "Choose a segment",
        profile_view["Cluster"].tolist(),
        format_func=lambda value: (
            f"PROFILE {int(value):02d} — "
            + str(
                profile_view.loc[
                    profile_view["Cluster"] == value,
                    "segment_name",
                ].iloc[0]
            )
        ),
    )

    selected = profile_view.loc[
        profile_view["Cluster"] == selected_cluster
    ].iloc[0]

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Customer count",
        f"{int(selected['customer_count']):,}",
    )

    m2.metric(
        "Population share",
        f"{selected['share_pct']:.2f}%",
    )

    m3.metric(
        "Mean recency",
        f"{selected['recency_mean']:.1f} days",
    )

    m4.metric(
        "Mean frequency",
        f"{selected['frequency_mean']:.1f}",
    )

    st.markdown("")

    st.markdown(
        f"""
        <div class="story-card">
            <div class="card-label">PROFILE {int(selected['Cluster']):02d}</div>
            <div class="card-title">{escape(str(selected['segment_name']))}</div>
            <div class="card-copy">
                Mean monetary value:
                <span style="color:#d5fa62;font-weight:700;">
                    £{selected['monetary_mean']:,.2f}
                </span>
                <br><br>
                Median recency: {selected['recency_median']:.1f} days
                <br>
                Median frequency: {selected['frequency_median']:.1f}
                <br>
                Median monetary value: £{selected['monetary_median']:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    section_heading("03", "Compare the profiles")

    comparison = profile_view[
        [
            "segment_name",
            "customer_count",
            "share_pct",
            "recency_mean",
            "frequency_mean",
            "monetary_mean",
        ]
    ].rename(
        columns={
            "segment_name": "Segment",
            "customer_count": "Customers",
            "share_pct": "Share (%)",
            "recency_mean": "Mean recency (days)",
            "frequency_mean": "Mean frequency",
            "monetary_mean": "Mean monetary (GBP)",
        }
    )

    st.dataframe(
        comparison.style.format(
            {
                "Share (%)": "{:.2f}%",
                "Mean recency (days)": "{:.2f}",
                "Mean frequency": "{:.2f}",
                "Mean monetary (GBP)": "£{:,.2f}",
            }
        ),
        hide_index=True,
        width="stretch",
    )

    st.caption(
        "Lower recency means a more recent purchase. "
        "Frequency represents distinct invoices. "
        "Monetary values are aggregate revenue in GBP."
    )

    st.warning(
        "The smallest cluster contains very few profiles. "
        "Its unusually high frequency and monetary values should "
        "not be interpreted as a broadly representative customer type."
    )


# ============================================================
# PAGE 3 — THE MODEL
# ============================================================

elif selected_page == "THE MODEL":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">MODEL SELECTION · 03 / 05</div>
            <div class="hero-title">
                THE BEST<br>
                FIT ISN'T<br>
                ALWAYS THE <span class="accent">BEST.</span>
            </div>
            <div class="hero-bottom">
                <div class="hero-description">
                    Choosing the number of clusters is a trade-off.
                    A metric can look excellent while the resulting
                    groups tell an incomplete story.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("01", "The candidate models")

    metric_options = {
        "silhouette_score": "Silhouette score",
        "calinski_harabasz_score": "Calinski–Harabasz score",
        "davies_bouldin_score": "Davies–Bouldin score",
        "inertia": "Inertia",
    }

    metric_choice = st.selectbox(
        "Choose an evaluation metric",
        list(metric_options.keys()),
        format_func=lambda value: metric_options[value],
    )

    metric_data = evaluation[
        ["n_clusters", metric_choice]
    ].rename(
        columns={
            "n_clusters": "Number of clusters",
            metric_choice: "Score",
        }
    )

    st.bar_chart(
        metric_data,
        x="Number of clusters",
        y="Score",
        color="#d5fa62",
        width="stretch",
    )

    if metric_choice in [
        "silhouette_score",
        "calinski_harabasz_score",
    ]:
        st.caption("Higher values are generally preferred.")
    else:
        st.caption("Lower values are generally preferred.")

    st.dataframe(
        evaluation[
            [
                "n_clusters",
                "silhouette_score",
                "calinski_harabasz_score",
                "davies_bouldin_score",
                "min_cluster_size",
                "max_cluster_size",
            ]
        ].rename(
            columns={
                "n_clusters": "k",
                "silhouette_score": "Silhouette",
                "calinski_harabasz_score": "Calinski–Harabasz",
                "davies_bouldin_score": "Davies–Bouldin",
                "min_cluster_size": "Smallest cluster",
                "max_cluster_size": "Largest cluster",
            }
        ).style.format(
            {
                "Silhouette": "{:.4f}",
                "Calinski–Harabasz": "{:,.2f}",
                "Davies–Bouldin": "{:.4f}",
            }
        ),
        hide_index=True,
        width="stretch",
    )

    st.divider()

    section_heading("02", "Why choose four?")

    two_cluster = evaluation.loc[
        evaluation["n_clusters"] == 2
    ]

    if not two_cluster.empty:
        two = two_cluster.iloc[0]

        a, b = st.columns(2)

        with a:
            story_card(
                "HIGHEST SILHOUETTE",
                f"{two['silhouette_score']:.4f}",
                "Two clusters",
                (
                    f"The largest cluster contains "
                    f"{int(two['max_cluster_size']):,} of "
                    f"{total_customers:,} profiles."
                ),
            )

        with b:
            story_card(
                "SELECTED BASELINE",
                "k = 4",
                "More differentiated profiles",
                (
                    "The selected solution offers more differentiated "
                    "aggregate profiles and a higher silhouette score "
                    "than k = 3."
                ),
                highlight=True,
            )

    st.markdown(
        """
        <div class="pull-quote">
            A high silhouette score is useful.
            <span>It isn't the whole decision.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "The k = 2 solution has the highest silhouette score (0.9013), "
        "but its largest cluster contains 4,284 of the 4,306 profiles. "
        "That level of imbalance offers limited differentiation for "
        "this study."
    )

    st.write(
        "The k = 4 baseline was retained because it provides more "
        "differentiated profiles and a higher silhouette score than "
        "k = 3. This is a reasoned analytical choice, not proof that "
        "four is the uniquely correct number of clusters."
    )

    st.warning(
        "The smallest k = 4 cluster contains only 11 profiles. "
        "This is a material limitation of the selected baseline."
    )

    st.divider()

    section_heading("03", "The baseline configuration")

    x1, x2, x3 = st.columns(3)

    with x1:
        story_card(
            "FEATURE SCALING",
            "01",
            "StandardScaler",
            "Standardizes RFM features before clustering.",
        )

    with x2:
        story_card(
            "CLUSTERING",
            "04",
            "K-Means",
            "The selected baseline uses four clusters.",
        )

    with x3:
        story_card(
            "REPRODUCIBILITY",
            "42",
            "Random state",
            "The baseline uses random_state=42 and n_init=10.",
        )


# ============================================================
# PAGE 4 — THE STRESS TEST
# ============================================================

elif selected_page == "THE STRESS TEST":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">ROBUSTNESS & SENSITIVITY · 04 / 05</div>
            <div class="hero-title">
                WHAT<br>
                HAPPENS WHEN<br>
                WE <span class="accent">PUSH BACK?</span>
            </div>
            <div class="hero-bottom">
                <div class="hero-description">
                    A segmentation is only useful if we understand
                    how sensitive it is to analytical choices.
                    We challenged the baseline in two ways.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("01", "Change the scaling. What changes?")

    scale_view = preprocessing[
        [
            "scaling",
            "silhouette_score",
            "min_cluster_size",
            "max_cluster_size",
        ]
    ].rename(
        columns={
            "scaling": "Scaling",
            "silhouette_score": "Silhouette",
            "min_cluster_size": "Smallest cluster",
            "max_cluster_size": "Largest cluster",
        }
    )

    st.dataframe(
        scale_view.style.format(
            {"Silhouette": "{:.4f}"}
        ),
        hide_index=True,
        width="stretch",
    )

    st.write(
        "RobustScaler produces a higher silhouette score in this "
        "comparison, but also changes the cluster-size distribution "
        "substantially. A higher metric alone does not establish "
        "a better or more useful segmentation."
    )

    st.divider()

    section_heading("02", "Repeat the experiment")

    st.markdown(
        """
        <div class="section-subtitle">
            Bootstrap comparisons across random states 42–46.
            Smaller profile distances indicate closer matches
            between reference and candidate profiles.
        </div>
        """,
        unsafe_allow_html=True,
    )

    distance_summary = (
        bootstrap.groupby(
            "reference_cluster",
            as_index=False,
        )["profile_distance"]
        .mean()
        .rename(
            columns={
                "reference_cluster": "Reference cluster",
                "profile_distance": "Mean profile distance",
            }
        )
    )

    st.markdown("##### MEAN PROFILE DISTANCE BY REFERENCE CLUSTER")

    st.bar_chart(
        distance_summary,
        x="Reference cluster",
        y="Mean profile distance",
        color="#d5fa62",
        width="stretch",
    )

    st.markdown("##### EXPERIMENT DETAILS")

    selected_state = st.selectbox(
        "Inspect a random state",
        sorted(bootstrap["random_state"].unique().tolist()),
    )

    state_view = bootstrap.loc[
        bootstrap["random_state"] == selected_state
    ].sort_values("reference_cluster")

    st.dataframe(
        state_view,
        hide_index=True,
        width="stretch",
    )

    st.caption(
        "Cluster labels can change between runs. "
        "Profile matching is based on the recorded comparison distances."
    )

    st.divider()

    section_heading("03", "What survives the stress test?")

    st.markdown(
        """
        <div class="story-card highlight">
            <div class="card-label">THE IMPORTANT DISTINCTION</div>
            <div class="card-title">
                Recognizable patterns are not the same as guaranteed stability.
            </div>
            <div class="card-copy">
                Larger profiles are more recognizable across the
                limited bootstrap comparisons. The very small
                extreme-frequency group is more sensitive.
                Five random states do not establish long-term
                or out-of-sample stability.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.warning(
        "The robustness checks are limited exploratory diagnostics. "
        "They do not establish that the segmentation will remain "
        "stable over time or on another retailer's data."
    )


# ============================================================
# PAGE 5 — THE FINE PRINT
# ============================================================

elif selected_page == "THE FINE PRINT":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">METHODOLOGY & RESPONSIBLE USE · 05 / 05</div>
            <div class="hero-title">
                GOOD DATA.<br>
                CLEAR LIMITS.<br>
                <span class="accent">NO PRETENDING.</span>
            </div>
            <div class="hero-bottom">
                <div class="hero-description">
                    Every model has assumptions. Every dataset
                    has boundaries. Here's what this study
                    can tell us — and what it cannot.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("01", "The study, documented")

    method_items = [
        (
            "SOURCE",
            "UCI Online Retail",
            "Dataset ID 352. Transaction records from a UK-based "
            "non-store online retailer covering 2010–2011. "
            "DOI: 10.24432/C5BW33.",
        ),
        (
            "CLEANING",
            "Documented transaction rules",
            "Cancellation rows, non-positive quantities, missing "
            "customer identifiers, exact duplicates, invalid dates "
            "or prices, and extreme transaction lines were removed "
            "using the documented 99.5th-percentile outlier rule.",
        ),
        (
            "FEATURES",
            "Customer-level RFM",
            "Recency measures days since the most recent transaction. "
            "Frequency counts distinct invoices. Monetary measures "
            "total transaction revenue.",
        ),
        (
            "MODEL",
            "StandardScaler + K-Means",
            "Four clusters, random_state=42, n_init=10.",
        ),
        (
            "VALIDATION",
            "Model comparison and sensitivity",
            "Candidate cluster evaluation, alternative scaling, "
            "and bootstrap profile comparisons.",
        ),
    ]

    for index, (label, title, copy) in enumerate(method_items, start=1):
        st.markdown(
            f"""
            <div class="method-row">
                <div class="method-index">{escape(label)}</div>
                <div>
                    <div class="method-title">{escape(title)}</div>
                    <div class="method-copy">{escape(copy)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    section_heading("02", "What this study cannot claim")

    limitations = [
        (
            "Historical coverage",
            "The dataset covers one retailer and a historical period. "
            "Its patterns may not generalize to other retailers or "
            "present-day purchasing behaviour.",
        ),
        (
            "Cleaning effects",
            "Outlier thresholds and cleaning decisions influence "
            "which transactions remain in the analysis.",
        ),
        (
            "Smallest cluster",
            "The smallest segment is very small and less stable.",
        ),
        (
            "Exploratory model",
            "This is an aggregate analytical study, not a "
            "production-ready customer decision system.",
        ),
        (
            "Responsible interpretation",
            "Segments describe transaction purchasing patterns. "
            "They do not establish identity, personality, "
            "creditworthiness, or individual worth.",
        ),
    ]

    for title, copy in limitations:
        st.markdown(
            f"""
            <div class="method-row">
                <div class="method-index">NOTE</div>
                <div>
                    <div class="method-title">{escape(title)}</div>
                    <div class="method-copy">{escape(copy)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    section_heading("03", "Privacy by design")

    st.markdown(
        """
        <div class="story-card highlight">
            <div class="card-label">AGGREGATE-ONLY DISPLAY</div>
            <div class="card-title">
                No individual customer records are displayed.
            </div>
            <div class="card-copy">
                This experience loads aggregate project reports only.
                Raw transaction data, customer identifiers, invoice
                identifiers, and individual RFM records are not
                loaded into the application. A schema-level privacy
                guard rejects unexpected identifier-level columns.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.caption(
        "Source: UCI Machine Learning Repository — Online Retail. "
        "Dataset ID 352 · DOI 10.24432/C5BW33."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <div>
            <strong>RETAIL / REFRAMED</strong><br>
            AN AGGREGATE ANALYTICAL STUDY
        </div>
        <div>
            APPLIED AI & DATA FELLOWSHIP<br>
            BHUMIKA CHIDRAWAR
        </div>
        <div>
            UCI ONLINE RETAIL<br>
            2010—2011
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
