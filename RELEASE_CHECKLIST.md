# 📋 v2.1 Release Checklist

Complete these steps to publish SDD v2.1 officially on GitHub.

---

## ✅ Pre-Release Checklist

### Documentation
- [x] README.md updated with metrics roadmap
- [x] CHANGELOG.md created with v2.1 details
- [x] RELEASE_v2.1.md created (release notes)
- [x] CONSTITUTION-CUSTOMIZATION.md created
- [x] HONEST-CRITIQUE-CONSTITUTION.md created
- [x] ULTRA-LITE-ADOPTION.md added
- [x] lite-constitution.yaml template created
- [x] context/ cleaned (78 → 30 files)

### Framework Quality
- [x] No breaking changes (v2.0 code works unchanged)
- [x] All adoption paths tested (ULTRA-LITE, LITE, FULL)
- [x] Constitution disclaimer added
- [x] All links verified and working

### Version Numbers
- [x] Version in README: 2.1
- [x] CHANGELOG marked as v2.1
- [x] RELEASE_v2.1.md complete

---

## 🚀 Release Steps

### Step 1: Prepare Git

```bash
# Ensure you're on main branch
git branch  # Check current branch
git checkout main

# Verify all changes are committed
git status  # Should show: working tree clean

# Update git to latest commit
git pull origin main
```

### Step 2: Create Release Tag

```bash
# Create lightweight tag
git tag v2.1

# Or create annotated tag (recommended)
git tag -a v2.1 -m "SDD v2.1 - Honest, transparent, production-ready

Major additions:
- ULTRA-LITE adoption path (5 min setup)
- Constitutional transparency (Python/FastAPI honest claim)
- Customization guide
- Missing templates added
- Context directory cleaned (67% size reduction)
- Metrics roadmap (Q2 2026)

Backward compatible with v2.0. No breaking changes."

# Verify tag created
git tag -l v2.1
```

### Step 3: Push to GitHub

```bash
# Push tag to GitHub
git push origin v2.1

# Or if you want to include commits:
git push origin main
git push origin v2.1
```

### Step 4: Create GitHub Release

**Option A: Via GitHub Web UI (Recommended for First Release)**

1. Go to: https://github.com/SergioLacerda/sdd-architecture/releases
2. Click "Create a new release"
3. Select tag: v2.1
4. Title: "SDD v2.1 — Honest, Transparent, Production-Ready"
5. Description: Copy content from [RELEASE_v2.1.md](./RELEASE_v2.1.md)
6. Attach files (optional):
   - CHANGELOG.md
   - RELEASE_v2.1.md
7. "Publish release"

**Option B: Via GitHub CLI**

```bash
# Install gh if not already installed
# brew install gh  (on macOS)
# apt install gh   (on Linux)

# Create release from tag
gh release create v2.1 \
  --title "SDD v2.1 — Honest, Transparent, Production-Ready" \
  --notes-file RELEASE_v2.1.md

# Or with pre-release flag
gh release create v2.1 \
  --title "SDD v2.1 — Honest, Transparent, Production-Ready" \
  --notes-file RELEASE_v2.1.md \
  --prerelease  # Use if not final

# Verify release created
gh release list
```

### Step 5: Update GitHub Settings

1. **Set as Latest Release:**
   - Go to: https://github.com/SergioLacerda/sdd-architecture/releases
   - Find v2.1 release
   - Verify "Latest" badge appears

2. **Update Repository About Section (Optional):**
   - Repository settings
   - Add description: "SDD Framework v2.1 - Specification-Driven Development"
   - Add link: https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.1

### Step 6: Verify Release

```bash
# Check GitHub shows release
curl https://api.github.com/repos/SergioLacerda/sdd-architecture/releases/latest

# Should show v2.1 details
# Look for: "tag_name": "v2.1"
```

---

## 📢 Announce Release

### Option 1: GitHub Discussions

Create a discussion post:

```
Title: "SDD v2.1 is Live! 🚀"

Content:
SDD v2.1 is officially released and production-ready.

Major additions:
✅ ULTRA-LITE adoption path (5-minute setup)
✅ Constitutional transparency (honest about Python/FastAPI)
✅ Customization guide
✅ Missing templates now available
✅ Metrics roadmap (real data in Q2 2026)

All v2.0 code works unchanged (100% backward compatible).

🚀 Get started: https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.1

Questions? Open an issue or start a discussion!
```

### Option 2: README Badge

Add to README.md:

```markdown
[![Release](https://img.shields.io/github/v/release/SergioLacerda/sdd-architecture?style=flat-square)](https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.1)
```

### Option 3: Announcements (Optional)

- Post in:
  - Relevant Slack/Discord communities
  - Dev.to (as a post)
  - Twitter/X (if applicable)
  - Newsletter (if you have one)

**Message Template:**

