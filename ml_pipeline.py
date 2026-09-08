"""
Land Acquisition Delay Prediction - ML Pipeline
Advanced scikit-learn/XGBoost solution for SIH Hackathon
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    precision_recall_curve, f1_score, accuracy_score
)
import shap
import joblib
import warnings
warnings.filterwarnings('ignore')

class LandAcquisitionPredictor:
    """
    ML Pipeline for predicting land acquisition delays
    Includes training, evaluation, explainability, and prediction
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        self.explainer = None
        self.feature_importance = None
        
    def create_sample_dataset(self, n_samples=500):
        """
        Generate realistic sample data for demonstration
        Features based on problem statement
        """
        np.random.seed(self.random_state)
        
        data = {
            # Project basics
            'project_type': np.random.choice(['Highway', 'Railway', 'Port', 'Water', 'Power'], n_samples),
            'land_area_acres': np.random.normal(150, 80, n_samples).clip(10, 1000),
            'affected_families': np.random.poisson(50, n_samples),
            
            # Administrative factors
            'approval_days_passed': np.random.randint(30, 500, n_samples),
            'approval_days_total': np.random.randint(180, 730, n_samples),
            'pending_approvals': np.random.randint(0, 8, n_samples),
            
            # Legal & compensation
            'legal_disputes_count': np.random.poisson(2, n_samples),
            'compensation_pending_families': np.random.randint(0, 200, n_samples),
            'compensation_disbursed_pct': np.random.uniform(0, 100, n_samples),
            
            # Documentation & possession
            'documentation_complete_pct': np.random.uniform(20, 100, n_samples),
            'possession_acquired_pct': np.random.uniform(0, 100, n_samples),
            
            # Rehabilitation & coordination
            'rehabilitation_progress_pct': np.random.uniform(0, 100, n_samples),
            'stakeholder_responsiveness_score': np.random.randint(1, 10, n_samples),
            'inter_dept_coordination_score': np.random.randint(1, 10, n_samples),
            
            # Historical performance
            'past_project_success_rate': np.random.uniform(0.3, 1.0, n_samples),
            'district_avg_delay_days': np.random.randint(-100, 300, n_samples),
            'project_status': np.random.choice(['Active', 'Pending', 'Under Review'], n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Create target variable (delay probability)
        # Projects with legal disputes, low compensation, low coordination → higher delay risk
        delay_factors = (
            (df['legal_disputes_count'] / (df['legal_disputes_count'].max() + 1)) * 0.3 +
            (1 - df['compensation_disbursed_pct'] / 100) * 0.2 +
            (1 - df['stakeholder_responsiveness_score'] / 10) * 0.2 +
            (1 - df['inter_dept_coordination_score'] / 10) * 0.15 +
            (1 - df['possession_acquired_pct'] / 100) * 0.15
        )
        
        df['delay_probability'] = delay_factors
        df['is_delayed'] = (df['delay_probability'] > 0.5).astype(int)
        
        return df
    
    def preprocess_data(self, df, fit=True):
        """
        Preprocess features: encode categorical, scale numerical
        """
        df = df.copy()
        
        # Separate features and target
        X = df.drop(['is_delayed', 'delay_probability'], axis=1, errors='ignore')
        y = df.get('is_delayed', None)
        
        # Encode categorical features
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if fit:
                self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col])
            else:
                X[col] = self.label_encoders[col].transform(X[col])
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Scale numerical features
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        return X_scaled, y
    
    def train(self, df, test_size=0.2):
        """
        Train XGBoost model with hyperparameter tuning
        """
        print("🚀 Starting ML Pipeline Training...")
        
        # Preprocess
        print("📊 Preprocessing data...")
        X, y = self.preprocess_data(df, fit=True)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        print(f"✅ Train set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")
        print(f"✅ Positive class: {y_train.sum()} ({100*y_train.mean():.1f}%)")
        
        # Train XGBoost with hyperparameter tuning
        print("\n🤖 Training XGBoost model...")
        
        # Initial model
        xgb_base = XGBClassifier(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=self.random_state,
            eval_metric='logloss',
            n_jobs=-1
        )
        
        # Optional: Uncomment for hyperparameter tuning (adds 2-3 mins)
        # param_grid = {
        #     'max_depth': [5, 7, 9],
        #     'learning_rate': [0.01, 0.1, 0.05],
        #     'n_estimators': [100, 200, 300]
        # }
        # grid_search = GridSearchCV(xgb_base, param_grid, cv=3, scoring='f1')
        # grid_search.fit(X_train, y_train)
        # self.model = grid_search.best_estimator_
        # print(f"✅ Best params: {grid_search.best_params_}")
        
        # Train without tuning for speed
        self.model = xgb_base
        self.model.fit(X_train, y_train)
        
        # Evaluate
        print("\n📈 Model Evaluation:")
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        print(f"✅ Accuracy: {accuracy:.3f}")
        print(f"✅ F1-Score: {f1:.3f}")
        print(f"✅ ROC-AUC: {roc_auc:.3f}")
        print(f"\n{classification_report(y_test, y_pred)}")
        
        # Generate SHAP explainer
        print("\n🔍 Computing SHAP explanations...")
        self.explainer = shap.TreeExplainer(self.model)
        
        # Feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🎯 Top Features:")
        print(self.feature_importance.head(10))
        
        return {
            'accuracy': accuracy,
            'f1': f1,
            'roc_auc': roc_auc,
            'model': self.model,
            'explainer': self.explainer
        }
    
    def predict_with_explanation(self, project_data):
        """
        Predict delay probability and provide explanation
        
        Input: project_data (dict or pd.Series with features)
        Output: risk_score, top_factors, recommendations
        """
        # Ensure single sample
        if isinstance(project_data, dict):
            project_data = pd.DataFrame([project_data])
        elif isinstance(project_data, pd.Series):
            project_data = project_data.to_frame().T
        
        # Preprocess
        X, _ = self.preprocess_data(project_data, fit=False)
        
        # Predict
        delay_prob = self.model.predict_proba(X)[0, 1]
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
        
        # SHAP explanation
        shap_values = self.explainer.shap_values(X)[0]
        
        # Get top contributing factors
        factor_contributions = pd.DataFrame({
            'feature': self.feature_names,
            'shap_value': np.abs(shap_values),
            'direction': ['↑ Increases' if s > 0 else '↓ Decreases' for s in shap_values]
        }).sort_values('shap_value', ascending=False).head(5)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(project_data.iloc[0])
        
        return {
            'delay_probability': delay_prob,
            'risk_score': risk_score,
            'risk_category': risk_category,
            'top_factors': factor_contributions.to_dict('records'),
            'recommendations': recommendations,
            'shap_values': shap_values
        }
    
    def _generate_recommendations(self, project):
        """
        Rule-based recommendation engine
        """
        recommendations = []
        
        # High legal disputes
        if project.get('legal_disputes_count', 0) > 3:
            recommendations.append("⚖️ Expedite legal clearance: Assign dedicated legal team")
        
        # High compensation pending
        if project.get('compensation_pending_families', 0) > 50:
            recommendations.append("💰 Accelerate compensation: Prioritize disbursement for pending families")
        
        # Low stakeholder engagement
        if project.get('stakeholder_responsiveness_score', 5) < 4:
            recommendations.append("🤝 Improve coordination: Schedule stakeholder engagement meetings")
        
        # Slow possession acquisition
        if project.get('possession_acquired_pct', 50) < 50:
            recommendations.append("📋 Expedite land possession: Resolve ownership disputes urgently")
        
        # Low rehabilitation progress
        if project.get('rehabilitation_progress_pct', 50) < 30:
            recommendations.append("🏘️ Accelerate rehabilitation: Allocate additional resources")
        
        # Incomplete documentation
        if project.get('documentation_complete_pct', 50) < 70:
            recommendations.append("📄 Complete documentation: Fill pending records immediately")
        
        if not recommendations:
            recommendations.append("✅ Project on track: Continue current pace and monitoring")
        
        return recommendations
    
    def save_model(self, filepath='model.pkl'):
        """Save trained model and explainer"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'explainer': self.explainer,
            'feature_importance': self.feature_importance
        }, filepath)
        print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath='model.pkl'):
        """Load pre-trained model"""
        loaded = joblib.load(filepath)
        self.model = loaded['model']
        self.scaler = loaded['scaler']
        self.label_encoders = loaded['label_encoders']
        self.feature_names = loaded['feature_names']
        self.explainer = loaded['explainer']
        self.feature_importance = loaded['feature_importance']
        print(f"✅ Model loaded from {filepath}")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Initialize
    predictor = LandAcquisitionPredictor()
    
    # Create sample dataset
    print("📁 Generating sample dataset...")
    df = predictor.create_sample_dataset(n_samples=500)
    
    # Train model
    results = predictor.train(df)
    
    # Save model
    predictor.save_model('land_acquisition_model.pkl')
    
    # Example prediction
    print("\n" + "="*60)
    print("🔮 EXAMPLE PREDICTION")
    print("="*60)
    
    sample_project = {
        'project_type': 'Highway',
        'land_area_acres': 200,
        'affected_families': 150,
        'approval_days_passed': 120,
        'approval_days_total': 365,
        'pending_approvals': 3,
        'legal_disputes_count': 4,
        'compensation_pending_families': 80,
        'compensation_disbursed_pct': 35,
        'documentation_complete_pct': 60,
        'possession_acquired_pct': 40,
        'rehabilitation_progress_pct': 25,
        'stakeholder_responsiveness_score': 3,
        'inter_dept_coordination_score': 2,
        'past_project_success_rate': 0.65,
        'district_avg_delay_days': 120,
        'project_status': 'Pending'
    }
    
    prediction = predictor.predict_with_explanation(sample_project)
    
    print(f"\n🎯 Risk Score: {prediction['risk_score']}/100 {prediction['risk_category']}")
    print(f"📊 Delay Probability: {prediction['delay_probability']:.1%}\n")
    
    print("🔍 TOP CONTRIBUTING FACTORS:")
    for factor in prediction['top_factors']:
        print(f"  • {factor['feature']}: {factor['direction']} risk")
    
    print("\n💡 RECOMMENDATIONS:")
    for rec in prediction['recommendations']:
        print(f"  {rec}")
