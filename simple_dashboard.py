import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Simple dashboard for testing
st.set_page_config(page_title="Micro-Lending Risk Assessment", layout="wide")

def main():
    st.title("🏦 AI-Driven Micro-Lending Risk Assessment Platform")
    st.markdown("Real-time risk heatmaps and analytics for safer micro-lending decisions")
    
    # Check if data exists
    if not os.path.exists("data"):
        st.error("No data found. Please generate sample data first.")
        st.info("Run: `python generate_sample_data.py` in terminal")
        return
    
    # Load data
    try:
        if os.path.exists("results/individual_risk_scores.csv"):
            individual_data = pd.read_csv("results/individual_risk_scores.csv")
            st.success(f"✅ Loaded {len(individual_data):,} borrower records")
        else:
            st.error("Individual risk scores not found")
            return
            
        if os.path.exists("results/district_risk_aggregation.csv"):
            district_data = pd.read_csv("results/district_risk_aggregation.csv")
            st.success(f"✅ Loaded {len(district_data)} districts")
        else:
            district_data = None
            
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    # Overview metrics
    st.header("📈 Risk Assessment Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_risk = individual_data['overall_risk_score'].mean()
        st.metric("Average Risk Score", f"{avg_risk:.3f}")
    
    with col2:
        high_risk_pct = (individual_data['overall_risk_score'] > 0.7).mean() * 100
        st.metric("High Risk Borrowers", f"{high_risk_pct:.1f}%")
    
    with col3:
        total_exposure = individual_data['total_loan_amount'].sum()
        st.metric("Total Loan Exposure", f"₹{total_exposure/1e6:.1f}M")
    
    with col4:
        total_borrowers = len(individual_data)
        st.metric("Total Borrowers", f"{total_borrowers:,}")
    
    # Risk distribution
    st.header("📊 Risk Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Distribution", "Geographic", "District Summary"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk score histogram
            fig_hist = px.histogram(
                individual_data,
                x='overall_risk_score',
                nbins=30,
                title='Risk Score Distribution'
            )
            fig_hist.add_vline(x=avg_risk, line_dash="dash", line_color="red", annotation_text="Mean")
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Risk category pie chart
            risk_counts = individual_data['risk_category'].value_counts()
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title='Risk Category Distribution'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        if 'latitude' in individual_data.columns and 'longitude' in individual_data.columns:
            # Geographic scatter plot
            sample_data = individual_data.sample(min(1000, len(individual_data)), random_state=42)
            fig_scatter = px.scatter(
                sample_data,
                x='longitude',
                y='latitude',
                color='overall_risk_score',
                size='total_loan_amount',
                hover_data=['risk_category', 'income', 'age'],
                title='Geographic Distribution of Risk',
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("Geographic coordinates not available")
    
    with tab3:
        if district_data is not None:
            st.subheader("District Level Risk Summary")
            st.dataframe(district_data, use_container_width=True)
            
            # District risk chart
            fig_bar = px.bar(
                district_data,
                x='district_id',
                y='avg_risk_score',
                color='risk_level',
                title='Average Risk Score by District'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("District aggregation data not available")
    
    # Data table
    st.header("📋 Detailed Data")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        risk_filter = st.slider("Filter by Risk Score", 0.0, 1.0, (0.0, 1.0))
    
    with col2:
        risk_categories = st.multiselect(
            "Filter by Risk Category",
            individual_data['risk_category'].unique(),
            default=individual_data['risk_category'].unique()
        )
    
    # Apply filters
    filtered_data = individual_data[
        (individual_data['overall_risk_score'] >= risk_filter[0]) & 
        (individual_data['overall_risk_score'] <= risk_filter[1]) &
        (individual_data['risk_category'].isin(risk_categories))
    ]
    
    st.dataframe(filtered_data, use_container_width=True, height=400)
    
    # Summary
    st.metric("Filtered Records", f"{len(filtered_data):,}")

if __name__ == "__main__":
    main()
