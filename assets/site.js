// Clubhouse Apps: the site's own behaviour, for what the kit doesn't do (the kit's files stay untouched).
//
// Card spotlight: one soft glow follows the pointer across a group of cards marked [data-spot] (the pricing
// plans), lighting the card surfaces and their borders together, also while the pointer crosses the gap
// between them; it fades when the pointer leaves. The look is in site.css. Nothing runs on touch screens or
// under reduced motion: the cards stay exactly as they are.
const still = matchMedia('(prefers-reduced-motion: reduce)');
const fine = matchMedia('(hover: hover) and (pointer: fine)');

for (const group of document.querySelectorAll('[data-spot]')) {
  const cards = [...group.querySelectorAll('.card')];
  let x = 0, y = 0, raf = 0;
  const paint = () => {
    raf = 0;
    for (const card of cards) {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--spot-x', `${(x - r.left).toFixed(1)}px`);
      card.style.setProperty('--spot-y', `${(y - r.top).toFixed(1)}px`);
    }
  };
  group.addEventListener('pointermove', (e) => {
    if (still.matches || !fine.matches) return;
    x = e.clientX; y = e.clientY;
    group.classList.add('is-lit');
    if (!raf) raf = requestAnimationFrame(paint);
  }, { passive: true });
  group.addEventListener('pointerleave', () => group.classList.remove('is-lit'));
}
