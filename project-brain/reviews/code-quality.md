# Subsfolio — Code Quality Review Rubric

Review each implementation against the following 8 dimensions (each scored 0–100):

1. **Architecture**: Adheres to layer boundaries (UI -> API -> Service -> DB), avoids premature complexity, preserves separation of concerns.
2. **Maintainability**: Modular, cleanly structured, well-factored code with minimal tech debt and high testability.
3. **Readability**: Self-documenting code, consistent naming conventions, clear formatting, informative comments where needed.
4. **Intent Matching**: Faithfully fulfills the specified task requirements without omitting requirements or introducing unrequested deviations.
5. **Side Effects**: Isolated scope of change, zero unintended mutations, no regressions in adjacent modules or untouched files.
6. **Scalability**: Sensible query efficiency, non-blocking asynchronous I/O where appropriate, clean data structures.
7. **Security**: Mandatory user-scoping on all operations, authorization verification, safe input handling, environment variable protection.
8. **Overall**: Harmonic composite score across all areas. Must be ≥ 90 to pass Stage 7.
