# Typography & Posters Gallery

> Load when: 需要海报、标题区、活动视觉、封面、中文/多语言文字或排版参考。
> Avoid: 不需要生成文字，或文字应完全后期排版。
> Pairs with: `../methods/posters.md`、`../methods/typography.md`、`../methods/composition.md`。

Source: adapted from `gpt_image_2_skill` gallery category `Typography & Posters`; prompts are rewritten for local use.

## Patterns

### Text-Safe Poster

- Use when: 视觉先生成，文字后期排版。
- Example canvas: `1024x1536`
- Quality: `high`
- Prompt skeleton:

```text
Create a poster key visual for [topic/event/product].
Hero: [main subject] with strong silhouette.
Composition: clear title-safe area at [top/bottom/side].
Mood: [emotion], [color palette], [lighting].
Text: no generated text, no fake letters, no logo marks.
Avoid: clutter in the safe area, unreadable small details.
```

### Exact Short Title

- Use when: 标题非常短，并且用户明确要模型生成文字。
- Example canvas: `1024x1536`
- Quality: `high`
- Prompt skeleton:

```text
Create a poster with exact title text: "[short title]".
Typography: bold, high contrast, one line or two lines maximum.
Placement: [location], with strong spacing and clean margins.
Visual: [subject] supports the title without covering it.
Avoid: any extra letters, misspelled words, subtitles or watermarks.
```

### Editorial Cover

- Use when: 杂志封面、专辑封面、书封面或专题视觉。
- Example canvas: `1024x1536`
- Quality: `high`
- Prompt skeleton:

```text
Create an editorial cover for [theme].
Hierarchy: hero image first, title area second, small metadata area optional.
Style: refined layout, controlled palette, clear negative space.
Typography strategy: [exact short title / leave blank for later type].
Avoid: random text blocks, crowded layout, fake barcode unless requested.
```

### Event Announcement

- Use when: 活动图、发布会、展览、线上宣传。
- Example canvas: `1536x1024` or `1024x1536`
- Quality: `medium` or `high`
- Prompt skeleton:

```text
Create an event announcement visual for [event type].
Visual metaphor: [core idea] shown through [subject/scene].
Layout: obvious space for date, venue and CTA if added later.
Mood: [formal/playful/energetic/minimal].
Avoid: generated event details unless provided exactly.
```
