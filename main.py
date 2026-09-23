# ============================================
# MAIN QUESTIONNAIRE - SecureScore (ENHANCED)
# ============================================
# This file asks all 30 questions and collects answers
# With COLORS, LIVE SCORING, and MODES
# ============================================

import json
import os
from datetime import datetime
from colorama import Fore, Back, Style, init
from questions import get_all_questions, get_categories

# Initialize colorama for cross-platform colors
init(autoreset=True)

# ============================================
# CONFIGURATION
# ============================================

DATA_FOLDER = "data"
ANSWERS_FILE = f"{DATA_FOLDER}/assessment_answers.json"
COMPANY_NAME = "Naviotech Solutions"

# ============================================
# SETUP - Create data folder if doesn't exist
# ============================================

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

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

def print_welcome():
    """Print welcome message"""
    print_header("Welcome to SecureScore!")
    print(Fore.WHITE + "Welcome to SecureScore!")
    print()
    print(Fore.WHITE + "This tool will assess your small business cybersecurity posture")
    print(Fore.WHITE + "by asking 30 questions across 3 categories:")
    print()
    print(Fore.CYAN + "  📡 Network Security (10 questions)")
    print(Fore.CYAN + "  👥 Human Factors (12 questions)")
    print(Fore.CYAN + "  💾 Data Protection (8 questions)")
    print()
    print(Fore.WHITE + "It should take approximately 10-15 minutes.")
    print()
    input(Fore.YELLOW + "Press Enter to continue...")

def select_mode():
    """Ask user to select Quick or Detailed mode"""
    print_header("Select Assessment Mode")
    print()
    print(Fore.WHITE + "Choose your assessment mode:")
    print()
    print(Fore.CYAN + "  1) QUICK MODE")
    print(Fore.WHITE + "     - Faster questions with minimal explanation")
    print(Fore.WHITE + "     - ~5-10 minutes")
    print()
    print(Fore.CYAN + "  2) DETAILED MODE")
    print(Fore.WHITE + "     - Full explanations for each question")
    print(Fore.WHITE + "     - Better for learning")
    print(Fore.WHITE + "     - ~10-15 minutes")
    print()
    
    while True:
        choice = input(Fore.YELLOW + "Your choice (1/2): ").strip()
        if choice == "1":
            return "quick"
        elif choice == "2":
            return "detailed"
        else:
            print(Fore.RED + "❌ Invalid input! Please enter 1 or 2.")

def get_business_name():
    """Get business name from user"""
    print_header("Business Information")
    business_name = input(Fore.YELLOW + "What is your business name? (or press Enter for 'Test Business'): ").strip()
    
    if not business_name:
        business_name = "Test Business"
    
    return business_name

