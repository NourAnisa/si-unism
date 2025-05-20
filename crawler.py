from scholarly import scholarly
import time

def get_publications(scholar_id: str, user_id: int):
    try:
        author = scholarly.search_author_id(scholar_id)
        scholarly.fill(author, sections=['publications'])
        
        publications = []
        for pub in author['publications']:
            scholarly.fill(pub)
            publications.append({
                'user_id': user_id,
                'title': pub['bib'].get('title', ''),
                'journal': pub['bib'].get('venue', ''),
                'year': pub['bib'].get('year', 0),
                'citation_count': pub.get('num_citations', 0)
            })
            time.sleep(1)  # Delay untuk menghindari blocking
            
        return publications
    except Exception as e:
        print(f"Error crawling Google Scholar: {e}")
        return []
