# SagaAHA CSS Structure

This document outlines the CSS structure for the SagaAHA application, including the color scheme, file organization, and usage guidelines.

## Color Scheme

The SagaAHA application uses a carefully selected color palette that reflects the historical theme of the application. The colors are defined as CSS variables in the `style.css` file.

### Primary Colors
- `--primary-1: #d4844a;` (Terracotta) - Used for headers, buttons, and important UI elements
- `--primary-2: #f5f1e8;` (Cream) - Used for backgrounds and subtle highlights

### Accent Colors
- `--accent-1: #daa520;` (Goldenrod) - Used for interactive elements and highlights
- `--accent-2: #2d5016;` (Forest Green) - Used for headings and important text

### Supporting Colors
- `--supporting-1: #8b4513;` (Saddle Brown) - Used for navigation and secondary elements
- `--supporting-2: #87936b;` (Sage Green) - Used for borders and subtle accents

### Special Purpose Colors
- `--special-1: #722f37;` (Burgundy) - Used for error messages and special highlights
- `--special-2: #cc5500;` (Burnt Orange) - Used for warnings and call-to-action elements

### Neutral Colors
- `--text-dark: #333333;` - Used for main text
- `--text-light: #ffffff;` - Used for text on dark backgrounds
- `--background-light: var(--primary-2);` - Used for page backgrounds

## File Structure

The CSS is organized into several files to maintain a modular and maintainable codebase:

### 1. style.css
The main stylesheet that defines global styles, color variables, and basic layout. This file should be included on all pages.

### 2. buttons.css
Styles for all button types and interactive elements.

### 3. forms.css
Styles for form elements, inputs, and validation.

### 4. timeline.css
Specific styles for the timeline component, including events, filters, and interactive elements.

### 5. reference.css
Styles for the reference section, including cards, details, and category badges.

### 6. quiz.css
Styles for the quiz section, including questions, options, results, and progress tracking.

## Usage Guidelines

### Including CSS Files

The base template (`templates/base.html`) already includes the main stylesheet and component stylesheets. Module-specific stylesheets should be included in the templates that need them using the `extra_css` block:

```html
{% extends 'base.html' %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/timeline.css' %}">
{% endblock %}
```

### Using Color Variables

Always use the CSS variables for colors instead of hardcoding hex values. This ensures consistency and makes it easier to update the color scheme in the future:

```css
/* Good */
.my-element {
    color: var(--primary-1);
    background-color: var(--primary-2);
}

/* Bad */
.my-element {
    color: #d4844a;
    background-color: #f5f1e8;
}
```

### Adding New Styles

When adding new styles:

1. Determine if the styles belong in an existing file or if a new file is needed
2. Use the established naming conventions and organization
3. Use the color variables for all color properties
4. Include responsive styles for mobile and tablet devices
5. Test the styles on different screen sizes

### Responsive Design

All styles should be responsive and work well on mobile, tablet, and desktop devices. Use the following breakpoints:

- Mobile: up to 768px
- Tablet: 769px to 1024px
- Desktop: 1025px and above

Example:

```css
@media (max-width: 768px) {
    .container {
        width: 90%;
    }
}
```

## Best Practices

1. Keep selectors as simple as possible
2. Avoid using `!important`
3. Group related styles together
4. Add comments for complex or non-obvious styles
5. Maintain consistent indentation and formatting
6. Test styles on different browsers and devices