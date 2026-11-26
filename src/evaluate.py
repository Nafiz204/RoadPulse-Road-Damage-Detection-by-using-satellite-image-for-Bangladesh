"""
Evaluation and Spatial Cross-Validation Module for RoadPulse:
- Spatial K-Fold splitting to prevent spatial autocorrelation leakage
- Multi-class classification metrics: Macro F1, Per-class Precision/Recall, PR-AUC
- Confusion matrix plotting
"""
from typing import Dict, Any, List
import numpy as np

try:
    from sklearn.metrics import (
        classification_report,
        confusion_matrix,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.model_selection import GroupKFold
except ImportError:
    pass

from src.config import CONDITION_CLASSES


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray = None) -> Dict[str, Any]:
    """
    Compute comprehensive classification metrics across the 3 road condition classes.
    """
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    per_class_f1 = f1_score(y_true, y_pred, average=None, zero_division=0)
    per_class_precision = precision_score(y_true, y_pred, average=None, zero_division=0)
    per_class_recall = recall_score(y_true, y_pred, average=None, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    
    results = {
        "macro_f1": float(macro_f1),
        "confusion_matrix": cm.tolist(),
        "per_class": {},
    }
    
    for cls_idx, meta in CONDITION_CLASSES.items():
        if cls_idx < len(per_class_f1):
            results["per_class"][meta["label"]] = {
                "precision": float(per_class_precision[cls_idx]),
                "recall": float(per_class_recall[cls_idx]),
                "f1": float(per_class_f1[cls_idx]),
            }
            
    if y_proba is not None and y_proba.shape[1] == 3:
        try:
            results["ovr_roc_auc"] = float(roc_auc_score(y_true, y_proba, multi_class="ovr"))
        except Exception:
            results["ovr_roc_auc"] = None

    return results


def run_spatial_kfold(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    model_fn,
    n_splits: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform Spatial Cross-Validation by partitioning by spatial clusters or Upazilas.
    Ensures that road segments from the same geographic cluster are never split across train and validation folds.
    """
    gkf = GroupKFold(n_splits=n_splits)
    fold_results = []
    
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups=groups)):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        model = model_fn()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        y_proba = model.predict_proba(X_val) if hasattr(model, "predict_proba") else None
        
        metrics = compute_metrics(y_val, y_pred, y_proba)
        metrics["fold"] = fold + 1
        fold_results.append(metrics)
        print(f"Fold {fold+1} Spatial Macro F1: {metrics['macro_f1']:.4f}")
        
    return fold_results
