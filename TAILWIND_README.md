# Tailwind CSS Setup

This project uses Tailwind CSS v4.2.2 standalone CLI (no npm required).

## Files Structure

```
├── tailwind.config.js      # Tailwind configuration
├── tailwindcss             # Standalone Tailwind CLI binary
├── static/
│   └── css/
│       ├── input.css       # Source CSS with @import "tailwindcss"
│       └── output.css      # Generated CSS (committed to repo)
├── build-tailwind-dev.sh   # Development build script (with watch mode)
└── build-tailwind-prod.sh  # Production build script (minified)
```

## Important: Tailwind CSS v4

This project uses Tailwind CSS v4.2.2, which uses the new `@import "tailwindcss"` syntax instead of the old `@tailwind` directives.

The input.css file should contain:
```css
@import "tailwindcss";
```

## Building CSS

### For Development (with watch mode):
```bash
./build-tailwind-dev.sh
```
This will watch for changes in your templates and rebuild automatically.

### For Production (minified):
```bash
./build-tailwind-prod.sh
```
This creates a minified version of the CSS.

### Manual Build:
```bash
./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
```

## Using Tailwind in Templates

1. Extend the base template:
```html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container mx-auto">
    <h1 class="text-4xl font-bold text-blue-600">Hello World</h1>
</div>
{% endblock %}
```

2. Or include the CSS in your own templates:
```html
<link rel="stylesheet" href="{% static 'css/output.css' %}">
```

## Adding Custom Styles

Add custom CSS to `static/css/input.css` after the Tailwind directives:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Your custom styles here */
.custom-class {
    /* ... */
}
```

## Configuration

The `tailwind.config.js` file scans these locations for classes:
- `./templates/**/*.html`
- All app templates (`./*/templates/**/*.html`)
- `./static/**/*.js`

## Notes

- The standalone CLI requires no Node.js or npm
- Output CSS is committed to the repository for deployment
- Run the build script before committing template changes
- Watch mode is recommended during active development
