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
        """Generate HTML content for the latest research cycle."""
        if not self.data.get('research_cycles'):
            return "<p>No research data available yet.</p>"
        
        latest_cycle = self.data['research_cycles'][-1]
        
        # Generate summary statistics
        total_papers = self.data['metrics'].get('total_papers_reviewed', 0)
        last_updated = datetime.fromisoformat(self.data['last_updated'].replace('Z', '+00:00'))
        
        html_content = f"""
        <div class="research-summary bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg mb-6">
            <h4 class="text-xl font-semibold text-gray-900 mb-3">Latest Research Update</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div class="text-center">
                    <div class="text-2xl font-bold text-blue-600">{latest_cycle.get('papers_analyzed', 0)}</div>
                    <div class="text-sm text-gray-600">Papers This Week</div>
                </div>
                <div class="text-center">
                    <div class="text-2xl font-bold text-purple-600">{total_papers}</div>
                    <div class="text-sm text-gray-600">Total Papers Reviewed</div>
                </div>
                <div class="text-center">
                    <div class="text-2xl font-bold text-green-600">{len(self.data.get('categories', {}))}</div>
                    <div class="text-sm text-gray-600">Research Areas</div>
                </div>
            </div>
            <p class="text-gray-700 mb-2"><strong>Week:</strong> {latest_cycle.get('date_range', 'Unknown')}</p>
            <p class="text-gray-700 mb-4">{latest_cycle.get('summary', 'No summary available.')}</p>
            <div class="text-xs text-gray-500">Last updated: {last_updated.strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        """
        
        return html_content
    
    def generate_recent_papers_html(self, limit: int = 5) -> str:
        """Generate HTML for recent papers."""
        if not self.data.get('research_cycles'):
            return ""
        
        latest_cycle = self.data['research_cycles'][-1]
        papers = latest_cycle.get('findings', [])[:limit]
        
        if not papers:
            return "<p>No recent papers available.</p>"
        
        html_content = """
        <div class="recent-papers">
            <h4 class="text-xl font-semibold text-gray-900 mb-4">Recent Research Papers</h4>
            <div class="space-y-3">
        """
        
        for paper in papers:
            title = paper.get('title', 'Untitled')
            authors = ', '.join(paper.get('authors', [])[:3])
            if len(paper.get('authors', [])) > 3:
                authors += " et al."
            journal = paper.get('journal', 'Unknown Journal')
            year = paper.get('year', 'Unknown')
            url = paper.get('url', '#')
            categories = ', '.join(paper.get('categories', []))
            models = ', '.join(paper.get('models_mentioned', []))
            
            html_content += f"""
                <div class="paper-item bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                    <h5 class="font-semibold text-gray-900 mb-2">
                        <a href="{url}" target="_blank" class="text-blue-600 hover:text-blue-800">{title}</a>
                    </h5>
                    <p class="text-sm text-gray-600 mb-2">{authors} • {journal} ({year})</p>
                    {f'<div class="text-xs text-purple-600 mb-1"><strong>Categories:</strong> {categories}</div>' if categories else ''}
                    {f'<div class="text-xs text-green-600"><strong>Models:</strong> {models}</div>' if models else ''}
                </div>
            """
        
        html_content += """
            </div>
        </div>
        """
        
        return html_content
    
    def update_deep_learning_section(self):
        """Update the Deep Learning in Neuroscience section with latest research."""
        html_content = self.load_html()
        
        # Generate new content
        research_summary = self.generate_research_summary_html()
        recent_papers = self.generate_recent_papers_html()
        
        # Create updated content for the Deep Learning modal
        new_modal_content = f"""<h3 class='text-2xl font-semibold text-gray-900 mb-4'>AI-Powered Brain Research</h3>
        <p class='text-gray-700 leading-relaxed mb-6'>Deep Learning is revolutionizing neuroscience by analyzing complex brain data, improving surgical precision, and enabling breakthrough discoveries in neural interfaces and brain connectivity analysis.</p>
        
        {research_summary}
        
        {recent_papers}
        
        <div class="mt-6 p-4 bg-gray-50 rounded-lg">
            <p class='text-sm text-gray-600'><strong>Key Technologies:</strong> Graph Neural Networks for brain connectivity, Transformers for neural signal processing, CNNs for neuroimaging analysis, and multimodal AI for comprehensive brain understanding.</p>
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