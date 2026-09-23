# ============================================
# SCORING ENGINE - SecureScore
# ============================================
# This file calculates risk scores and generates recommendations
# ============================================

import json
import os
from datetime import datetime
from colorama import Fore, Back, Style, init
from questions import get_all_questions, get_categories

# Initialize colorama
init(autoreset=True)

# ============================================
# CONFIGURATION
# ============================================

DATA_FOLDER = "data"
ANSWERS_FILE = f"{DATA_FOLDER}/assessment_answers.json"
SCORES_FILE = f"{DATA_FOLDER}/assessment_scores.json"
COMPANY_NAME = "Naviotech Solutions"

# Category weights (30% Network, 30% Human, 40% Data)
CATEGORY_WEIGHTS = {
    "Network Security": 0.30,
    "Human Factors": 0.30,
    "Data Protection": 0.40
}

# ============================================
# FUNCTIONS
# ============================================

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title=""):
    """Print the header/logo"""
    clear_screen()
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + f"  🔐 {COMPANY_NAME} - SecureScore 🔐")
    print(Fore.CYAN + "=" * 70)
    if title:
        print(Fore.YELLOW + f"\n  {title}\n")
    else:
        print()

def load_answers():
    """
    Load previously saved answers from JSON file
    
    Returns:
        Dictionary with answers, or None if file doesn't exist
    """
    
    if not os.path.exists(ANSWERS_FILE):
        print_header()
        print(Fore.RED + "❌ No assessment found!")
        print(Fore.WHITE + "Please run 'python main.py' first to create an assessment.")
        input(Fore.YELLOW + "Press Enter to exit...")
        return None
    
    with open(ANSWERS_FILE, 'r') as f:
        return json.load(f)

def calculate_question_score(answer, question_data):
    """
    Calculate risk score for a single question
    
    Args:
        answer: "yes", "partial", or "no"
        question_data: Question dictionary with scores
    
    Returns:
        Risk score (higher = more risky)
    """
    
    return question_data["scores"][answer]

def calculate_category_score(answers_dict, category):
    """
    Calculate weighted risk score for a specific category
    
    Args:
        answers_dict: Dictionary with all answers
        category: Category name ("Network Security", etc.)
    
    Returns:
        Risk score (0-100, higher = more risk)
    """
    
    questions_db = get_all_questions()
    
    # Get all questions in this category
    category_questions = {qid: qdata for qid, qdata in questions_db.items() 
                         if qdata['category'] == category}
    
    if not category_questions:
        return 0
    
    total_weighted_score = 0
    total_possible_weighted_score = 0
    
    for question_id, question_data in category_questions.items():
        if question_id in answers_dict:
            answer = answers_dict[question_id]["answer"]
            score = question_data["scores"][answer]
            weight = question_data["weight"]
            
            # Add weighted score
            total_weighted_score += (score * weight)
            
            # Add maximum possible weighted score
            total_possible_weighted_score += (100 * weight)
    
    if total_possible_weighted_score == 0:
        return 0
    
    # Calculate percentage (0-100)
    category_score = (total_weighted_score / total_possible_weighted_score) * 100
    return round(category_score, 1)

def calculate_overall_score(category_scores):
    """
    Calculate overall risk score using category weights
    
    Args:
        category_scores: Dictionary with scores for each category
    
    Returns:
        Overall risk score (0-100)
    """
    
    overall = 0
    
    for category, weight in CATEGORY_WEIGHTS.items():
        if category in category_scores:
            overall += (category_scores[category] * weight)
    
    return round(overall, 1)

def get_risk_level(score):
    """
    Determine risk level based on score
    
    Args:
        score: Risk score (0-100)
    
    Returns:
        Tuple of (level_name, color, emoji)
    """
    
    if score < 20:
        return ("LOW RISK", Fore.GREEN, "🟢")
    elif score < 50:
        return ("MEDIUM RISK", Fore.YELLOW, "🟡")
    else:
        return ("HIGH RISK", Fore.RED, "🔴")

