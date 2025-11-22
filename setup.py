"""
Setup script for AI-Driven Micro-Lending Risk Assessment Platform
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_platform():
    """Set up the entire platform"""
    
    print("🏦 AI-DRIVEN MICRO-LENDING RISK ASSESSMENT PLATFORM SETUP")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    # Create directories
    print("\n📁 Creating directories...")
    directories = ["data", "results", "visualizations", "models"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    packages = [
        "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn",
        "plotly", "streamlit", "folium", "faker"
    ]
    
    for package in packages:
        success = run_command(f"pip install {package}", f"Installing {package}")
        if not success:
            print(f"⚠️  Warning: Failed to install {package}")
    
    # Generate sample data
    print("\n📊 Generating sample data...")
    success = run_command("python generate_sample_data.py", "Generating sample data")
    
    if success:
        print("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("\n🚀 Next steps:")
        print("  1. Launch dashboard: streamlit run simple_dashboard.py")
        print("  2. Run demo analysis: python demo.py")
        print("  3. Explore Jupyter notebook: jupyter lab notebooks/risk_analysis.ipynb")
        
        # Launch dashboard automatically
        print("\n🌐 Would you like to launch the dashboard now? (y/n)")
        response = input().lower().strip()
        if response in ['y', 'yes']:
            print("🚀 Launching dashboard...")
            os.system("streamlit run simple_dashboard.py")
    
    else:
        print("\n❌ Setup encountered errors. Please check the output above.")

if __name__ == "__main__":
    setup_platform()
