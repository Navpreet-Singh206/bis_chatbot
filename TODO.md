# FIXED: No Duplicates, Longer Answers (v2)

✅ **API & Retrieval** (`route.js`):
- Fixed chunks.json parsing (strings + metadata)
- Improved weighted search + always fallback
- STRICT prompt: NO "Sources:" text (all in system)
- max_tokens=2000, temp=0.0 → detailed 500-1200 words

✅ **UI Clean** (`MessageBuble.jsx`):
- Strip leaked "Sources: ..." regex before render
- ONLY clickable footer sources (no text dupes)

**Test:** `cd frontend & npm run dev` (Windows cmd uses &)

Expected: Pure long answers + single clickable sources list
