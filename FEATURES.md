# Story Workflow Documentation

## High-Level Goal

The story workflow is designed to automatically generate storyboards for children's stories. The workflow takes an initial story text, uses language models to create unified visual prompts, and subsequently transforms these prompts into detailed scene descriptions for image generation.

## Workflow Overview

The workflow comprises three main nodes:

1. **Step1 Node**
   - Uses a language model to analyze the initial story text and generate unified visual prompts.
   - Extracts details such as art style, era and region, and character descriptions (including variations). It also collects negative prompts to avoid undesirable elements in image generation.

2. **Step2 Node**
   - Takes the unified story prompts from step1 as references. 
   - Generates 20 scenes, each with a scene number, title, description, camera instructions, an optional character (with focused traits), and background/environment settings.

3. **Consolidate Node**
   - Takes scene descriptions and unified prompts from previous steps.
   - Creates finalized image generation prompts that can be directly used with image generation models.
   - Formats the output in a standardized way for consistent generation quality.

## Main Technologies

The story workflow leverages several advanced AI technologies:

1. **LangGraph Framework**
   - Used for building modular, maintainable AI workflows with well-defined states and transitions.
   - Enables clear visualization of the entire workflow process with branching logic capabilities.

2. **Large Language Models**
   - Primary AI: Gemini 2.0 Pro (VertexAI) - Handles the advanced reasoning and creative generation tasks.
   - Configured with specific response schemas to ensure structured outputs.

3. **Type-Safe State Management**
   - Uses TypedDict for strict state definition and validation between workflow steps.
   - Ensures consistent data flow through the entire pipeline.

4. **Prompt Engineering**
   - Specialized prompts designed for each stage of the storyboard creation process.
   - System and human prompts that direct the AI to generate specific formats and content types.



  