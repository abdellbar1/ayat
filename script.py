#بسم الله الرحمان الرحيم
#improved html parsing reduced text 
import requests
from lxml import etree
import urllib.parse
import re
import logging
import sqlite3
from bs4 import BeautifulSoup

def fetch_html(url, ssl_v=True):
    """Helper function to fetch HTML content from a given URL."""
    logging.info(f"Fetching HTML content from URL: {url}")
    with requests.Session() as session:
        response = session.get(url, verify=ssl_v)
        if response.status_code == 200:
            logging.info("HTML content fetched successfully")
            return response.text
        else:
            logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

def fetch_word_occurrences(word):
    """Fetches the number of occurrences of a word in the Quran."""
    base_url = "https://holyquran.net/cgi-bin/qsearch.pl?st={}&sc=1&sv=0&ec=114&ev=0&ae=&mw=r&alef=ON"
    encoded_word = urllib.parse.quote(word.encode('windows-1256'))
    search_url = base_url.format(encoded_word)
    logging.info(f"Fetching word occurrences for '{word}' from URL: {search_url}")
    search_html_content = fetch_html(search_url)
    if search_html_content:
        # Regular expression to match <script> tags and their contents
        script_pattern = re.compile(r'<script.*?>.*?</script>', re.DOTALL)
        # Remove <script> content from HTML text
        reduced_html_text = script_pattern.sub('', search_html_content[:6992])

        #reduced_html_text = re.sub(r'\(.*?\)', '', search_html_content[:6992])
        pattern = r"عدد الكلمات المنقّبة عنها في الآيات لهذه الصفحة: (\d+)"
        root_word_pattern = r"الجذور المتوفرة هي: ([\w\s-]+)"
        match = re.search(pattern, reduced_html_text)
        root_word_matches = re.findall(root_word_pattern, reduced_html_text)
        if match and root_word_matches :
            occurrences = match.group(1)
            root_words_list = root_word_matches
            logging.info(f"Occurrences of '{word}': {occurrences}")
            logging.info(f"Root words list of '{word}' is : {root_words_list}")
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

def insert_into_database(word, url, count, sura, aya, root_words, ayah_text):
    """Inserts data into the SQLite database."""
    conn = sqlite3.connect('quran_data.db')
    c = conn.cursor()
    try:
        #c.execute("INSERT INTO word_occurrences VALUES (?, ?, ?, ?, ?, ?)", (word, url, count, sura, aya, root_words))
        c.execute("INSERT INTO word_occurrences (word, url, count, sura, aya, root_words, ayah_text) VALUES (?, ?, ?, ?, ?, ?, ?)", (word, url, count, sura, aya, root_words, ayah_text))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Word '{word}' already exists in the database.")
    conn.close()

def print_table():
    """Prints the contents of the SQLite table."""
    """Prints the contents of the SQLite table."""
    conn = sqlite3.connect('quran_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM word_occurrences")
    rows = c.fetchall()
    print("{:<3} | {:<10} | {:<30} | {:<4} | {:<2} | {:<3} | {:<10} | {:<100}".format("ID", "Word", "URL", "Count", "Sura", "Aya", "Root Words", "Ayah Text"))
    for row in rows:
        print("{:<3} | {:<10} | {:<30} | {:<4} | {:<2} | {:<3} | {:<10} | {:<100}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    conn.close()

def process_text(html_text):
    ayats_list = []
    # Remove text between parentheses
    html_text = re.sub(r'\(.*?\)', '', html_text)
    text_without_parentheses = html_text

    # Parse HTML
    soup = BeautifulSoup(text_without_parentheses, 'html.parser')

    # Extract text and links
    ayahs = soup.find_all('a')

    for ayah in ayahs:
        ayah_text = ayah.text
        ayah_href = ayah['href'] #http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya7.html

        sura_number, aya_number = map(int, re.findall(r'\d+', ayah_href))

        print(f"{ayah_text.strip()} ({int(aya_number)}, {int(sura_number)})")
        ayats_list.append((ayah_text.strip(), aya_number, sura_number))
    
    
    first_line_ayah = soup.find('strong')
    if first_line_ayah:
        line_ayah_text, line_ayah_number, line_sura_number = ayats_list[0]
        if line_ayah_number == 1: #current aya on the second line of teh text 
            
            first_line_sura_number = line_sura_number-1
            first_line_ayah_number = 0
        else:
            
            first_line_sura_number = line_sura_number
            first_line_ayah_number = line_ayah_number-1

        
        first_line_ayah_text   = first_line_ayah.text
        print(f"{first_line_ayah_text.strip()} ({first_line_ayah_number}, {first_line_sura_number})")

        ayats_list.insert(0,(first_line_ayah_text.strip(), first_line_ayah_number, first_line_sura_number))

    return ayats_list

def process_main_url_and_store(main_url):
    """Processes the main URL and extracts word occurrences, then stores them in the database."""
    main_html_content = fetch_html(main_url, False)
    if main_html_content:
        ayats_list = process_text(main_html_content)


        for ayah in ayats_list:
            ayah_text, ayah_number, sura_number = ayah
            print(ayah_text)
            words = ayah_text.split()
            for word in words:
                try:
                    occurrences, root_words_list = fetch_word_occurrences(word)
                    root_words_str = ', '.join(root_words_list)
                    insert_into_database(word, main_url, occurrences, sura_number, ayah_number, root_words_str,ayah_text)
                except Exception as e:
                    logging.error(f"Error parsing word: {word}. Error: {str(e)}")

def main():
    """Main function to create the database, process the main URLs, and print the table."""
    logging.basicConfig(level=logging.INFO)
    create_database()
    
    for p in range(1,100): #605):
            main_url = f"https://quran.ksu.edu.sa/tafseer/interface.php?p={p}&t_str=tabary"
            process_main_url_and_store(main_url)
    
    print_table()

if __name__ == "__main__":
    main()
