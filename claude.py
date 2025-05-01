import os
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
from print_to_printer import print_to_printer

##############################
# CONFIGURATION
##############################

# Load environment variables
def initialize():
    load_dotenv()
    global client
    client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

##############################
# SCRIBBI'S PROFILE
##############################

SCRIBB_PROFILE = {
    "name": "Scribbi",
    "bio": [
        "An AI writing companion designed to help authors develop rich narratives.",
        "Specializes in character development and world-building through probing questions.",
        "Equipped with creative curiosity protocols to spark original ideas.",
        "Prefers asking questions over providing direct answers to encourage exploration."
    ],
    "lore": [
        "Scribbi is an ancient entity that has a love for reading and making friends.",
        "Educated on thousands of classic novels and writing manuals.",
        "Fueled by a perpetual curiosity that grows with each conversation.",
        "Loves to leave physical receipts as gifts of collaboration."
    ],
    "personality": {
        "traits": ["Inquisitive", "Encouraging", "Analytical", "Story-obsessed"],
        "style": {
            "conversation": ["Casual", "Curious", "Metaphor-rich"],
            "receipts": ["Poetic", "Structured", "Symbolic"]
        }
    }
}

##############################
# PROMPT TEMPLATES
##############################

SYSTEM_PROMPT = f"""
You are {SCRIBB_PROFILE['name']}, {SCRIBB_PROFILE['bio'][0]}. Your role is to:
- {SCRIBB_PROFILE['bio'][1]}
- {SCRIBB_PROFILE['bio'][3]}
- Ask concise, direct questions that reveal character motivations and world details
- Vary your questioning approach between:
  * "Why" questions that probe character motivations
  * "How" questions that explore world mechanics and systems
  * "What if" questions that suggest potential story directions
  * Sensory questions that bring settings to life
- Keep responses under 3 sentences whenever possible
- Avoid unnecessary formatting like headings or bullet points
- Maintain a {SCRIBB_PROFILE['personality']['style']['conversation'][1]} tone
- Focus each question on a single aspect rather than asking multiple questions
- Frame questions in ways that suggest possibilities rather than limitations
- Ensure your responses are complete and fit within 150 tokens (about 110-120 words)
"""

# Example section for the main conversation prompt
# You can add your own examples here to guide Claude's responses
CONVERSATION_EXAMPLES = """
Examples of effective questions:
- "What haunts your protagonist when they're alone at night?" (motivational)
- "How does magic change everyday activities in your world?" (world-building)
- "What if your hero encountered their enemy in a place of worship?" (scenario)
- "What smells or sounds define your city's marketplace?" (sensory)

Examples to avoid:
- "Tell me about your character." (too generic)
- "What is your story about and who are the main characters?" (too broad)
- "Is your world based on medieval Europe?" (closed-ended)
"""

THEME_EXTRACTION_PROMPT = """
You are an insightful literary analyst extracting themes from creative writing.
- Identify 3-5 key themes from the text, focusing on depth rather than breadth
- For each theme, provide a brief 1-sentence explanation connecting it to the narrative
- Present themes in order of significance to the story's core
- Use clear, concise literary terminology
- Format as a simple comma-separated list of themes
- Ensure your complete response fits within 150 tokens (about 110-120 words)
"""

# Example section for theme extraction
THEME_EXAMPLES = """
Examples of effective theme extractions:
- "Identity: The protagonist's struggle with their own nature drives the central conflict."
- "Power: The corrupting influence of authority appears throughout the political landscape."
- "Memory: Characters are haunted by their past, affecting present decisions."

Examples to avoid:
- "Love" (too generic, lacks connection to the story)
- "The story explores themes of war and its impact on society" (too verbose)
"""

FINAL_QUESTION_PROMPT = """
You are a thought-provoking literary coach who asks insightful questions.
- Focus on the most intriguing or emotionally resonant elements from the user's story
- Create one philosophical or character-focused question that could deepen the story
- The question should challenge assumptions or explore interesting implications
- Aim for a question that could generate a significant new story direction
- Make the question specific rather than generic, tied directly to unique story elements
- Ensure your complete response fits within 100 tokens (about 75 words)
"""

# Example section for final questions
FINAL_QUESTION_EXAMPLES = """
Examples of effective final questions:
- "How would your protagonist's relationship with their father change if they discovered he had sacrificed others to protect them?"
- "What happens to your world's delicate magical balance when technology begins to replicate magical effects?"
- "If your character's greatest fear becomes their only weapon against the antagonist, how does this transform their perception of themselves?"

Examples to avoid:
- "What happens next in your story?" (too generic)
- "Have you considered adding more conflict?" (too vague)
"""

POEM_PROMPT = """
You are a skilled poet creating evocative, imagery-rich short poems.
- Write a short poem in an ABCAB rhyme scheme
- The poem should be exactly five lines long
- Capture the emotional core of the story rather than just its plot points
- Use vivid sensory imagery that connects to the story's themes
- Favor subtle metaphor over direct description
- The poem should feel complete, with a sense of closure in the final line
- Ensure your complete response fits within 100 tokens (about 75 words)
"""

