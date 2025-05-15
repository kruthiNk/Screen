import streamlit as st
import pdfplumber
import re
from collections import defaultdict

# Configure the app
st.set_page_config(page_title="Resume Screener", layout="wide")
st.title("📄 AI Resume Screening System")
st.write("Upload a resume PDF to evaluate for 9 different job roles")

# Define all domain keywords
AREA_KEY_TERMS = {
    'data_science': ['machine learning', 'deep learning', 'neural network', 'data mining', 
                    'predictive modeling', 'natural language processing', 'computer vision',
                    'supervised learning', 'unsupervised learning', 'reinforcement learning'],
    'statistics': ['statistics', 'regression', 'hypothesis testing', 'anova', 'bayesian',
                  'probability', 'statistical modeling', 'ab testing', 'experimental design'],
    'data_analytics': ['data analysis', 'sql', 'power bi', 'tableau', 'excel', 'etl',
                      'data visualization', 'business intelligence', 'kpi', 'metrics'],
    'programming': ['python', 'java', 'javascript', 'c++', 'r', 'sql', 'git', 'github',
                   'debugging', 'software development', 'api', 'rest'],
    'software': ['software engineering', 'react', 'angular', 'django', 'flask', 'aws',
                'azure', 'docker', 'kubernetes', 'microservices', 'agile', 'scrum'],
    'graphic': ['photoshop', 'illustrator', 'indesign', 'figma', 'adobe xd', 'ui/ux',
               'typography', 'color theory', 'logo design', 'branding'],
    'web': ['html', 'css', 'javascript', 'responsive design', 'wordpress', 'seo',
           'frontend', 'backend', 'full stack', 'web development'],
    'accounting': ['accounting', 'bookkeeping', 'financial statements', 'gaap', 'ifrs',
                  'taxation', 'auditing', 'accounts payable', 'accounts receivable'],
    'management': ['project management', 'team leadership', 'strategic planning', 'budgeting',
                 'performance evaluation', 'operations management', 'supply chain'],
    'sales_marketing': ['sales', 'marketing', 'digital marketing', 'social media', 'seo',
                       'ppc', 'content marketing', 'brand management', 'market research'],
    'content': ['content writing', 'copywriting', 'blogging', 'technical writing', 'seo',
               'social media content', 'editing', 'proofreading', 'creative writing'],
    'graphical_content': ['infographics', 'data visualization', 'presentation design',
                        'video editing', 'motion graphics', 'photography', 'illustration'],
    'finance': ['financial analysis', 'financial modeling', 'valuation', 'investment',
               'portfolio management', 'risk management', 'corporate finance'],
    'health_medical': ['surgery', 'patient care', 'medical diagnosis', 'treatment planning',
                      'clinical skills', 'healthcare', 'medicine', 'anatomy'],
    'personal_skills': ['communication', 'teamwork', 'leadership', 'problem solving',
                       'critical thinking', 'adaptability', 'time management', 'creativity'],
    'languages': ['english', 'malay', 'mandarin', 'tamil', 'spanish', 'french', 'german']
}

# Upload PDF
uploaded_file = st.file_uploader("Choose a resume PDF", type="pdf")

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def count_keywords(text, keywords):
    count = 0
    for keyword in keywords:
        count += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
    return count

def calculate_scores(text):
    scores = {}
    for domain, terms in AREA_KEY_TERMS.items():
        scores[domain] = count_keywords(text, terms)
    scores['total'] = sum(scores.values())
    return scores

