#!/usr/bin/env python3
"""
Web Updater for Deep Learning Neurology Research
Updates the HTML website with latest research findings.
"""

import json
import re
from datetime import datetime
from typing import Dict, List

class WebUpdater:
    def __init__(self, data_file: str = "research_data.json", html_file: str = "index.html"):
        self.data_file = data_file
        self.html_file = html_file
        self.load_data()
    
    def load_data(self):
        """Load research data from JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Data file {self.data_file} not found.")
            self.data = {}
    
    def load_html(self) -> str:
        """Load HTML content from file."""
        with open(self.html_file, 'r') as f:
            return f.read()
    
    def save_html(self, content: str):
        """Save updated HTML content to file."""
        with open(self.html_file, 'w') as f:
            f.write(content)
    
    def generate_research_summary_html(self) -> str:
        """Generate minimal research summary for home page."""
        return ""  # Return empty string - no summary on home page
    
    def generate_recent_papers_html(self, limit: int = 5) -> str:
        """Generate minimal content for home page."""
        return ""  # Return empty string - no recent papers on home page
    
    def update_deep_learning_section(self):
        """Update the Deep Learning in Neuroscience section with latest research."""
        html_content = self.load_html()
        
        # Get latest cycle data
        latest_cycle = self.data['research_cycles'][-1] if self.data.get('research_cycles') else {}
        total_papers = self.data['metrics'].get('total_papers_reviewed', 0)
        
        # Generate new content
        research_summary = self.generate_research_summary_html()
        recent_papers = self.generate_recent_papers_html()
        
        # Create clean card-only design for Deep Learning modal (following previous context)
        new_modal_content = f"""
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- GNN Card -->
            <div class="bg-gradient-to-br from-blue-500 to-indigo-600 text-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 cursor-pointer" onclick="showFeynmanExplanation('gnn')">
                <div class="text-center">
                    <div class="text-3xl mb-3">🌐</div>
                    <div class="font-bold text-lg mb-2">Graph Neural Networks</div>
                    <div class="text-sm opacity-90 mb-3">Brain connectivity mapping</div>
                    <div class="text-xs opacity-75">🧠 Tap for Feynman explanation</div>
                </div>
            </div>
            
            <!-- Transformers Card -->
            <div class="bg-gradient-to-br from-purple-500 to-pink-600 text-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 cursor-pointer" onclick="showFeynmanExplanation('transformers')">
                <div class="text-center">
                    <div class="text-3xl mb-3">🎯</div>
                    <div class="font-bold text-lg mb-2">Transformers</div>
                    <div class="text-sm opacity-90 mb-3">Neural signal processing</div>
                    <div class="text-xs opacity-75">🧠 Tap for Feynman explanation</div>
                </div>
            </div>
            
            <!-- CNNs Card -->
            <div class="bg-gradient-to-br from-green-500 to-emerald-600 text-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 cursor-pointer" onclick="showFeynmanExplanation('cnns')">
                <div class="text-center">
                    <div class="text-3xl mb-3">👁️</div>
                    <div class="font-bold text-lg mb-2">CNNs</div>
                    <div class="text-sm opacity-90 mb-3">Neuroimaging analysis</div>
                    <div class="text-xs opacity-75">🧠 Tap for Feynman explanation</div>
                </div>
            </div>
            
            <!-- Multimodal AI Card -->
            <div class="bg-gradient-to-br from-orange-500 to-red-600 text-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 cursor-pointer" onclick="showFeynmanExplanation('multimodal')">
                <div class="text-center">
                    <div class="text-3xl mb-3">🔗</div>
                    <div class="font-bold text-lg mb-2">Multimodal AI</div>
                    <div class="text-sm opacity-90 mb-3">Comprehensive analysis</div>
                    <div class="text-xs opacity-75">🧠 Tap for Feynman explanation</div>
                </div>
            </div>
            
            <!-- Research Papers Card -->
            <div class="sm:col-span-2">
                <a href="research.html" class="block bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div class="text-center">
                        <div class="text-3xl mb-3">📄</div>
                        <div class="font-bold text-lg mb-2">Explore Research Papers</div>
                        <div class="text-sm opacity-90">View {latest_cycle.get('papers_analyzed', 0)} papers with detailed analysis</div>
                    </div>
                </a>
            </div>
        </div>"""
        
        # Find and update the Deep Learning section
        pattern = r'(data-title="Deep Learning in Neuroscience" data-content=")(.*?)(")'
        
        # Escape the content properly for HTML attribute
        escaped_content = new_modal_content.replace("\\", "\\\\").replace('"', '\\"')
        replacement = f'\\1{escaped_content}\\3'
        
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # Save updated HTML
        self.save_html(updated_html)
        print("Successfully updated the Deep Learning in Neuroscience section.")
    
    def add_research_status_indicator(self):
        """Add a status indicator showing when research was last updated."""
        html_content = self.load_html()
        
        if not self.data.get('last_updated'):
            return
        
        last_updated = datetime.fromisoformat(self.data['last_updated'].replace('Z', '+00:00'))
        
        # Create status indicator HTML
        status_html = f"""
        <!-- Research Status Indicator -->
        <div class="fixed bottom-4 right-4 bg-white rounded-lg shadow-lg p-3 border border-gray-200 z-50">
            <div class="flex items-center space-x-2">
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <div class="text-xs text-gray-600">
                    <div class="font-semibold">Research Updated</div>
                    <div>{last_updated.strftime('%b %d, %Y')}</div>
                </div>
            </div>
        </div>
        """
        
        # Insert before closing body tag
        updated_html = html_content.replace('</body>', f'{status_html}</body>')
        
        self.save_html(updated_html)
        print("Added research status indicator.")
    
    def update_website(self):
        """Perform complete website update with latest research data."""
        print("Updating website with latest research data...")
        
        try:
            self.update_deep_learning_section()
            self.add_research_status_indicator()
            print("Website update completed successfully!")
            
        except Exception as e:
            print(f"Error updating website: {e}")

def main():
    """Main function to update the website."""
    updater = WebUpdater()
    updater.update_website()

if __name__ == "__main__":
    main()