from flask import Flask, render_template, request, jsonify, session
import random
from connection import conn
import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # שנה את זה למפתח סודי אקראי




logger = logging.getLogger("hungman_logger")
logger.setLevel(logging.INFO)
logstash_formatter = logging.Formatter(fmt="%(name)s :: %(levelname)s :: %(message)s")
logstash_handler = AsynchronousLogstashHandler('logstash', 5001, database_path=None)
logstash_handler.setFormatter(logstash_formatter)
logger.addHandler(logstash_handler)



# רשימה של 20 מילות פרי באנגלית
fruits = ['cat', 'dog', 'elephant', 'fox', 'giraffe', 'hedgehog', 'iguana', 'jaguar', 'kangaroo', 'leopard', 'mantis', 'ninja', 'octopus', 'panda', 'bird', 'rabbit', 'snake', 'tiger', 'lion', 'vampire']

# ASCII art עבור ה"איש תלוי"
hangman_art = [
    """
        +---+
        |   |
            |
            |
            |
            |
    =========
    """,
    """
        +---+
        |   |
        O   |
            |
            |
            |
    =========
    """,
    """
        +---+
        |   |
        O   |
        |   |
            |
            |
    =========
    """,
    """
        +---+
        |   |
        O   |
       /|   |
            |
            |
    =========
    """,
    """
        +---+
        |   |
        O   |
       /|\  |
            |
            |
    =========
    """,
    """
        +---+
        |   |
        O   |
       /|\  |
       /    |
            |
    =========
    """,
    """
        +---+
        |   |
        O   |
       /|\  |
       / \  |
            |


    =========
    """
]

@app.route('/')
def index():
    logger.info("index")
    return render_template('/index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    player_name = request.form['player_name']
    word = random.choice(fruits)
    session['player_name'] = player_name
    session['word'] = word
    session['guess_word'] = ['_'] * len(word)
    session['incorrect_guesses'] = 0
    return jsonify({'guess_word': ' '.join(session['guess_word']), 'hangman': hangman_art[0]})

@app.route('/guess', methods=['POST'])
def guess():
    guess = request.form['guess'].lower()
    word = session['word']
    guess_word = session['guess_word']
    incorrect_guesses = session['incorrect_guesses']

    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                guess_word[i] = guess
    else:
        incorrect_guesses += 1

    session['guess_word'] = guess_word
    session['incorrect_guesses'] = incorrect_guesses

    game_over = False
    message = ""
    if ''.join(guess_word) == word:
        message = f" well done {session['player_name']}! the word was '{word}'."
        save_score(session['player_name'], 6 - incorrect_guesses)
        logger.info(message)
        game_over = True
    elif incorrect_guesses >= 6:
        message = f"sorry {session['player_name']}, the word was '{word}'."
        save_score(session['player_name'], 0)
        logger.info(message)
        game_over = True

    return jsonify({
        'guess_word': ' '.join(guess_word),
        'hangman': hangman_art[min(incorrect_guesses, len(hangman_art) - 1)],
        'message': message,
        'game_over': game_over
    })

def save_score(name, score):
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (name, score) VALUES (%s, %s)", (name, score))
    conn.commit()
    cur.close()

if __name__ == '__main__':
    app.run(debug=True)
