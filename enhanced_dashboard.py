import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Enhanced Micro-Lending Risk Assessment", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_enhanced_data():
    """Load all enhanced datasets"""
    data = {}
    
    # Check for enhanced data files
    enhanced_files = {
        'individual': 'results/individual_risk_scores.csv',
        'district': 'results/district_risk_aggregation.csv',
        'block': 'results/block_risk_aggregation.csv', 
        'panchayat': 'results/panchayat_risk_aggregation.csv',
        'districts_geo': 'data/districts.csv',
        'blocks_geo': 'data/blocks.csv',
        'panchayats_geo': 'data/panchayats.csv'
    }
    
    files_loaded = []
    for key, filepath in enhanced_files.items():
        if os.path.exists(filepath):
            try:
                data[key] = pd.read_csv(filepath)
                files_loaded.append(key)
            except Exception as e:
                st.warning(f"Error loading {filepath}: {e}")
    
    return data, files_loaded

def main():
    st.title("🏦 Enhanced AI-Driven Micro-Lending Risk Assessment Platform")
    st.markdown("**Real-time risk heatmaps with Block & Panchayat level granularity**")
    
    # Load enhanced data
    data, files_loaded = load_enhanced_data()
    
    if not data:
        st.error("No data found. Please run: `python generate_enhanced_data.py`")
        return
    
    st.success(f"✅ Loaded {len(files_loaded)} datasets: {', '.join(files_loaded)}")
    
    # Sidebar for controls
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Administrative level selection
    available_levels = []
    if 'district' in data:
        available_levels.append('District')
    if 'block' in data:
        available_levels.append('Block') 
    if 'panchayat' in data:
        available_levels.append('Panchayat')
    
    if available_levels:
        selected_level = st.sidebar.selectbox(
            "📍 Administrative Level", 
            available_levels,
            help="Choose the granularity level for analysis"
        )
        level_key = selected_level.lower()
    else:
        st.error("No administrative aggregation data found")
        return
    
    # Risk filters
    if 'individual' in data:
        individual_data = data['individual']
        
        st.sidebar.subheader("⚠️ Risk Filters")
        risk_range = st.sidebar.slider(
            "Risk Score Range",
            0.0, 1.0, (0.0, 1.0), 0.05,
            help="Filter by overall risk score"
        )
        
        if 'risk_category' in individual_data.columns:
            risk_categories = st.sidebar.multiselect(
                "Risk Categories",
                sorted(individual_data['risk_category'].unique()),
                default=sorted(individual_data['risk_category'].unique()),
                help="Filter by risk category"
            )
    
    # Main dashboard content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", "🗺️ Geographic Analysis", "📊 Risk Breakdown", 
        "🏛️ Administrative Analysis", "📋 Detailed Data"
    ])
    
    with tab1:
        display_overview_metrics(data)
    
    with tab2:
        display_geographic_analysis(data, level_key)
    
    with tab3:
        display_risk_breakdown(data)
    
    with tab4:
        display_administrative_analysis(data, available_levels)
    
    with tab5:
        display_detailed_data(data, level_key)

