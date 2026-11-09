// Form Video: embeds the YouTube video in this note's `url` with Obsidian's own
// player, which works around YouTube's Error 153 where a hand-written iframe can't.
// A form video reference note runs it as its body:
//   ```dataviewjs
//   await dv.view("Public/93 Views/Scripts/form-video")
//   ```
// Shorts, youtu.be, embed, and live links are turned into watch links, since
// Obsidian only embeds those. The plain link below the player is for iOS and
// iPadOS, where YouTube embeds don't play.

const url = String(dv.current().url ?? "").trim();
const id = url.match(/(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/|\/live\/)([\w-]{11})/)?.[1];

if (!url) {
  dv.paragraph("No `url` yet.");
} else if (!id) {
  dv.paragraph(`[Open the video](${url})`);
} else {
  const watch = `https://www.youtube.com/watch?v=${id}`;
  dv.paragraph(`![](${watch})`);
  dv.paragraph(`[Watch on YouTube](${watch})`);
}
