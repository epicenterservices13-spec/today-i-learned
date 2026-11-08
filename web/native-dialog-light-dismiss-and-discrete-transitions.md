# Native Dialog Light-Dismiss and Top-Layer Discrete Transitions

Modern web applications can achieve fully accessible, hardware-accelerated modals using native HTML5 `<dialog>` with declarative `closedby="any"` and CSS discrete transitions, completely replacing third-party overlay libraries.

## Context

Custom JavaScript modal libraries often suffer from broken accessibility, leaking focus traps, incorrect `z-index` stacking wars, and layout shifts from manual scroll locking (`overflow: hidden` on `body`). Furthermore, animating elements toggling to/from `display: none` in the browser's top layer previously caused instant dismissal clipping unless discrete transitions are properly sequenced.

## Implementation / Code

### 1. Declarative Markup & Fallback Dismissal

```html
<!-- Native modal dialog with declarative light-dismiss -->
<dialog id="media-modal" closedby="any" aria-label="Media Preview">
  <form method="dialog">
    <button type="submit" class="modal-close" aria-label="Close dialog">✕</button>
  </form>
  <div class="modal-body">
    <!-- Dynamic Content -->
  </div>
</dialog>
```

```javascript
// Progressive enhancement fallback for browsers lacking native closedby support
if (!('closedBy' in HTMLDialogElement.prototype)) {
  const outside = (e, dialog) => {
    const r = dialog.getBoundingClientRect();
    return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
  };
  
  let pressedOutside = false;
  dialog.addEventListener('pointerdown', (e) => {
    pressedOutside = outside(e, dialog);
  });
  
  dialog.addEventListener('pointerup', (e) => {
    // Require pointerdown AND pointerup outside to prevent dismissal on text selection drag
    if (pressedOutside && outside(e, dialog)) dialog.close();
    pressedOutside = false;
  });
}
```

### 2. Modern CSS Top-Layer Animations & Scroll Containment

```css
/* Contain scrolling without layout shifts */
dialog:modal {
  overscroll-behavior: contain;
}

dialog::backdrop {
  overflow: hidden;
  overscroll-behavior: contain;
  background-color: rgba(5, 5, 8, 0.85);
  backdrop-filter: blur(10px);
  opacity: 0;
  transition-property: opacity, display, overlay;
  transition-duration: 0.25s;
  transition-timing-function: ease-out;
  transition-behavior: allow-discrete;
}

dialog[open]::backdrop {
  opacity: 1;

  @starting-style {
    opacity: 0;
  }
}

/* Modal container with discrete transition and entry starting style */
dialog#media-modal {
  opacity: 0;
  transform: scale(0.92);
  transition-property: opacity, transform, display, overlay;
  transition-duration: 0.25s;
  transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
  transition-behavior: allow-discrete;
}

dialog#media-modal[open] {
  opacity: 1;
  transform: scale(1);

  @starting-style {
    opacity: 0;
    transform: scale(0.92);
  }
}
```

## Takeaways

- **Always use `showModal()`**: Opening with `.show()` or the `open` attribute bypasses the top-layer, backdrop generation, and focus containment.
- **Transition `display` and `overlay`**: For top-layer entry/exit animations, `transition-behavior: allow-discrete` and `overlay` are mandatory to prevent premature clipping during closing transitions.
- **Never lock `body` overflow**: Use `dialog:modal { overscroll-behavior: contain; }` and `dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }` instead of `overflow: hidden` on `html`/`body`, preserving root scrollbars and preventing layout shifts.
- **Pointer tracking over `event.target`**: The `<dialog>` element is also the target for its own padding and internal flex gaps. Testing coordinates via `getBoundingClientRect()` prevents unintended dismissals when users click empty space inside the dialog.
