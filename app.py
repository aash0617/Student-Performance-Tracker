from flask import Flask, render_template,request,redirect,url_for
import pandas as pd



app = Flask(__name__)
@app.route('/cleaning')
def cleaning_page():
    import pandas as pd
    df = pd.read_csv('studentsPerformance.csv')

    # 🔹 Original shape
    original_shape = df.shape

    # 🔹 Clean column names
    df.columns = df.columns.str.strip()

    # 🔹 Drop fully empty rows
    df.dropna(how='all', inplace=True)

    # 🔹 Drop rows with any missing values
    df.dropna(inplace=True)

    # 🔹 Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # 🔹 Convert score columns to int
    df[['math score', 'reading score', 'writing score']] = df[['math score', 'reading score', 'writing score']].astype(int)

    cleaned_shape = df.shape

    return render_template('cleaning.html', original=original_shape, cleaned=cleaned_shape)



@app.route('/outliers')
def outlier_page():
    import pandas as pd

    df = pd.read_csv('studentsPerformance.csv')
    df.columns = df.columns.str.strip()

    subjects = ['math score', 'reading score', 'writing score']
    outlier_counts = {}

    for subject in subjects:
        Q1 = df[subject].quantile(0.25)
        Q3 = df[subject].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[subject] < Q1 - 1.5 * IQR) | (df[subject] > Q3 + 1.5 * IQR)]
        outlier_counts[subject] = len(outliers)

    return render_template('outliers.html', outliers=outlier_counts)


@app.route('/')
def home():
    return render_template('index.html') 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@example.com' and password == 'admin':
            return redirect('/dashboard')
        else:
            return "Invalid credentials!"
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analysis')

def analysis():
    import plotly.graph_objs as go
    import plotly.offline as pyo

    # Load CSV
    df = pd.read_csv('studentsPerformance.csv')

    # Gender-wise average
    gender_avg = df.groupby('gender')[["math score", "reading score", "writing score"]].mean().round(2)
    gender_table = gender_avg.to_html(classes="table table-bordered table-striped", border=0)

    # Prepare Plotly chart
    trace1 = go.Bar(x=gender_avg.index, y=gender_avg["math score"].tolist(), name="Math Score")
    trace2 = go.Bar(x=gender_avg.index, y=gender_avg["reading score"].tolist(), name="Reading Score")
    trace3 = go.Bar(x=gender_avg.index, y=gender_avg["writing score"].tolist(), name="Writing Score")
   
    data = [trace1, trace2, trace3]
    layout = go.Layout(title="Average Scores by Gender", barmode="group")
    fig = go.Figure(data=data, layout=layout)
    
    chart_div = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    return render_template('analysis.html', gender_table=gender_table, chart_div=chart_div)


@app.route('/test_prep')
def test_prep():
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.offline as pyo

    # Load dataset
    df = pd.read_csv('studentsperformance.csv')

    # Calculate average scores based on test preparation status
    testprep_avg = df.groupby('test preparation course')[['math score', 'reading score', 'writing score']].mean().round(2)

    # Prepare Plotly bar chart (same structure as gender-based)
    trace1 = go.Bar(x=testprep_avg.index, y=testprep_avg["math score"].tolist(), name="Math Score", marker=dict(color='blue'))
    trace2 = go.Bar(x=testprep_avg.index, y=testprep_avg["reading score"].tolist(), name="Reading Score", marker=dict(color='orange'))
    trace3 = go.Bar(x=testprep_avg.index, y=testprep_avg["writing score"].tolist(), name="Writing Score", marker=dict(color='green'))

    data = [trace1, trace2, trace3]
    layout = go.Layout(title="Test Preparation Impact on Scores", barmode="group")
    fig = go.Figure(data=data, layout=layout)

    # Create chart div
    chart_div = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    # Optional: convert testprep_avg DataFrame to HTML table if you want to display a table too
    testprep_table = testprep_avg.to_html(classes='table table-bordered', border=0)

    return render_template('test_prep_impact.html', chart_div=chart_div, testprep_table=testprep_table)


 
    
@app.route('/parental_impact')
def parental_impact():
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.offline as pyo

    df = pd.read_csv('studentsperformance.csv')

    # Group by parental education and get average scores
    education_avg = df.groupby('parental level of education')[['math score', 'reading score', 'writing score']].mean().round(2)

    # Create bar traces using .tolist()
    trace1 = go.Bar(x=education_avg.index.tolist(), y=education_avg["math score"].tolist(), name="Math Score")
    trace2 = go.Bar(x=education_avg.index.tolist(), y=education_avg["reading score"].tolist(), name="Reading Score")
    trace3 = go.Bar(x=education_avg.index.tolist(), y=education_avg["writing score"].tolist(), name="Writing Score")

    data = [trace1, trace2, trace3]
    layout = go.Layout(title="Average Scores by Parental Education", barmode="group")
    fig = go.Figure(data=data, layout=layout)

    chart_div = pyo.plot(fig, include_plotlyjs=False, output_type='div')
    return render_template('parent_education.html', chart_div=chart_div)




@app.route('/race_impact')
def race_impact():
    import pandas as pd
    import plotly.graph_objs as go
    import plotly.offline as pyo

    df = pd.read_csv('studentsperformance.csv')

    # Group by race/ethnicity and get average scores
    race_avg = df.groupby('race/ethnicity')[['math score', 'reading score', 'writing score']].mean().round(2)

    # Create bar traces using .tolist()
    trace1 = go.Bar(x=race_avg.index.tolist(), y=race_avg["math score"].tolist(), name="Math Score")
    trace2 = go.Bar(x=race_avg.index.tolist(), y=race_avg["reading score"].tolist(), name="Reading Score")
    trace3 = go.Bar(x=race_avg.index.tolist(), y=race_avg["writing score"].tolist(), name="Writing Score")

    data = [trace1, trace2, trace3]
    layout = go.Layout(title="Average Scores by Race/Ethnicity Group", barmode="group")
    fig = go.Figure(data=data, layout=layout)

    chart_div = pyo.plot(fig, include_plotlyjs=False, output_type='div')
    return render_template('race_performance.html', chart_div=chart_div)




@app.route('/top_students')
def top_students():
    df = pd.read_csv('studentsperformance.csv')
    df['total_score'] = df[['math score', 'reading score', 'writing score']].sum(axis=1)
    top10 = df.sort_values(by='total_score', ascending=False).head(10)
    top_table = top10[['gender', 'race/ethnicity', 'parental level of education', 'test preparation course',
                       'math score', 'reading score', 'writing score', 'total_score']].to_html(classes='table table-hover', border=0)

    return render_template('top_students.html', top_table=top_table)

    
   
if __name__ == '__main__':
    app.run(debug=True)
