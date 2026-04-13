# METHEAN Mobile Testing Matrix

## Device Matrix

| Device | Viewport | OS | Test Focus |
|--------|----------|-----|------------|
| iPhone SE | 375x667 | iOS 16+ | Smallest common. Everything must fit. No overflow. |
| iPhone 14 | 390x844 | iOS 16+ | Standard iPhone. Primary target. Notch safe areas. |
| iPhone 15 Pro Max | 430x932 | iOS 17+ | Largest iPhone. Dynamic Island. No wasted space. |
| iPad Mini | 768x1024 | iPadOS 16+ | Tablet breakpoint boundary. 2-column layouts. |
| Galaxy A14 | 360x800 | Android 13+ | Android midrange. Performance test target. |
| Pixel 7 | 412x915 | Android 13+ | Android flagship. Gesture nav safe areas. |

## Per-Device Checklist

### For ALL devices:
- [ ] Safe area insets render correctly (notch, Dynamic Island, home indicator)
- [ ] Bottom tab bar sits above home indicator/gesture bar
- [ ] Bottom sheet does not overlap system UI
- [ ] All text readable (min 13px parent, 14px child UI)
- [ ] All touch targets >= 44px
- [ ] No horizontal overflow (no horizontal scrollbar on any page)
- [ ] Landscape: pages don't break (may not be optimized, must not crash)

### PWA-specific:
- [ ] "Add to Home Screen" works (Safari / Chrome install prompt)
- [ ] App launches in standalone mode (no browser chrome)
- [ ] Theme color (#0F1B2D) applied to status bar
- [ ] Apple touch icon appears on home screen
- [ ] Maskable icon renders correctly on Android

### Navigation:
- [ ] Bottom tab bar: 5 tabs visible, correct active states
- [ ] Tab taps navigate correctly with haptic feedback
- [ ] Tab bar hides on scroll down, reappears on scroll up
- [ ] "More" tab opens full navigation in bottom sheet
- [ ] Bottom sheet: drag-to-dismiss works (slow drag + fast flick)
- [ ] Mobile header: child selector pill opens bottom sheet
- [ ] Switching child updates all data

### Touch Gestures:
- [ ] Press states visible on buttons, cards, list rows
- [ ] Governance queue: swipe approve/reject works
- [ ] Swipe respects velocity (fast flick at short distance triggers)
- [ ] Only one swipe action open at a time
- [ ] Page transitions: correct direction (deeper=left, shallower=right)
- [ ] Toast: appears from bottom on mobile, swipeable to dismiss

### Child Experience:
- [ ] Greeting is personalized and time-aware
- [ ] Progress ring shows correct X/Y count
- [ ] Activity cards: large, clear, tappable
- [ ] Tapping activity transitions to full-screen view
- [ ] "I'm Done" triggers celebration animation + haptic
- [ ] TutorChat: keyboard doesn't hide input bar
- [ ] Theme/avatar selection persists across reloads

### Offline:
- [ ] Offline banner appears when network disconnected
- [ ] Cached pages load with stale data
- [ ] "Back online" banner shows when reconnected
- [ ] No white screen on any offline page

### Performance:
- [ ] Lighthouse mobile: Performance > 85
- [ ] Lighthouse mobile: Accessibility > 90
- [ ] Lighthouse mobile: Best Practices > 90
- [ ] No CLS on page load
- [ ] No rubber-band bounce (overscroll-behavior working)

### Accessibility:
- [ ] Tab bar has role="tablist", tabs have role="tab"
- [ ] Bottom sheet has role="dialog", aria-modal="true"
- [ ] Focus moves to sheet on open, returns to trigger on close
- [ ] Escape key closes bottom sheet
- [ ] All decorative icons have aria-hidden="true"
- [ ] prefers-reduced-motion disables all animations
- [ ] Gold text uses accessible variant (--color-brand-gold-text)

## Animation Budget

| Animation | Max Duration | Properties |
|-----------|-------------|------------|
| Page transition | 200ms | transform, opacity |
| Press/active state | 100ms | transform |
| Bottom sheet open | 300ms | transform |
| Bottom sheet close | 250ms | transform |
| Pull-to-refresh snap | 200ms | transform, opacity |
| Celebration | 400ms | transform, opacity |
| Tab bar show/hide | 200ms | transform |
| Toast appear/dismiss | 200ms | transform, opacity |

**Rule**: No animation uses width, height, top, left, margin, or padding.
Only `transform` and `opacity` for GPU compositing.
