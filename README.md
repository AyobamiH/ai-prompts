# ai-prompts

> A curated collection of the AI prompts I actually use — ready to copy, paste, and adapt.

[![License: MIT](https://img.shields.io/github/license/eddiejaoude/ai-prompts)](LICENSE)
[![Stars](https://img.shields.io/github/stars/eddiejaoude/ai-prompts?style=social)](https://github.com/eddiejaoude/ai-prompts/stargazers)

## Table of contents

- [About](#about)
- [What's inside](#whats-inside)
- [How the prompts are organized](#how-the-prompts-are-organized)
- [Categories](#categories)
- [How to use these prompts](#how-to-use-these-prompts)
- [Contributing](#contributing)
- [License](#license)

## About

This repo is a personal, growing library of prompts I use with AI tools — coding assistants, video generators, and content helpers. Each one is written up as a self-contained spec you can hand straight to an AI model, or read yourself to understand the reasoning behind it.

They aren't throwaway one-liners. The prompts here are pulled from real, working builds — every number, palette, and constraint is something that shipped, not something invented for a demo.

**Who it's for:** developers, creators, and anyone who wants dependable, battle-tested prompts they can reuse instead of writing from scratch.

## What's inside

- **Full prompts, not fragments.** Each file gives you the complete prompt plus the context needed to get a good result.
- **Reproducible.** Where a prompt produced a specific artifact (a video, a layout), the exact settings are documented so you can reproduce the result.
- **Copy-paste ready.** Grab a prompt, drop it into your AI tool of choice, and adjust the details to fit your project.

## How the prompts are organized

Prompts are grouped into **category folders** at the root of the repo. Each category holds one Markdown file per prompt, and each file is self-contained:

- a short description (and a preview screenshot where relevant),
- any requirements or dependencies,
- the prompt itself, ready to paste into an AI tool.

To add or find a prompt, look inside the category folder that fits it. New categories are just new folders — see the [Categories](#categories) list below for what exists today.

## Categories

| Category | Description | Prompts |
| --- | --- | --- |
| [Automation](automation) | Prompts for deterministic and externally verified automation | [Deterministic social publication](automation/deterministic-social-publication.md) — publish through official APIs with durable idempotency and readback |
| [Socials](socials) | Prompts for social and video content | [Audiogram](socials/audiogram.md) — build a 1:1 audiogram in Remotion |

_More categories will be added over time._

## How to use these prompts

Every prompt here is a self-contained Markdown file you can hand straight to an AI tool.

1. **Find a prompt.** Browse the category folders (for example [`socials/`](socials)) and open the file you want.
2. **Copy it.** Each file holds the complete prompt. Where a file separates its notes from the prompt with a `---` divider, copy everything below the divider — that's the part written for the AI.
3. **Paste it into your AI tool.** Drop it into a coding assistant (Claude, Cursor, Copilot Chat) or the model of your choice.
4. **Adapt the specifics.** The prompts come from real, working builds, so many carry exact values — palettes, sizes, sample data. Keep the structure and swap those details for your own project.

For example, to generate a social audiogram, open [`socials/audiogram.md`](socials/audiogram.md) and paste its prompt into your assistant:

> Build me a square audiogram in Remotion. It turns a short audio clip into a 1080x1080 video with word-by-word captions, a speaker credit card and a waveform driven by the actual audio…

The assistant returns a working Remotion project; from there you swap the palette and speaker details for your own brand.

## Contributing

Contributions are welcome — the aim is a growing library of prompts that actually work. To add one:

1. **Fork** this repository and create a branch.
2. **Pick a category.** Add your prompt as a Markdown file inside the category folder it best fits (for example `socials/`). If none fit, create a new folder — a new category is just a new folder.
3. **Write it as a self-contained spec**, following the shape of the existing prompts (see [`socials/audiogram.md`](socials/audiogram.md)):
   - an H1 title and a short description (add a preview screenshot where it helps),
   - any requirements or dependencies,
   - the prompt itself, ready to paste into an AI tool.
4. **Keep it reproducible.** If your prompt produced a specific result, document the real settings that made it work rather than inventing values for a demo.
5. **Open a pull request** describing what the prompt does and what you built with it.

## License

Released under the [MIT License](LICENSE) — © 2026 Eddie Jaoude. You're free to use, adapt, and share these prompts; a link back is always appreciated.
