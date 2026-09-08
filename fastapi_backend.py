"""
FastAPI Backend - Land Acquisition Delay Prediction
Production-ready API server for SIH hackathon
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Initialize FastAPI app
app = FastAPI(
    title="Land Acquisition Delay Prediction API",
    description="AI-powered predictive analytics for infrastructure projects",
    version="1.0.0"
)

# Add CORS middleware (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model (global)
MODEL_PATH = "land_acquisition_model.pkl"
try:
    model_data = joblib.load(MODEL_PATH)
    MODEL = model_data['model']
    SCALER = model_data['scaler']
    LABEL_ENCODERS = model_data['label_encoders']
    FEATURE_NAMES = model_data['feature_names']
    EXPLAINER = model_data['explainer']
    FEATURE_IMPORTANCE = model_data['feature_importance']
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    print(f"❌ Model file not found at {MODEL_PATH}")
    print("   Generate model using: python ml_pipeline.py")
    MODEL = None

# ============================================================================
# DATA MODELS
# ============================================================================

class ProjectInput(BaseModel):
    """Input schema for project data"""
    project_type: str
    land_area_acres: float
    affected_families: int
    approval_days_passed: int
    approval_days_total: int
    pending_approvals: int
    legal_disputes_count: int
    compensation_pending_families: int
    compensation_disbursed_pct: float
    documentation_complete_pct: float
    possession_acquired_pct: float
    rehabilitation_progress_pct: float
    stakeholder_responsiveness_score: int
    inter_dept_coordination_score: int
    past_project_success_rate: float
    district_avg_delay_days: int
    project_status: str


class RiskFactor(BaseModel):
    """Risk factor with contribution information"""
    feature: str
    shap_value: float
    direction: str


class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    risk_score: int
    risk_category: str
    delay_probability: float
    top_factors: List[RiskFactor]
    recommendations: List[str]
    timestamp: str


class ProjectDatabase(BaseModel):
    """Schema for project analytics"""
    total_projects: int
    avg_risk_score: float
    critical_projects: int
    high_risk_projects: int
    district_trends: Dict[str, float]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if MODEL is None:
        return {"status": "error", "message": "Model not loaded"}
    return {
        "status": "healthy",
        "model_loaded": True,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_delay(project: ProjectInput):
    """
    Predict delay probability for a project
    
    Returns: risk_score (0-100), risk_category, delay_probability, top_factors, recommendations
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert input to DataFrame
        project_df = pd.DataFrame([project.dict()])
        
        # Preprocess
        X = project_df.copy()
        
        # Encode categorical features
        for col in LABEL_ENCODERS:
            if col in X.columns:
                X[col] = LABEL_ENCODERS[col].transform(X[col])
        
        # Scale features
        X_scaled = SCALER.transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=FEATURE_NAMES)
        
        # Predict
        delay_prob = float(MODEL.predict_proba(X_scaled)[0, 1])
        risk_score = int(delay_prob * 100)
        
        # Risk category
        if risk_score < 30:
            risk_category = "🟢 LOW RISK"
        elif risk_score < 60:
            risk_category = "🟡 MEDIUM RISK"
        elif risk_score < 80:
            risk_category = "🟠 HIGH RISK"
        else:
            risk_category = "🔴 CRITICAL"
        
        # Get SHAP explanations
        shap_values = EXPLAINER.shap_values(X_scaled)[0]
        
        # Top contributing factors
        factor_contributions = []
        for feature, shap_val in zip(FEATURE_NAMES, shap_values):
            factor_contributions.append({
                'feature': feature,
                'shap_value': float(np.abs(shap_val)),
                'direction': '↑ Increases Risk' if shap_val > 0 else '↓ Decreases Risk'
            })
        
        top_factors = sorted(factor_contributions, key=lambda x: x['shap_value'], reverse=True)[:5]
        
        # Generate recommendations
        recommendations = _generate_recommendations(project.dict())
        
        return PredictionResponse(
            risk_score=risk_score,
            risk_category=risk_category,
            delay_probability=delay_prob,
            top_factors=[RiskFactor(**f) for f in top_factors],
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.post("/batch_predict")
async def batch_predict(projects: List[ProjectInput]):
    """
    Batch predict for multiple projects
    
    Useful for district/state-level analytics
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for project in projects:
        try:
            result = await predict_delay(project)
            results.append(result.dict())
        except Exception as e:
            results.append({"error": str(e), "project": project.dict()})
    
    return {
        "total_projects": len(projects),
        "predictions": results,
        "summary": {
            "avg_risk_score": np.mean([r.get('risk_score', 0) for r in results if 'risk_score' in r]),
            "critical_count": len([r for r in results if r.get('risk_score', 0) >= 80]),
            "high_risk_count": len([r for r in results if 60 <= r.get('risk_score', 0) < 80])
        }
    }


@app.get("/feature_importance")
async def get_feature_importance(top_n: int = 10):
    """Get top N most important features for model predictions"""
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    top_features = FEATURE_IMPORTANCE.head(top_n).to_dict('records')
    
    return {
        "top_features": top_features,
        "total_features": len(FEATURE_NAMES),
        "model_type": "XGBoost"
    }


@app.get("/model_info")
async def get_model_info():
    """Get model metadata and performance info"""
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "XGBoost",
        "n_features": len(FEATURE_NAMES),
        "features": FEATURE_NAMES,
        "n_classes": 2,
        "classes": ["No Delay", "Delay"],
        "timestamp": datetime.now().isoformat()
    }


@app.post("/risk_distribution")
async def get_risk_distribution(projects: List[ProjectInput]):
    """
    Get risk distribution across projects
    Useful for state/district dashboard
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    risk_scores = []
    risk_categories = {"🟢 LOW": 0, "🟡 MEDIUM": 0, "🟠 HIGH": 0, "🔴 CRITICAL": 0}
    
    for project in projects:
        prediction = await predict_delay(project)
        score = prediction.risk_score
        risk_scores.append(score)
        
        if score < 30:
            risk_categories["🟢 LOW"] += 1
        elif score < 60:
            risk_categories["🟡 MEDIUM"] += 1
        elif score < 80:
            risk_categories["🟠 HIGH"] += 1
        else:
            risk_categories["🔴 CRITICAL"] += 1
    
    return {
        "total_projects": len(projects),
        "avg_risk_score": float(np.mean(risk_scores)),
        "median_risk_score": float(np.median(risk_scores)),
        "min_risk_score": float(np.min(risk_scores)),
        "max_risk_score": float(np.max(risk_scores)),
        "risk_distribution": risk_categories,
        "percentile_90": float(np.percentile(risk_scores, 90))
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _generate_recommendations(project: Dict) -> List[str]:
    """Generate actionable recommendations based on project features"""
    recommendations = []
    
    # Legal disputes
    if project.get('legal_disputes_count', 0) > 3:
        recommendations.append("⚖️ URGENT: Expedite legal clearance - Assign dedicated legal team for dispute resolution")
    
    # Compensation delays
    if project.get('compensation_pending_families', 0) > 50:
        recommendations.append("💰 URGENT: Accelerate compensation disbursement - Process pending applications within 2 weeks")
    
    # Low stakeholder engagement
    if project.get('stakeholder_responsiveness_score', 5) < 4:
        recommendations.append("🤝 Schedule stakeholder engagement - Conduct monthly coordination meetings with all parties")
    
    # Slow land possession
    if project.get('possession_acquired_pct', 50) < 50:
        recommendations.append("📋 Expedite land possession - Resolve ownership disputes and clear pending titles")
    
    # Poor documentation
    if project.get('documentation_complete_pct', 50) < 70:
        recommendations.append("📄 Complete missing documentation - Audit all pending records and fast-track completions")
    
    # Rehabilitation lag
    if project.get('rehabilitation_progress_pct', 50) < 30:
        recommendations.append("🏘️ Accelerate rehabilitation - Allocate additional resources for affected communities")
    
    # High approval backlog
    approval_progress = project.get('approval_days_passed', 0) / max(project.get('approval_days_total', 1), 1)
    if approval_progress < 0.3:
        recommendations.append("✋ Expedite approvals - Escalate pending clearances to senior officials")
    
    # Low coordination
    if project.get('inter_dept_coordination_score', 5) < 4:
        recommendations.append("🏢 Improve inter-departmental coordination - Establish project monitoring committee")
    
    # Fallback
    if not recommendations:
        recommendations.append("✅ Project progressing well - Continue regular monitoring and stakeholder engagement")
    
    return recommendations


# ============================================================================
# SAMPLE DATA ENDPOINTS (for demo)
# ============================================================================

@app.get("/sample_projects")
async def get_sample_projects():
    """Get sample projects for testing"""
    samples = [
        {
            "name": "Tamil Nadu Highway Expansion",
            "project_type": "Highway",
            "land_area_acres": 250,
            "affected_families": 120,
            "approval_days_passed": 90,
            "approval_days_total": 180,
            "pending_approvals": 2,
            "legal_disputes_count": 1,
            "compensation_pending_families": 20,
            "compensation_disbursed_pct": 70,
            "documentation_complete_pct": 85,
            "possession_acquired_pct": 80,
            "rehabilitation_progress_pct": 60,
            "stakeholder_responsiveness_score": 8,
            "inter_dept_coordination_score": 8,
            "past_project_success_rate": 0.85,
            "district_avg_delay_days": -10,
            "project_status": "Active"
        },
        {
            "name": "Railway Station Development",
            "project_type": "Railway",
            "land_area_acres": 180,
            "affected_families": 95,
            "approval_days_passed": 150,
            "approval_days_total": 360,
            "pending_approvals": 4,
            "legal_disputes_count": 3,
            "compensation_pending_families": 60,
            "compensation_disbursed_pct": 40,
            "documentation_complete_pct": 65,
            "possession_acquired_pct": 45,
            "rehabilitation_progress_pct": 30,
            "stakeholder_responsiveness_score": 3,
            "inter_dept_coordination_score": 2,
            "past_project_success_rate": 0.60,
            "district_avg_delay_days": 150,
            "project_status": "Pending"
        }
    ]
    return {"samples": samples}


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting FastAPI Server...")
    print("📍 API Documentation: http://localhost:8000/docs")
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
