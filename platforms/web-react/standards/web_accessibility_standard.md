# Web Accessibility Standard

Platform: Web React.

- Use semantic landmarks such as `header`, `nav`, `main`, `aside`, and appropriately labelled regions.
- Use native `button`, `a`, `input`, and other interactive elements before recreating their semantics on generic elements.
- Preserve keyboard reachability, logical focus order, visible focus indication, and expected activation keys.
- Expose locked, selected, expanded, busy, loading, invalid, and error states through text or appropriate HTML/ARIA semantics.
- Do not communicate state by color alone; pair color with text, iconography, shape, or another explicit signal.
- Use live-region or status semantics only for dynamic changes that require announcement; avoid noisy duplicate announcements.
- Respect `prefers-reduced-motion` for non-essential animation and provide a stable reduced-motion presentation.
- Verify touch target size, text contrast, zoom/reflow, and lossless access to core actions at the consumer's supported responsive breakpoints.

ARIA supplements native semantics; it does not repair an inappropriate element or a missing interaction model.
