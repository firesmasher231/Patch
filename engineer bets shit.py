from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bet1 = request.form['bet1']
        bet2 = request.form['bet2']
        stake = float(request.form['stake'])
        
        # You can process the bets and stake here
        result = f"Bet 1: {bet1}, Bet 2: {bet2}, Stake: ${stake:.2f}"
        return render_template('result.html', result=result)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
