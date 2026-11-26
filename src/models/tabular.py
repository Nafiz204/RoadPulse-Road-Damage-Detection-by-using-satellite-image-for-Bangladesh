"""
Tabular Classification Models for RoadPulse:
- Random Forest Classifier
- XGBoost Classifier
Trained on aggregated corridor band statistics and temporal delta indices.
"""
from typing import Dict, Any, Tuple
import numpy as np

try:
    from sklearn.ensemble import RandomForestClassifier
    import xgboost as xgb
except ImportError:
    pass


def build_random_forest_classifier(
    n_estimators: int = 150,
    max_depth: int = 12,
    random_state: int = 42
):
    """
    Construct Random Forest classifier with balanced class weighting.
    """
    return RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )


def build_xgboost_classifier(
    n_estimators: int = 150,
    max_depth: int = 6,
    learning_rate: float = 0.05,
    random_state: int = 42
):
    """
    Construct XGBoost classifier for 3-class road damage classification:
    Class 0: Intact / Paved
    Class 1: Degraded / Earthen
    Class 2: Submerged / Washed Out
    """
    return xgb.XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        objective="multi:softprob",
        num_class=3,
        random_state=random_state,
        eval_metric="mlogloss",
    )
