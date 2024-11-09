from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from collections import defaultdict
import statistics
from trie import load_words_in_trie, Trie, TrieNode
from board import Board
from stats import generate_weighted_string, gamepigeon_weights

# Initialize Flask app
app = Flask(__name__)

# Load the words from file and the trie
valid_dict = load_words_in_trie()

# Define Board class and TrieNode class here (you can import them if they're in a separate module)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve input from form
        board_input = request.form.get('board_input')
        
        if board_input and len(board_input) == 16:
            board = Board(board_input)
            board._find_all_valid_words()
            valid_words = sorted(board.valid_words, key=lambda s: (-len(s), s))
            word_scores = board.print_word_scores()
            return render_template('index.html', board=board_input, valid_words=valid_words, word_scores=word_scores)
        
        return render_template('index.html', error="Invalid board input. Please enter exactly 16 letters.")
    
    return render_template('index.html', board=None, valid_words=None, word_scores=None)

@app.route('/generate_random_board', methods=['GET'])
def generate_random_board():
    # Generate a random board (16 letters)
    random_board = generate_weighted_string(16, gamepigeon_weights)
    return render_template('index.html', board=random_board, valid_words=None, word_scores=None)

if __name__ == '__main__':
    app.run(debug=True)
