# Design System Document

## 1. Overview & Creative North Star: "The Digital Atelier"
This design system is built upon the concept of **The Digital Atelier**. It rejects the industrial, "templated" feel of modern e-commerce in favor of high-end editorial curation. The objective is to treat every digital screen like a bespoke physical space—think of it as a gallery or a private fitting room in a flagship boutique.

To achieve this, we break the traditional rigid grid. We embrace **intentional asymmetry**, allowing high-resolution fashion photography to bleed off-edge or overlap with sophisticated typography. This system prioritizes breathing room, tonal depth, and a "quiet luxury" aesthetic that feels timeless yet technologically advanced.

---

## 2. Colors: Tonal Luxury & Atmosphere
The palette is rooted in three core pillars: **Silk Cream** (softness), **Deep Charcoal** (authority), and **Metallic Gold** (prestige).

### The "No-Line" Rule
**Explicit Instruction:** Use of `1px` solid borders for sectioning is strictly prohibited. Boundaries must be defined solely through background color shifts. For example, a `surface-container-low` section sitting against a `surface` background creates a sophisticated, architectural transition that a line simply cannot replicate.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of fine vellum paper.
- **Surface (Background):** Use `#fbf9f1` (Silk Cream) as the base for all editorial content.
- **Surface-Container-Lowest:** Use for the most elevated elements (e.g., product detail cards) to create a soft, natural lift.
- **Surface-Container-Highest:** Use for footer or heavy-weight sections to ground the layout in `#e4e3db`.

### Signature Textures & Glassmorphism
- **The Glass Rule:** For floating navigation or modal overlays, use a semi-transparent `surface` color with a `20px` backdrop-blur. This allows the richness of the fashion imagery to bleed through, ensuring the UI feels integrated rather than "pasted on."
- **Metallic Soul:** For Primary CTAs, use a subtle linear gradient (45°) from `primary` (#735c00) to `primary-container` (#d4af37). This prevents the "flat gold" look and provides a professional, shimmering finish.

---

## 3. Typography: Editorial Authority
The juxtaposition of a high-contrast Serif and a functional Sans-Serif creates a dialogue between tradition and modernity.

*   **Display & Headline (Playfair Display):** These are our "hero" voices. Use `display-lg` and `headline-lg` with generous tracking (letter-spacing) for a high-fashion, masthead feel.
*   **Title & Body (Inter):** Inter provides the functional clarity required for luxury e-commerce. It should be used with increased line-height (1.6x) to ensure the text feels as "light" as the visual layout.
*   **Label (Inter Medium/Bold):** Used for micro-copy, price points, and navigation, often in all-caps with `0.1rem` letter spacing to denote prestige.

---

## 4. Elevation & Depth: The Layering Principle
We convey hierarchy through **Tonal Layering** rather than structural shadows.

*   **Ambient Shadows:** If a floating element (like a "Quick Buy" drawer) requires lift, use an extra-diffused shadow: `box-shadow: 0 20px 50px rgba(44, 44, 44, 0.05)`. The shadow must be a tinted version of the `on-surface` color to mimic natural light.
*   **The Ghost Border:** If a border is required for accessibility (e.g., input fields), use `outline-variant` (#d0c5af) at **20% opacity**. Never use 100% opaque, high-contrast borders.
*   **Spatial Breathing:** Utilize the Spacing Scale’s larger values (`16`, `20`, `24`) to separate content. In luxury design, white space is not "empty"—it is a premium commodity.

---

## 5. Components: Refined Interaction

### Buttons
*   **Primary:** Background: Gold Gradient; Text: `on-primary`; Radius: `4px` (`DEFAULT`).
*   **Secondary:** Background: `Deep Charcoal` (#2c2c2c); Text: `Silk Cream` (#fffdf5); Radius: `4px`.
*   **Tertiary (Editorial):** No background. Underlined with a `2px` gold border-bottom that expands on hover.

### Cards & Lists
*   **Constraint:** Forbid the use of divider lines. 
*   **Execution:** Separate list items using `spacing-4` (1.4rem) of vertical white space or a subtle shift to `surface-container-low` on hover. Cards should appear "borderless," using only the `surface-container` tiers to define their boundaries.

### Input Fields
*   **Style:** Minimalist. Only a bottom-border (Ghost Border style) at 20% opacity. 
*   **States:** On focus, the bottom border transitions to 100% `primary` (Gold), and the label (Inter) shifts to `label-sm`.

### Signature Component: The "Atelier Carousel"
A non-standard carousel where the center image is larger and the flanking images are partially transparent and grayscale, emphasizing the curated nature of the collection.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical layouts where text overlaps the edge of an image.
*   **Do** prioritize high-resolution imagery; the UI should serve as a frame for the fashion.
*   **Do** use "Silk Cream" as the default background instead of pure white to reduce eye strain and feel more "organic."
*   **Do** use the `4px` (0.25rem) corner radius consistently across all interactive elements.

### Don't:
*   **Don't** use 1px solid black borders to separate sections.
*   **Don't** use standard "drop shadows" (e.g., `0 2px 4px`). They look cheap.
*   **Don't** crowd the interface. If you think there’s enough space, add 20% more.
*   **Don't** use "Inter" for large headlines. It lacks the romantic, editorial weight required for the brand.