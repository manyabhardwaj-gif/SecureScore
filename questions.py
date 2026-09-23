# ============================================
# QUESTIONS STORAGE - SecureScore
# ============================================
# This file stores ALL 30 questions with their properties
# ============================================

questions_database = {
    # ================== NETWORK SECURITY (10 Questions) ==================
    
    "Q1": {
        "text": "Do passwords have special characters (like @, #, $)?",
        "category": "Network Security",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q2": {
        "text": "Do they use two-factor authentication (2FA) - like password + code from phone?",
        "category": "Network Security",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 40,
            "no": 100
        }
    },
    
    "Q3": {
        "text": "Is their WiFi password protected and not given to everyone?",
        "category": "Network Security",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q4": {
        "text": "Do they clear browsing history and cache regularly?",
        "category": "Network Security",
        "weight": 0.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 20,
            "partial": 50,
            "no": 80
        }
    },
    
    "Q5": {
        "text": "Can they remotely block a stolen/lost laptop or device?",
        "category": "Network Security",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q6": {
        "text": "Do they have backup copies of important data stored separately?",
        "category": "Network Security",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q7": {
        "text": "Do they install security updates when available?",
        "category": "Network Security",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q8": {
        "text": "Do they keep different networks separate? (e.g., guest WiFi separate from office WiFi)",
        "category": "Network Security",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 20,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q9": {
        "text": "Do they have a firewall to protect their network?",
        "category": "Network Security",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q10": {
        "text": "Do they check for suspicious login attempts from unknown places?",
        "category": "Network Security",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    # ================== HUMAN FACTORS (12 Questions) ==================
    
    "Q11": {
        "text": "Do they change passwords every few months or use the same one forever?",
        "category": "Human Factors",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q12": {
        "text": "Can employees recognize fake phishing emails and suspicious calls?",
        "category": "Human Factors",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 40,
            "no": 100
        }
    },
    
    "Q13": {
        "text": "Do they save passwords in browsers or write them down unsafely?",
        "category": "Human Factors",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q14": {
        "text": "Have employees received security training from their company?",
        "category": "Human Factors",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q15": {
        "text": "Do employees know who to contact if they suspect a security problem?",
        "category": "Human Factors",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q16": {
        "text": "Do they have rules about passwords (minimum length, complexity)?",
        "category": "Human Factors",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q17": {
        "text": "Do they use fingerprint or face recognition for login?",
        "category": "Human Factors",
        "weight": 0.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 20,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q18": {
        "text": "Do they remove access when an employee leaves the company?",
        "category": "Human Factors",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q19": {
        "text": "Do they allow employees to use personal phones/laptops for work? (Is this a risk for them?)",
        "category": "Human Factors",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 20,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q20": {
        "text": "Do they have a plan for what to do if they get hacked?",
        "category": "Human Factors",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q21": {
        "text": "Do they check if vendors/contractors they work with are secure?",
        "category": "Human Factors",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 20,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q22": {
        "text": "Do they regularly check their own security? (Security checkups)",
        "category": "Human Factors",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    # ================== DATA PROTECTION (8 Questions) ==================
    
    "Q23": {
        "text": "Is sensitive data encrypted more than once for extra safety?",
        "category": "Data Protection",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q24": {
        "text": "Can only approved employees access the important data?",
        "category": "Data Protection",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q25": {
        "text": "Do they check online if their company data was stolen in hacks?",
        "category": "Data Protection",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q26": {
        "text": "Do they know which information is most important and needs extra protection?",
        "category": "Data Protection",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q27": {
        "text": "Do they backup important data to an external drive or cloud storage?",
        "category": "Data Protection",
        "weight": 2.0,
        "type": "yes_no_partial",
        "scores": {
            "yes": 10,
            "partial": 50,
            "no": 100
        }
    },
    
    "Q28": {
        "text": "Do they keep records of who accessed what data and when?",
        "category": "Data Protection",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q29": {
        "text": "Do they have tools to stop data from accidentally being sent outside?",
        "category": "Data Protection",
        "weight": 0.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 20,
            "partial": 60,
            "no": 100
        }
    },
    
    "Q30": {
        "text": "Do they safely destroy old computers/devices before throwing them away?",
        "category": "Data Protection",
        "weight": 1.5,
        "type": "yes_no_partial",
        "scores": {
            "yes": 15,
            "partial": 60,
            "no": 100
        }
    },
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_all_questions():
    """Returns ALL questions"""
    return questions_database

def get_questions_by_category(category):
    """Returns questions for a specific category"""
    return {k: v for k, v in questions_database.items() if v["category"] == category}

def get_question_text(question_id):
    """Returns just the text of a specific question"""
    return questions_database[question_id]["text"]

def get_question_weight(question_id):
    """Returns the weight of a specific question"""
    return questions_database[question_id]["weight"]

def get_categories():
    """Returns all unique categories"""
    categories = set()
    for q in questions_database.values():
        categories.add(q["category"])
    return sorted(list(categories))

# ============================================
# TEST (to see if it works)
# ============================================

if __name__ == "__main__":
    print("✅ Questions loaded successfully!\n")
    print(f"Total questions: {len(questions_database)}\n")
    
    # Show categories
    print("Categories found:")
    for cat in get_categories():
        count = len(get_questions_by_category(cat))
        print(f"  - {cat}: {count} questions")
    
    # Show first question as example
    print("\n📝 Example Question (Q1):")
    q1 = questions_database["Q1"]
    print(f"  Text: {q1['text']}")
    print(f"  Category: {q1['category']}")
    print(f"  Weight: {q1['weight']}")
    print(f"  Scores: {q1['scores']}")