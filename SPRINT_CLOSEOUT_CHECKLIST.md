# Sprint Closeout Checklist

## 1. Documentation ✍️
- [ ] Create `SPRINT_X_X_COMPLETE.md` with:
  - Sprint goals and achievements
  - Technical decisions made
  - Metrics and challenges
  - Lessons learned
  - Next sprint recommendations
- [ ] Update `CLAUDE.md` with:
  - Current project state
  - Critical discoveries
  - Quick start commands
  - Important patterns

## 2. Code Cleanup 🧹
- [ ] Remove test files created during development
- [ ] Clean up any experimental code
- [ ] Ensure all important code is committed
- [ ] Run linting if applicable

## 3. Git Management 🔄
- [ ] Stage and commit all sprint work
- [ ] Use descriptive commit messages
- [ ] Push all commits to remote repository
- [ ] Verify remote is synchronized:
  ```bash
  git fetch origin
  git push origin main
  git log --oneline -n 5
  ```

## 4. Todo Management 📋
- [ ] Update todo list to reflect completed items
- [ ] Clear completed todos
- [ ] Add next sprint items if known

## 5. Handoff Preparation 🤝
- [ ] Ensure CLAUDE.md has clear next steps
- [ ] Document any critical patterns discovered
- [ ] Include working example commands
- [ ] Note any environment-specific issues

## 6. Final Verification ✅
- [ ] Confirm all tests are passing (if applicable)
- [ ] Verify key features are working
- [ ] Check that documentation is complete
- [ ] Ensure clean git status (except ongoing work)

## Example Commands
```bash
# Full closeout sequence
git add -A
git status
git commit -m "feat/docs: Sprint X.X complete - [Brief description]"
git push origin main
git status --short
```

## Sprint Closeout Complete When:
1. All code is committed and pushed
2. Documentation is updated
3. Remote repository is synchronized
4. Next session has clear starting point
5. Todo list is cleaned up

---
*Always leave the codebase better than you found it!*