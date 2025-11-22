"""
Demo script to showcase the AI-Driven Micro-Lending Risk Assessment Platform
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_risk_data():
    """Analyze the generated risk assessment data"""
    
    print("🏦 AI-DRIVEN MICRO-LENDING RISK ASSESSMENT PLATFORM")
    print("=" * 60)
    
    # Load data
    print("\n📊 Loading risk assessment data...")
    
    try:
        borrowers_df = pd.read_csv("results/individual_risk_scores.csv")
        district_df = pd.read_csv("results/district_risk_aggregation.csv")
        print(f"✅ Loaded {len(borrowers_df):,} borrower records")
        print(f"✅ Loaded {len(district_df)} district aggregations")
    except FileNotFoundError:
        print("❌ Data files not found. Please run data generation first.")
        return
    
    # Overall statistics
    print(f"\n📈 RISK ASSESSMENT SUMMARY:")
    print(f"  • Total borrowers analyzed: {len(borrowers_df):,}")
    print(f"  • Average risk score: {borrowers_df['overall_risk_score'].mean():.4f}")
    print(f"  • Risk score std deviation: {borrowers_df['overall_risk_score'].std():.4f}")
    print(f"  • Total loan exposure: ₹{borrowers_df['total_loan_amount'].sum()/1e6:.1f}M")
    
    # Risk distribution
    print(f"\n🎯 RISK CATEGORY DISTRIBUTION:")
    risk_dist = borrowers_df['risk_category'].value_counts()
    for category, count in risk_dist.items():
        percentage = count / len(borrowers_df) * 100
        print(f"  • {category}: {count:,} borrowers ({percentage:.1f}%)")
    
    # High-risk analysis
    high_risk_threshold = 0.7
    high_risk_borrowers = borrowers_df[borrowers_df['overall_risk_score'] > high_risk_threshold]
    print(f"\n⚠️  HIGH-RISK ANALYSIS (Risk Score > {high_risk_threshold}):")
    print(f"  • High-risk borrowers: {len(high_risk_borrowers):,} ({len(high_risk_borrowers)/len(borrowers_df)*100:.1f}%)")
    print(f"  • High-risk loan exposure: ₹{high_risk_borrowers['total_loan_amount'].sum()/1e6:.1f}M")
    print(f"  • Average age of high-risk borrowers: {high_risk_borrowers['age'].mean():.1f} years")
    print(f"  • Average income of high-risk borrowers: ₹{high_risk_borrowers['income'].mean():,.0f}")
    
    # District-level insights
    print(f"\n🗺️  DISTRICT-LEVEL INSIGHTS:")
    print(f"  • Number of districts: {len(district_df)}")
    print(f"  • District with highest risk: District {district_df.loc[district_df['avg_risk_score'].idxmax(), 'district_id']} (score: {district_df['avg_risk_score'].max():.3f})")
    print(f"  • District with lowest risk: District {district_df.loc[district_df['avg_risk_score'].idxmin(), 'district_id']} (score: {district_df['avg_risk_score'].min():.3f})")
    print(f"  • Average borrowers per district: {district_df['num_borrowers'].mean():.0f}")
    
    # Age and income analysis
    print(f"\n👥 DEMOGRAPHIC INSIGHTS:")
    print(f"  • Average borrower age: {borrowers_df['age'].mean():.1f} years")
    print(f"  • Age range: {borrowers_df['age'].min()}-{borrowers_df['age'].max()} years")
    print(f"  • Average income: ₹{borrowers_df['income'].mean():,.0f}")
    print(f"  • Income range: ₹{borrowers_df['income'].min():,.0f} - ₹{borrowers_df['income'].max():,.0f}")
    
    # Risk correlations
    numeric_columns = ['age', 'income', 'overall_risk_score', 'total_loan_amount']
    correlation_matrix = borrowers_df[numeric_columns].corr()
    
    print(f"\n🔗 RISK CORRELATIONS:")
    risk_corr = correlation_matrix['overall_risk_score'].sort_values(key=abs, ascending=False)
    for var, corr in risk_corr.items():
        if var != 'overall_risk_score':
            direction = "positive" if corr > 0 else "negative"
            strength = "strong" if abs(corr) > 0.5 else "moderate" if abs(corr) > 0.3 else "weak"
            print(f"  • {var}: {corr:.3f} ({strength} {direction} correlation)")
    
    # Recommendations
    print(f"\n💡 KEY RECOMMENDATIONS:")
    print(f"  • Focus enhanced due diligence on {len(high_risk_borrowers)} high-risk borrowers")
    print(f"  • Implement dynamic pricing based on risk scores")
    print(f"  • Deploy additional field officers in high-risk districts")
    print(f"  • Establish early warning systems for borrowers with >0.7 risk score")
    print(f"  • Consider portfolio diversification to balance risk exposure")
    
    # Technology stack info
    print(f"\n🛠️  TECHNOLOGY STACK:")
    print(f"  • Machine Learning: scikit-learn clustering algorithms")
    print(f"  • Data Processing: Pandas, NumPy for data manipulation")
    print(f"  • Visualization: Plotly, Folium for interactive charts and maps")
    print(f"  • Dashboard: Streamlit for real-time risk monitoring")
    print(f"  • Geographic Analysis: Multi-level administrative hierarchy")
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"  1. Launch interactive dashboard: streamlit run simple_dashboard.py")
    print(f"  2. View detailed analysis in Jupyter notebook: notebooks/risk_analysis.ipynb")
    print(f"  3. Train advanced ML models: python main.py models")
    print(f"  4. Generate comprehensive visualizations: python main.py viz")
    
    return borrowers_df, district_df

def create_summary_plots(borrowers_df, district_df):
    """Create summary visualization plots"""
    
    print(f"\n📊 Creating summary visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create a figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('AI-Driven Micro-Lending Risk Assessment - Summary Dashboard', fontsize=16, fontweight='bold')
    
    # Plot 1: Risk Score Distribution
    axes[0, 0].hist(borrowers_df['overall_risk_score'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].axvline(borrowers_df['overall_risk_score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {borrowers_df["overall_risk_score"].mean():.3f}')
    axes[0, 0].set_title('Overall Risk Score Distribution')
    axes[0, 0].set_xlabel('Risk Score')
    axes[0, 0].set_ylabel('Number of Borrowers')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Risk Categories
    risk_counts = borrowers_df['risk_category'].value_counts()
    colors = ['green', 'orange', 'red'] if len(risk_counts) == 3 else ['green', 'yellow', 'orange', 'red', 'darkred']
    axes[0, 1].pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', colors=colors[:len(risk_counts)])
    axes[0, 1].set_title('Risk Category Distribution')
    
    # Plot 3: District Risk Comparison
    axes[1, 0].bar(district_df['district_id'], district_df['avg_risk_score'], color='lightcoral', alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('Average Risk Score by District')
    axes[1, 0].set_xlabel('District ID')
    axes[1, 0].set_ylabel('Average Risk Score')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Risk vs Income Scatter
    scatter = axes[1, 1].scatter(borrowers_df['income'], borrowers_df['overall_risk_score'], 
                                alpha=0.6, c=borrowers_df['total_loan_amount'], cmap='viridis', s=30)
    axes[1, 1].set_title('Risk Score vs Income')
    axes[1, 1].set_xlabel('Income (₹)')
    axes[1, 1].set_ylabel('Risk Score')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Add colorbar for loan amount
    cbar = plt.colorbar(scatter, ax=axes[1, 1])
    cbar.set_label('Loan Amount (₹)')
    
    plt.tight_layout()
    
    # Save the plot
    os.makedirs('visualizations', exist_ok=True)
    plt.savefig('visualizations/risk_assessment_summary.png', dpi=300, bbox_inches='tight')
    print(f"✅ Summary plots saved to visualizations/risk_assessment_summary.png")
    
    plt.show()

def main():
    """Main demo function"""
    
    # Analyze risk data
    borrowers_df, district_df = analyze_risk_data()
    
    # Create summary plots
    if 'age' in borrowers_df.columns:  # Check if we have the expected columns
        create_summary_plots(borrowers_df, district_df)
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"\n📋 Available outputs:")
    print(f"  • data/ - Synthetic datasets")
    print(f"  • results/ - Risk assessment results") 
    print(f"  • visualizations/ - Summary charts")
    print(f"\n🌐 To explore interactively:")
    print(f"  streamlit run simple_dashboard.py")

if __name__ == "__main__":
    main()
