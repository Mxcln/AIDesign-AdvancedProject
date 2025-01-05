import re

def count_tokens_in_file(file_path):
    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Tokenize the content using a simple regex
        # This splits by words, numbers, and punctuation
        tokens = re.findall(r'\b\w+\b|[^\w\s]', content)
        
        # Print and return the token count
        token_count = len(tokens)
        print(f"The file '{file_path}' contains {token_count} tokens.")
        return token_count
    except Exception as e:
        print(f"Error: {e}")

# Example usage
file_path = r"E:\MyCardLibrary\ygopro\expansions\script\c99999335.lua"  # Replace with your file path
count_tokens_in_file(file_path)
