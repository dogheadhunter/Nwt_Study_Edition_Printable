"""
Analyze the live HTML structure from Psalms 83 to identify correct selectors.
"""
from bs4 import BeautifulSoup
import json

# Sample of the actual HTML structure I extracted
sample_html = """
<article>
<h1 class="sectionHeading"><span>Psalm</span> <span>83:1-18</span></h1>

<div class="bodyTxt">
<div id="tt4">
<sup><span id="v19083000-1" class="verse chapterNum">
<a class="study-note-ref" href="#xref">a</a>
</span>A song. A melody of Aʹsaph.
</sup>
</div>

<div id="section1">
<p id="p3" data-pid="3" class="sb">
<sup><span id="v19083001-1" class="verse verseNum">1</span></sup>
O God, do not be silent;
<a class="study-note-ref" href="#xref">b</a>
</p>
<p id="p3" data-pid="3" class="sb">
Do not keep quiet<a class="fn" href="#footnote">*</a> or still, O Divine One.
</p>
</div>

<div id="section2">
<p id="p4" data-pid="4" class="sb">
<sup><span id="v19083002-1" class="verse verseNum">2</span></sup>
For look! your enemies are in an uproar;
<a class="study-note-ref" href="#xref">c</a>
</p>
<p id="p4" data-pid="4" class="sb">
Those who hate you act arrogantly.<a class="fn" href="#footnote">*</a>
</p>
</div>

<!-- More verses... -->

<p id="p21" data-pid="21" class="sb">
<sup><span id="v19083018-1" class="verse verseNum">18</span></sup>
May people know that you, whose name is Jehovah,
<a class="study-note-ref" href="#xref">v</a>
</p>
<p id="p21" data-pid="21" class="sb">
You alone are the Most High over all the earth.
<a class="study-note-ref" href="#xref">w</a>
</p>

</div>
</article>
"""

print("=== ANALYZING LIVE HTML STRUCTURE ===\n")
soup = BeautifulSoup(sample_html, 'html.parser')

# Analyze verse structure
print("1. VERSE SELECTORS:")
verse_nums = soup.find_all('span', class_='verseNum')
print(f"   - Found {len(verse_nums)} verse numbers")
print(f"   - Selector: span.verseNum")
if verse_nums:
    print(f"   - Example: '{verse_nums[0].text}'")

# Analyze verse containers
verse_containers = soup.find_all('p', class_='sb')
print(f"\n   - Found {len(verse_containers)} verse containers")
print(f"   - Selector: p.sb (paragraph with 'sb' class)")

# Analyze superscription
superscript = soup.find('sup')
if superscript:
    print(f"\n2. SUPERSCRIPTION:")
    print(f"   - Found in <sup> tag")
    print(f"   - Text: '{superscript.get_text(strip=True)[:50]}...'")

# Analyze footnotes
footnotes = soup.find_all('a', class_='fn')
print(f"\n3. FOOTNOTES:")
print(f"   - Found {len(footnotes)} footnote markers")
print(f"   - Selector: a.fn")

# Analyze cross-references
xrefs = soup.find_all('a', class_='study-note-ref')
print(f"\n4. CROSS-REFERENCES:")
print(f"   - Found {len(xrefs)} cross-reference markers")
print(f"   - Selector: a.study-note-ref")

print("\n=== RECOMMENDED SELECTORS ===")
selectors = {
    'verse_container': 'p.sb',
    'verse_number': 'span.verseNum',
    'superscription': 'sup',
    'footnote_marker': 'a.fn',
    'cross_reference_marker': 'a.study-note-ref',
    'chapter_heading': 'h1.sectionHeading',
}

print(json.dumps(selectors, indent=2))
