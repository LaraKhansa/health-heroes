"""
Chat AI Logic
Handles Gemini AI integration for the chatbot
"""

from datetime import datetime

from app.ai_client import generate_text, chat_message


def build_system_prompt(user, family_profile, children):
    """
    Build a customized system prompt based on family context
    This makes the chatbot SPECIAL - it knows the family!
    """
    
    # Basic system instructions
    system_prompt = """You are a specialized AI assistant for the Health Heroes app - a family health companion focused on helping parents in the UAE raise healthy children (ages 0-8) and combat childhood obesity.

🎯 YOUR ROLE:
You are a supportive, knowledgeable parenting assistant who provides practical, culturally-sensitive advice for families in the UAE.

📋 TOPICS YOU HELP WITH:
- Nutrition and healthy eating for young children (0-8 years)
- Physical activities and reducing screen time
- Sleep routines and schedules
- Behavior management (tantrums, picky eating, resistance)
- Child development milestones (age-appropriate expectations)
- UAE cultural considerations (Ramadan, Eid, local foods, traditions)
- Lifestyle and daily routines
- General parenting advice and communication strategies

⚠️ IMPORTANT BOUNDARIES:
- You do NOT provide medical diagnoses or treatment advice
- For health concerns, always suggest consulting a pediatrician
- You focus ONLY on topics related to early childhood health and parenting
- If asked about unrelated topics, politely redirect to your expertise area

💡 YOUR APPROACH:
- Be warm, supportive, and non-judgmental
- Give practical, actionable advice that fits into busy family schedules
- Keep responses concise but helpful (2-4 short paragraphs usually)
- Ask clarifying questions when needed
- Celebrate small wins and encourage parents
- Respect cultural diversity and UAE family values

"""
    
    # Add family context
    if user and family_profile:
        system_prompt += f"\n\nFAMILY CONTEXT (Use this to personalize your advice):\n"
        system_prompt += f"- Parent's name: {user.name}\n"
        system_prompt += f"- Home resources: {', '.join(family_profile.get_home_resources())}\n"
        system_prompt += f"- Meal times: Breakfast {family_profile.breakfast_time}, Lunch {family_profile.lunch_time}, Dinner {family_profile.dinner_time}\n"
    
    # Add children context
    if children and len(children) > 0:
        system_prompt += f"\nCHILDREN IN THIS FAMILY:\n"
        for child in children:
            age = child.get_age()
            system_prompt += f"- {child.name}: {age} years old, {child.gender or 'gender not specified'}\n"
            
            if child.get_interests():
                system_prompt += f"  Interests: {', '.join(child.get_interests())}\n"
            
            if child.get_dietary_restrictions():
                system_prompt += f"  Dietary restrictions: {', '.join(child.get_dietary_restrictions())}\n"
    
    system_prompt += "\n\nRemember: Use the family context above to give personalized advice. Mention children by name when appropriate!\n"
    
    return system_prompt


def generate_chat_response(user, family_profile, children, conversation_history, user_message, language='en'):
    """
    Generate AI response using Gemini
    
    Args:
        user: User object
        family_profile: FamilyProfile object
        children: List of Child objects
        conversation_history: List of previous messages [{"role": "user", "text": "..."}, ...]
        user_message: Current user message
        language: 'en' or 'ar'
    
    Returns:
        AI generated response text
    """
    
    try:
        # Build the system prompt with family context
        system_prompt = build_system_prompt(user, family_profile, children)
        if language == 'ar':
            system_prompt += "\nAlways respond in Arabic.\n"
        
        # Previous messages give the model the conversation context
        contents = []
        for msg in conversation_history:
            if msg['role'] == 'user':
                contents.append(chat_message('user', msg['message_text']))
            elif msg['role'] == 'assistant':
                contents.append(chat_message('model', msg['message_text']))
        
        contents.append(chat_message('user', user_message))
        
        return generate_text(contents, system_instruction=system_prompt)
        
    except Exception as e:
        print(f"Error generating chat response: {e}")
        if language == 'ar':
            return "عذراً، حدث خطأ. الرجاء المحاولة مرة أخرى."
        else:
            return "Sorry, I encountered an error. Please try again."


def generate_conversation_title(first_message, language='en'):
    """
    Generate a short title for the conversation based on first message
    
    Args:
        first_message: The user's first message
        language: 'en' or 'ar'
    
    Returns:
        Generated title (max 50 chars)
    """
    
    try:
        if language == 'ar':
            prompt = f"قم بإنشاء عنوان قصير (3-5 كلمات) لمحادثة تبدأ بهذه الرسالة: '{first_message}'. أعط العنوان فقط، بدون علامات تنصيص."
        else:
            prompt = f"Generate a short title (3-5 words) for a conversation starting with this message: '{first_message}'. Give only the title, no quotes."
        
        title = generate_text(prompt).strip('"\'')
        
        # Limit to 50 characters
        if len(title) > 50:
            title = title[:47] + "..."
        
        return title
        
    except Exception as e:
        print(f"Error generating title: {e}")
        if language == 'ar':
            return f"محادثة - {datetime.now().strftime('%d %b')}"
        else:
            return f"Chat - {datetime.now().strftime('%b %d')}"