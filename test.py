# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

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

# Example usage
html_text = '''<body data-new-gr-c-s-check-loaded="14.1167.0" data-gr-ext-installed=""><strong class="text-success">إِنَّ الَّذِينَ كَفَرُوا سَوَاءٌ عَلَيْهِمْ أَأَنذَرْتَهُمْ أَمْ لَمْ تُنذِرْهُمْ لَا يُؤْمِنُونَ (6) </strong><a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya7.html">خَتَمَ اللَّهُ عَلَىٰ قُلُوبِهِمْ وَعَلَىٰ سَمْعِهِمْ ۖ وَعَلَىٰ أَبْصَارِهِمْ غِشَاوَةٌ ۖ وَلَهُمْ عَذَابٌ عَظِيمٌ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya7.html">7</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya8.html">وَمِنَ النَّاسِ مَن يَقُولُ آمَنَّا بِاللَّهِ وَبِالْيَوْمِ الْآخِرِ وَمَا هُم بِمُؤْمِنِينَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya8.html">8</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya9.html">يُخَادِعُونَ اللَّهَ وَالَّذِينَ آمَنُوا وَمَا يَخْدَعُونَ إِلَّا أَنفُسَهُمْ وَمَا يَشْعُرُونَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya9.html">9</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya10.html">فِي قُلُوبِهِم مَّرَضٌ فَزَادَهُمُ اللَّهُ مَرَضًا ۖ وَلَهُمْ عَذَابٌ أَلِيمٌ بِمَا كَانُوا يَكْذِبُونَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya10.html">10</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya11.html">وَإِذَا قِيلَ لَهُمْ لَا تُفْسِدُوا فِي الْأَرْضِ قَالُوا إِنَّمَا نَحْنُ مُصْلِحُونَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya11.html">11</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya12.html">أَلَا إِنَّهُمْ هُمُ الْمُفْسِدُونَ وَلَٰكِن لَّا يَشْعُرُونَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya12.html">12</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya13.html">وَإِذَا قِيلَ لَهُمْ آمِنُوا كَمَا آمَنَ النَّاسُ قَالُوا أَنُؤْمِنُ كَمَا آمَنَ السُّفَهَاءُ ۗ أَلَا إِنَّهُمْ هُمُ السُّفَهَاءُ وَلَٰكِن لَّا يَعْلَمُونَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya13.html">13</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya14.html">وَإِذَا لَقُوا الَّذِينَ آمَنُوا قَالُوا آمَنَّا وَإِذَا خَلَوْا إِلَىٰ شَيَاطِينِهِمْ قَالُوا إِنَّا مَعَكُمْ إِنَّمَا نَحْنُ مُسْتَهْزِئُونَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya14.html">14</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya15.html">اللَّهُ يَسْتَهْزِئُ بِهِمْ وَيَمُدُّهُمْ فِي طُغْيَانِهِمْ يَعْمَهُونَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya15.html">15</a>) <a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya16.html">أُولَٰئِكَ الَّذِينَ اشْتَرَوُا الضَّلَالَةَ بِالْهُدَىٰ فَمَا رَبِحَت تِّجَارَتُهُمْ وَمَا كَانُوا مُهْتَدِينَ</a> (<a href="http://quran.ksu.edu.sa/tafseer/qortobi/sura2-aya16.html">16</a>) </body>'''
print(process_text(html_text))