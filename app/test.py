from utils import detect_spam

if __name__=="__main__":
   email_input = """Congratulations! You've been selected to win a free iPhone 15.
       Click here to claim your prize."""
   result = detect_spam(email_input)
   print(result)