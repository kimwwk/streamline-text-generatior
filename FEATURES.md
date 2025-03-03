# Story Workflow Documentation

## High-Level Goal

The story workflow is designed to automatically generate storyboards for children's stories. The workflow takes an initial story text, uses language models to create unified visual prompts, and subsequently transforms these prompts into detailed scene descriptions for image generation.

## Workflow Overview

The workflow comprises two main nodes:

1. **Step1 Node**
   - Uses a language model to analyze the initial story text and generate unified visual prompts.
   - Extracts details such as art style, era and region, and character descriptions (including variations). It also collects negative prompts to avoid undesirable elements in image generation.

2. **Step2 Node**
   - Takes the unified story prompts from step1 as references. 
   - Generates 20 scenes, each with a scene number, title, description, camera instructions, an optional character (with focused traits), and background/environment settings.



  