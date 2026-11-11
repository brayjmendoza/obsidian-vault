---
type: documentation
created: 2026-11-11
updated: 2026-11-11
aliases:
  - Cooking Tracking
---
# About Cooking

The Cooking domain tracks what you cook: recipe notes hold the dishes you make, and meal notes log each time you made them. The binding rules are in [[CONVENTIONS]], and each note's layout is in its template (see [[Vault Templates]]).

```
Recipe ◀── recipes ── Meal
 what you make          when you made it
```

## The Notes

| Note | What it's for |
|---|---|
| Recipes | One dish, with its ingredients, steps, and every meal that used it |
| Meals | One time you cooked, named for the meal (e.g., `2026-11-11 Dinner`), listing the recipes you made |

- **One note for a recipe's whole life:** its status moves from `to-try` to `tried`, then to `staple` or `retired`, so there's no separate list of recipes to try.
- **Nothing is typed twice:** a recipe's Meals section is a live view of your meal notes.
- **How-tos live elsewhere:** techniques like knife skills go in `50 References/` (see [[Domain Skeleton]]).

## Logging a Meal

1. Create a meal note from the [[Meal Template]] and list the recipes you made.
2. Each recipe's `last_cooked` moves to that day on its own (see [[Sync Last Cooked]]).

## Known Limits

- **Sync doesn't follow edits:** adding a recipe to an older meal note doesn't update the recipe until you run [[Sync Last Cooked]] on its own.
