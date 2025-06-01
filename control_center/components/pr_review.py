"""
PR Review Panel - Review and manage pull requests from agents
"""

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, Button, Label, TextArea
from textual.screen import ModalScreen


@dataclass
class PullRequest:
    """Container for PR information."""
    number: int
    title: str
    author: str
    branch: str
    description: str
    files_changed: List[str]
    created_at: str
    
    @classmethod
    def from_file(cls, filepath: Path) -> Optional['PullRequest']:
        """Load PR from .pr_info.json file."""
        try:
            with open(filepath) as f:
                data = json.load(f)
                return cls(**data)
        except Exception:
            return None


class DiffViewerDialog(ModalScreen):
    """Modal dialog for viewing PR diff."""
    
    def __init__(self, pr: PullRequest, **kwargs):
        super().__init__(**kwargs)
        self.pr = pr
        
    def compose(self) -> ComposeResult:
        """Create the dialog layout."""
        with Vertical(classes="modal-dialog"):
            yield Label(f"PR #{self.pr.number} Diff", classes="panel-title")
            
            # Get diff
            diff_text = self.get_diff()
            
            # Show diff in text area
            diff_area = TextArea(diff_text, language="diff", read_only=True)
            diff_area.styles.height = "80%"
            yield diff_area
            
            yield Button("Close", id="close")
            
    def get_diff(self) -> str:
        """Get git diff for the PR."""
        try:
            result = subprocess.run(
                ['git', 'diff', f'main...{self.pr.branch}'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout or "No changes found"
        except Exception as e:
            return f"Error getting diff: {e}"
            
    @on(Button.Pressed, "#close")
    def handle_close(self):
        """Handle close button."""
        self.dismiss()


class PRReviewPanel(Widget):
    """Panel for reviewing pull requests."""
    
    current_pr: reactive[Optional[PullRequest]] = reactive(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pr_files: List[Path] = []
        
    def compose(self) -> ComposeResult:
        """Create the panel layout."""
        with Vertical():
            yield Label("🔍 PR Review", classes="panel-title")
            
            # PR info container
            self.pr_info = Vertical(classes="pr-info")
            yield self.pr_info
            
            # Control buttons
            with Horizontal():
                yield Button("View Diff", id="view-diff", classes="primary-button")
                yield Button("Approve", id="approve", classes="success-button")
                yield Button("Request Changes", id="request-changes", classes="danger-button")
                yield Button("Scan for PRs", id="scan-prs")
                
    async def on_mount(self) -> None:
        """Initialize when panel mounts."""
        # Scan for existing PRs
        await self.scan_for_prs()
        
        # If no PRs, show demo
        if not self.current_pr:
            self.show_demo_pr()
            
    async def scan_for_prs(self):
        """Scan for PR info files."""
        self.pr_files = list(Path(".").glob(".pr_info*.json"))
        
        if self.pr_files:
            # Load the first PR
            pr = PullRequest.from_file(self.pr_files[0])
            if pr:
                self.current_pr = pr
                self.update_pr_display()
                self.app.log.info(f"Loaded PR #{pr.number}")
        else:
            self.app.log.info("No PRs found")
            
    def show_demo_pr(self):
        """Show a demonstration PR."""
        self.current_pr = PullRequest(
            number=142,
            title="feat(monitoring): Complete WebSocket monitoring server",
            author="Marcus Chen",
            branch="feature/sprint-1.6-monitoring-backend",
            description="Implements MON-001: Complete monitoring server with JWT auth, event handling, and Redis persistence",
            files_changed=[
                "monitoring_system/server.py",
                "monitoring_system/metrics_collector.py",
                "core/intelligence/error_recovery.py"
            ],
            created_at=datetime.now().isoformat()
        )
        self.update_pr_display()
        
    def update_pr_display(self):
        """Update the PR information display."""
        self.pr_info.remove_children()
        
        if not self.current_pr:
            self.pr_info.mount(Static("No PR selected"))
            return
            
        pr = self.current_pr
        
        # PR title and number
        self.pr_info.mount(Label(f"PR #{pr.number}: {pr.title}", classes="pr-title"))
        
        # Metadata
        metadata = f"""
Author: {pr.author}
Branch: {pr.branch}
Created: {pr.created_at[:19]}
Files: {len(pr.files_changed)} changed
"""
        self.pr_info.mount(Static(metadata.strip(), classes="pr-metadata"))
        
        # Description
        self.pr_info.mount(Static("\nDescription:"))
        self.pr_info.mount(Static(pr.description))
        
        # Files changed
        self.pr_info.mount(Static("\nFiles changed:"))
        for file in pr.files_changed[:5]:  # Show first 5 files
            self.pr_info.mount(Static(f"  • {file}"))
        if len(pr.files_changed) > 5:
            self.pr_info.mount(Static(f"  ... and {len(pr.files_changed) - 5} more"))
            
    def refresh(self):
        """Public refresh method."""
        asyncio.create_task(self.scan_for_prs())
        
    @on(Button.Pressed, "#view-diff")
    async def handle_view_diff(self):
        """Handle view diff button."""
        if not self.current_pr:
            self.app.notify("No PR selected", severity="warning")
            return
            
        await self.app.push_screen(DiffViewerDialog(self.current_pr))
        
    @on(Button.Pressed, "#approve")
    def handle_approve(self):
        """Handle PR approval."""
        if not self.current_pr:
            self.app.notify("No PR selected", severity="warning")
            return
            
        pr = self.current_pr
        
        # In production, this would:
        # 1. Run merge command
        # 2. Update PR status
        # 3. Notify relevant parties
        
        self.app.notify(
            f"PR #{pr.number} approved!\n"
            f"Would merge {pr.branch} → main",
            severity="success",
            title="PR Approved"
        )
        
        # Simulate merge
        try:
            # Check out main
            subprocess.run(['git', 'checkout', 'main'], capture_output=True)
            
            # Merge the branch
            result = subprocess.run(
                ['git', 'merge', pr.branch, '--no-ff', '-m',
                 f'Merge PR #{pr.number}: {pr.title}'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.app.notify("PR merged successfully!", severity="success")
                
                # Remove PR info file
                if self.pr_files:
                    self.pr_files[0].unlink(missing_ok=True)
                    
                # Clear current PR
                self.current_pr = None
                self.update_pr_display()
            else:
                self.app.notify(f"Merge failed: {result.stderr}", severity="error")
                
        except Exception as e:
            self.app.notify(f"Error merging PR: {e}", severity="error")
            
    @on(Button.Pressed, "#request-changes")
    def handle_request_changes(self):
        """Handle request changes."""
        if not self.current_pr:
            self.app.notify("No PR selected", severity="warning")
            return
            
        pr = self.current_pr
        
        # In production, this would create feedback
        feedback = """
Changes requested:
- Add more comprehensive error handling
- Include unit tests for new functionality
- Update documentation
"""
        
        self.app.notify(
            f"Changes requested for PR #{pr.number}\n{feedback}",
            severity="warning",
            title="Changes Requested"
        )
        
        # Create feedback file
        feedback_file = Path(f"feedback_PR_{pr.number}.md")
        feedback_file.write_text(f"# Feedback for PR #{pr.number}\n\n{feedback}")
        
        self.app.notify(f"Feedback saved to {feedback_file}", severity="information")
        
    @on(Button.Pressed, "#scan-prs")
    async def handle_scan_prs(self):
        """Handle scan for PRs button."""
        self.app.notify("Scanning for PRs...", severity="information")
        await self.scan_for_prs()
        
        if self.pr_files:
            self.app.notify(f"Found {len(self.pr_files)} PR(s)", severity="success")
        else:
            self.app.notify("No PRs found", severity="information")