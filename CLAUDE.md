# Documentation Rewriting Instructions

## Core Philosophy

Documentation should give users the right mental model, not list features. Reference Linear's approach: short, illustrative, user-focused.

## Process

1. **Deep dive into implementation** - Understand the actual code architecture, data models, and functionality. Don't write about features that don't exist.

2. **Understand user intent** - What are users trying to accomplish? Focus on outcomes, not processes.

3. **Cut out listicle bullshit** - No "best practice" sections, verbose tips, or generic advice. Be direct.

4. **Lead with the mental model** - Start with what the thing IS and how it fits into the user's world, not what it does.

## Writing Style

- **Concise over comprehensive** - Better to explain the core concept well than list every feature
- **User outcomes over feature descriptions** - "Track performance" not "The dashboard displays metrics"
- **Progressive disclosure** - Start with the essential concept, add details only if needed
- **No preamble or postamble** - Jump straight into the content

## Structure Patterns

### For foundational concepts (like Workspaces):
- What it is and why it matters
- How everything connects to it  
- Common usage patterns
- Keep it short

### For feature docs (like Dashboard):
- What it shows you (with screenshot)
- Brief explanation of key elements
- Essential actions you can take
- Done

### For process docs (like Annotations):
- When and why to use it
- How it works (briefly)
- Key setup steps
- Management approach

## What to Avoid

- Long procedural walkthroughs
- "Best practices" sections
- Verbose explanations of obvious UI elements
- Marketing copy about benefits
- Generic optimization advice
- Telling users what they "should" do

## Implementation Notes

- Always explore the actual codebase first to understand real functionality
- Reference Linear's documentation style for user-focused approach
- Rewrite existing content, don't just edit it
- Remove files that don't serve the core mental model
- Create new structure based on actual architecture, not legacy organization

## Example Transformations

**Before:** "The annotated replies feature provides customizable high-quality question-and-answer responses through manual editing and annotation..."

**After:** "Annotations let you create a curated library of perfect responses for specific questions."

**Before:** Long sections about "workspace organization tips" and "collaboration best practices"

**After:** "A workspace contains and isolates everything your organization needs: applications, knowledge bases, team members, model configurations, plugins, and billing."

The goal is documentation that helps users understand and use the product effectively, not documentation that demonstrates how much the product can do.