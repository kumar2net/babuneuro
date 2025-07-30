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
        """Generate HTML for recent papers as cards."""
        if not self.data.get('research_cycles'):
            return ""
        
        latest_cycle = self.data['research_cycles'][-1]
        papers = latest_cycle.get('findings', [])[:limit]
        
        if not papers:
            return "<p>No recent papers available.</p>"
        
        # Category info for icons and colors
        category_info = {
            'neural_implants': {'icon': '🧠', 'color': 'from-blue-400 to-blue-600'},
            'surgical_ai': {'icon': '🔬', 'color': 'from-purple-400 to-purple-600'},
            'neuroimaging': {'icon': '📊', 'color': 'from-green-400 to-green-600'},
            'neuromodulation': {'icon': '⚡', 'color': 'from-yellow-400 to-yellow-600'},
            'diagnosis_prediction': {'icon': '🔍', 'color': 'from-red-400 to-red-600'},
            'brain_connectivity': {'icon': '🌐', 'color': 'from-indigo-400 to-indigo-600'},
            'other': {'icon': '📄', 'color': 'from-gray-400 to-gray-600'}
        }
        
        html_content = """
        <div class="recent-papers">
            <h4 class="text-xl font-semibold text-gray-900 mb-6 text-center">📚 Recent Research Papers</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        """
        
        for paper in papers:
            title = paper.get('title', 'Untitled')
            authors = ', '.join(paper.get('authors', [])[:2])
            if len(paper.get('authors', [])) > 2:
                authors += " et al."
            journal = paper.get('journal', 'Unknown Journal')
            year = paper.get('year', 'Unknown')
            url = paper.get('url', '#')
            categories = paper.get('categories', [])
            models = paper.get('models_mentioned', [])
            
            # Get primary category for icon
            primary_category = categories[0] if categories else 'other'
            cat_info = category_info.get(primary_category, category_info['other'])
            
            # Truncate title for card display
            truncated_title = title if len(title) <= 70 else title[:70] + '...'
            
            html_content += f"""
                <div class="bg-white p-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100">
                    <div class="flex items-center justify-center w-12 h-12 bg-gradient-to-r {cat_info['color']} rounded-full mb-4 mx-auto">
                        <span class="text-white text-xl">{cat_info['icon']}</span>
                    </div>
                    <h5 class="font-semibold text-gray-900 mb-2 text-center leading-tight text-sm">
                        <a href="{url}" target="_blank" class="text-gray-900 hover:text-blue-600 transition-colors">{truncated_title}</a>
                    </h5>
                    <p class="text-xs text-gray-600 text-center mb-3">{authors}<br><span class="font-medium">{journal}</span> ({year})</p>
                    
                    {f'''
                    <div class="flex flex-wrap justify-center gap-1 mb-2">
                        {' '.join([f'<span class="px-2 py-1 bg-purple-50 text-purple-700 rounded-full text-xs">{cat.replace("_", " ")}</span>' for cat in categories[:2]])}
                        {f'<span class="text-xs text-gray-500">+{len(categories)-2}</span>' if len(categories) > 2 else ''}
                    </div>
                    ''' if categories else ''}
                    
                    {f'''
                    <div class="flex flex-wrap justify-center gap-1">
                        {' '.join([f'<span class="px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs">{model.upper()}</span>' for model in models[:2]])}
                        {f'<span class="text-xs text-gray-500">+{len(models)-2}</span>' if len(models) > 2 else ''}
                    </div>
                    ''' if models else ''}
                </div>
            """
        
        html_content += """
            </div>
            <div class="text-center">
                <a href="research.html" class="inline-flex items-center px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors text-sm font-medium">
                    View All Papers
                    <svg class="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </a>
            </div>
        </div>
        """
        
        return html_content
    
    def update_deep_learning_section(self):
        """Update the Deep Learning in Neuroscience section with latest research."""
        html_content = self.load_html()
        
        # Get latest cycle data
        latest_cycle = self.data['research_cycles'][-1] if self.data.get('research_cycles') else {}
        total_papers = self.data['metrics'].get('total_papers_reviewed', 0)
        
        # Generate new content
        research_summary = self.generate_research_summary_html()
        recent_papers = self.generate_recent_papers_html()
        
        # Create updated content for the Deep Learning modal with clean card design
        new_modal_content = f"""<h3 class='text-2xl font-semibold text-gray-900 mb-4 text-center'>🧠 AI-Powered Brain Research</h3>
        <p class='text-gray-700 leading-relaxed mb-6 text-center'>Deep Learning is revolutionizing neuroscience by analyzing complex brain data, improving surgical precision, and enabling breakthrough discoveries in neural interfaces and brain connectivity analysis.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            <!-- Research Stats Card -->
            <div class="bg-gradient-to-br from-blue-500 to-purple-600 text-white p-4 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-2xl font-bold">{latest_cycle.get('papers_analyzed', 0)}</div>
                    <div class="text-sm opacity-90">Papers This Week</div>
                </div>
            </div>
            
            <!-- Total Papers Card -->
            <div class="bg-gradient-to-br from-green-500 to-emerald-600 text-white p-4 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-2xl font-bold">{total_papers}</div>
                    <div class="text-sm opacity-90">Total Papers</div>
                </div>
            </div>
            
            <!-- Research Areas Card -->
            <div class="bg-gradient-to-br from-orange-500 to-red-600 text-white p-4 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-2xl font-bold">{len(self.data.get('categories', {}))}</div>
                    <div class="text-sm opacity-90">Research Areas</div>
                </div>
            </div>
        </div>
        
        <div class="mb-6">
            <h4 class="text-lg font-semibold text-gray-900 mb-4 text-center">🔑 Key Technologies</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div class="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-100 hover:shadow-md transition-shadow">
                    <div class="flex items-center mb-2">
                        <span class="text-xl mr-3">🌐</span>
                        <h5 class="font-semibold text-blue-900">Graph Neural Networks</h5>
                    </div>
                    <p class="text-sm text-blue-800">Advanced AI for mapping brain connectivity and neural pathways</p>
                </div>
                <div class="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-100 hover:shadow-md transition-shadow">
                    <div class="flex items-center mb-2">
                        <span class="text-xl mr-3">🎯</span>
                        <h5 class="font-semibold text-purple-900">Transformers</h5>
                    </div>
                    <p class="text-sm text-purple-800">Attention-based models for neural signal processing</p>
                </div>
                <div class="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-xl border border-green-100 hover:shadow-md transition-shadow">
                    <div class="flex items-center mb-2">
                        <span class="text-xl mr-3">👁️</span>
                        <h5 class="font-semibold text-green-900">CNNs</h5>
                    </div>
                    <p class="text-sm text-green-800">Convolutional networks for neuroimaging analysis</p>
                </div>
                <div class="bg-gradient-to-r from-orange-50 to-red-50 p-4 rounded-xl border border-orange-100 hover:shadow-md transition-shadow">
                    <div class="flex items-center mb-2">
                        <span class="text-xl mr-3">🔗</span>
                        <h5 class="font-semibold text-orange-900">Multimodal AI</h5>
                    </div>
                    <p class="text-sm text-orange-800">Integrated AI for comprehensive brain understanding</p>
                </div>
            </div>
        </div>
        
        <div class="text-center">
            <a href="research.html" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg">
                📄 Explore All Research Papers
                <svg class="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
            </a>
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