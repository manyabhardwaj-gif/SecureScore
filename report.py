# ============================================
# HTML REPORT GENERATOR - SecureScore
# ============================================
# This file generates a beautiful HTML report
# ============================================

import json
import os
from datetime import datetime
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# ============================================
# CONFIGURATION
# ============================================

DATA_FOLDER = "data"
SCORES_FILE = f"{DATA_FOLDER}/assessment_scores.json"
REPORTS_FOLDER = "reports"
COMPANY_NAME = "Naviotech Solutions"

# ============================================
# SETUP - Create reports folder if doesn't exist
# ============================================

if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

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

def load_scores():
    """Load previously saved scores from JSON file"""
    
    if not os.path.exists(SCORES_FILE):
        print_header()
        print(Fore.RED + "❌ No assessment scores found!")
        print(Fore.WHITE + "Please run 'python main.py' then 'python scoring.py' first.")
        input(Fore.YELLOW + "Press Enter to exit...")
        return None
    
    with open(SCORES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html_report(scores_data):
    """
    Generate beautiful HTML report from scores
    
    Args:
        scores_data: Dictionary with all scores and recommendations
    
    Returns:
        HTML string
    """
    
    business_name = scores_data["business_name"]
    overall_score = scores_data["scores"]["overall"]
    category_scores = scores_data["scores"]["categories"]
    recommendations = scores_data["recommendations"]
    
    # Determine colors
    def get_color_code(score):
        if score < 20:
            return "#2ecc71"  # Green
        elif score < 50:
            return "#f39c12"  # Orange
        else:
            return "#e74c3c"  # Red
    
    def get_risk_text(score):
        if score < 20:
            return "LOW RISK"
        elif score < 50:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"
    
    # Create progress bar HTML
    def create_progress_bar(score):
        percentage = min(100, max(0, score))
        return f'<div style="width: 100%; background-color: #ecf0f1; border-radius: 5px; height: 30px; overflow: hidden;"><div style="width: {percentage}%; background-color: {get_color_code(score)}; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{score}%</div></div>'
    
    # Separate recommendations by severity
    critical_recs = [r for r in recommendations if "CRITICAL" in r]
    improve_recs = [r for r in recommendations if "IMPROVE" in r]
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureScore Report - {business_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .business-info {{
            background: #f8f9fa;
            padding: 20px 30px;
            border-bottom: 2px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .info-item {{
            flex: 1;
            min-width: 200px;
        }}
        
        .info-label {{
            font-weight: bold;
            color: #667eea;
            font-size: 0.9em;
        }}
        
        .info-value {{
            font-size: 1.1em;
            color: #333;
            margin-top: 5px;
        }}
        
        .content {{
            padding: 40px 30px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .overall-score {{
            background: linear-gradient(135deg, {get_color_code(overall_score)}40, {get_color_code(overall_score)}20);
            border-left: 5px solid {get_color_code(overall_score)};
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .score-big {{
            font-size: 3.5em;
            font-weight: bold;
            color: {get_color_code(overall_score)};
            margin: 10px 0;
        }}
        
        .score-label {{
            font-size: 1.2em;
            color: #666;
        }}
        
        .risk-status {{
            font-size: 1.5em;
            font-weight: bold;
            color: {get_color_code(overall_score)};
            margin-top: 10px;
        }}
        
        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .category-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 25px;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .category-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .category-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .category-score {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 15px 0;
        }}
        
        .recommendations-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
        }}
        
        .rec-category {{
            margin-bottom: 25px;
        }}
        
        .rec-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        .rec-critical {{
            color: #e74c3c;
        }}
        
        .rec-improve {{
            color: #f39c12;
        }}
        
        .rec-list {{
            list-style: none;
        }}
        
        .rec-item {{
            padding: 12px;
            margin-bottom: 10px;
            background: white;
            border-left: 4px solid;
            border-radius: 5px;
            line-height: 1.6;
        }}
        
        .rec-item.critical {{
            border-left-color: #e74c3c;
            background: #fdedec;
        }}
        
        .rec-item.improve {{
            border-left-color: #f39c12;
            background: #fef5e7;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            border-top: 2px solid #e9ecef;
            font-size: 0.95em;
        }}
        
        .footer-logo {{
            color: #667eea;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .score-big {{
                font-size: 2.5em;
            }}
            
            .business-info {{
                flex-direction: column;
            }}
            
            .categories-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>Secure Risk Assessment Report</h1>
            <p>{COMPANY_NAME}</p>
        </div>
        
        <!-- BUSINESS INFO -->
        <div class="business-info">
            <div class="info-item">
                <div class="info-label">Business Name</div>
                <div class="info-value">{business_name}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Assessment Date</div>
                <div class="info-value">{scores_data['assessment_date']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Report Generated</div>
                <div class="info-value">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
            </div>
        </div>
        
        <!-- MAIN CONTENT -->
        <div class="content">
            <!-- OVERALL SCORE SECTION -->
            <div class="section">
                <div class="section-title">Overall Risk Assessment</div>
                <div class="overall-score">
                    <div class="score-label">Cybersecurity Risk Score</div>
                    <div class="score-big">{overall_score}</div>
                    <div class="score-label">out of 100</div>
                    <div class="risk-status">{get_risk_text(overall_score)}</div>
                </div>
            </div>
            
            <!-- CATEGORY BREAKDOWN -->
            <div class="section">
                <div class="section-title">Category Breakdown</div>
                <div class="categories-grid">
"""
    
    # Add category cards
    for category, score in category_scores.items():
        color = get_color_code(score)
        html += f"""
                    <div class="category-card">
                        <div class="category-name">{category}</div>
                        <div class="category-score" style="color: {color};">{score}</div>
                        <div style="font-size: 0.9em; color: #666; margin-bottom: 15px;">out of 100</div>
                        {create_progress_bar(score)}
                        <div style="text-align: center; margin-top: 10px; font-weight: bold; color: {color};">
                            {get_risk_text(score)}
                        </div>
                    </div>
"""
    
    html += """
                </div>
            </div>
            
            <!-- RECOMMENDATIONS SECTION -->
            <div class="section">
                <div class="section-title">Action Recommendations</div>
                <div class="recommendations-section">
"""
    
    # Critical recommendations
    if critical_recs:
        html += """
                    <div class="rec-category">
                        <div class="rec-title rec-critical">CRITICAL (DO FIRST)</div>
                        <ul class="rec-list">
"""
        for rec in critical_recs:
            # Remove the emoji prefix for cleaner display
            rec_text = rec.replace("CRITICAL: ", "").strip()
            html += f'                            <li class="rec-item critical">{rec_text}</li>\n'
        html += """
                        </ul>
                    </div>
"""
    
    # Improvement recommendations
    if improve_recs:
        html += """
                    <div class="rec-category">
                        <div class="rec-title rec-improve">IMPROVEMENTS NEEDED</div>
                        <ul class="rec-list">
"""
        for rec in improve_recs:
            # Remove the emoji prefix for cleaner display
            rec_text = rec.replace("IMPROVE: ", "").strip()
            html += f'                            <li class="rec-item improve">{rec_text}</li>\n'
        html += """
                        </ul>
                    </div>
"""
    
    html += """
                </div>
            </div>
            
            <!-- INTERPRETATION SECTION -->
            <div class="section">
                <div class="section-title">What Does This Mean?</div>
"""
    
    # Add interpretation based on score
    if overall_score < 20:
        html += """
                <div style="background: #d5f4e6; border-left: 5px solid #2ecc71; padding: 20px; border-radius: 5px;">
                    <p style="color: #27ae60; font-size: 1.1em;">
                        <strong>Excellent Security Posture</strong><br><br>
                        Your business demonstrates strong cybersecurity practices across all categories. 
                        Continue regular security audits and stay updated with the latest security practices.
                        Maintain this level of security and consider becoming a model for industry standards.
                    </p>
                </div>
"""
    elif overall_score < 50:
        html += """
                <div style="background: #fef5e7; border-left: 5px solid #f39c12; padding: 20px; border-radius: 5px;">
                    <p style="color: #d68910; font-size: 1.1em;">
                        <strong>Good Foundation, Room for Improvement</strong><br><br>
                        Your business has implemented many security measures, but there are areas that need attention.
                        Prioritize the improvements listed above to strengthen your security posture.
                        Most issues can be resolved with proper implementation and employee training.
                    </p>
                </div>
"""
    else:
        html += """
                <div style="background: #fdedec; border-left: 5px solid #e74c3c; padding: 20px; border-radius: 5px;">
                    <p style="color: #c0392b; font-size: 1.1em;">
                        <strong>Urgent Action Required</strong><br><br>
                        Your business faces multiple significant cybersecurity vulnerabilities.
                        Immediate action is required to implement the critical recommendations above.
                        Consider hiring a cybersecurity consultant to develop a comprehensive security strategy.
                        The longer these vulnerabilities persist, the higher the risk of a successful cyber attack.
                    </p>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <!-- FOOTER -->
        <div class="footer">
            <div class="footer-logo">Naviotech Solutions - SecureScore</div>
            <p>Professional Cybersecurity Risk Assessment Tool</p>
            <p style="font-size: 0.85em; margin-top: 10px; opacity: 0.8;">
                This report is confidential and intended for authorized personnel only.
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def save_report(html_content, scores_data):
    """
    Save HTML report to file
    
    Args:
        html_content: HTML string to save
        scores_data: Scores dictionary (for filename)
    """
    
    business_name = scores_data["business_name"].replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{REPORTS_FOLDER}/SecureScore_Report_{business_name}_{timestamp}.html"
    
    # FIX: Added encoding='utf-8' to support special characters and emojis
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

# ============================================
# MAIN PROGRAM
# ============================================

def main():
    """Main report generation program"""
    
    print_header("Generating HTML Report...")
    
    # Load scores
    scores_data = load_scores()
    if not scores_data:
        return
    
    print(Fore.WHITE + "Generating HTML report...\n")
    
    # Generate HTML
    html_content = generate_html_report(scores_data)
    
    # Save report
    filename = save_report(html_content, scores_data)
    
    print_header("Report Generated!")
    print()
    print(Fore.GREEN + "Check Report generated successfully!")
    print()
    print(Fore.WHITE + f"File saved to: {filename}")
    print()
    print(Fore.CYAN + "Report Features:")
    print(Fore.WHITE + "  - Overall risk score visualization")
    print(Fore.WHITE + "  - Category breakdown with progress bars")
    print(Fore.WHITE + "  - Specific recommendations organized by priority")
    print(Fore.WHITE + "  - Professional layout with company branding")
    print(Fore.WHITE + "  - Responsive design (works on mobile too)")
    print()
    print(Fore.YELLOW + "Next Steps:")
    print(Fore.WHITE + "  1. Open the HTML file in your browser")
    print(Fore.WHITE + "  2. Print or save as PDF for sharing")
    print(Fore.WHITE + "  3. Share with stakeholders for action items")
    print()
    print(Fore.GREEN + "Your SecureScore assessment is complete!")
    print()
    
    input(Fore.YELLOW + "Press Enter to exit...")

# ============================================
# RUN PROGRAM
# ============================================

if __name__ == "__main__":
    main()