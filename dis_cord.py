import requests
import pandas as pd
import re
import json

# Get Item ID name 
def item_name(id):
    with open("./item_discord.json", "r") as json_file:
        data = json.load(json_file)
    try:
        return data[id]
    except:
        return False


def dis_cord():
    file_path = 'secret.txt'  # Change this to your file's path
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        file_content = file.read()

    result = requests.get(
        url='https://discord.com/api/v9/channels/275501342666260482/messages?limit=100',
        # Might be better to replace this with an alt account session
        headers={
            "Authorization": file_content,
        }
    )

    if result.status_code == 200:
        resultJson = result.json()
        headers = ["author", "content"]
        temp = []
        for i in resultJson:
            temp.append([
                i["author"]["username"],
                i["content"].lower()
            ])
        content_df = pd.DataFrame(columns=headers)
        df_row = pd.DataFrame(temp, columns=headers)
        content_df = content_df.append(df_row)
        return result.status_code, content_df
    else:
        return result.status_code, []

def remove_discord_emojis(input_string):
    # Pattern to match Unicode emojis used in Discord
    pattern = re.compile(r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]')

    # Replace emojis with an empty string
    clean_string = re.sub(pattern, '', input_string)

    return clean_string

def remove_discord_custom_emojis(input_string):
    # To add on here
    emojis_to_remove = ['🧀', '☁️', '🧿', '⛈️', '🫘']
    # Pattern to match <:emoji_name:emoji_id>
    pattern = re.compile(r'<:[a-zA-Z0-9_]+:[0-9]+>')

    # Replace custom emojis with an empty string
    clean_string = re.sub(pattern, '', input_string)

    for emoji in emojis_to_remove:
        clean_string = clean_string.replace(emoji, '')

    return clean_string

def remove_parentheses(input_string):
    # Remove text within parentheses including parentheses
    return re.sub(r'\([^)]*\)', '', input_string)

def remove_suffix(text):
    # Define the custom lemmatization rules using a dictionary
    words = ['each', 'ea', 'sb','can','take','bulk','for','stock','got','with','your', ':']
    for word in words:
        if text.endswith(word):
            text = text[:-len(word)].strip()

    return text

def is_numeric(input_string):
    cleaned_string = input_string.replace(",", "")  # Remove commas
    return re.match(r'^[-+]?\d*\.?\d+$', cleaned_string) is not None

# Steps 
# 1. Delinate by "\n" and "|"
# 2. Remove custom characters 
# 3. Remove parentheses content
# 3. Trimm string 
# 4. Append "b> " or "s> " if missing 
# 5. Filiter out stikeout listings 
# 6. Remove listing less then 3 length
# 7. Filiter out trading listings
# 8. Filiter custom listings
# 8. Format characters; Example: ["S>GGC"] into ["S>", "GGC"] and Replace ["S", ">"] into ["S>"]
# 9. Remove listing less then 3 length
# 10. Return n-gram
def custom_ngrams(content, WordsToCombine):
    headers = ["author", "content", "orginial"]
    error_df = pd.DataFrame()
    words_df = pd.DataFrame()

    # Remove duplicates and keep the first occurrence
    content = content.drop_duplicates()

    ### DELINITER and Removal off custom characters
    # Deliniter: "\n" and "|"
    # Removed Characters: "-, *, _, ="
    save_words_1 = ["selling", "sell", "selling:", "selling>", "s>", "s >"]
    save_words_2 = ["buying", "buy", "buying:", "buying>", "b>", "b >"]
    content_split = pd.DataFrame(columns=headers) 
    append_word = ""
    for index, row in content.iterrows():
        row["content"] = row["content"].lower()

        split_parts = []
        # Split by "\n"
        for line in row["content"].split('\n'):
            # Further split by "|"
            split_parts.extend(line.split('|'))
        for part in split_parts:
            # Remove Custom Characters
            part = part.replace("-", "").replace("=", "").replace("*", "").replace("_", "").replace("@", "").replace("+", "").replace(",", "")
            # Remove Discord Emojis
            part = remove_discord_emojis(part)
            part = remove_discord_custom_emojis(part)

            part = remove_parentheses(part)
            # Trimm string
            part = part.lstrip()

            if any(_ in part for _ in save_words_1):
                append_word = "s> "
            elif any(_ in part for _ in save_words_2):
                append_word = "b> "
            else:
                # Append Selling or Buying if missing prefix
                part = append_word + part
                
            content_split = content_split.append({'author': row["author"], 
                                                'content': part,
                                                'orginial': row["content"],
                                            }, ignore_index=True)

    # Filiter out listing that is strikeout
    rows_to_delete = []
    for index, row in content_split.iterrows():
        words = row["content"].split()
        if len(words) > 0:
            if words[0][0:2] == "~~":
                rows_to_delete.append(index)
        if len(words) < 3:
            rows_to_delete.append(index)
    content_split = content_split.drop(rows_to_delete)

    # Delete Trading Listing
    rows_to_delete= []
    delete_words = ["trade", "trading", "t>", "t"]
    for index, row in content_split.iterrows():
        words = row["content"].split()
        for i in words:
            for j in delete_words:
                if i == j:
                    error_df.append(row, ignore_index=True)
                    rows_to_delete.append(index)
    content_split = content_split.drop(rows_to_delete)

    # Delete Custom Listing
    rows_to_delete= []
    listings_words = ["lgs", "2023"]
    for index, row in content_split.iterrows():
        words = row["content"].split()
        for i in words:
            for j in listings_words:
                if i == j:
                    rows_to_delete.append(index)
    content_split = content_split.drop(rows_to_delete)

    ### FILITER 1-GRAM
    for _, row in content_split.iterrows():
        words = row["content"].split()
        # Check if not empty
        if len(words) > 0:
            filiter_words_1 = ["s>", "b>"]
            filiter_words_2 = ["selling", "buying", "sell", "buy", "selling:", "buying:", "selling>", "buying>"]

            # Replace ["S>GGC"] into ["S>", "GGC"]
            if len(words[0]) > 2 and any(_ in words[0] for _ in filiter_words_1):
                words.insert(1, words[0][2:])
                words[0] = words[0][0:1]

            # Replace ["S", ">"] into ["S>"]
            if (words[0] == "s" and words[1][0] == ">") or (words[0] == "b" and words[1][0] == ">"):
                words[0] = words[0] + words[1]
                del words[1]

            # Return 1-3 terms
            filiter_words_1 = ["s>", "b>", "s", "b"]
            for i in range(1):
                if (words[0] not in filiter_words_2 and words[0][-2:] not in filiter_words_1):
                    error_df = error_df.append({
                        "author": row["author"],
                        "content": words[i:i+WordsToCombine],
                        "orginial": row["orginial"]
                    }, ignore_index=True)
                else:
                    words[0] = words[0][0:1]
                    words_df = words_df.append({
                        "author": row["author"],
                        "content": words[i:i+WordsToCombine],
                        "orginial": row["orginial"]
                    }, ignore_index=True)

    # Filiter out listing that is strikeout
    rows_to_delete = []
    for index, row in words_df.iterrows():
        if len(words) < 3:
            rows_to_delete.append(index)
    content_split = content_split.drop(rows_to_delete)

    return words_df, error_df

