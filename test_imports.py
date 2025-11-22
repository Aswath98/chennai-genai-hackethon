"""
Test script to verify imports work correctly
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    print("Testing imports...")
    
    # Test config import
    from config.settings import RANDOM_SEED, DATA_SIZE
    print("✅ Config import successful")
    
    # Test utils import
    from src.utils.helpers import generate_geographic_coordinates
    print("✅ Utils import successful")
    
    # Test data generation import
    from src.data_generation.generate_data import DataGenerator
    print("✅ Data generation import successful")
    
    print("\n🎉 All imports working correctly!")
    
    # Quick test of data generation
    print("\nTesting data generation...")
    coords = generate_geographic_coordinates(5)
    print(f"Generated 5 coordinates: {coords}")
    
    generator = DataGenerator()
    print("✅ DataGenerator initialized successfully")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
