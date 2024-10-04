from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

class MarkovChain:
    def __init__(self, order=1):
        self.order = order
        self.chain = {}

    def train(self, text):
        words = text.split()
        for i in range(len(words) - self.order):
            key = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            if key not in self.chain:
                self.chain[key] = []
            self.chain[key].append(next_word)

    def generate(self, length=50):
        if not self.chain:
            return ""

        # Randomly select a starting key
        current_key = random.choice(list(self.chain.keys()))
        output = list(current_key)

        for _ in range(length):
            next_words = self.chain.get(current_key)
            if not next_words:
                break
            next_word = random.choice(next_words)
            output.append(next_word)
            # Move the window
            current_key = tuple(output[-self.order:])

        return ' '.join(output)

# Create a global instance of the MarkovChain
markov_chain = MarkovChain(order=1)

# Route to serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle text generation
@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    markov_chain.train(data['text'])
    generated_text = markov_chain.generate(length=50)
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    # Read the text data from input.txt at startup
    with open('input.txt', 'r', encoding='utf-8') as file:
        text_data = file.read()
    markov_chain.train(text_data)  # Train on the initial text
    app.run(debug=True)
