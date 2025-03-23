import ollama
import re


def handle_ollama_stream_response(stream, verbose_thinking=True, display_func=print):
    """
    Handles streamed response from an Ollama model.

    Args:
        stream: An iterable stream of response chunks (each with 'message' > 'content').
        verbose_thinking (bool): If True, displays thoughts inside <think> blocks.
                                 If False, shows '[thinking...]' instead.
        display_func (function): Function to display text (default: print).

    Returns:
        Cleaned final assistant message without <think> blocks.
    """
    final_message = ""

    for chunk in stream:
        content = chunk.get("message", {}).get("content", "")

        # Find all <think>...</think> blocks in this chunk
        while "<think>" in content and "</think>" in content:
            pre_think, rest = content.split("<think>", 1)
            thinking_text, post_think = rest.split("</think>", 1)

            # Display text before the think block
            if pre_think.strip():
                display_func(pre_think)
                final_message += pre_think

            # Display either verbose thinking or placeholder
            if verbose_thinking:
                display_func(f"(thinking: {thinking_text.strip()})")
            else:
                display_func("[thinking...]")

            content = post_think

        # Display remaining content
        if content.strip():
            display_func(content)
            final_message += content

    # Remove all think blocks from final result
    final_message_clean = re.sub(r"<think>.*?</think>", "", final_message, flags=re.DOTALL).strip()

    return final_message_clean


# Example usage
def call_ollama_with_thinking(model, prompt, verbose_thinking=True):
    # response_stream = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], stream=True)
    # final_response = handle_ollama_stream_response(response_stream, verbose_thinking=verbose_thinking)
    for part in ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], stream=True):
        print(part['message']['content'], end='', flush=True)
    # return final_response


if __name__ == "__main__":
    # Example call with verbose thinking
    result = call_ollama_with_thinking("deepseek-r1:8b", "Explain the concept of recursion.", verbose_thinking=True)
    print("\nFinal Cleaned Response:\n", result)
