# Redfearn Group Callout System: Implementation Reference

Eight semantic callout variants. Each uses a 4px left accent bar plus an ~8% tint background. Load this file when building reports, dashboards, or any artifact that needs structured emphasis.

## Tint Backgrounds

```css
:root {
  --tint-blue:    #E9E9EE;  /* Key Insight bg */
  --tint-slate:  #EEF0F2;  /* Note bg */
  --tint-paper:  #F8F9FA;  /* Bottom Line bg (already near-white) */
  --tint-mist:   #EFEFF1;  /* Definition bg */
  --tint-tawny:  #FCF4F0;  /* Quote bg */
  --tint-yellow: #FFFBEB;  /* Warning bg */
  --tint-ember:  #FAF2EE;  /* Caution bg */
  --tint-red:    #FAEDEE;  /* Alert bg */
  --tint-green:  #EDF3EF;  /* On Track / positive bg */
}
```

## Base Callout CSS

```css
.callout {
  border-radius: 0 6px 6px 0;
  padding: 0.75rem 1rem;
  margin-bottom: 0.6rem;
  position: relative;
  overflow: hidden;
}
.callout::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4px;
}
.callout .lbl {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}
.callout p {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.875rem;
  color: var(--rg-blue);
  font-weight: 300;
  line-height: 1.6;
}
```

## Eight Variants

```css
/* 1. KEY INSIGHT, primary finding, strongest non-semantic signal */
.co-insight   { background: var(--tint-blue); }
.co-insight::before  { background: var(--rg-blue); }
.co-insight .lbl     { color: var(--rg-blue); }

/* 2. NOTE, informational, non-urgent context */
.co-note      { background: var(--tint-slate); }
.co-note::before     { background: var(--rg-slate); }
.co-note .lbl        { color: var(--rg-slate); }

/* 3. BOTTOM LINE, TL;DR / recommendation */
.co-bottom    { background: var(--tint-paper); }
.co-bottom::before   { background: var(--rg-blue); }
.co-bottom .lbl      { color: var(--rg-blue); }

/* 4. DEFINITION, term introduction, code context */
.co-def       { background: var(--tint-mist); }
.co-def::before      { background: var(--rg-graphite); }
.co-def .lbl         { color: var(--rg-graphite); }

/* 5. QUOTE, attributed excerpts */
.co-quote     { background: var(--tint-tawny); }
.co-quote::before    { background: var(--rg-tawny); }
.co-quote .lbl       { color: var(--rg-blue); }

/* 6. WARNING, risks/caveats. Yellow bar, ember label (yellow fails as text) */
.co-warning   { background: var(--tint-yellow); }
.co-warning::before  { background: var(--rg-gape); }
.co-warning .lbl     { color: var(--rg-ember); }

/* 7. CAUTION, do-not-proceed, one level below Alert */
.co-caution   { background: var(--tint-ember); }
.co-caution::before  { background: var(--rg-ember); }
.co-caution .lbl     { color: var(--rg-ember); }

/* 8. ALERT, most severe, already failing */
.co-alert     { background: var(--tint-red); }
.co-alert::before    { background: var(--rg-red); }
.co-alert .lbl       { color: var(--rg-red); }
```

## Status Signal Pills

```css
.sc { display: inline-block; padding: 0.18em 0.6em; border-radius: 3px; font-weight: 700; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; }
.sc-green  { background: var(--tint-green); color: var(--rg-green); }  /* ON TRACK, 7.2:1 AAA */
.sc-tawny  { background: var(--tint-tawny); color: var(--rg-tawny); } /* AT RISK */
.sc-ember  { background: var(--tint-ember); color: var(--rg-ember); } /* BLOCKED */
.sc-red    { background: var(--tint-red);   color: var(--rg-red);   } /* CRITICAL, 6.1:1 AA */
```

## KPI Delta Display

```css
.kpi-delta { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; line-height: 1; }
.kpi-up      { color: var(--rg-green); }  /* ▲ */
.kpi-down    { color: var(--rg-ember); }  /* ▼ moderate */
.kpi-severe  { color: var(--rg-red); }    /* ▼ severe */
```

## Sample HTML

```html
<div class="callout co-insight"><div class="lbl">Key Insight</div><p>Primary finding goes here.</p></div>
<div class="callout co-note"><div class="lbl">Note</div><p>Non-urgent context.</p></div>
<div class="callout co-bottom"><div class="lbl">Bottom Line</div><p>The TL;DR recommendation.</p></div>
<div class="callout co-def"><div class="lbl">Definition</div><p>Term introduction.</p></div>
<div class="callout co-quote"><div class="lbl">Quote</div><p>Attributed excerpt.</p></div>
<div class="callout co-warning"><div class="lbl">Warning</div><p>Risk or caveat.</p></div>
<div class="callout co-caution"><div class="lbl">Caution</div><p>Do not proceed without review.</p></div>
<div class="callout co-alert"><div class="lbl">Alert</div><p>Already failing, most severe.</p></div>

<span class="sc sc-green">ON TRACK</span>
<span class="sc sc-tawny">AT RISK</span>
<span class="sc sc-ember">BLOCKED</span>
<span class="sc sc-red">CRITICAL</span>

<div class="kpi-delta kpi-up">▲ 12%</div>
<div class="kpi-delta kpi-down">▼ 5%</div>
<div class="kpi-delta kpi-severe">▼ SLA</div>
```