def print_progress_bar(current, total):
    """Print a visual progress bar"""
    percentage = (current / total) * 100
    filled = int(20 * current // total)
    bar = '█' * filled + '░' * (20 - filled)
    print(Fore.CYAN + f"  [{bar}] {percentage:.0f}% ({current}/{total})")

def ask_question(question_id, question_data, question_number, total_questions, mode):
    """
    Ask a single question and get user's answer
    
    Args:
        question_id: ID like "Q1", "Q2"
        question_data: Dictionary with question properties
        question_number: Current question number (1-30)
        total_questions: Total questions (30)
        mode: "quick" or "detailed"
    
    Returns:
        User's answer: "yes", "partial", or "no"
    """
    
    print_header()
    
    # Show progress
    print(Fore.YELLOW + f"Progress: Question {question_number}/{total_questions}")
    print_progress_bar(question_number - 1, total_questions)
    print()
    
    print(Fore.MAGENTA + f"Category: {question_data['category']}")
    print()
    
    # Show question
    print(Fore.WHITE + f"📝 {question_id}: {question_data['text']}")
    print()
    
    # Show explanation in detailed mode
    if mode == "detailed":
        print(Fore.CYAN + "Why this matters:")
        if "2FA" in question_data['text'] or "2FA" in question_data['text']:
            print(Fore.CYAN + "  This is a CRITICAL security feature that stops most hacks")
        elif "backup" in question_data['text'].lower():
            print(Fore.CYAN + "  A critical feature for disaster recovery and ransomware protection")
        elif "training" in question_data['text'].lower():
            print(Fore.CYAN + "  Trained employees are your best defense against attacks")
        else:
            print(Fore.CYAN + "  This helps assess your overall security posture")
        print()
    
    # Show answer options
    print(Fore.YELLOW + "Answer options:")
    print(Fore.GREEN + "  1) Yes (or Excellent)")
    print(Fore.YELLOW + "  2) Partial (or Sometimes)")
    print(Fore.RED + "  3) No (or Not Implemented)")
    print()
    
    # Get user input
    while True:
        answer = input(Fore.YELLOW + "Your answer (1/2/3): ").strip()
        
        if answer == "1":
            print(Fore.GREEN + "  ✅ Recorded: Yes")
            return "yes"
        elif answer == "2":
            print(Fore.YELLOW + "  🟡 Recorded: Partial")
            return "partial"
        elif answer == "3":
            print(Fore.RED + "  ❌ Recorded: No")
            return "no"
        else:
            print(Fore.RED + "❌ Invalid input! Please enter 1, 2, or 3.")

def calculate_category_score(answers, category):
    """
    Calculate risk score for a specific category
    
    Args:
        answers: Dictionary with all answers
        category: Category name ("Network Security", "Human Factors", "Data Protection")
    
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
    total_weight = 0
    
    for question_id, question_data in category_questions.items():
        if question_id in answers:
            answer = answers[question_id]["answer"]
            score = question_data["scores"][answer]
            weight = question_data["weight"]
            
            total_weighted_score += (score * weight)
            total_weight += weight
    
    if total_weight == 0:
        return 0
    
    # Normalize to 0-100
    category_score = (total_weighted_score / total_weight) / 100 * 100
    return round(category_score, 1)

def print_category_score(category, score):
    """
    Print category score with color coding
    
    Args:
        category: Category name
        score: Risk score (0-100)
    """
    
    print_header(f"{category} Score")
    print()
    
    # Color code based on risk level
    if score < 30:
        color = Fore.GREEN
        status = "✅ LOW RISK"
    elif score < 60:
        color = Fore.YELLOW
        status = "🟡 MEDIUM RISK"
    else:
        color = Fore.RED
        status = "❌ HIGH RISK"
    
    print(color + f"Risk Score: {score}/100")
    print(color + f"Status: {status}")
    print()
    
    # Print bar
    filled = int(20 * score / 100)
    bar = '█' * filled + '░' * (20 - filled)
    print(color + f"[{bar}]")
    print()

def conduct_assessment(business_name, mode):
    """
    Conduct the full assessment by asking all 30 questions
    
    Args:
        business_name: Name of the business being assessed
        mode: "quick" or "detailed"
    
    Returns:
        Dictionary with all answers
    """
    
    questions_db = get_all_questions()
    answers = {
        "business_name": business_name,
        "mode": mode,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "answers": {}
    }
    
    total_questions = len(questions_db)
    current_category = None
    category_answers = {}
    
    for question_number, (question_id, question_data) in enumerate(questions_db.items(), 1):
        category = question_data['category']
        
        # If category changed, show previous category score
        if current_category and current_category != category:
            print_category_score(current_category, 
                               calculate_category_score(category_answers, current_category))
            input(Fore.YELLOW + "Press Enter to continue to next category...")
            category_answers = {}
        
        current_category = category
        
        # Ask question
        answer = ask_question(question_id, question_data, question_number, total_questions, mode)
        
        # Store answer
        answers["answers"][question_id] = {
            "text": question_data["text"],
            "category": question_data["category"],
            "answer": answer
        }
        
        category_answers[question_id] = {
            "answer": answer,
            "weight": question_data["weight"],
            "scores": question_data["scores"]
        }
    
    # Show final category score
    if current_category and category_answers:
        print_category_score(current_category, 
                           calculate_category_score(category_answers, current_category))
    
    return answers

def save_answers(answers):
    """
    Save answers to a JSON file
    
    Args:
        answers: Dictionary with all answers
    """
    
    with open(ANSWERS_FILE, 'w') as f:
        json.dump(answers, f, indent=2)
    
    print_header("Assessment Saved")
    print(Fore.GREEN + "✅ Answers saved successfully!")
    print(Fore.WHITE + f"📁 Saved to: {ANSWERS_FILE}")
    print()

def load_previous_answers():
    """
    Check if previous answers exist
    
    Returns:
        Previous answers if exist, None otherwise
    """
    
    if os.path.exists(ANSWERS_FILE):
        with open(ANSWERS_FILE, 'r') as f:
            return json.load(f)
    
    return None

def ask_resume_assessment():
    """Ask user if they want to resume previous assessment"""
    print_header("Previous Assessment Found")
    print()
    
    previous_answers = load_previous_answers()
    print(Fore.CYAN + "📋 Previous assessment found!")
    print()
    print(Fore.WHITE + f"Business: {previous_answers['business_name']}")
    print(Fore.WHITE + f"Mode: {previous_answers['mode'].upper()}")
    print(Fore.WHITE + f"Date: {previous_answers['timestamp']}")
    print()
    
    choice = input(Fore.YELLOW + "Do you want to:\n  1) Start a new assessment\n  2) View previous results\n\nYour choice (1/2): ").strip()
    
    if choice == "1":
        return "new"
    elif choice == "2":
        return "view"
    else:
        return ask_resume_assessment()

def show_summary(answers):
    """
    Show a summary of answers before saving
    
    Args:
        answers: Dictionary with all answers
    """
    
    print_header("Assessment Summary")
    print()
    print(Fore.CYAN + f"Business: {answers['business_name']}")
    print(Fore.CYAN + f"Mode: {answers['mode'].upper()}")
    print(Fore.CYAN + f"Total Questions Answered: {len(answers['answers'])}")
    print()
    
    # Count by category
    categories_list = get_categories()
    for category in categories_list:
        count = sum(1 for ans in answers['answers'].values() if ans['category'] == category)
        print(Fore.WHITE + f"  {category}: {count} questions")
    
    print()
    
    # Show answer distribution
    yes_count = sum(1 for ans in answers['answers'].values() if ans['answer'] == 'yes')
    partial_count = sum(1 for ans in answers['answers'].values() if ans['answer'] == 'partial')
    no_count = sum(1 for ans in answers['answers'].values() if ans['answer'] == 'no')
    
    print(Fore.YELLOW + "Answer Distribution:")
    print(Fore.GREEN + f"  ✅ Yes: {yes_count}")
    print(Fore.YELLOW + f"  🟡 Partial: {partial_count}")
    print(Fore.RED + f"  ❌ No: {no_count}")
    print()

# ============================================
# MAIN PROGRAM
# ============================================

def main():
    """Main program flow"""
    
    # Check if previous answers exist
    if os.path.exists(ANSWERS_FILE):
        choice = ask_resume_assessment()
        
        if choice == "view":
            print_header("Previous Results")
            print(Fore.CYAN + "✅ To view detailed results, run: python scoring.py")
            print()
            input(Fore.YELLOW + "Press Enter to exit...")
            return
    
    # Show welcome
    print_welcome()
    
    # Select mode
    mode = select_mode()
    
    # Get business name
    business_name = get_business_name()
    
    # Conduct assessment
    answers = conduct_assessment(business_name, mode)
    
    # Show summary
    show_summary(answers)
    
    # Save answers
    confirm = input(Fore.YELLOW + "Save this assessment? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        save_answers(answers)
        print()
        print(Fore.GREEN + "🎉 Assessment complete!")
        print(Fore.CYAN + "Next: Run 'python scoring.py' to analyze your results!")
    else:
        print_header()
        print(Fore.RED + "❌ Assessment not saved.")

# ============================================
# RUN PROGRAM
# ============================================

if __name__ == "__main__":
    main()