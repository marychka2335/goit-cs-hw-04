import logging

# Searching keywords
def search_keywords(file_path, keywords, results):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                amount = content.count(keyword)
                if amount > 0:
                    results.setdefault(keyword, []).append(file_path)
    except Exception as e:
        logging.error(f"Processing {file_path}: {str(e)}")
        