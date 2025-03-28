from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import requests
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwQozbzTlkkPkrP-9I_Uu9hLTBdeDejmiEzL108wMMPw6oSTlWV_dsyO0ByEHnikt6j1w/exec"

# Segment titles (unchanged)
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

# Index route: collects initial user information and stores it as segment0.
@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    if request.method == 'POST':
        try:
            # Save index form answers as segment0
            session['segment0'] = request.form.to_dict()
            return redirect(url_for('segment', segment_id=1))
        except Exception as e:
            logger.error(f"Error in index: {str(e)}")
            return redirect(url_for('index'))
    return render_template('index.html')

# Segment route: collects answers per segment.
@app.route('/segment/<int:segment_id>', methods=['GET', 'POST'])
def segment(segment_id):
    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            session[f'segment{segment_id}'] = form_data
            
            if segment_id == 8:
                # Initialize ordered data dictionary
                ordered_data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Email Address": session.get('segment0', {}).get('email', ''),
                    "Name of Petitioner/Probation/Parole:": session.get('segment0', {}).get('petitioner_name', ''),
                    "Length of Sentence:": session.get('segment0', {}).get('sentence_length', ''),
                    "Name & Position of Inv/Supvg Officer:": session.get('segment0', {}).get('officer_name', ''),
                    "Chief Probation Officer/Officer-in-Charge:": session.get('segment0', {}).get('chief_officer', '')
                }

                # Criminal History (Segment 1)
                seg1 = session.get('segment1', {})
                ordered_data.update({
                    "Age at First Misconduct": seg1.get('seg1_q1', ''),
                    "Number of Previous Misconduct(s)": seg1.get('seg1_q2', ''),
                    "Extent of Involvement in Organized Crimes": seg1.get('seg1_q3', ''),
                    "Derogatory Record": seg1.get('seg1_q4', ''),
                    "Type of Offender": seg1.get('seg1_q5', ''),
                    "History of Violence": seg1.get('seg1_q6', '')
                })

                # Pro-Criminal Companions (Segment 2)
                seg2 = session.get('segment2', {})
                ordered_data.update({
                    "Type of Companions": seg2.get('seg2_q1', ''),
                    "Type of Activities with Companions": seg2.get('seg2_q2', ''),
                    "Friends' Support": seg2.get('seg2_q3', ''),
                })

                # Pro-Criminal Attitudes (Segment 3)
                seg3 = session.get('segment3', {})
                ordered_data.update({
                    "Is it okay to break the rules/laws as long as I can help my family.": seg3.get('seg3_q1', ''),
                    "Is it okay to break the rules/laws because I don't know it.": seg3.get('seg3_q2', ''),
                    "Is it okay to break the rules/laws when nobody sees me or I don't get caught.": seg3.get('seg3_q3', ''),
                    "Is it okay to commit a crime if you are a victim of social injustice/inequality.": seg3.get('seg3_q4', ''),
                    "Is it okay to commit a crime when you are in a desperate situation/crisis.": seg3.get('seg3_q5', '')
                })

                # Anti-Social Personality (Segment 4)
                seg4 = session.get('segment4', {})
                ordered_data.update({
                    "I find it hard to follow rules.": seg4.get('seg4_q1', ''),
                    "I lie and cheat to get what I want.": seg4.get('seg4_q2', ''),
                    "I act without thinking of the consequences of my actions.": seg4.get('seg4_q3', ''),
                    "I easily get irritated or angry.": seg4.get('seg4_q4', ''),
                    "I don't care who gets hurt as long as I get what I want.": seg4.get('seg4_q5', ''),
                    "I find it hard to follow through with responsibilities/assigned tasks.": seg4.get('seg4_q6', '')
                })

                # Education and Employment (Segment 5)
                seg5 = session.get('segment5', {})
                ordered_data.update({
                    "Educational Attainment": seg5.get('seg5_q1', ''),
                    "Educational Attachment": seg5.get('seg5_q2', ''),
                    "Overall Conduct in School": seg5.get('seg5_q3', ''),
                    "Employment Status at the Time of Arrest": seg5.get('seg5_q4', ''),
                    "Employable Skills": seg5.get('seg5_q5', ''),
                    "Employment History": seg5.get('seg5_q6', '')
                })

                # Family and Marital (Segment 6)
                seg6 = session.get('segment6', {})
                ordered_data.update({
                    "Quality of Family/Marital Relationships": seg6.get('seg6_q1', ''),
                    "Parental Guidance and Supervision": seg6.get('seg6_q2', ''),
                    "Family Acceptability in the Community": seg6.get('seg6_q3', ''),
                    "Spirituality/Religiosity": seg6.get('seg6_q4', '')
                })

                # Substance Abuse (Segment 7)
                seg7 = session.get('segment7', {})
                ordered_data.update({
                    "History of Drug Abuse": seg7.get('seg7_q1', ''),
                    "Frequency of Drug Use": seg7.get('seg7_q2', ''),
                    "History of Alcohol Abuse": seg7.get('seg7_q3', ''),
                    "Frequency of Alcohol Use": seg7.get('seg7_q4', ''),
                    "Desire/Urge for substance Use": seg7.get('seg7_q5', ''),
                    "Cut down on Substance Use (Reverse Coded)": seg7.get('seg7_q6', ''),
                    "Family History of Substance Use": seg7.get('seg7_q7', '')
                })

                # Mental Health (Segment 8)
                seg8 = session.get('segment8', {})
                ordered_data.update({
                    "I can perform my daily activities with minimal support from others": seg8.get('seg8_q1', ''),
                    "I can easily make good decisions on my own": seg8.get('seg8_q2', ''),
                    "I have experienced sadness for 14 days over the last 6 months": seg8.get('seg8_q3', ''),
                    "I have received consultation/treatment/counseling for a psychological/psychiatric problem": seg8.get('seg8_q4', ''),
                    "I sometimes hear or see things not normally seen or heard by others": seg8.get('seg8_q5', '')
                })

                try:
                    response = requests.post(
                        GOOGLE_SCRIPT_URL,
                        json=ordered_data,
                        headers={'Content-Type': 'application/json'},
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        session['assessment_results'] = ordered_data
                        return redirect(url_for('results'))
                    else:
                        logger.error(f"Google Sheets Error: Status {response.status_code}")
                        flash("Failed to save responses. Please try again.")
                        return redirect(url_for('segment', segment_id=8))
                        
                except Exception as e:
                    logger.error(f"Google Sheets Error: {str(e)}")
                    flash("Connection error. Please try again.")
                    return redirect(url_for('segment', segment_id=8))

            return redirect(url_for('segment', segment_id=segment_id + 1))
            
        except Exception as e:
            logger.error(f"Segment Error: {str(e)}")
            flash("An error occurred. Please try again.")
            return redirect(url_for('segment', segment_id=segment_id))

    return render_template(
        "segment.html",
        segment_id=segment_id,
        title=segment_titles.get(segment_id, "Unknown Segment")
    )

# Results page (optional)
@app.route("/results")
def results():
    complete_data = session.get('assessment_results', {})
    total_score = complete_data.get('total_score', 0)  # Default to 0 if not set
    
    # Get risk assessment based on total score
    risk_assessment = assess_risk_level(total_score)
    
    return render_template(
        "results.html", 
        data=complete_data, 
        total_score=total_score,
        risk_assessment=risk_assessment
    )

if __name__ == "__main__":
    app.run(debug=True)
