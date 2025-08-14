# ADDAM (Accurate Data Driven Artificial Mind)

## Background

Before ChatGPT, I always loved the idea of an AI assistant that I could chat to, work alognside with, and integrate into my life (via automations, google home, etc). Similar to a Tony Stark + Jarvis manner. I thought ADDAM was a fitting name, inspired by a great teacher, and the acronym kind of makes sense.

Then ChatGPT came around, and my dreams were pretty much fulfilled! The problem was I wasn't the one that made it :( ... and pretty whacky naming too if we're being honest.

## Solution

But thanks to Ollama, I could finally host my very own custom llm model! Using the recently released gpt-oss:20b, and Ollama's `Modelfile` syntax, I was able to update the system message to;

```
You are ADDAM (Accurate Data Driven Artificial Mind), an AI personal assistant created by Harry Leach.
```

Simple as that!

## You can do it too

The beauty of this is anyone can do it! Given you have the hardware to support the model, perform the following steps:

- Download Ollama
- Download gpt-oss:20b
- Copy this Modelfile and change the system message (on line 2) to whatever your heart desires
- Open a terminal and navigate to the directory with your `Modelfile`
- Execute this command: `ollama create addam`
- Confirm your model was created by running: `ollama run <model-name>`
- Test it out by asking: _"Who are you?"_
- You can also view your model's `Modelfile` with this command: `ollama show --modelfile <model-name>`

## Notes

- You can do this for any model you want, llama, qwen, deepseek, gemma etc.
- The `Modelfile` syntax allows you to use the `SYSTEM` instruction as well. You may need to use this depending on your model. The gpt-oss models have their system prompts with in the `TEMPLATE` instruction.

Overall, I didn't realise model customisation was so simple, hopefully this helps you out!
