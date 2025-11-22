"""
Main execution script for the AI-Driven Micro-Lending Risk Assessment Platform
"""
import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data_generation.generate_data import main as generate_data_main
from src.models.risk_assessment import main as risk_assessment_main
from src.visualization.heatmap_generator import main as visualization_main

def setup_directories():
    """Create necessary directories"""
    directories = ["data", "models", "results", "visualizations"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created/verified directory: {directory}")

def run_full_pipeline():
    """Run the complete risk assessment pipeline"""
    print("🚀 Starting AI-Driven Micro-Lending Risk Assessment Platform")
    print("=" * 60)
    
    # Setup directories
    print("\n📁 Setting up directories...")
    setup_directories()
    
    # Step 1: Generate synthetic data
    print("\n📊 Step 1: Generating synthetic data...")
    try:
        generate_data_main()
        print("✅ Data generation completed successfully")
    except Exception as e:
        print(f"❌ Error in data generation: {e}")
        return False
    
    # Step 2: Train models and assess risk
    print("\n🤖 Step 2: Training models and assessing risk...")
    try:
        risk_assessment_main()
        print("✅ Risk assessment completed successfully")
    except Exception as e:
        print(f"❌ Error in risk assessment: {e}")
        return False
    
    # Step 3: Generate visualizations
    print("\n📈 Step 3: Generating visualizations...")
    try:
        visualization_main()
        print("✅ Visualizations generated successfully")
    except Exception as e:
        print(f"❌ Error in visualization generation: {e}")
        return False
    
    print("\n🎉 Pipeline completed successfully!")
    print("\n📋 Generated outputs:")
    print("  • data/ - Synthetic datasets")
    print("  • models/ - Trained ML models")
    print("  • results/ - Risk assessment results")
    print("  • visualizations/ - Interactive heatmaps and charts")
    print("\n🌐 To view the dashboard, run:")
    print("  streamlit run dashboard/app.py")
    
    return True

def run_data_generation_only():
    """Run only data generation"""
    print("📊 Generating synthetic data...")
    setup_directories()
    generate_data_main()
    print("✅ Data generation completed")

def run_risk_assessment_only():
    """Run only risk assessment"""
    print("🤖 Running risk assessment...")
    setup_directories()
    risk_assessment_main()
    print("✅ Risk assessment completed")

def run_visualization_only():
    """Run only visualization generation"""
    print("📈 Generating visualizations...")
    setup_directories()
    visualization_main()
    print("✅ Visualizations generated")

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🌐 Launching dashboard...")
    os.system("streamlit run dashboard/app.py")

def main():
    parser = argparse.ArgumentParser(
        description="AI-Driven Micro-Lending Risk Assessment Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        choices=["full", "data", "models", "viz", "dashboard"],
        help="""
Command to execute:
  full      - Run complete pipeline (data + models + visualizations)
  data      - Generate synthetic data only
  models    - Run risk assessment and model training only
  viz       - Generate visualizations only
  dashboard - Launch Streamlit dashboard
        """
    )
    
    args = parser.parse_args()
    
    if args.command == "full":
        run_full_pipeline()
    elif args.command == "data":
        run_data_generation_only()
    elif args.command == "models":
        run_risk_assessment_only()
    elif args.command == "viz":
        run_visualization_only()
    elif args.command == "dashboard":
        launch_dashboard()

if __name__ == "__main__":
    main()
