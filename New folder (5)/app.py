from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Segment titles
segment_titles = {
    1: "CRIMINAL HISTORY",
    2: "PRO-CRIMINAL COMPANIONS",
    3: "PRO-CRIMINAL ATTITUDES & COGNITIONS",
    4: "ANTI-SOCIAL PERSONALITY PATTERNS",
    5: "EDUCATION AND EMPLOYMENT",
    6: "FAMILY AND MARITAL STATUS",
    7: "SUBSTANCE ABUSE",
    8: "MENTAL HEALTH"
}

# Questions for each segment
segments = {
    1: [
        {
            "question": "Age at First Misconduct",
            "options": [
                {"text": "26 years old and above", "score": 0},
                {"text": "18-25 years old", "score": 1},
                {"text": "17 years old and below", "score": 2}
            ]
        },
        {
            "question": "Number of Previous Misconduct(s)",
            "options": [
                {"text": "No Misconduct", "score": 0},
                {"text": "1 Misconduct", "score": 1},
                {"text": "2 or more misconducts", "score": 2}
            ]
        },
        {
            "question": "Extent of Involvement in Organized Crimes",
            "options": [
                {"text": "Not a member", "score": 0},
                {"text": "Member but Inactive", "score": 1},
                {"text": "Active membership", "score": 2}
            ]
        },
        {
            "question": "Derogatory Record",
            "options": [
                {"text": "No Record", "score": 0},
                {"text": "With 1 Record", "score": 1},
                {"text": "With 2 or More Records", "score": 2}
            ]
        },
        {
            "question": "Type of Offender",
            "options": [
                {"text": "Situational/Circumstantial", "score": 0},
                {"text": "\"Paminsan-minsan\"", "score": 1},
                {"text": "Career Offender", "score": 2}
            ]
        },
        {
            "question": "History of Violence",
            "options": [
                {"text": "No History of violence", "score": 0},
                {"text": "1 Incident of violence", "score": 1},
                {"text": "2 or more history of violence", "score": 2}
            ]
        }
    ],
    2: [
        {
            "question": "Type of Companions",
            "options": [
                {"text": "Mostly conventional", "score": 0},
                {"text": "Sometimes conventional, Sometimes delinquent", "score": 1},
                {"text": "Mostly deliquent", "score": 2}
            ]
        },
        {
            "question": "Type of Activities with Companions",
            "options": [
                {"text": "Mostly convetional", "score": 0},
                {"text": "Sometimes conventional, Sometimes delinquent", "score": 1},
                {"text": "Mostly delinquent", "score": 2}
            ]
        },
        {
            "question": "Friends' Support",
            "options": [
                {"text": "Mostly supportive friends", "score": 0},
                {"text": "Few supportive friends", "score": 1},
                {"text": "No supportive friends", "score": 2}
            ]
        }
    ],
    3: [
        {
            "question": "Is it okay to break the rules/laws as long as I can help my family.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 2}
            ]
        },
        {
            "question": "Is it okay to break the rules/laws because I don't know it.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 2}
            ]
        },
        {
            "question": "Is it okay to break the rules/laws when nobody sees me or I don't get caught.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 2}
            ]
        },
        {
            "question": "Is it okay to commit a crime if you are a victim of social injustice/inequality.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 2}
            ]
        },
        {
            "question": "Is it okay to commit a crime when you are in a desperate situation/crisis.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 2}
            ]
        }
    ],
    4: [
        {
            "question": "I find it hard to follow rules.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 1}
            ]
        },
        {
            "question": "I lie and cheat to get what I want.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 1}
            ]
        },
        {
            "question": "I act without thinking of the consequences of my actions.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 1}
            ]
        },
        {
            "question": "I easily get irritated or angry.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 1}
            ]
        },
        {
            "question": "I don't care who gets hurt as long as I get what I want.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 1}
            ]
        },
        {
            "question": "I find it hard to follow through with responsibilities/assigned tasks.",
            "options": [
                {"text": "No", "score": 0},
                {"text": "Yes", "score": 1}
            ]
        }
    ],
    5: [
        {
            "question": "Educational Attainment",
            "options": [
                {"text": "Vocational/College level & above", "score": 0},
                {"text": "Grade 7 to 12", "score": 1},
                {"text": "Grade 6 and below", "score": 2}
            ]
        },
        {
            "question": "Educational Attachment",
            "options": [
                {"text": "Interested in school", "score": 0},
                {"text": "Lacks interest in school", "score": 1},
                {"text": "Did not get along well with teachers and other students/No interest in school", "score": 2}
            ]
        },
        {
            "question": "Overall Conduct in School",
            "options": [
                {"text": "Without misdeamenor", "score": 0},
                {"text": "With misdeamenor", "score": 2}
            ]
        },
        {
            "question": "Employment Status at the Time of Arrest",
            "options": [
                {"text": "Employed", "score": 0},
                {"text": "Irregurlarly employed", "score": 1},
                {"text": "Unemployed", "score": 2}
            ]
        },
        {
            "question": "Employable Skills",
            "options": [
                {"text": "With at least one employable skill", "score": 0},
                {"text": "No employable skill but with potential and capacity to acquire one", "score": 1},
                {"text": "No Employable Skill", "score": 2}
            ]
        },
        {
            "question": "Employment History",
            "options": [
                {"text": "Treats job seriously; Finds work rewarding; Good relationship with employer and co-workers", "score": 0},
                {"text": "Inconsistent employment; No employment that lasts 3 months; Minimun attchement to work", "score": 1},
                {"text": "Does not like/love job; Conflict with the employer; No interest in working; No attachments to work; Frequently fired from work", "score": 2}
            ]
        }
    ],
    6: [
        {
            "question": "Quality of Family/Marital Relationships",
            "options": [
                {"text": "With positive influence", "score": 0},
                {"text": "With occasional negative influence", "score": 1},
                {"text": "With regular negative influence", "score": 2}
            ]
        },
        {
            "question": "Parental Guidance and Supervision",
            "options": [
                {"text": "Adequate guidance and supervision", "score": 0},
                {"text": "Minimal guidance and supervision", "score": 1},
                {"text": "Without guidance and supervision; Overbearing/Over Protective", "score": 2}
            ]
        },
        {
            "question": "Family Acceptability in the Community",
            "options": [
                {"text": "Acceptable", "score": 0},
                {"text": "Unacceptable", "score": 1},
                {"text": "Heghly unacceptable", "score": 2}
            ]
        },
        {
            "question": "Spirituality/Religiosity",
            "options": [
                {"text": "Integrated spiritual belief and religous activities", "score": 0},
                {"text": "Disintegrated spiritual belief but with some manifested positive religious belief", "score": 1},
                {"text": "Disintegrated religous belief and negative religous activites", "score": 2}
            ]
        }
    ],
    7: [
        {
            "question": "History of Drug Abuse",
            "options": [
                {"text": "If client abuse drugs (other than those required for medical reasons)", "score": 1},
                {"text": "Never", "score": 0}
            ]
        },
        {
            "question": "Frequency of Drug Use",
            "options": [
                {"text": "No Usage", "score": 0},
                {"text": "At least once a month", "score": 1},
                {"text": "At least once a week", "score": 2},
                {"text": "Almost Daily", "score": 3}
            ]
        },
        {
            "question": "History of Alcohol Abuse",
            "options": [
                {"text": "If client abuse alcoholic beverages", "score": 1},
                {"text": "Never", "score": 0}
            ]
        },
        {
            "question": "Frequency of Alcohol Use",
            "options": [
                {"text": "No Usage", "score": 0},
                {"text": "At least once a month", "score": 1},
                {"text": "At least once a week", "score": 2},
                {"text": "Almost Daily", "score": 3}
            ]
        },
        {
            "question": "Desire/Urge for substance Use",
            "options": [
                {"text": "Never", "score": 0},
                {"text": "Sometimes", "score": 1},
                {"text": "Always", "score": 2},
            ]
        },
        {
            "question": "Cut down on Substance Use (Reverse Coded)",
            "options": [
                {"text": "Always Able to Stop", "score": 0},
                {"text": "Unable to Stop", "score": 1}
            ]
        },
        {
            "question": "Family History of Substance Use",
            "options": [
                {"text": "YES", "score": 1},
                {"text": "NO", "score": 0}
            ]
        }
    ],
    8: [
        {
            "question": "I can perform my daily activities with minimal support from others",
            "options": [
                {"text": "YES", "score": 0},
                {"text": "NO", "score": 1}
            ]
        },
        {
            "question": "I can easily make good decisions on my own",
            "options": [
                {"text": "YES", "score": 0},
                {"text": "NO", "score": 1}
            ]
        },
        {
            "question": "I have experienced sadness for 14 days over the last 6 months",
            "options": [
                {"text": "YES", "score": 1},
                {"text": "NO", "score": 0}
            ]
        },
        {
            "question": "I have received consultation/treatment/counseling for a psychological/psychiatric problem",
            "options": [
                {"text": "YES", "score": 1},
                {"text": "NO", "score": 0}
            ]
        },
        {
            "question": "I sometimes hear or see things not normally seen or heard by others",
            "options": [
                {"text": "YES", "score": 1},
                {"text": "NO", "score": 0}
            ]
        }
    ]
}

