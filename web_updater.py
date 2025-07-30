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
        
        # Create comprehensive Deep Learning content with detailed explanations
        new_modal_content = f"""
        <div class="max-h-96 overflow-y-auto">
            <h3 class="text-2xl font-bold text-center text-gray-900 mb-6">🧠 Deep Learning in Neuroscience</h3>
            
            <!-- Quick Stats -->
            <div class="grid grid-cols-3 gap-4 mb-6">
                <div class="bg-gradient-to-br from-blue-500 to-purple-600 text-white p-4 rounded-xl text-center">
                    <div class="text-2xl font-bold">{latest_cycle.get('papers_analyzed', 0)}</div>
                    <div class="text-xs opacity-90">Papers This Week</div>
                </div>
                <div class="bg-gradient-to-br from-green-500 to-emerald-600 text-white p-4 rounded-xl text-center">
                    <div class="text-2xl font-bold">{len(self.data.get('categories', {}))}</div>
                    <div class="text-xs opacity-90">Research Areas</div>
                </div>
                <div class="bg-gradient-to-br from-orange-500 to-red-600 text-white p-4 rounded-xl text-center">
                    <div class="text-2xl font-bold">4</div>
                    <div class="text-xs opacity-90">AI Models</div>
                </div>
            </div>
            
            <!-- Deep Learning Models Section -->
            <div class="space-y-6">
                
                <!-- Graph Neural Networks -->
                <div class="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border border-blue-100">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <span class="text-2xl mr-3">🌐</span>
                            <h4 class="text-lg font-bold text-blue-900">Graph Neural Networks (GNNs)</h4>
                        </div>
                        <button onclick="showFeynmanExplanation('gnn')" class="bg-gradient-to-r from-pink-400 to-red-400 text-white px-3 py-1 rounded-full text-sm font-semibold hover:scale-105 transition-transform">
                            🧠 Explain as Feynman
                        </button>
                    </div>
                    <p class="text-sm text-blue-800 mb-3">Revolutionary AI for understanding brain connectivity networks and neural pathways.</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-blue-900">Applications:</strong><br>
                            • Brain connectivity mapping<br>
                            • Neural pathway analysis<br>
                            • Disease progression modeling
                        </div>
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-blue-900">Key Benefits:</strong><br>
                            • Captures complex relationships<br>
                            • Handles irregular brain structures<br>
                            • Predicts neurological conditions
                        </div>
                    </div>
                </div>
                
                <!-- Transformers -->
                <div class="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border border-purple-100">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <span class="text-2xl mr-3">🎯</span>
                            <h4 class="text-lg font-bold text-purple-900">Transformers</h4>
                        </div>
                        <button onclick="showFeynmanExplanation('transformers')" class="bg-gradient-to-r from-pink-400 to-red-400 text-white px-3 py-1 rounded-full text-sm font-semibold hover:scale-105 transition-transform">
                            🧠 Explain as Feynman
                        </button>
                    </div>
                    <p class="text-sm text-purple-800 mb-3">Attention-based models that focus on the most important parts of neural signals.</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-purple-900">Applications:</strong><br>
                            • EEG signal analysis<br>
                            • Neural spike prediction<br>
                            • Brain-computer interfaces
                        </div>
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-purple-900">Key Benefits:</strong><br>
                            • Selective attention mechanism<br>
                            • Long-range dependencies<br>
                            • Real-time processing
                        </div>
                    </div>
                </div>
                
                <!-- CNNs -->
                <div class="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl border border-green-100">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <span class="text-2xl mr-3">👁️</span>
                            <h4 class="text-lg font-bold text-green-900">Convolutional Neural Networks (CNNs)</h4>
                        </div>
                        <button onclick="showFeynmanExplanation('cnns')" class="bg-gradient-to-r from-pink-400 to-red-400 text-white px-3 py-1 rounded-full text-sm font-semibold hover:scale-105 transition-transform">
                            🧠 Explain as Feynman
                        </button>
                    </div>
                    <p class="text-sm text-green-800 mb-3">Specialized networks for analyzing brain images and detecting patterns.</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-green-900">Applications:</strong><br>
                            • MRI/fMRI analysis<br>
                            • Tumor detection<br>
                            • Brain segmentation
                        </div>
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-green-900">Key Benefits:</strong><br>
                            • Pattern recognition<br>
                            • Spatial feature extraction<br>
                            • Medical imaging expertise
                        </div>
                    </div>
                </div>
                
                <!-- Multimodal AI -->
                <div class="bg-gradient-to-r from-orange-50 to-red-50 p-6 rounded-xl border border-orange-100">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <span class="text-2xl mr-3">🔗</span>
                            <h4 class="text-lg font-bold text-orange-900">Multimodal AI</h4>
                        </div>
                        <button onclick="showFeynmanExplanation('multimodal')" class="bg-gradient-to-r from-pink-400 to-red-400 text-white px-3 py-1 rounded-full text-sm font-semibold hover:scale-105 transition-transform">
                            🧠 Explain as Feynman
                        </button>
                    </div>
                    <p class="text-sm text-orange-800 mb-3">Integrated AI systems that combine multiple types of brain data.</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-orange-900">Applications:</strong><br>
                            • Combining MRI + EEG data<br>
                            • Comprehensive diagnosis<br>
                            • Holistic brain understanding
                        </div>
                        <div class="bg-white p-3 rounded-lg">
                            <strong class="text-orange-900">Key Benefits:</strong><br>
                            • Complete picture analysis<br>
                            • Better accuracy<br>
                            • Cross-validation of findings
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Action Button -->
            <div class="text-center mt-6">
                <a href="research.html" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg">
                    📄 Explore Detailed Research Papers
                    <svg class="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
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