```
SDD Framework v2.1 is now available! 🚀

🎯 What's new:
- 3-tier adoption (pick your level: ULTRA-LITE/LITE/FULL)
- Honest positioning (Python/FastAPI, not fake multi-language)
- Customization guide (adapt framework to your needs)
- Context cleaned (328KB, vs 984KB in v2.0)
- Metrics roadmap (real data coming in Q2 2026)

✨ Perfect for:
- Solo devs → ULTRA-LITE (5 min setup)
- Small teams → LITE (15 min setup)
- Production → FULL (40 min setup)

🔗 Get started: [Link to release]
📖 Read details: [Link to RELEASE_v2.1.md]
```

---

## ✅ Post-Release Verification

### Checklist

```bash
# 1. Verify release shows on GitHub
[ ] https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.1 exists

# 2. Verify README shows badge
[ ] Badge displays in README
[ ] Badge links to release page

# 3. Verify CHANGELOG is accessible
[ ] CHANGELOG.md exists in repo
[ ] Can access via GitHub interface

# 4. Verify adoption guides work
[ ] ULTRA-LITE path loads: https://github.com/.../ULTRA-LITE-ADOPTION.md
[ ] LITE path loads: https://github.com/.../LITE-ADOPTION.md
[ ] FULL path loads: https://github.com/.../FULL-ADOPTION.md

# 5. Verify new documents exist
[ ] CONSTITUTION-CUSTOMIZATION.md available
[ ] HONEST-CRITIQUE-CONSTITUTION.md available
[ ] lite-constitution.yaml template available
```

### Commands to Verify

```bash
# Clone fresh copy and verify
rm -rf /tmp/sdd-test
git clone https://github.com/SergioLacerda/sdd-architecture.git /tmp/sdd-test
cd /tmp/sdd-test

# Check version in README
grep "Version.*2.1" README.md

# Check release files exist
ls -la CHANGELOG.md
ls -la RELEASE_v2.1.md
ls -la EXECUTION/spec/guides/adoption/ULTRA-LITE-ADOPTION.md
ls -la EXECUTION/spec/guides/adoption/templates/lite-constitution.yaml

# Check context cleanup worked
wc -l EXECUTION/spec/guides/adoption/templates/lite-constitution.yaml
# Should be much smaller than before

echo "✅ All checks passed!"
```

---

## 🎯 Success Metrics

Release is successful when:

✅ **GitHub shows v2.1 release with:**
- Tag: v2.1
- Title: "SDD v2.1 — Honest, Transparent, Production-Ready"
- Release notes describing changes
- Marked as "Latest"

✅ **Documentation complete:**
- CHANGELOG.md has v2.1 section
- RELEASE_v2.1.md published
- README.md references v2.1
- Adoption guides all updated

✅ **Technical quality:**
- All links work (verified via fresh clone)
- No broken cross-references
- All new files accessible
- Code still works (backward compatible)

✅ **Team notified:**
- Release announced
- Adoption guides discoverable
- Early adopters invited to test

---

## 🔧 If Something Goes Wrong

### Release Not Showing

```bash
# Verify tag exists locally
git tag | grep v2.1

# Verify tag pushed to GitHub
git ls-remote origin refs/tags/v2.1

# If missing, recreate:
git tag v2.1
git push origin v2.1
```

### Wrong Release Notes

```bash
# Delete release on GitHub (via web UI)
# Delete tag:
git tag -d v2.1
git push origin --delete v2.1

# Recreate:
git tag v2.1
git push origin v2.1
```

### Files Missing

```bash
# Verify all new files committed
git status  # Should be clean

# If files missing:
git add CHANGELOG.md RELEASE_v2.1.md ...
git commit -m "Add v2.1 release files"
git push origin main

# Then create release tag on updated commit
```

---

## 📖 After Release

### Immediate (Day 1-2)
- Monitor for early feedback
- Fix any broken links found
- Update documentation if needed
- Respond to questions/issues

### Short-term (Week 1)
- Gather feedback from early adopters
- Plan v2.2 based on v2.1 usage
- Start collecting real metrics
- Document common adoption questions

### Medium-term (Q2 2026)
- Publish metrics from pilot teams
- Plan v2.2 features
- Announce multi-language roadmap

---

## 📞 Support

### If You Need Help

**Option 1: GitHub Issues**
- Create issue: "Release v2.1 — [Problem]"
- Include reproduction steps
- Reference relevant adoption level

**Option 2: GitHub Discussions**
- Start discussion: "Question about v2.1"
- Broader conversations welcome

**Option 3: This Document**
- Refer back to "If Something Goes Wrong"
- Follow troubleshooting steps

---

## ✨ You Did It!

Congratulations on releasing SDD v2.1! 🎉

You've:
- ✅ Built a mature framework
- ✅ Been honest about limitations
- ✅ Provided clear adoption paths
- ✅ Empowered teams to customize
- ✅ Published for the world to use

**Now:** Gather feedback, measure real impact, keep improving.

**Next:** v2.2 with real metrics, v3.0 with multi-language.

---

**Questions? Create an issue or discussion on GitHub!** 🚀