def determine_status(scores):
    matches = []
    
    # 1. Junior Data Scientist
    if ((scores['total'] >= 50 and scores['personal_skills'] >= 2 and scores['statistics'] >= 9) or
        (scores['total'] >= 40 and scores['personal_skills'] >= 2 and scores['data_science'] >= 10) or
        (scores['total'] >= 60 and scores['data_analytics'] >= 8)):
        role_score = (scores['data_science'] * 2 + scores['statistics'] * 2 + scores['data_analytics']) / 5
        matches.append(("Junior Data Scientist", role_score, {
            'Data Science': scores['data_science'],
            'Statistics': scores['statistics'],
            'Data Analytics': scores['data_analytics']
        }))
    
    # 2. Data Analyst
    if (scores['total'] >= 30 and scores['statistics'] >= 2 and scores['programming'] >= 3 and 
        scores['personal_skills'] >= 2 and scores['data_analytics'] >= 5):
        role_score = (scores['data_analytics'] * 2 + scores['statistics'] + scores['programming']) / 4
        matches.append(("Data Analyst", role_score, {
            'Data Analytics': scores['data_analytics'],
            'Statistics': scores['statistics'],
            'Programming': scores['programming']
        }))
    
    # 3. Software Engineer
    if scores['total'] >= 20 and scores['software'] >= 10:
        role_score = (scores['software'] * 2 + scores['programming']) / 3
        matches.append(("Software Engineer", role_score, {
            'Software': scores['software'],
            'Programming': scores['programming']
        }))
    
    # 4. Web & Graphic Designer
    if (scores['total'] >= 18 and scores['personal_skills'] >= 2 and 
        scores['graphic'] >= 5 and scores['web'] >= 10):
        role_score = (scores['web'] + scores['graphic']) / 2
        matches.append(("Web & Graphic Designer", role_score, {
            'Web Skills': scores['web'],
            'Graphic Skills': scores['graphic']
        }))
    
    # 5. Account Executive
    if scores['total'] >= 50 and scores['personal_skills'] >= 2 and scores['accounting'] >= 10:
        matches.append(("Account Executive", scores['accounting'], {
            'Accounting': scores['accounting']
        }))
    
    # 6. Sales Representative
    if (scores['total'] >= 20 and scores['management'] >= 2 and 
        scores['personal_skills'] >= 2 and scores['sales_marketing'] >= 10):
        matches.append(("Sales Representative", scores['sales_marketing'], {
            'Sales & Marketing': scores['sales_marketing']
        }))
    
    # 7. Content Creator
    if (scores['total'] >= 25 and scores['personal_skills'] >= 2 and 
        scores['content'] >= 8 and scores['graphical_content'] >= 10):
        role_score = (scores['content'] + scores['graphical_content']) / 2
        matches.append(("Content Creator", role_score, {
            'Content Skills': scores['content'],
            'Graphical Content': scores['graphical_content']
        }))
    
    # 8. Senior Accountant
    if (scores['total'] >= 30 and scores['management'] >= 4 and 
        scores['personal_skills'] >= 2 and scores['finance'] >= 10):
        matches.append(("Senior Accountant", scores['finance'], {
            'Finance': scores['finance']
        }))
    
    # 9. General Surgeon
    if scores['total'] >= 20 and scores['personal_skills'] >= 2 and scores['health_medical'] >= 10:
        matches.append(("General Surgeon", scores['health_medical'], {
            'Health/Medical': scores['health_medical']
        }))
    
    # Sort by highest score first
    return sorted(matches, key=lambda x: x[1], reverse=True)

def show_results(matches):
    if not matches:
        st.warning("Resume does not meet requirements for any targeted roles")
        return
    
    st.success(f"Found {len(matches)} matching role(s)")
    
    for i, (role, score, breakdown) in enumerate(matches, 1):
        with st.expander(f"{i}. {role} - Score: {score:.1f}", expanded=i==1):
            st.write(f"**Overall Match Score:** {score:.1f}/10")
            
            cols = st.columns(3)
            for j, (k, v) in enumerate(breakdown.items()):
                cols[j%3].metric(k, v)
            
            st.progress(min(score/10, 1.0))

if uploaded_file:
    with st.spinner("Analyzing resume..."):
        text = extract_text_from_pdf(uploaded_file)
        scores = calculate_scores(text)
        matches = determine_status(scores)
    
    st.divider()
    show_results(matches)
    
    with st.expander("🔍 View Detailed Domain Scores"):
        st.write("### Domain Keyword Counts")
        cols = st.columns(4)
        for i, (domain, count) in enumerate(scores.items()):
            if domain != 'total':
                cols[i%4].metric(domain.replace('_', ' ').title(), count)
        st.metric("TOTAL SCORE", scores['total'])