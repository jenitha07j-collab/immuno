import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ImmunoMimic", page_icon="🧬", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/mimicry_database.csv")

df = load_data()

# ---------- SIDEBAR NAV ----------
st.sidebar.title("🧬 ImmunoMimic")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Personalized Risk Check", "Pathogen Comparison", "Mimicry Leaderboard", "About the Science"]
)

# ---------- HOME ----------
if page == "Home":
    st.title("🧬 ImmunoMimic")
    st.subheader("Predicting Autoimmune Risk Through Pathogen–Human Molecular Mimicry")
    st.markdown("""
    Some infections leave more than a memory — they can leave your immune system confused.
    **Molecular mimicry** happens when a pathogen's proteins closely resemble your own body's
    proteins. After your immune system learns to attack the pathogen, it can mistakenly keep
    attacking the look-alike human protein — a documented trigger behind several autoimmune diseases.

    This tool lets you:
    - ✅ Check your **personal risk profile** based on infections you've had
    - 🔍 **Compare** two pathogens side-by-side
    - 🏆 See which pathogens carry the **highest mimicry risk**
    - 📖 Learn the **real immunology** behind each case
    """)
    col1, col2, col3 = st.columns(3)
    col1.metric("Pathogens Tracked", len(df))
    col2.metric("Organ Systems Covered", df["organ_system"].nunique())
    col3.metric("Diseases Linked", df["associated_disease"].nunique())
    st.info("👈 Use the sidebar to explore. Start with **Personalized Risk Check**.")

# ---------- PERSONALIZED RISK CHECK ----------
elif page == "Personalized Risk Check":
    st.title("🔍 Personalized Risk Check")
    st.write("Select infections you remember having. We'll cross-reference them against documented molecular mimicry cases.")

    selected = st.multiselect("Past infections:", df["pathogen"].tolist())
    family_history = st.checkbox("Family history of autoimmune disease")

    if st.button("Check My Risk Profile", type="primary"):
        if not selected:
            st.warning("Select at least one infection to check.")
        else:
            subset = df[df["pathogen"].isin(selected)].sort_values("severity_score", ascending=False)
            total_score = subset["severity_score"].sum()
            if family_history:
                total_score = round(total_score * 1.15, 1)

            st.subheader(f"Your Cumulative Mimicry Risk Score: {total_score}")
            if total_score >= 15:
                st.error("⚠️ Elevated cross-reactivity risk based on your infection history.")
            elif total_score >= 7:
                st.warning("🟡 Moderate cross-reactivity risk — worth being aware of.")
            else:
                st.success("🟢 Low cross-reactivity risk based on selections.")

            for _, row in subset.iterrows():
                with st.expander(f"{row['pathogen']} → {row['associated_disease']}"):
                    st.write(f"**Human target mimicked:** {row['human_target']}")
                    st.write(f"**Organ system affected:** {row['organ_system']}")
                    st.write(f"**Mechanism:** {row['mimicry_basis']}")
                    st.write(f"**Evidence level:** {row['evidence_level']}")
                    st.caption(f"Source: {row['source']}")

            st.caption("This is an educational screening tool based on published research, not a medical diagnosis. Consult a doctor for real health concerns.")

# ---------- PATHOGEN COMPARISON ----------
elif page == "Pathogen Comparison":
    st.title("⚖️ Pathogen Comparison")
    col1, col2 = st.columns(2)
    p1 = col1.selectbox("Pathogen A", df["pathogen"].tolist(), index=0)
    p2 = col2.selectbox("Pathogen B", df["pathogen"].tolist(), index=1)

    row1 = df[df["pathogen"] == p1].iloc[0]
    row2 = df[df["pathogen"] == p2].iloc[0]

    c1, c2 = st.columns(2)
    for col, row in [(c1, row1), (c2, row2)]:
        with col:
            st.subheader(row["pathogen"])
            st.write(f"**Type:** {row['pathogen_type']}")
            st.write(f"**Human target:** {row['human_target']}")
            st.write(f"**Organ system:** {row['organ_system']}")
            st.write(f"**Disease link:** {row['associated_disease']}")
            st.write(f"**Severity score:** {row['severity_score']}/10")

    if row1["organ_system"] == row2["organ_system"]:
        st.success(f"🔗 Both pathogens converge on the same organ system: **{row1['organ_system']}** — shared downstream autoimmune risk.")
    else:
        st.info("These pathogens mimic proteins in different organ systems — distinct autoimmune risk pathways.")

    fig = go.Figure(data=[
        go.Bar(name="Severity Score", x=[row1["pathogen"], row2["pathogen"]],
               y=[row1["severity_score"], row2["severity_score"]],
               marker_color=["#4C78A8", "#F58518"])
    ])
    fig.update_layout(yaxis_title="Mimicry Severity Score (0-10)")
    st.plotly_chart(fig, use_container_width=True)

# ---------- LEADERBOARD ----------
elif page == "Mimicry Leaderboard":
    st.title("🏆 Mimicry Leaderboard")
    st.write("Pathogens ranked by documented molecular mimicry severity.")

    sorted_df = df.sort_values("severity_score", ascending=False)
    fig = px.bar(sorted_df, x="severity_score", y="pathogen", orientation="h",
                 color="organ_system", labels={"severity_score": "Severity Score", "pathogen": ""},
                 title="Pathogen Mimicry Severity Ranking")
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Organ Systems Most Frequently Targeted")
    organ_counts = df["organ_system"].value_counts().reset_index()
    organ_counts.columns = ["Organ System", "Count"]
    fig2 = px.pie(organ_counts, names="Organ System", values="Count", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(sorted_df[["pathogen", "associated_disease", "organ_system", "severity_score", "evidence_level"]],
                 use_container_width=True, hide_index=True)

# ---------- ABOUT ----------
elif page == "About the Science":
    st.title("📖 About Molecular Mimicry")
    st.markdown("""
    ### What is molecular mimicry?
    Your immune system learns to recognize invaders by their proteins. Sometimes, a pathogen's
    protein sequence or structure closely resembles a protein your own body makes. When your
    immune system builds antibodies or T-cells to fight the infection, those same defenders can
    mistakenly attack your own matching tissue — even after the infection is gone.

    ### Why this matters
    This mechanism is considered a real contributor to several autoimmune diseases, including
    rheumatic heart disease, Guillain-Barré syndrome, and forms of multiple sclerosis and Type 1
    diabetes — conditions that together affect millions of people worldwide.

    ### How this database was built
    Each entry reflects **published, peer-reviewed evidence** of cross-reactivity between a
    specific pathogen component and a human protein — sourced from immunology and infectious
    disease literature (see sources listed under each pathogen).

    ### Important note
    This tool is for educational purposes. Severity scores reflect a simplified synthesis of
    published evidence strength and are **not a clinical diagnostic measure**. Always consult a
    healthcare professional for medical concerns.
    """)

st.sidebar.markdown("---")
st.sidebar.caption("ImmunoMimic — built as an academic project on pathogen-human molecular mimicry.")
