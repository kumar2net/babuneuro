#!/usr/bin/env python3
"""
Weekly Research Scheduler
Automated scheduler for running research cycles and updating the website.
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
from research_agent import NeuroResearchAgent
from web_updater import WebUpdater

class ResearchScheduler:
    def __init__(self):
        self.agent = NeuroResearchAgent()
        self.updater = WebUpdater()
    
    def run_weekly_update(self):
        """Run the complete weekly research update process."""
        print(f"\\n{'='*50}")
        print(f"WEEKLY RESEARCH UPDATE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        
        try:
            # Step 1: Run research cycle
            print("\\n1. Running research cycle...")
            cycle_data = self.agent.run_research_cycle()
            
            # Step 2: Update website
            print("\\n2. Updating website...")
            self.updater.update_website()
            
            # Step 3: Generate summary report
            print("\\n3. Generating summary report...")
            self._generate_summary_report(cycle_data)
            
            print("\\n✅ Weekly update completed successfully!")
            
        except Exception as e:
            print(f"\\n❌ Error during weekly update: {e}")
            self._log_error(e)
    
    def _generate_summary_report(self, cycle_data):
        """Generate a summary report of the research cycle."""
        report = f"""
# Weekly Research Summary - {cycle_data['date_range']}

## Overview
- **Papers Analyzed:** {cycle_data['papers_analyzed']}
- **Research Areas Covered:** {len(set(cat for paper in cycle_data.get('findings', []) for cat in paper.get('categories', [])))}
- **Completion Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
{cycle_data.get('summary', 'No summary available.')}

## Top Research Areas
"""
        
        # Count categories
        category_counts = {}
        for paper in cycle_data.get('findings', []):
            for category in paper.get('categories', []):
                category_counts[category] = category_counts.get(category, 0) + 1
        
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{category.replace('_', ' ').title()}:** {count} papers\\n"
        
        report += f"""
## Model Architectures Mentioned
"""
        
        # Count models
        model_counts = {}
        for paper in cycle_data.get('findings', []):
            for model in paper.get('models_mentioned', []):
                model_counts[model] = model_counts.get(model, 0) + 1
        
        for model, count in sorted(model_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{model.upper()}:** {count} papers\\n"
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"reports/weekly_summary_{timestamp}.md"
        
        try:
            import os
            os.makedirs('reports', exist_ok=True)
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"Summary report saved to: {report_file}")
        except Exception as e:
            print(f"Could not save report: {e}")
    
    def _log_error(self, error):
        """Log errors to a file for debugging."""
        try:
            import os
            os.makedirs('logs', exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f"logs/error_{timestamp}.log"
            
            with open(log_file, 'w') as f:
                f.write(f"Error occurred at: {datetime.now()}\\n")
                f.write(f"Error: {str(error)}\\n")
                f.write(f"Type: {type(error).__name__}\\n")
            
            print(f"Error logged to: {log_file}")
        except Exception as e:
            print(f"Could not log error: {e}")
    
    def run_manual_update(self):
        """Run a manual update immediately."""
        print("Running manual research update...")
        self.run_weekly_update()
    
    def start_scheduler(self):
        """Start the automated weekly scheduler."""
        print("🤖 Deep Learning Neurology Research Scheduler Started")
        print("⏰ Scheduled to run every Monday at 9:00 AM")
        print("📊 Manual update available with 'python scheduler.py --manual'")
        print("🛑 Press Ctrl+C to stop\\n")
        
        # Schedule weekly updates every Monday at 9:00 AM
        schedule.every().monday.at("09:00").do(self.run_weekly_update)
        
        # Also schedule a mid-week check on Thursday at 2:00 PM
        schedule.every().thursday.at("14:00").do(self._mid_week_check)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\\n🛑 Scheduler stopped by user.")
    
    def _mid_week_check(self):
        """Perform a mid-week check for high-impact papers."""
        print(f"\\n📋 Mid-week check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run a lighter search for high-impact terms
        high_impact_queries = [
            "breakthrough neural implant",
            "novel brain computer interface",
            "revolutionary neurosurgery AI"
        ]
        
        papers_found = 0
        for query in high_impact_queries:
            papers = self.agent.search_pubmed(query, max_results=3)
            papers_found += len(papers)
            time.sleep(1)
        
        if papers_found > 5:  # If we find many new papers, trigger an update
            print(f"🔥 Found {papers_found} potentially important papers. Running update...")
            self.run_weekly_update()
        else:
            print(f"📊 Found {papers_found} papers. Waiting for Monday update.")

def main():
    """Main function with command line interface."""
    scheduler = ResearchScheduler()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--manual':
        # Run manual update
        scheduler.run_manual_update()
    elif len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test run with limited data
        print("🧪 Running test update...")
        scheduler.run_weekly_update()
    else:
        # Start automated scheduler
        scheduler.start_scheduler()

if __name__ == "__main__":
    main()