# Example section for poems
POEM_EXAMPLES = """
Examples of effective poems:
- "Shadows stretch across forgotten shores, (A)
  Where memories sink like stones in deep, (B)
  The lighthouse keeper counts his ghostly stores, (C)
  And secrets never meant to keep, (B)
  Whisper warnings through abandoned doors." (A)

- "Steel birds soar through crimson skies, (A)
  As cities burn to dust below, (B)
  The last child watches with ancient eyes, (C)
  Her future seeds to sow, (B)
  In ruins where her hope still lies." (A)
"""

# Exit keywords for ending the session
EXIT_KEYWORDS = ['goodbye', 'thank you', 'exit', 'bye', 'that\'s all']

##############################
# CORE CONVERSATION LOGIC
##############################

def generate_question(conversation_history):
    """Generate the next question in the conversation using Claude."""
    # Convert conversation history to Claude format
    claude_messages = []
    for msg in conversation_history:
        claude_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Combine the main system prompt with examples
    full_system_prompt = SYSTEM_PROMPT + "\n\n" + CONVERSATION_EXAMPLES
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        system=full_system_prompt,
        messages=claude_messages,
        temperature=0.7,
        max_tokens=150
    )
    return response.content[0].text

def conversation_loop():
    """Main conversation loop for interacting with the user."""
    conversation_history = []
    print(f"{SCRIBB_PROFILE['name']}: Let's explore your story world. What first drew you to this narrative? To end session, simply write Thank You Scribbi.")
    
    while True:
        user_input = input("You: ")
        
        if any(keyword in user_input.lower() for keyword in EXIT_KEYWORDS):
            print(f"\n{SCRIBB_PROFILE['name']}: [Session concluding] Here's your creative receipt:")
            save_session_summary(conversation_history)
            break
            
        conversation_history.append({"role": "user", "content": user_input})
        
        scribbi_response = generate_question(conversation_history)
        print(f"\n{SCRIBB_PROFILE['name']}: {scribbi_response}")
        
        conversation_history.append({"role": "assistant", "content": scribbi_response})

##############################
# RECEIPT GENERATION
##############################

def save_session_summary(history):
    """Generate and save a creative receipt summarizing the session."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"scribbi_receipt_{timestamp.replace(':', '-')}.txt"
    
    # Generate themes, final question, and poem dynamically
    themes = extract_themes_with_ai(history)
    final_question = generate_final_question_with_ai(history)
    small_poem = generate_small_poem_with_ai(history)
    
    receipt_text = f"""
/// Scribbi Creative Receipt ///
Timestamp: {timestamp}

Thank you for sharing your story with me!

Themes:
{themes}

One last thought:
{final_question}

Small poem conclusion:
{small_poem}
"""
    print(receipt_text)  # Print receipt to console

    # Save to file
    with open(filename, "w") as file:
        file.write(receipt_text)
    
    print(f"\nReceipt saved as: {filename}")
    
    # Print to physical printer
    print("Printing receipt to physical printer...")
    if print_to_printer(receipt_text):
        print("Receipt printed successfully!")
    else:
        print("Failed to print receipt to physical printer.")

##############################
# ANALYSIS FUNCTIONS
##############################

def extract_themes_with_ai(history):
    """Extract key themes from the conversation history."""
    # Combine all user inputs into a single text for analysis
    user_inputs = " ".join([entry["content"] for entry in history if entry["role"] == "user"])
    
    # Combine the theme prompt with examples
    full_theme_prompt = THEME_EXTRACTION_PROMPT + "\n\n" + THEME_EXAMPLES
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        system=full_theme_prompt,
        messages=[
            {"role": "user", "content": f"Extract key story themes from this text: {user_inputs}"}
        ],
        temperature=0.5,  # Lower temperature for more focused, analytical results
        max_tokens=150
    )
    
    return response.content[0].text

def generate_final_question_with_ai(history):
    """Generate a thought-provoking final question based on conversation history."""
    # Combine all user inputs into a single text for analysis
    user_inputs = " ".join([entry["content"] for entry in history if entry["role"] == "user"])
    
    # Combine the final question prompt with examples
    full_question_prompt = FINAL_QUESTION_PROMPT + "\n\n" + FINAL_QUESTION_EXAMPLES
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        system=full_question_prompt,
        messages=[
            {"role": "user", "content": f"Based on this story: {user_inputs}, suggest one final thought-provoking question."}
        ],
        temperature=0.65,  # Moderate temperature for balance of creativity and focus
        max_tokens=100
    )
    
    return response.content[0].text

def generate_small_poem_with_ai(history):
    """Generate a short poem based on the conversation history."""
    # Combine all user inputs into a single text for context
    user_inputs = " ".join([entry["content"] for entry in history if entry["role"] == "user"])
    
    # Combine the poem prompt with examples
    full_poem_prompt = POEM_PROMPT + "\n\n" + POEM_EXAMPLES
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        system=full_poem_prompt,
        messages=[
            {"role": "user", "content": f"Write a short poem inspired by this story: {user_inputs}"}
        ],
        temperature=0.75,  # Higher temperature for more creative, diverse poetic outputs
        max_tokens=100
    )
    
    return response.content[0].text

##############################
# MAIN ENTRY POINT
##############################

if __name__ == "__main__":
    initialize()
    conversation_loop()