def display_overview_metrics(data):
    """Display key overview metrics"""
    st.header("📈 Enhanced Risk Assessment Overview")
    
    if 'individual' not in data:
        st.warning("Individual risk data not available")
        return
    
    individual_data = data['individual']
    
    # Enhanced metrics row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_risk = individual_data['overall_risk_score'].mean()
        st.metric(
            "Average Risk Score",
            f"{avg_risk:.3f}",
            delta=f"{(avg_risk - 0.5):+.3f} vs neutral"
        )
    
    with col2:
        high_risk_pct = (individual_data['overall_risk_score'] > 0.7).mean() * 100
        st.metric(
            "High Risk Borrowers",
            f"{high_risk_pct:.1f}%",
            delta=f"{high_risk_pct - 20:+.1f}% vs target",
            delta_color="inverse"
        )
    
    with col3:
        if 'loan_amount' in individual_data.columns:
            total_exposure = individual_data['loan_amount'].sum()
            st.metric("Total Loan Exposure", f"₹{total_exposure/1e6:.1f}M")
        else:
            total_exposure = individual_data['total_loan_amount'].sum()
            st.metric("Total Loan Exposure", f"₹{total_exposure/1e6:.1f}M")
    
    with col4:
        st.metric("Total Borrowers", f"{len(individual_data):,}")
    
    # Enhanced metrics row 2
    if all(col in individual_data.columns for col in ['demographic_risk', 'financial_risk']):
        st.subheader("🎯 Risk Component Analysis")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        risk_components = ['demographic_risk', 'financial_risk', 'geographic_risk', 'asset_risk', 'social_risk']
        available_components = [comp for comp in risk_components if comp in individual_data.columns]
        
        for i, component in enumerate(available_components[:5]):
            with [col1, col2, col3, col4, col5][i]:
                avg_component_risk = individual_data[component].mean()
                component_name = component.replace('_risk', '').title()
                st.metric(
                    f"{component_name} Risk",
                    f"{avg_component_risk:.3f}",
                    delta=f"{(avg_component_risk - 0.5):+.3f}"
                )
    
    # Quick insights
    if 'occupation' in individual_data.columns:
        st.subheader("💡 Quick Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            # Highest risk occupation
            occupation_risk = individual_data.groupby('occupation')['overall_risk_score'].mean().sort_values(ascending=False)
            st.info(f"**Highest Risk Occupation:** {occupation_risk.index[0]} (avg risk: {occupation_risk.iloc[0]:.3f})")
        
        with col2:
            # Geographic spread
            if all(col in individual_data.columns for col in ['latitude', 'longitude']):
                lat_range = individual_data['latitude'].max() - individual_data['latitude'].min()
                lon_range = individual_data['longitude'].max() - individual_data['longitude'].min()
                st.info(f"**Geographic Coverage:** {lat_range:.2f}° × {lon_range:.2f}° (lat × lon)")

def display_geographic_analysis(data, level_key):
    """Display geographic analysis and mapping"""
    st.header(f"🗺️ Geographic Risk Analysis - {level_key.title()} Level")
    
    if level_key not in data:
        st.warning(f"{level_key.title()} level data not available")
        return
    
    level_data = data[level_key]
    geo_data_key = f"{level_key}s_geo"
    
    # Geographic scatter plot
    if 'individual' in data and all(col in data['individual'].columns for col in ['latitude', 'longitude']):
        st.subheader("🌍 Risk Distribution Map")
        
        individual_data = data['individual']
        sample_size = min(2000, len(individual_data))
        sample_data = individual_data.sample(sample_size, random_state=42)
        
        color_col = 'overall_risk_score'
        size_col = 'loan_amount' if 'loan_amount' in sample_data.columns else 'total_loan_amount'
        
        fig_map = px.scatter_mapbox(
            sample_data,
            lat='latitude',
            lon='longitude',
            color=color_col,
            size=size_col,
            hover_data=['risk_category'] + ([col for col in ['occupation', 'education', 'age'] if col in sample_data.columns]),
            color_continuous_scale='RdYlGn_r',
            size_max=15,
            zoom=7,
            mapbox_style='open-street-map',
            title=f'Risk Distribution Map ({sample_size:,} borrowers)',
            height=600
        )
        
        # Center map on Tamil Nadu
        fig_map.update_layout(
            mapbox=dict(
                center=dict(lat=11.0, lon=78.0),
                zoom=6
            )
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    # Administrative level analysis
    st.subheader(f"📊 {level_key.title()} Level Risk Analysis")
    
    if 'avg_risk_score' in level_data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution by administrative unit
            fig_hist = px.histogram(
                level_data,
                x='avg_risk_score',
                nbins=20,
                title=f'Risk Score Distribution - {level_key.title()} Level',
                labels={'avg_risk_score': 'Average Risk Score'}
            )
            fig_hist.add_vline(
                x=level_data['avg_risk_score'].mean(),
                line_dash="dash", line_color="red",
                annotation_text=f"Mean: {level_data['avg_risk_score'].mean():.3f}"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Risk level distribution
            if 'risk_level' in level_data.columns:
                risk_counts = level_data['risk_level'].value_counts()
                fig_pie = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title=f'Risk Level Distribution - {level_key.title()}',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_pie, use_container_width=True)
    
    # Top risk areas
    if 'avg_risk_score' in level_data.columns:
        st.subheader(f"⚠️ Highest Risk {level_key.title()}s")
        top_risk = level_data.nlargest(10, 'avg_risk_score')[
            [f'{level_key}_id', 'avg_risk_score', 'num_borrowers', 'total_loan_volume']
        ]
        st.dataframe(top_risk, use_container_width=True)

def display_risk_breakdown(data):
    """Display detailed risk factor breakdown"""
    st.header("📊 Risk Factor Analysis")
    
    if 'individual' not in data:
        st.warning("Individual data required for risk breakdown")
        return
    
    individual_data = data['individual']
    
    # Risk factor correlation analysis
    risk_columns = [col for col in individual_data.columns if col.endswith('_risk')]
    
    if len(risk_columns) > 1:
        st.subheader("🔗 Risk Factor Correlations")
        
        correlation_matrix = individual_data[risk_columns + ['overall_risk_score']].corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu',
            title='Risk Factor Correlation Matrix'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Risk factor distributions
        st.subheader("📈 Risk Factor Distributions")
        
        fig_box = go.Figure()
        for factor in risk_columns:
            factor_name = factor.replace('_risk', '').replace('_', ' ').title()
            fig_box.add_trace(go.Box(
                y=individual_data[factor],
                name=factor_name,
                boxpoints='outliers'
            ))
        
        fig_box.update_layout(
            title='Risk Factor Distribution Comparison',
            yaxis_title='Risk Score',
            xaxis_title='Risk Factor'
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Demographic analysis
    if all(col in individual_data.columns for col in ['age', 'education', 'occupation']):
        st.subheader("👥 Demographic Risk Patterns")
        
        tab1, tab2, tab3 = st.tabs(["Age Analysis", "Education Impact", "Occupation Risk"])
        
        with tab1:
            # Age vs risk analysis
            age_risk = individual_data.groupby(pd.cut(individual_data['age'], bins=5))['overall_risk_score'].mean()
            fig_age = px.bar(
                x=[str(interval) for interval in age_risk.index],
                y=age_risk.values,
                title='Average Risk Score by Age Group',
                labels={'x': 'Age Group', 'y': 'Average Risk Score'}
            )
            st.plotly_chart(fig_age, use_container_width=True)
        
        with tab2:
            # Education vs risk
            education_risk = individual_data.groupby('education')['overall_risk_score'].mean().sort_values(ascending=False)
            fig_edu = px.bar(
                x=education_risk.index,
                y=education_risk.values,
                title='Average Risk Score by Education Level',
                labels={'x': 'Education Level', 'y': 'Average Risk Score'}
            )
            st.plotly_chart(fig_edu, use_container_width=True)
        
        with tab3:
            # Occupation vs risk
            occupation_risk = individual_data.groupby('occupation')['overall_risk_score'].mean().sort_values(ascending=False)
            fig_occ = px.bar(
                x=occupation_risk.values,
                y=occupation_risk.index,
                orientation='h',
                title='Average Risk Score by Occupation',
                labels={'x': 'Average Risk Score', 'y': 'Occupation'}
            )
            st.plotly_chart(fig_occ, use_container_width=True)

def display_administrative_analysis(data, available_levels):
    """Display administrative level comparison"""
    st.header("🏛️ Multi-Level Administrative Analysis")
    
    if len(available_levels) < 2:
        st.warning("Need at least 2 administrative levels for comparison")
        return
    
    # Prepare comparison data
    comparison_data = []
    for level in available_levels:
        level_key = level.lower()
        if level_key in data:
            df = data[level_key].copy()
            df['admin_level'] = level
            df['admin_units'] = len(df)
            comparison_data.append(df[['admin_level', 'admin_units', 'avg_risk_score', 'num_borrowers', 'total_loan_volume']])
    
    if comparison_data:
        # Summary comparison
        st.subheader("📊 Administrative Level Summary")
        
        summary_stats = []
        for level in available_levels:
            level_key = level.lower()
            if level_key in data:
                df = data[level_key]
                summary_stats.append({
                    'Level': level,
                    'Total Units': len(df),
                    'Avg Risk Score': f"{df['avg_risk_score'].mean():.3f}",
                    'Risk Std Dev': f"{df['avg_risk_score'].std():.3f}",
                    'Total Borrowers': f"{df['num_borrowers'].sum():,}",
                    'Total Loan Volume': f"₹{df['total_loan_volume'].sum()/1e6:.1f}M"
                })
        
        summary_df = pd.DataFrame(summary_stats)
        st.dataframe(summary_df, use_container_width=True)
        
        # Visual comparisons
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk score comparison
            fig_comp = go.Figure()
            for level in available_levels:
                level_key = level.lower()
                if level_key in data:
                    df = data[level_key]
                    fig_comp.add_trace(go.Box(
                        y=df['avg_risk_score'],
                        name=level,
                        boxpoints='outliers'
                    ))
            
            fig_comp.update_layout(
                title='Risk Score Distribution by Administrative Level',
                yaxis_title='Average Risk Score',
                xaxis_title='Administrative Level'
            )
            st.plotly_chart(fig_comp, use_container_width=True)
        
        with col2:
            # Volume comparison
            volume_data = []
            for level in available_levels:
                level_key = level.lower()
                if level_key in data:
                    df = data[level_key]
                    volume_data.append({
                        'Level': level,
                        'Avg Borrowers per Unit': df['num_borrowers'].mean(),
                        'Avg Loan Volume per Unit': df['total_loan_volume'].mean() / 1e6
                    })
            
            volume_df = pd.DataFrame(volume_data)
            fig_vol = px.bar(
                volume_df,
                x='Level',
                y='Avg Loan Volume per Unit',
                title='Average Loan Volume per Administrative Unit',
                labels={'y': 'Avg Loan Volume (₹M)'}
            )
            st.plotly_chart(fig_vol, use_container_width=True)

def display_detailed_data(data, level_key):
    """Display detailed data tables with filtering"""
    st.header("📋 Detailed Data Explorer")
    
    # Data selection
    data_options = []
    if 'individual' in data:
        data_options.append('Individual Borrowers')
    if level_key in data:
        data_options.append(f'{level_key.title()} Aggregation')
    
    if not data_options:
        st.warning("No data available for display")
        return
    
    selected_data = st.selectbox("Select Dataset", data_options)
    
    if selected_data == 'Individual Borrowers' and 'individual' in data:
        df = data['individual']
        st.subheader(f"👥 Individual Borrower Data ({len(df):,} records)")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'overall_risk_score' in df.columns:
                risk_filter = st.slider(
                    "Risk Score Filter",
                    float(df['overall_risk_score'].min()),
                    float(df['overall_risk_score'].max()),
                    (float(df['overall_risk_score'].min()), float(df['overall_risk_score'].max())),
                    step=0.01
                )
            else:
                risk_filter = None
        
        with col2:
            if 'risk_category' in df.columns:
                risk_cat_filter = st.multiselect(
                    "Risk Categories",
                    sorted(df['risk_category'].unique()),
                    default=sorted(df['risk_category'].unique())
                )
            else:
                risk_cat_filter = None
        
        with col3:
            if 'occupation' in df.columns:
                occupation_filter = st.multiselect(
                    "Occupations",
                    sorted(df['occupation'].unique()),
                    default=sorted(df['occupation'].unique())
                )
            else:
                occupation_filter = None
        
        # Apply filters
        filtered_df = df.copy()
        
        if risk_filter and 'overall_risk_score' in df.columns:
            filtered_df = filtered_df[
                (filtered_df['overall_risk_score'] >= risk_filter[0]) &
                (filtered_df['overall_risk_score'] <= risk_filter[1])
            ]
        
        if risk_cat_filter and 'risk_category' in df.columns:
            filtered_df = filtered_df[filtered_df['risk_category'].isin(risk_cat_filter)]
        
        if occupation_filter and 'occupation' in df.columns:
            filtered_df = filtered_df[filtered_df['occupation'].isin(occupation_filter)]
        
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Summary of filtered data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filtered Records", f"{len(filtered_df):,}")
        with col2:
            if 'overall_risk_score' in filtered_df.columns:
                st.metric("Avg Risk Score", f"{filtered_df['overall_risk_score'].mean():.3f}")
        with col3:
            loan_col = 'loan_amount' if 'loan_amount' in filtered_df.columns else 'total_loan_amount'
            if loan_col in filtered_df.columns:
                st.metric("Total Loan Volume", f"₹{filtered_df[loan_col].sum()/1e6:.1f}M")
    
    elif f'{level_key.title()} Aggregation' in selected_data and level_key in data:
        df = data[level_key]
        st.subheader(f"🏛️ {level_key.title()} Level Aggregation ({len(df):,} {level_key}s)")
        
        # Sorting options
        if 'avg_risk_score' in df.columns:
            sort_col = st.selectbox(
                "Sort by",
                [col for col in df.columns if col not in [f'{level_key}_id']],
                index=0 if 'avg_risk_score' in df.columns else 0
            )
            
            sort_order = st.radio("Sort order", ["Descending", "Ascending"])
            ascending = sort_order == "Ascending"
            
            sorted_df = df.sort_values(sort_col, ascending=ascending)
        else:
            sorted_df = df
        
        st.dataframe(sorted_df, use_container_width=True, height=400)

if __name__ == "__main__":
    main()
