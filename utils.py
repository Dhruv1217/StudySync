import random

def get_random_quote():
    quotes = [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "It always seems impossible until it's done. – Nelson Mandela",
        "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
        "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
        "Start where you are. Use what you have. Do what you can. – Arthur Ashe",
        "There are no secrets to success. It is the result of preparation, hard work, and learning from failure. – Colin Powell",
        "Doubt kills more dreams than failure ever will. – Suzy Kassem",
        "Your limitation—it's only your imagination."
    ]
    return random.choice(quotes)
