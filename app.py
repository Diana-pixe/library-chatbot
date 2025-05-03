from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

library_db = {
    "Pride and Prejudice": {"author": "Jane Austen", "available": True, "location": "Fiction"},
    "The Lord of the Rings": {"author": "J.R.R. Tolkien", "available": True, "location": "Fantasy"},
    "The Hitchhiker's Guide to the Galaxy": {"author": "Douglas Adams", "available": True, "location": "Science Fiction"},
    "To Kill a Mockingbird": {"author": "Harper Lee", "available": True, "location": "Fiction"},
    "1984": {"author": "George Orwell", "available": False, "location": "Dystopian Fiction"},
    "Animal Farm": {"author": "George Orwell", "available": True, "location": "Satire"},
    "Things Fall Apart": {"author": "Chinua Achebe", "available": True, "location": "Fiction"},
    "The Great Gatsby": {"author": "F. Scott Fitzgerald", "available": False, "location": "Fiction"},
    "Half of a Yellow Sun": {"author": "Chimamanda Ngozi Adichie", "available": True, "location": "Historical Fiction"},
    "The Hobbit": {"author": "J.R.R. Tolkien", "available": True, "location": "Fantasy"},
}

def search_books(query):
    """Searches the library database based on the query."""
    results = {}
    for book, details in library_db.items():
        match = True
        for key, value in query.items():
            if key not in details or value.lower() not in details[key].lower():
                match = False
                break
        if match:
            results[book] = details
    return results

def check_availability(title):
    """Checks the availability of a book."""
    if title in library_db:
        return "available" if library_db[title]["available"] else "not available"
    return None

def get_library_info():
    """Returns general library information."""
    return "The library is open from 9 AM to 5 PM, Monday to Friday.  Our location is 123 Main Street."

@app.route('/chat', methods=['POST'])
def chat():
    """Handles user messages and returns responses."""
    try:
        data = request.get_json()
        message = data['message']
        logging.info(f"Received message: {message}")

        response = process_message(message)
        logging.info(f"Generated response: {response}")
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return jsonify({'response': "Sorry, there was an error processing your request."}), 500

def process_message(message):
    """Processes the user's message and generates an appropriate response."""
    message = message.lower()

    if "hello" in message or "hi" in message or "hey" in message:
        return "Hello! How can I help you today?"

    elif "goodbye" in message or "bye" in message:
        return "Goodbye!"

    elif "book" in message and "search" in message:
        query = {}
        if "title" in message:
            title_start = message.find("title") + len("title") + 1
            title_end = message.find("available")
            if title_end == -1:
                title_end = len(message)
            title = message[title_start:title_end].strip()
            query["title"] = title
        if "author" in message:
            author_start = message.find("author") + len("author") + 1
            author_end = len(message)
            author = message[author_start:author_end].strip()
            query["author"] = author
        if "subject" in message:
            subject_start = message.find("subject") + len("subject") + 1
            subject_end = len(message)
            subject = message[subject_start:subject_end].strip()
            query["subject"] = subject
        results = search_books(query)
        if results:
            response = "Here are the books I found:\n"
            for book, details in results.items():
                response += f"- {book} by {details['author']} (Available: {'Yes' if details['available'] else 'No'}, Location: {details['location']})\n"
            return response
        else:
            return "Sorry, I couldn't find any books matching your search."

    elif "availability" in message:
        title_start = message.find("availability") + len("availability") + 1
        title_end = len(message)
        title = message[title_start:title_end].strip()
        availability = check_availability(title)
        if availability:
            return f"The book '{title}' is {availability}."
        else:
            return f"Sorry, I couldn't find the book '{title}' in the library."

    elif "opening hours" in message or "location" in message:
        return get_library_info()

    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

if __name__ == "__main__":
    app.run(debug=True)

