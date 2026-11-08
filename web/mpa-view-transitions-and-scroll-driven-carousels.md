# MPA Cross-Document View Transitions and Scroll-Driven Snap Carousels

Multi-Page Applications (MPAs) can achieve app-like page navigation transitions and fluid scroll-snapped carousels natively in CSS without single-page application framework overhead.

## Context

Traditionally, seamless screen transitions and swipeable carousels required heavy single-page application (SPA) routers, virtual DOMs, and third-party touch libraries (such as Swiper or Flickity). With modern CSS specifications, multi-page architectures can achieve equivalent or superior 60fps compositor-driven experiences using `@view-transition` and scroll-driven animation timelines.

## Implementation / Code

### 1. Cross-Document View Transitions (MPA)

```css
/* Enable seamless transitions across same-origin page navigations */
@media (prefers-reduced-motion: no-preference) {
  @view-transition {
    navigation: auto;
  }

  ::view-transition-old(root) {
    animation: 0.22s cubic-bezier(0.16, 1, 0.3, 1) both vh-page-fade-out;
  }

  ::view-transition-new(root) {
    animation: 0.25s cubic-bezier(0.16, 1, 0.3, 1) both vh-page-fade-in;
  }
}

@keyframes vh-page-fade-out {
  to {
    opacity: 0;
    transform: scale(0.995);
  }
}

@keyframes vh-page-fade-in {
  from {
    opacity: 0;
    transform: scale(1.005);
  }
}
```

### 2. Scroll-Driven Snap Carousel

```css
/* Horizontal snap container */
.carousel-scroller {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  gap: 1.5rem;
  scrollbar-width: thin;
}

.carousel-scroller > .slide {
  flex: 0 0 min(100%, 28rem);
  scroll-snap-align: center;
}

/* Scroll-driven continuous scale and fade on the inline axis */
@supports ((animation-timeline: view()) and (animation-range: entry)) {
  @keyframes slide-scroll-effect {
    0% {
      opacity: 0.45;
      transform: scale(0.92);
    }
    50% {
      opacity: 1;
      transform: scale(1);
    }
    100% {
      opacity: 0.45;
      transform: scale(0.92);
    }
  }

  .carousel-scroller > .slide {
    animation: slide-scroll-effect auto linear both;
    animation-timeline: view(inline);
  }
}
```

### 3. Lightweight Indicator Synchronization

```javascript
// Synchronize slide counter/indicator using IntersectionObserver
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && entry.intersectionRatio >= 0.55) {
        const index = slides.indexOf(entry.target);
        if (index !== -1) updateCounter(index + 1, slides.length);
      }
    });
  },
  { root: scroller, threshold: 0.55 }
);

slides.forEach((slide) => observer.observe(slide));
```

## Takeaways

- **Progressive enhancement by default**: If a browser lacks support for `@view-transition` or scroll-driven animations, standard instant navigation and baseline horizontal scroll continue to function seamlessly with zero script errors.
- **Always scope to `prefers-reduced-motion`**: Wrap view transition navigation in `@media (prefers-reduced-motion: no-preference)` to honor user accessibility preferences.
- **Inline axis tracking**: In horizontal scrollers, be explicit with `animation-timeline: view(inline)` rather than the default block axis.
- **Combine CSS Snapping with `scrollIntoView`**: Programmatic navigation buttons simply invoke `element.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' })` without manual pixel tracking calculations.
