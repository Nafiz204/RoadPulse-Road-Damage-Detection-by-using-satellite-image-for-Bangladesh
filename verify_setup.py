"""
RoadPulse Phase 1 Local Environment Verification Script.
Checks directory structure, configuration integrity, and core modules.
"""
import sys
from pathlib import Path

def test_environment():
    print("=" * 60)
    print("🛰️  RoadPulse - Phase 1 Environment Verification")
    print("=" * 60)
    print(f"Python Version: {sys.version.split()[0]}")
    
    base_dir = Path(__file__).resolve().parent
    print(f"Project Base Directory: {base_dir}")
    
    required_dirs = [
        "data/raw_vectors",
        "data/processed_vectors",
        "data/ground_truth",
        "data/features",
        "notebooks",
        "src",
        "src/models",
        "app",
    ]
    
    print("\n[1/3] Verifying Directory Layout:")
    all_dirs_ok = True
    for rel_dir in required_dirs:
        p = base_dir / rel_dir
        status = "✅ Found" if p.is_dir() else "❌ Missing"
        if not p.is_dir():
            all_dirs_ok = False
        print(f"  - {rel_dir:<25}: {status}")
        
    print("\n[2/3] Verifying Core Configuration & Files:")
    required_files = [
        "requirements.txt",
        "README.md",
        "src/config.py",
        "src/data_ingestion.py",
        "src/preprocessing.py",
        "src/feature_extract.py",
        "src/models/tabular.py",
        "src/models/deep_learning.py",
        "src/evaluate.py",
        "app/app.py",
    ]
    all_files_ok = True
    for rel_file in required_files:
        f = base_dir / rel_file
        status = "✅ Found" if f.is_file() else "❌ Missing"
        if not f.is_file():
            all_files_ok = False
        print(f"  - {rel_file:<25}: {status}")

    print("\n[3/3] Checking Configuration Parameters:")
    try:
        from src.config import PILOT_UPAZILAS, CONDITION_CLASSES, SEASONAL_WINDOWS
        print(f"  - Pilot Upazilas Configured: {list(PILOT_UPAZILAS.keys())}")
        print(f"  - Road Classes Defined: {[v['label'] for v in CONDITION_CLASSES.values()]}")
        print(f"  - Time Windows Defined: {list(SEASONAL_WINDOWS.keys())}")
        config_ok = True
    except Exception as e:
        print(f"  ❌ Error importing configuration: {e}")
        config_ok = False
        
    print("\n" + "=" * 60)
    if all_dirs_ok and all_files_ok and config_ok:
        print("🎉 PHASE 1 LOCAL SETUP COMPLETE & VERIFIED!")
        print("Next step: Install packages with 'pip install -r requirements.txt'")
        print("Then proceed to Phase 2 (OSM Road Vector Acquisition).")
    else:
        print("⚠️ Some components are missing. Please inspect errors above.")
    print("=" * 60)

if __name__ == "__main__":
    test_environment()