def get_specific_recommendations(answers_dict, category):
    """
    Generate SPECIFIC recommendations based on weak answers
    
    Args:
        answers_dict: Dictionary with all answers
        category: Category to analyze
    
    Returns:
        List of specific recommendations
    """
    
    questions_db = get_all_questions()
    recommendations = []
    
    # Get all questions in this category
    category_questions = {qid: qdata for qid, qdata in questions_db.items() 
                         if qdata['category'] == category}
    
    for question_id, question_data in category_questions.items():
        if question_id in answers_dict:
            answer = answers_dict[question_id]["answer"]
            
            # Only recommend for "no" and "partial" answers
            if answer in ["no", "partial"]:
                score = question_data["scores"][answer]
                text = question_data["text"]
                
                # Create specific recommendation
                if answer == "no":
                    severity = "🔴 CRITICAL"
                    action = "IMPLEMENT IMMEDIATELY"
                else:
                    severity = "🟡 IMPROVE"
                    action = "IMPROVE SOON"
                
                # Create specific recommendation based on question
                if "2FA" in text or "two-factor" in text:
                    rec = f"{severity}: Enable 2FA/MFA on all accounts (blocks 99% of hacks)"
                elif "backup" in text.lower():
                    rec = f"{severity}: Set up automatic daily/weekly backups to external storage"
                elif "update" in text.lower() or "patch" in text.lower():
                    rec = f"{severity}: Enable automatic security updates for all systems"
                elif "firewall" in text.lower():
                    rec = f"{severity}: Install/enable firewall protection immediately"
                elif "password" in text.lower() and "special" in text.lower():
                    rec = f"{severity}: Enforce strong passwords with special characters (@,#,$)"
                elif "password" in text.lower() and "change" in text.lower():
                    rec = f"{severity}: Implement password change policy (every 3 months)"
                elif "phishing" in text.lower():
                    rec = f"{severity}: Conduct security awareness training on phishing detection"
                elif "training" in text.lower():
                    rec = f"{severity}: Provide cybersecurity training to all employees"
                elif "encryption" in text.lower():
                    rec = f"{severity}: Implement data encryption for sensitive information"
                elif "access" in text.lower() and "employee" in text.lower():
                    rec = f"{severity}: Create process to remove access when employees leave"
                elif "monitor" in text.lower() or "check" in text.lower():
                    rec = f"{severity}: Set up monitoring/logging system for access attempts"
                elif "segmentation" in text.lower() or "separate" in text.lower():
                    rec = f"{severity}: Separate guest WiFi from company network"
                else:
                    rec = f"{severity}: Address: {text}"
                
                recommendations.append(rec)
    
    return recommendations

def print_category_breakdown(category_scores):
    """Print detailed breakdown of each category"""
    
    print_header("Category Breakdown")
    print()
    
    for category, score in category_scores.items():
        level, color, emoji = get_risk_level(score)
        
        # Print category header
        print(color + f"{emoji} {category}: {score}/100")
        
        # Print risk bar
        filled = int(30 * score / 100)
        bar = '█' * filled + '░' * (30 - filled)
        print(color + f"  [{bar}]")
        
        # Print status
        print(color + f"  Status: {level}")
        print()

def print_overall_score(overall_score):
    """Print overall risk score with emphasis"""
    
    print_header("Overall Risk Assessment")
    print()
    
    level, color, emoji = get_risk_level(overall_score)
    
    print(Fore.WHITE + f"Business Cybersecurity Risk Score:")
    print()
    print(color + f"  {emoji} OVERALL SCORE: {overall_score}/100")
    print(color + f"  Status: {level}")
    print()
    
    # Print large risk bar
    filled = int(50 * overall_score / 100)
    bar = '█' * filled + '░' * (50 - filled)
    print(color + f"  [{bar}]")
    print()
    
    # Print interpretation
    if overall_score < 20:
        print(Fore.GREEN + "✅ Excellent cybersecurity posture! Keep up the good work.")
    elif overall_score < 50:
        print(Fore.YELLOW + "⚠️  Good foundation, but some improvements needed.")
    else:
        print(Fore.RED + "🚨 URGENT: Multiple critical vulnerabilities. Take immediate action!")
    
    print()

