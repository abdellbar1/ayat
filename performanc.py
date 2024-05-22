import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import logging
import sqlite3

def fetch_html(url, ssl_v=True):
    """Helper function to fetch HTML content from a given URL."""
    with requests.Session() as session:
        response = session.get(url, verify=ssl_v)
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

def fetch_word_occurrences(word):
    """Fetches the number of occurrences of a word in the Quran."""
    base_url = "https://holyquran.net/cgi-bin/qsearch.pl?st={}&sc=1&sv=0&ec=114&ev=0&ae=&mw=r&alef=ON"
    encoded_word = urllib.parse.quote(word.encode('windows-1256'))
    search_url = base_url.format(encoded_word)
    search_html_content = fetch_html(search_url)
    if search_html_content:
        pattern = r"عدد الكلمات المنقّبة عنها في الآيات لهذه الصفحة: (\d+)"
        root_word_pattern = r"الجذور المتوفرة هي: ([\w\s-]+)"
        match = re.search(pattern, search_html_content)
        root_word_matches = re.findall(root_word_pattern, search_html_content)
        if match and root_word_matches:
            occurrences = match.group(1)
            root_words_list = root_word_matches
            return occurrences, root_words_list
        else:
            logging.error("Pattern not found in the HTML content.")
            return "00", []
    else:
        logging.error("Failed to fetch HTML content for word occurrences.")
        return "00", []

def create_database():
    """Creates a SQLite database and table if they don't exist."""
    conn = sqlite3.connect('quran_data.db')
    c = conn.cursor()
    c.execute('''
                    CREATE TABLE IF NOT EXISTS word_occurrences
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    word TEXT, 
                    url TEXT, 
                    count INTEGER, 
                    sura INTEGER, 
                    aya INTEGER, 
                    root_words TEXT,
                    ayah_text TEXT)
                ''')
    conn.commit()
    conn.close()

def insert_batch_into_database(data):
    """Inserts a batch of data into the SQLite database."""
    conn = sqlite3.connect('quran_data.db')
    c = conn.cursor()
    try:
        c.executemany("INSERT INTO word_occurrences (word, url, count, sura, aya, root_words, ayah_text) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Handle integrity errors if needed
    conn.close()

def process_text(html_text, main_url):
    """Processes the HTML text to extract word occurrences."""
    ayats_list = []
    soup = BeautifulSoup(html_text, 'html.parser')
    ayahs = soup.find_all('a')

    for ayah in ayahs:
        ayah_text = ayah.text.strip()
        sura_number, aya_number = map(int, re.findall(r'\d+', ayah['href']))
        ayats_list.append((ayah_text, aya_number, sura_number))

    first_line_ayah = soup.find('strong')
    if first_line_ayah:
        line_ayah_text, line_ayah_number, line_sura_number = ayats_list[0]
        if line_ayah_number == 1:
            first_line_sura_number = line_sura_number - 1
            first_line_ayah_number = 0
        else:
            first_line_sura_number = line_sura_number
            first_line_ayah_number = line_ayah_number - 1

        first_line_ayah_text = first_line_ayah.text.strip()
        ayats_list.insert(0, (first_line_ayah_text, first_line_ayah_number, first_line_sura_number))

    return ayats_list

def process_main_url_and_store(main_url):
    """Processes the main URL, extracts word occurrences, and stores them in the database."""
    main_html_content = fetch_html(main_url, False)
    if main_html_content:
        ayats_list = process_text(main_html_content, main_url)
        data_to_insert = []

        for ayah in ayats_list:
            ayah_text, ayah_number, sura_number = ayah
            words = ayah_text.split()
            for word in words:
                try:
                    occurrences, root_words_list = fetch_word_occurrences(word)
                    root_words_str = ', '.join(root_words_list)
                    data_to_insert.append((word, main_url, occurrences, sura_number, ayah_number, root_words_str, ayah_text))
                except Exception as e:
                    logging.error(f"Error parsing word: {word}. Error: {str(e)}")

        insert_batch_into_database(data_to_insert)

def main():
    """Main function to create the database, process the main URLs."""
    logging.basicConfig(level=logging.ERROR)  # Set logging level to ERROR
    create_database()

    for p in range(1, 3):
        main_url = f"https://quran.ksu.edu.sa/tafseer/interface.php?p={p}&t_str=tabary"
        process_main_url_and_store(main_url)

if __name__ == "__main__":
    main()
