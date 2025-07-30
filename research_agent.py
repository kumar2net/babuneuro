#!/usr/bin/env python3
"""
Deep Learning Neurology Research Agent
Automated system for gathering and processing research papers on deep learning applications in neurology.
"""

import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

class NeuroResearchAgent:
    def __init__(self, data_file: str = "research_data.json"):
        self.data_file = data_file
        self.load_data()
        
    def load_data(self):
        """Load existing research data from JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Data file {self.data_file} not found. Creating new data structure.")
            self.data = self._create_empty_data_structure()
    
    def save_data(self):
        """Save research data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def _create_empty_data_structure(self) -> Dict:
        """Create empty data structure if file doesn't exist."""
        return {
            "last_updated": datetime.now().isoformat(),
            "research_cycles": [],
            "categories": {},
            "model_architectures": {"tracked_models": []},
            "metrics": {"total_papers_reviewed": 0, "active_research_areas": 0}
        }
    
    def search_pubmed(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search PubMed for research papers using the NCBI E-utilities API.
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
        # Step 1: Search for paper IDs
        search_url = f"{base_url}esearch.fcgi"
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'xml',
            'sort': 'pub_date',
            'reldate': 365  # Papers from last year
        }
        
        try:
            search_response = requests.get(search_url, params=search_params)
            search_response.raise_for_status()
            
            # Parse XML to get PMIDs
            root = ET.fromstring(search_response.content)
            pmids = [id_elem.text for id_elem in root.findall('.//Id')]
            
            if not pmids:
                return []
            
            # Step 2: Fetch paper details
            fetch_url = f"{base_url}efetch.fcgi"
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'xml'
            }
            
            fetch_response = requests.get(fetch_url, params=fetch_params)
            fetch_response.raise_for_status()
            
            return self._parse_pubmed_results(fetch_response.content)
            
        except requests.RequestException as e:
            print(f"Error searching PubMed: {e}")
            return []
    
    def _parse_pubmed_results(self, xml_content: bytes) -> List[Dict]:
        """Parse PubMed XML results into structured data."""
        papers = []
        root = ET.fromstring(xml_content)
        
        for article in root.findall('.//PubmedArticle'):
            try:
                # Extract basic information
                title_elem = article.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else "No title"
                
                abstract_elem = article.find('.//AbstractText')
                abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
                
                # Extract publication date
                pub_date = article.find('.//PubDate')
                year = pub_date.find('Year')
                year = year.text if year is not None else "Unknown"
                
                # Extract authors
                authors = []
                for author in article.findall('.//Author'):
                    lastname = author.find('LastName')
                    forename = author.find('ForeName')
                    if lastname is not None and forename is not None:
                        authors.append(f"{forename.text} {lastname.text}")
                
                # Extract journal
                journal_elem = article.find('.//Journal/Title')
                journal = journal_elem.text if journal_elem is not None else "Unknown Journal"
                
                # Extract PMID
                pmid_elem = article.find('.//PMID')
                pmid = pmid_elem.text if pmid_elem is not None else "Unknown"
                
                papers.append({
                    'title': title,
                    'abstract': abstract,
                    'authors': authors,
                    'journal': journal,
                    'year': year,
                    'pmid': pmid,
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                })
                
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        
        return papers
    
    def search_arxiv(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search arXiv for research papers.
        """
        base_url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': query,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            return self._parse_arxiv_results(response.content)
            
        except requests.RequestException as e:
            print(f"Error searching arXiv: {e}")
            return []
    
    def _parse_arxiv_results(self, xml_content: bytes) -> List[Dict]:
        """Parse arXiv XML results into structured data."""
        papers = []
        root = ET.fromstring(xml_content)
        
        # Register namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns):
            try:
                title = entry.find('atom:title', ns).text.strip()
                summary = entry.find('atom:summary', ns).text.strip()
                
                # Extract authors
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns)
                    if name is not None:
                        authors.append(name.text)
                
                # Extract publication date
                published = entry.find('atom:published', ns).text
                year = published.split('-')[0] if published else "Unknown"
                
                # Extract arXiv ID and URL
                arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
                url = entry.find('atom:id', ns).text
                
                papers.append({
                    'title': title,
                    'abstract': summary,
                    'authors': authors,
                    'journal': 'arXiv',
                    'year': year,
                    'arxiv_id': arxiv_id,
                    'url': url
                })
                
            except Exception as e:
                print(f"Error parsing arXiv entry: {e}")
                continue
        
        return papers
    
    def categorize_paper(self, paper: Dict) -> List[str]:
        """Categorize a paper based on its title and abstract."""
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
        categories = []
        
        for category, info in self.data['categories'].items():
            keywords = info.get('keywords', [])
            if any(keyword.lower() in text for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ['other']
    
    def analyze_models(self, paper: Dict) -> List[str]:
        """Extract deep learning model mentions from paper."""
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
        models_found = []
        
        model_keywords = {
            'transformer': ['transformer', 'attention mechanism', 'bert', 'gpt'],
            'cnn': ['convolutional neural network', 'cnn', 'convolution'],
            'rnn': ['recurrent neural network', 'rnn', 'lstm', 'gru'],
            'gnn': ['graph neural network', 'gnn', 'graph convolution'],
            'gan': ['generative adversarial network', 'gan'],
            'diffusion': ['diffusion model', 'ddpm', 'score-based'],
            'vit': ['vision transformer', 'vit'],
            'multimodal': ['multimodal', 'multi-modal', 'cross-modal']
        }
        
        for model_type, keywords in model_keywords.items():
            if any(keyword in text for keyword in keywords):
                models_found.append(model_type)
        
        return models_found
    
    def run_research_cycle(self):
        """Run a complete research cycle."""
        print(f"Starting research cycle at {datetime.now()}")
        
        # Define search queries for different aspects of neurology + deep learning
        queries = [
            "deep learning neurosurgery brain implant",
            "neural network brain computer interface",
            "machine learning neuroimaging MRI fMRI",
            "artificial intelligence neuromodulation DBS",
            "deep learning epilepsy seizure detection",
            "graph neural network brain connectivity",
            "transformer neural signal processing",
            "CNN neurological diagnosis"
        ]
        
        all_papers = []
        
        # Search PubMed
        for query in queries:
            print(f"Searching PubMed for: {query}")
            papers = self.search_pubmed(query, max_results=5)
            all_papers.extend(papers)
            time.sleep(1)  # Be respectful to the API
        
        # Search arXiv
        arxiv_queries = [
            "deep learning neurology",
            "neural network brain",
            "machine learning neuroimaging"
        ]
        
        for query in arxiv_queries:
            print(f"Searching arXiv for: {query}")
            papers = self.search_arxiv(query, max_results=3)
            all_papers.extend(papers)
            time.sleep(1)
        
        # Remove duplicates based on title
        unique_papers = []
        seen_titles = set()
        for paper in all_papers:
            title = paper.get('title', '').lower().strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_papers.append(paper)
        
        print(f"Found {len(unique_papers)} unique papers")
        
        # Process papers
        processed_papers = []
        for paper in unique_papers:
            categories = self.categorize_paper(paper)
            models = self.analyze_models(paper)
            
            processed_paper = {
                **paper,
                'categories': categories,
                'models_mentioned': models,
                'processed_date': datetime.now().isoformat()
            }
            processed_papers.append(processed_paper)
        
        # Create research cycle entry
        cycle_id = f"2025-week-{datetime.now().isocalendar()[1]}"
        cycle_data = {
            'cycle_id': cycle_id,
            'date_range': f"{datetime.now().strftime('%B %d')} - {(datetime.now() + timedelta(days=6)).strftime('%B %d, %Y')}",
            'papers_analyzed': len(processed_papers),
            'findings': processed_papers,
            'summary': self._generate_summary(processed_papers),
            'status': 'completed',
            'completion_date': datetime.now().isoformat()
        }
        
        # Update data structure
        self.data['research_cycles'].append(cycle_data)
        self.data['last_updated'] = datetime.now().isoformat()
        self.data['metrics']['total_papers_reviewed'] += len(processed_papers)
        
        # Save data
        self.save_data()
        
        print(f"Research cycle completed. Analyzed {len(processed_papers)} papers.")
        return cycle_data
    
    def _generate_summary(self, papers: List[Dict]) -> str:
        """Generate a summary of the research cycle findings."""
        if not papers:
            return "No papers found in this research cycle."
        
        # Count categories and models
        category_counts = {}
        model_counts = {}
        
        for paper in papers:
            for category in paper.get('categories', []):
                category_counts[category] = category_counts.get(category, 0) + 1
            for model in paper.get('models_mentioned', []):
                model_counts[model] = model_counts.get(model, 0) + 1
        
        summary_parts = [
            f"Analyzed {len(papers)} papers this week.",
            f"Top research areas: {', '.join(sorted(category_counts.keys(), key=category_counts.get, reverse=True)[:3])}",
            f"Most mentioned models: {', '.join(sorted(model_counts.keys(), key=model_counts.get, reverse=True)[:3])}"
        ]
        
        return " ".join(summary_parts)

def main():
    """Main function to run the research agent."""
    agent = NeuroResearchAgent()
    
    print("=== Deep Learning Neurology Research Agent ===")
    print("Starting automated research cycle...")
    
    try:
        cycle_data = agent.run_research_cycle()
        print(f"\\nResearch Summary:")
        print(f"- {cycle_data['summary']}")
        print(f"- Completion time: {cycle_data['completion_date']}")
        
    except Exception as e:
        print(f"Error during research cycle: {e}")

if __name__ == "__main__":
    main()