def lemmatize_helper(n_gram):
    for _, row in n_gram.iterrows():
        for i in range(len(row["content"])):
            row["content"][i] = remove_suffix(row["content"][i])
        row["content"] = [item for item in row["content"] if item != ""]
    return n_gram

def extract_listing_type(n_gram):
    n_gram['listing_type'] = '-'
    for _, row in n_gram.iterrows():
        row["listing_type"] = row["content"][0]
    return n_gram

def extract_quantity(n_gram):
    n_gram['quantity'] = '0'
    for _, row in n_gram.iterrows():
        if row["content"][1].isdigit():
            row["quantity"] = row["content"][1]
            del row["content"][1]
    
    return n_gram

def extract_price(n_gram):
    n_gram['price'] = '0'
    for _, row in n_gram.iterrows():
        for i in range(len(row["content"])):
            if is_numeric(row["content"][i]):
                row["price"] = row["content"][i]
                row["content"] = row["content"][:i+1]
                break
    return n_gram

def extract_item_id(n_gram, error):
    n_gram['item_id'] = '-'
    rows_to_delete= []
    for _, row in n_gram.iterrows():
        for i in row["content"]:
            if(item_name(i) is not False):
                row['item_id'] = item_name(i)
    # Combine String
    for index, row in n_gram.iterrows():
        if row['item_id'] == '-':
            combined_string = " ".join(row['content'][1:-1])
            if(item_name(combined_string) is not False):
                row['item_id'] = item_name(combined_string)
            else:
                error = error.append(row, ignore_index=True)
                rows_to_delete.append(index)
    n_gram = n_gram.drop(rows_to_delete)
            
    return n_gram, error

# data = {
#     'author': ["pong"],
#     'content': ["Selling\nCCC 0.18 | RSPC 0.6 | REPC 2.1\nBottled Wind 3.7 | USC 1.4 |  FBF 3.8 \nZugzwang's Leftover Rock 14000\nCTOT 2900 | CRM 0.32 | CC 16\n2023 0.25 | rift 2023 0.8 | UWC 3.5\nDBC 1.1 | SDBC 2 | EDBC 3 | UDBC 3.5 \nRonza's Beanstalk Supply Ship 6500\n2months lgs 500 | GSC 0.95\nCF 8.5 (>500 8.3) | 4months lgs 950"]
# }
# headers = ["author", "content"]
# content_df = pd.DataFrame(data, columns=headers)
# content, error = custom_ngrams(content_df, 10)
# content = lemmatize_helper(content)
# content = extract_quantity(content)


status_code, content = dis_cord()
if status_code == 200:
    content, error = custom_ngrams(content, 10)
    content = lemmatize_helper(content)
    content = extract_listing_type(content)
    content = extract_quantity(content)
    content = extract_price(content)
    content, error = extract_item_id(content, error)

    content.to_excel('output.xlsx', index=False)

    print(error)
else:
    print(status_code)