def print_recommendations(all_recommendations):
    """Print all recommendations organized by priority"""
    
    print_header("Action Recommendations")
    print()
    
    # Separate by severity
    critical = [r for r in all_recommendations if "CRITICAL" in r]
    improve = [r for r in all_recommendations if "IMPROVE" in r]
    
    if critical:
        print(Fore.RED + "🔴 CRITICAL (DO FIRST):")
        for i, rec in enumerate(critical, 1):
            print(Fore.RED + f"  {i}. {rec}")
        print()
    
    if improve:
        print(Fore.YELLOW + "🟡 IMPROVEMENTS NEEDED:")
        for i, rec in enumerate(improve, 1):
            print(Fore.YELLOW + f"  {i}. {rec}")
        print()
    
    if not critical and not improve:
        print(Fore.GREEN + "✅ No critical issues found!")
        print()

def save_scores_report(answers, category_scores, overall_score):
    """
    Save detailed scores and recommendations to JSON file
    
    Args:
        answers: Original answers dictionary
        category_scores: Scores for each category
        overall_score: Overall risk score
    """
    
    # Collect all recommendations
    all_recommendations = []
    for category in CATEGORY_WEIGHTS.keys():
        all_recommendations.extend(get_specific_recommendations(answers["answers"], category))
    
    # Create report dictionary
    report = {
        "business_name": answers["business_name"],
        "assessment_date": answers["timestamp"],
        "assessment_mode": answers["mode"],
        "scores": {
            "overall": overall_score,
            "categories": category_scores
        },
        "risk_levels": {
            "overall": get_risk_level(overall_score)[0],
            "categories": {cat: get_risk_level(score)[0] for cat, score in category_scores.items()}
        },
        "recommendations": all_recommendations,
        "total_answers": len(answers["answers"]),
        "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to JSON
    with open(SCORES_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    
    print_header("Report Saved")
    print(Fore.GREEN + "✅ Detailed report saved!")
    print(Fore.WHITE + f"📁 Saved to: {SCORES_FILE}")
    print()

# ============================================
# MAIN PROGRAM
# ============================================

def main():
    """Main scoring program"""
    
    # Load answers
    answers = load_answers()
    if not answers:
        return
    
    print_header("Analyzing Assessment...")
    print(Fore.WHITE + "Calculating risk scores...\n")
    
    # Extract answers
    answers_dict = answers["answers"]
    
    # Calculate category scores
    category_scores = {}
    for category in CATEGORY_WEIGHTS.keys():
        score = calculate_category_score(answers_dict, category)
        category_scores[category] = score
    
    # Calculate overall score
    overall_score = calculate_overall_score(category_scores)
    
    # Print category breakdown
    print_category_breakdown(category_scores)
    input(Fore.YELLOW + "Press Enter to see overall score...")
    
    # Print overall score
    print_overall_score(overall_score)
    input(Fore.YELLOW + "Press Enter to see recommendations...")
    
    # Collect all recommendations
    all_recommendations = []
    for category in CATEGORY_WEIGHTS.keys():
        all_recommendations.extend(get_specific_recommendations(answers_dict, category))
    
    # Print recommendations
    print_recommendations(all_recommendations)
    input(Fore.YELLOW + "Press Enter to save detailed report...")
    
    # Save report
    save_scores_report(answers, category_scores, overall_score)
    
    # Final message
    print_header("Next Steps")
    print()
    print(Fore.CYAN + "📊 Your assessment is complete!")
    print()
    print(Fore.WHITE + "1. Review the recommendations above")
    print(Fore.WHITE + "2. Priority critical issues first (🔴 CRITICAL)")
    print(Fore.WHITE + "3. Then tackle improvements (🟡 IMPROVE)")
    print()
    print(Fore.GREEN + "Optional: Run 'python report.py' to generate an HTML report")
    print()
    input(Fore.YELLOW + "Press Enter to exit...")

# ============================================
# RUN PROGRAM
# ============================================

if __name__ == "__main__":
    main()