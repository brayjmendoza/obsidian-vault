---
type: documentation
created: 2026-11-08
updated: 2026-11-08
aliases:
  - Music Tracking
---
The Music domain tracks what you play: pieces from wishlist to repertoire, the drills you work on, your practice sessions, and the composers behind it all. Piano and Violin are subdomains with the same shape, and both share one set of composers. The binding rules are in [[CONVENTIONS]], and each note's layout is in its template (see [[Vault Templates]]).

```
Composer ◀── composers ── Piece ◀── pieces ── Practice
 who wrote it              what you play       what you worked on
```

## The Notes

| Note | Lives in | What it's for |
|---|---|---|
| Composers | Music | One per composer, shared by every instrument, with every piece of theirs you have |
| Pieces | Each instrument | One piece, from the day you want to learn it to the day you retire it |
| Technique | Each instrument | A drill you track (e.g., a scale and its current tempo) |
| Practice | Each instrument | One practice session: how long, what it focused on, and which pieces |
| Practice plans | Each instrument | How you plan to practice (e.g., Piano's [[Practice Schedule]]) |

- **One note for a piece's whole life:** its status moves from `wishlist` through `learning` and `polishing` to `repertoire`, then to `retired` or `relearning`, so there's no separate wishlist.
- **Pieces name their composers:** the original composer first, then any arrangers (e.g., Bach, then Busoni for the Chaconne).
- **Explanations live elsewhere:** music theory goes in `40 Knowledge/`, and how-tos like fingerings go in `50 References/` (see [[Domain Skeleton]]).

## Features

- **Repertoire views:** the Music and Piano hubs list your repertoire and retired pieces, live from your piece notes.
- **Composer views:** each composer note lists your pieces by that composer. The [[Composer Template]] sets this up for every new composer.
- **[[Sync Last Practiced]]:** keeps each piece's `last_practiced` current from your practice notes.

## Logging Practice

1. Create a practice note from the [[Practice Template]] and list the pieces you worked on.
2. Each piece's `last_practiced` moves to that day on its own.

## Known Limits

- **Sync doesn't follow edits:** adding a piece to an older practice note doesn't update the piece until you run [[Sync Last Practiced]] on its own.
- **Composers who share a surname** (e.g., Clara and Robert Schumann) need their composer view set up by hand.
