# Frontend project rules template

Apply this document to an explicitly selected frontend repository; do not install it as a global rule for all projects.

- Read package.json, routes, existing components, the styling system, and test commands before starting. Follow the existing architecture.
- Include loading, empty, failure, insufficient-permission, retry, and success states in requirements. URL state, back navigation, and keyboard operation are part of the user flow.
- Validate only API fields actually consumed and affecting presentation, permissions, state, or calculations. Handle invalid values explicitly; avoid coupling unrelated endpoints through a shared schema.
- Hiding UI controls does not replace backend authorization. Invalid identity or role data must not render a normal actionable state.
- Run the project's actual type-check, lint, and unit-test commands. lint-staged checks staged files only.
- Component tests verify interactions and observable outcomes. Use browser acceptance checks for cross-page navigation, routing, login, and critical write flows; report URL, environment, data source, and uncovered scope.
- Verify images, text, colors, focus, labels, responsive behavior, and error feedback together. Mock screenshots are not evidence of backend integration.
