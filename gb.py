import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import zscore
import seaborn as sns
import matplotlib.pyplot as plt
import pyEDM


def run_ccm(cause, effect, ts):
    df_pair = ts[['event_date', cause, effect]].dropna()
    df_pair.columns = ['time', 'cause', 'effect']
    
    out = pyEDM.CCM(dataFrame=df_pair, E=4,
                    columns="cause", target="effect",
                    libSizes="10 150 5", sample=30)

    dfc = pd.DataFrame(out)
    dfc.columns = [c.lower() for c in dfc.columns]
    rho_col = [c for c in dfc.columns if ':' in c][0]
    
    return dfc[['libsize', rho_col]], rho_col


def main():
    st.set_page_config(page_title="CCM Dashboard", layout="wide")
    st.title(" Convergent Cross Mapping (CCM) Dashboard")

    
    uploaded_file = st.file_uploader("Upload your conflict CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file, parse_dates=["event_date"])
        
        df['event_label'] = df['event_type'] + '@' + df['admin1']
        top_labels = df['event_label'].value_counts().head(100).index.tolist()
        df_sub = df[df['event_label'].isin(top_labels)]

        ts = df_sub.groupby([pd.Grouper(key='event_date', freq='D'), 'event_label']) \
                   .size().unstack(fill_value=0).rolling(7).mean().dropna()
        ts = ts.apply(zscore).reset_index()

        st.success(" Data loaded and preprocessed!")

        labels = ts.columns[1:]

        cause = st.selectbox("Select Cause (X)", labels)
        effect = st.selectbox("Select Effect (Y)", labels)

        if st.button("Run CCM"):
            with st.spinner("Running CCM..."):
                dfc, rho_col = run_ccm(cause, effect, ts)
                st.success(f" CCM Complete — ρ (skill) shown below")

                
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.lineplot(data=dfc, x='libsize', y=rho_col, marker='o', ax=ax)
                ax.set_title(f"CCM Skill (ρ): {cause} → {effect}", fontsize=16)
                ax.set_xlabel("Library Size")
                ax.set_ylabel("Cross Mapping Skill (ρ)")
                ax.grid(True)
                st.pyplot(fig)

                st.dataframe(dfc)


if __name__ == "__main__":
    main()
