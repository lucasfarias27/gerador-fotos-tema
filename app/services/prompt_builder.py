def construir_prompt(tema_config: dict, numero_foto: int, total: int) -> str:
    """
    Builds a prompt for Gemini image generation.
    The automation will have already attached the reference photo before sending this prompt.
    Prompts are in English for better Gemini performance.
    """
    outfit = tema_config.get('outfit_hint', '')
    outfit_line = f"Clothing: {outfit}.\n\n" if outfit else ''

    return (
        f"Using the person in the uploaded reference photo as the subject, "
        f"create a high-quality photorealistic image with a {tema_config['keywords_en']} theme.\n\n"
        f"Style guidelines: {tema_config['style_hint']}.\n\n"
        f"{outfit_line}"
        f"Important: Keep the person's face, features, and identity clearly recognizable. "
        f"Naturally integrate the person into the scene — including appropriate themed clothing as described above. "
        f"Maintain photographic quality, high resolution. "
        f"Do not alter the person's facial features or physical proportions."
    )
