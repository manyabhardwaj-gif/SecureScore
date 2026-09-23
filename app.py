# ============================================
# FLASK WEB APP - SecureScore (FIXED)
# ============================================
# Web interface for Cybersecurity Risk Assessment
# ============================================

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from questions import get_all_questions, get_categories
from scoring import calculate_category_score, calculate_overall_score, get_risk_level, CATEGORY_WEIGHTS

app = Flask(__name__)
app.secret_key = 'securescore_secret_key_12345'

# ============================================
# CONFIGURATION
# ============================================

COMPANY_NAME = "Naviotech Solutions"

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Home page - displays questionnaire"""
    questions_db = get_all_questions()
    categories = get_categories()
    
    # Convert questions to list for template
    questions_list = []
    for q_id, q_data in questions_db.items():
        question_item = {
            'id': q_id,
            'text': q_data['text'],
            'category': q_data['category'],
            'weight': q_data['weight']
        }
        questions_list.append(question_item)
    
    return render_template('index.html', 
                         questions=questions_list,
                         company_name=COMPANY_NAME,
                         total_questions=len(questions_list))

@app.route('/api/submit-assessment', methods=['POST'])
def submit_assessment():
    """Process submitted assessment answers"""
    
    try:
        data = request.json
        business_name = str(data.get('business_name', 'Test Business'))
        answers = data.get('answers', {})
        
        # Validate answers
        if not answers or len(answers) == 0:
            return jsonify({'success': False, 'error': 'No answers provided'}), 400
        
        # Convert answers to proper format
        answers_dict = {}
        questions_db = get_all_questions()
        
        for q_id, q_data in questions_db.items():
            if q_id in answers:
                answer_value = str(answers[q_id]).lower()
                if answer_value not in ['yes', 'partial', 'no']:
                    continue
                    
                answers_dict[q_id] = {
                    "answer": answer_value,
                    "text": str(q_data['text']),
                    "category": str(q_data['category']),
                    "weight": float(q_data['weight']),
                    "scores": q_data['scores']
                }
        
        if len(answers_dict) == 0:
            return jsonify({'success': False, 'error': 'No valid answers'}), 400
        
        # Calculate scores
        category_scores = {}
        for category in get_categories():
            score = calculate_category_score(answers_dict, category)
            category_scores[str(category)] = float(score)
        
        # Calculate overall score
        overall_score = calculate_overall_score(category_scores)
        
        # Get risk level
        risk_level, color, emoji = get_risk_level(float(overall_score))
        
        # Generate recommendations
        recommendations = get_recommendations(answers_dict)
        
        # Create response - ensure everything is JSON serializable
        result = {
            'success': True,
            'business_name': business_name,
            'overall_score': float(overall_score),
            'category_scores': category_scores,
            'risk_level': str(risk_level),
            'recommendations': [str(r) for r in recommendations],  # Ensure strings
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/report')
def report():
    """Display report page"""
    return render_template('report.html', company_name=COMPANY_NAME)

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_recommendations(answers_dict):
    """Generate specific recommendations based on answers"""
    
    recommendations = []
    
    for q_id, answer_data in answers_dict.items():
        answer = answer_data['answer']
        text = answer_data['text']
        
        # Only recommend for "no" and "partial" answers
        if answer in ["no", "partial"]:
            if answer == "no":
                severity = "CRITICAL"
            else:
                severity = "IMPROVE"
            
            # Create specific recommendation based on question
            if "2fa" in text.lower() or "two-factor" in text.lower():
                rec = f"{severity}: Enable 2FA/MFA on all accounts (blocks 99% of hacks)"
            elif "backup" in text.lower():
                rec = f"{severity}: Set up automatic daily/weekly backups to external storage"
            elif "update" in text.lower() or "patch" in text.lower():
                rec = f"{severity}: Enable automatic security updates for all systems"
            elif "firewall" in text.lower():
                rec = f"{severity}: Install/enable firewall protection immediately"
            elif "password" in text.lower() and "special" in text.lower():
                rec = f"{severity}: Enforce strong passwords with special characters"
            elif "password" in text.lower() and "change" in text.lower():
                rec = f"{severity}: Implement password change policy (every 3 months)"
            elif "phishing" in text.lower():
                rec = f"{severity}: Conduct security awareness training on phishing"
            elif "training" in text.lower():
                rec = f"{severity}: Provide cybersecurity training to all employees"
            elif "encryption" in text.lower():
                rec = f"{severity}: Implement data encryption for sensitive data"
            elif "access" in text.lower() and "employee" in text.lower():
                rec = f"{severity}: Remove access when employees leave company"
            elif "monitor" in text.lower():
                rec = f"{severity}: Set up monitoring/logging system"
            elif "segment" in text.lower() or "separate" in text.lower():
                rec = f"{severity}: Separate guest WiFi from company network"
            else:
                rec = f"{severity}: Address: {text}"
            
            recommendations.append(rec)
    
    return recommendations

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', company_name=COMPANY_NAME, error="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    print(f"Server error: {error}")
    return render_template('index.html', company_name=COMPANY_NAME, error="Server error"), 500

# ============================================
# RUN APP
# ============================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print(f"  🔐 {COMPANY_NAME} - SecureScore Web App 🔐")
    print("="*70)
    print("\n✅ Starting Flask app...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='localhost', port=5000)