import sqlite3
import os

def escape_special_characters(text):
    # Replace special characters with their escape sequences
    text = text.replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')
    return text

def create_dataset(db_path, lua_folder, output_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List to store the missing IDs
    missing_ids = []
    
    # Open output file for writing
    with open(output_file, 'w', encoding='utf-8') as f:
        # Query the "texts" table for card data
        cursor.execute("SELECT id, name, desc FROM texts")
        rows = cursor.fetchall()

        # Process each row
        for row in rows:
            card_id, card_name, card_desc = row
            
            # Prepare the user content
            user_content = f"ID:{card_id};NAME:{card_name};DESC:{card_desc}"

            # Read the assistant content from the corresponding .lua file
            lua_file_path = os.path.join(lua_folder, f"c{card_id}.lua")
            
            if os.path.exists(lua_file_path):
                with open(lua_file_path, 'r', encoding='utf-8') as lua_file:
                    assistant_content = lua_file.read()
                    # Replace multiple empty lines with a single empty line
                    assistant_content = '\n'.join([line for line in assistant_content.splitlines() if line.strip() != ''])
            else:
                # If Lua file doesn't exist, add the ID to the missing list and skip this case
                missing_ids.append(card_id)
                continue
            
            # System content (static for all entries)
            with open('../prompt.txt', 'r', encoding='utf-8') as system_file:
                system_content = system_file.read().strip()
            # system_content = "You are a coder of yu-gi-oh card game simulator. I will give you the data and effect of a card, you need to write the code to simulate the card, based on ygopro."

            # Escape special characters in all contents
            system_content = escape_special_characters(system_content)
            user_content = escape_special_characters(user_content)
            assistant_content = escape_special_characters(assistant_content)

            # Prepare final entry as a single line
            entry = f"{{\"messages\": [{{\"role\": \"system\", \"content\": \"{system_content}\"}}, {{\"role\": \"user\", \"content\": \"{user_content}\"}}, {{\"role\": \"assistant\", \"content\": \"{assistant_content}\"}}]}}"
            
            # Write the entry to the output file
            f.write(entry + '\n')

    # Close the database connection
    conn.close()

    # Output the missed IDs
    if missing_ids:
        print("Missing IDs (no Lua file found):")
        for missed_id in missing_ids:
            print(missed_id)
    else:
        print("No missing IDs.")

# Example usage
create_dataset(r'E:\MyCardLibrary\ygopro\cards.cdb', r'E:\MyCardLibrary\ygopro\script', 'dataset.txt')