# Segment thresholds for program recommendations
segment_thresholds = {
    1: {"threshold": 5, "program": "ICARE Program"},
    2: {"threshold": 4, "program": "Social Integration Program"},
    3: {"threshold": 4, "program": "Family Counseling Program"},
    4: {"threshold": 4, "program": "Educational Support Program"},
    5: {"threshold": 4, "program": "Vocational Training Program"},
    6: {"threshold": 4, "program": "Substance Abuse Treatment Program"},
    7: {"threshold": 4, "program": "Mental Health Support Program"},
    8: {"threshold": 4, "program": "Behavioral Management Program"},
    9: {"threshold": 4, "program": "Risk Reduction Program"}
}

# Mandatory programs
mandatory_programs = [
    "Monthly/periodic report-in-person",
    "Monitoring and Supervision",
    "Therapeutic Community Ladderized Program (TCLP) Mandatory Reinforcing Activities",
    "Restorative Justice Processes",
    "Individual/Group Family/Marital Coaching",
    "Community Work Service/Involvement in community/barangay integration activities",
    "Spiritual/Moral Formation/Reformation activities"
]

# Risk level assessment
def assess_risk_level(total_score):
    if total_score <= 17:
        return {
            "level": "Low Risk (Level 1)",
            "probation_sentenced": "6 months",
            "probation_other": "1 year",
            "supervision": "Once in 2 months"
        }
    elif total_score <= 28:
        return {
            "level": "Medium Risk (Level 2)",
            "probation_sentenced": "6 months",
            "probation_other": "1 year",
            "supervision": "Once a month"
        }
    elif total_score <= 39:
        return {
            "level": "High Risk (Level 3)",
            "probation_sentenced": "1 year",
            "probation_other": "2 years",
            "supervision": "Twice a month"
        }
    else:
        return {
            "level": "Very High Risk (Level 4)",
            "probation_sentenced": "2 years",
            "probation_other": "3 years",
            "supervision": "Twice a month"
        }

