# Device and assistive-technology review

This worksheet separates browser-engine checks from testing with a real device
and assistive technology. Automated results live in `browser-review.md`.
No physical phone, VoiceOver, NVDA or TalkBack session was available on
2026-10-13. Those sessions remain **not run**, not passed.

## Sessions to record

| Platform | Status | Record with the result |
| --- | --- | --- |
| iPhone, Safari, VoiceOver | Not run | OS/browser versions, text size, rotor/focus behavior |
| Android, Chrome, TalkBack | Not run | OS/browser versions, font scale, reading order |
| Windows, Firefox or Chrome, NVDA | Not run | NVDA/browser versions, browse/forms mode |

Use https://www.alekpopovic.com after deployment. Write down the URL, exact
control, expected/observed behavior, device, and reproduction steps for each
failure. A screenshot alone cannot establish announcement behavior.

## Review scenario

1. Navigate using Tab and Shift+Tab. Activate Skip to content. At 200% browser
   zoom and 320 CSS pixels, open mobile navigation, then AI filters. Labels,
   current values and expanded states should be announced. Escape dismisses a
   popup, arrow keys select options, and Tab leaves the control without trapping
   focus. Content outside code samples should reflow without horizontal scroll.
2. Open `/learn/workspace/`. Navigate by headings and landmarks. All five books,
   five paths and four workshops have usable links even with JavaScript disabled.
   With JavaScript, the progress status should announce local-device scope.
3. Open `/learn/secret-contracts/`. Read each question legend and its options.
   Check incomplete answers, correct one answer, and activate Review mistakes.
   The status announces the score; hidden correct questions should leave the
   reading order. Practical step checkboxes must remain unchanged by quiz answers.
4. Open `/ai/workshops/`. Find the labelled JavaScript textarea in forms mode.
   Syntax overlays and line numbers should not be announced twice. Tab moves
   out of the editor; Ctrl/Cmd+Enter runs tests. Results are announced once after
   completion. Stop must remain reachable during a loop; controls recover after
   four seconds. Import requires explicit Use this file and never runs code.
5. Open a book chapter and scroll the text panel. Hide the global menu, then
   change chapters in the contents. The menu stays hidden. Enter focus mode,
   open a figure, move its zoom slider, and close with Escape. Focus returns to
   the figure and focus mode remains enabled. Open notes, save a synthetic note,
   complete a section, then find it in My Learning.
6. Export a backup, import it, cancel once, then restore it. The preview receives
   focus; cancel returns focus to the chooser. Verify notes and workshop source
   are preserved, and that overwrite happens only with the replace option.
7. Enable high contrast/forced colors and reduced motion. Textarea contents,
   selected controls, focus outlines and error messages stay readable. Turn off
   JavaScript and revisit the path, chapter and newsletter issue.

Do not describe an automated axe score, Linux WebKit run, screenshot review, or
viewport emulation as a real screen-reader or physical-phone session. Follow the
[WAI evaluation guidance](https://www.w3.org/WAI/test-evaluate/).
