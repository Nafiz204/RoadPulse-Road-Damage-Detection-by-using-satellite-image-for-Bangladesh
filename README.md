# RoadPulse: Road Damage Detection Using Satellite Imagery for Bangladesh
**Monitoring Macro-Scale Road Surface Degradation and Seasonal Flood Submergence Across Bangladesh Using Sentinel-2 Multi-Spectral Imagery and OpenStreetMap**

---

## 📌 Project Overview
- **Course:** CSE 445: Machine Learning
- **Institution:** North South University
- **Faculty:** Dr. Mohammad Abdul Qayum
- **Team Members:**
  - **Nafiz Imtiaz** (2222044042) — Project Lead
  - **Mahadi Hasan Nayan** (2222130042) — Co-Lead

RoadPulse combines free public satellite remote sensing (**Sentinel-2 Level-2A**) with open geospatial road vectors (**OpenStreetMap** & **Humanitarian Data Exchange**) to monitor macro-scale road surface degradation and flood-induced impassability across flood-vulnerable Upazilas in Bangladesh (e.g., Sunamganj Sadar, Chhatak, and Kurigram Sadar).

---

## 📂 Project Directory Structure

```text
RoadPulse/
├── data/
│   ├── raw_vectors/        # Raw OSM GeoJSON/shapefiles and HDX administrative boundaries
│   ├── processed_vectors/  # Segmented (100m) and buffered (15m) road corridor polygons
│   ├── ground_truth/       # UNOSAT flood inundation polygons and ground truth labels
│   └── features/           # Extracted multi-spectral band statistics and temporal delta indices
├── notebooks/              # Google Colab / Jupyter notebooks for prototyping and experimentation
├── src/
│   ├── __init__.py
│   ├── config.py           # Project constants, Upazila coordinates, band definitions, EPSG codes
│   ├── data_ingestion.py   # OSM road query and Sentinel-2 STAC search pipeline
│   ├── preprocessing.py    # Road segmentation, corridor buffering, and cloud masking
│   ├── feature_extract.py  # Spectral index formulations (NDWI, MNDWI, NDBI, BSI, NDVI)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tabular.py      # Random Forest and XGBoost classifiers
│   │   └── deep_learning.py# 1D-CNN and multi-spectral patch ResNet-18
│   └── evaluate.py         # Spatial K-Fold cross-validation, confusion matrices, PR-AUC
├── app/
│   └── app.py              # Streamlit + Leafmap interactive decision-support dashboard
├── requirements.txt        # Python package dependencies
└── README.md
```

---

## 🚀 Target Road Condition Classes
1. **Class 0 — Intact / Paved (Pucca):** Standard asphalt/concrete surface with stable reflectance and low water index.
2. **Class 1 — Degraded / Eroded Earthen (Katcha):** Stripped asphalt, bare mud, washed verge, or earthen track (characterized by high Bare Soil Index [BSI]).
3. **Class 2 — Submerged / Washed Out:** Flood-inundated or waterlogged road corridor (characterized by high Normalized Difference Water Index [NDWI/MNDWI] and high positive \(\Delta\text{NDWI}\)).

---

## 🛠️ Getting Started (Phase 1 Setup)

### 1. Python Environment
Python 3.10+ is recommended. You can install all project dependencies using pip:
```bash
pip install -r requirements.txt
```

### 2. Verified Data Pipeline Strategy
- **No paid API keys needed:** Uses Microsoft Planetary Computer open STAC endpoint and Geofabrik / Overpass OSM APIs.
- **Metric Projections:** Road geometries are projected to **EPSG:32645** / **EPSG:32646** (WGS 84 / UTM Zone 45N / 46N) for accurate 15-meter corridor buffering and 100-meter segmentation.