@app.route('/')
def index():
    # Initialize session
    session.clear()
    for i in range(1, 10):
        session[f'segment{i}_scores'] = []
    return render_template('index.html')

@app.route('/segment/<int:segment_id>', methods=['GET', 'POST'])
def segment(segment_id):
    if request.method == 'POST':
        # Save scores from previous segment
        prev_segment = segment_id - 1
        if prev_segment > 0:
            scores = []
            for i in range(len(segments[prev_segment])):
                score = int(request.form.get(f'q{i}', 0))
                scores.append(score)
            session[f'segment{prev_segment}_scores'] = scores
            
    # If we've completed all segments, go to results
    if segment_id > 9:
        return redirect(url_for('results'))
    
    # Create enumerated questions for Jinja template
    # Since Jinja doesn't support enumerate() directly
    enumerated_questions = []
    for i, question in enumerate(segments[segment_id]):
        enumerated_questions.append({
            'index': i,
            'question': question
        })
        
    return render_template(
        'segment.html', 
        segment_id=segment_id, 
        title=segment_titles[segment_id],
        enumerated_questions=enumerated_questions,  # Pass enumerated questions
        next_segment=segment_id + 1
    )

@app.route('/results')
def results():
    # Save scores from the last segment
    scores = []
    for i in range(len(segments[9])):
        score = int(request.args.get(f'q{i}', 0))
    if scores:
        session['segment9_scores'] = scores
    
    # Calculate subtotals for each segment
    subtotals = {}
    total_score = 0
    
    for i in range(1, 10):
        segment_scores = session.get(f'segment{i}_scores', [])
        subtotal = sum(segment_scores)
        subtotals[i] = subtotal
        total_score += subtotal
    
    # Determine risk level
    risk_assessment = assess_risk_level(total_score)
    
    # Determine recommended programs based on segment thresholds
    recommended_programs = []
    for segment_id, data in segment_thresholds.items():
        if subtotals.get(segment_id, 0) >= data["threshold"]:
            recommended_programs.append(data["program"])
    
    return render_template(
        'results.html',
        subtotals=subtotals,
        total_score=total_score,
        risk_assessment=risk_assessment,
        recommended_programs=recommended_programs,
        mandatory_programs=mandatory_programs,
        segment_titles=segment_titles,
        segment_thresholds=segment_thresholds  # Add this line
    )

if __name__ == '__main__':
    app.run(debug=True)