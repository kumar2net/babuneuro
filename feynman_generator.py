#!/usr/bin/env python3
"""
Feynman Explanation Generator
Generates simple, intuitive explanations for complex deep learning research papers.
"""

import json
import re
from typing import Dict, List

class FeynmanExplainer:
    def __init__(self):
        self.analogies = {
            'neural_implants': {
                'simple': "Like building a tiny translator between your brain and computers",
                'explanation': "Imagine your brain speaks one language and computers speak another. Neural implants are like having a super-smart translator that helps them understand each other. This lets paralyzed people control robot arms with just their thoughts!",
                'importance': "This could help millions of people with disabilities regain control over their environment."
            },
            'surgical_ai': {
                'simple': "Like giving surgeons superhuman eyes and steady hands",
                'explanation': "Think of AI as a GPS system for surgery. Just like GPS helps you navigate roads, surgical AI helps doctors navigate the delicate pathways in your brain without getting lost or making wrong turns.",
                'importance': "Surgeries become much safer with fewer complications and better outcomes."
            },
            'neuroimaging': {
                'simple': "Like teaching computers to be brain detectives",
                'explanation': "Brain scans are like mystery photos, and AI learns to spot clues that human doctors might miss. It's like having a super-detective that can see patterns invisible to the naked eye.",
                'importance': "Diseases can be caught much earlier, sometimes years before symptoms appear."
            },
            'neuromodulation': {
                'simple': "Like having a smart thermostat for your brain",
                'explanation': "Your brain runs on electricity, just like your house. Sometimes the 'wiring' doesn't work perfectly. Neuromodulation is like installing a smart system that adjusts the electrical signals to fix problems like depression or Parkinson's.",
                'importance': "People with brain disorders can get personalized treatments that work better than one-size-fits-all approaches."
            },
            'diagnosis_prediction': {
                'simple': "Like having a weather forecast for your brain health",
                'explanation': "Just like meteorologists predict storms by looking at weather patterns, AI can predict brain diseases by looking at subtle patterns in brain data that humans can't see.",
                'importance': "Early warning gives people time to prevent or prepare for neurological conditions."
            },
            'brain_connectivity': {
                'simple': "Like mapping the social network inside your head",
                'explanation': "Your brain has billions of neurons that need to communicate, like people in a giant social network. AI helps us understand who talks to whom and how these conversations affect your thoughts and behavior.",
                'importance': "Understanding brain networks could unlock secrets of consciousness and treat mental health conditions."
            }
        }
        
        self.model_explanations = {
            'transformer': "AI that pays attention to the most important parts of data, like a smart student who knows what to focus on during a lecture",
            'cnn': "AI that recognizes patterns in images, similar to how your eyes automatically recognize faces in a crowd",
            'gnn': "AI that understands connections and relationships, like mapping friendships in a social network",
            'rnn': "AI that remembers what happened before to understand what's happening now, like following a conversation",
            'gan': "Two AIs that compete against each other to create realistic fake data, like an art forger vs. an art detective",
            'vit': "AI that breaks images into small pieces and understands how they relate, like solving a jigsaw puzzle",
            'multimodal': "AI that can understand different types of information at once, like reading text while looking at pictures"
        }
    
    def generate_explanation(self, paper: Dict) -> Dict:
        """Generate a Feynman-style explanation for a research paper."""
        categories = paper.get('categories', [])
        models = paper.get('models_mentioned', [])
        title = paper.get('title', 'Research Paper')
        
        # Get primary category
        primary_category = categories[0] if categories else 'other'
        
        # Generate explanation sections
        explanation = {
            'title': title,
            'what_is_it': self._explain_what_it_is(primary_category, categories),
            'how_it_works': self._explain_how_it_works(models),
            'why_important': self._explain_importance(primary_category, categories),
            'future_impact': self._explain_future_impact(categories),
            'simple_analogy': self._get_simple_analogy(primary_category)
        }
        
        return explanation
    
    def _explain_what_it_is(self, primary_category: str, categories: List[str]) -> str:
        """Explain what the research is about in simple terms."""
        if primary_category in self.analogies:
            return self.analogies[primary_category]['explanation']
        
        # Fallback explanation
        areas = [cat.replace('_', ' ') for cat in categories]
        return f"This research focuses on {', '.join(areas)} using artificial intelligence to solve complex brain-related problems."
    
    def _explain_how_it_works(self, models: List[str]) -> str:
        """Explain how the AI models work in simple terms."""
        if not models:
            return "The researchers use artificial intelligence to find patterns in brain data that humans might miss."
        
        explanations = []
        for model in models[:2]:  # Limit to first 2 models to keep it simple
            if model in self.model_explanations:
                explanations.append(self.model_explanations[model])
        
        if explanations:
            return "The researchers use " + " and ".join(explanations) + "."
        else:
            return "The researchers use advanced AI techniques to analyze complex brain data and find hidden patterns."
    
    def _explain_importance(self, primary_category: str, categories: List[str]) -> str:
        """Explain why this research matters."""
        if primary_category in self.analogies:
            return self.analogies[primary_category]['importance']
        
        return "This research could lead to better treatments and understanding of brain-related conditions."
    
    def _explain_future_impact(self, categories: List[str]) -> str:
        """Explain potential future applications."""
        impact_map = {
            'neural_implants': "thought-controlled prosthetics and direct brain-computer communication",
            'surgical_ai': "robot-assisted surgeries that are safer than human hands alone",
            'neuroimaging': "brain scans that predict diseases years before symptoms appear",
            'neuromodulation': "personalized brain treatments for mental health and neurological disorders",
            'diagnosis_prediction': "early warning systems for brain diseases",
            'brain_connectivity': "understanding consciousness and treating psychiatric disorders"
        }
        
        impacts = []
        for category in categories:
            if category in impact_map:
                impacts.append(impact_map[category])
        
        if impacts:
            return f"In the future, this could lead to {', '.join(impacts[:2])}."
        else:
            return "This research could lead to breakthrough treatments and technologies for brain health."
    
    def _get_simple_analogy(self, primary_category: str) -> str:
        """Get a simple one-line analogy."""
        if primary_category in self.analogies:
            return self.analogies[primary_category]['simple']
        
        return "Like using artificial intelligence to understand how the brain works"
    
    def generate_batch_explanations(self, papers: List[Dict]) -> Dict:
        """Generate explanations for multiple papers."""
        explanations = {}
        
        for i, paper in enumerate(papers):
            paper_id = paper.get('pmid') or paper.get('arxiv_id') or f"paper_{i}"
            explanations[paper_id] = self.generate_explanation(paper)
        
        return explanations
    
    def create_explanation_database(self, research_data_file: str = "research_data.json", 
                                  output_file: str = "feynman_explanations.json"):
        """Create a database of Feynman explanations for all papers."""
        try:
            with open(research_data_file, 'r') as f:
                data = json.load(f)
            
            all_papers = []
            for cycle in data.get('research_cycles', []):
                all_papers.extend(cycle.get('findings', []))
            
            explanations = self.generate_batch_explanations(all_papers)
            
            # Save explanations
            explanation_db = {
                'generated_at': data.get('last_updated'),
                'total_papers': len(all_papers),
                'explanations': explanations
            }
            
            with open(output_file, 'w') as f:
                json.dump(explanation_db, f, indent=2)
            
            print(f"Generated Feynman explanations for {len(all_papers)} papers")
            print(f"Saved to: {output_file}")
            
            return explanation_db
            
        except Exception as e:
            print(f"Error creating explanation database: {e}")
            return None

def main():
    """Main function to generate explanations."""
    explainer = FeynmanExplainer()
    
    print("=== Feynman Explanation Generator ===")
    print("Generating simple explanations for complex research...")
    
    # Create explanation database
    explainer.create_explanation_database()

if __name__ == "__main__":
    main()