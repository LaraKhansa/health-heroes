"""
Chatbot Routes
Handles AI chat assistant for parents
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from db.models import db, User, FamilyProfile, Child, ChatConversation, ChatMessage
from app.chatbot.chat_ai import generate_chat_response, generate_conversation_title
from datetime import datetime

# Create blueprint
chatbot_bp = Blueprint(
    'chatbot',
    __name__,
    url_prefix='/chatbot',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)


def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@chatbot_bp.route('/')
@login_required
def chat_home():
    """
    Main chat page
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    # Get user name for display
    user_name = session.get('user_name', 'User')
    
    # Get language preference
    language = request.args.get('lang', family_profile.language if family_profile else 'en')
    
    # Get all children for context
    children = Child.query.filter_by(family_profile_id=family_profile.id).all() if family_profile else []
    
    return render_template(
        'chat.html',
        user_name=user_name,
        language=language,
        children=children,
        family_profile=family_profile
    )


@chatbot_bp.route('/api/conversations', methods=['GET'])
@login_required
def get_conversations():
    """
    Get list of user's conversations (last 20)
    """
    user_id = session.get('user_id')
    
    # Get last 20 conversations, ordered by most recent
    conversations = ChatConversation.query.filter_by(user_id=user_id)\
        .order_by(ChatConversation.updated_at.desc())\
        .limit(20)\
        .all()
    
    return jsonify({
        'success': True,
        'conversations': [conv.to_dict() for conv in conversations]
    })


@chatbot_bp.route('/api/conversation/<int:conversation_id>', methods=['GET'])
@login_required
def get_conversation(conversation_id):
    """
    Get a specific conversation with all its messages
    """
    user_id = session.get('user_id')
    
    # Get conversation and verify ownership
    conversation = ChatConversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    
    if not conversation:
        return jsonify({
            'success': False,
            'error': 'Conversation not found'
        }), 404
    
    # Get all messages
    messages = [msg.to_dict() for msg in conversation.messages]
    
    return jsonify({
        'success': True,
        'conversation': conversation.to_dict(),
        'messages': messages
    })


@chatbot_bp.route('/api/conversation/new', methods=['POST'])
@login_required
def create_conversation():
    """
    Create a new conversation
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    data = request.get_json()
    language = data.get('language', family_profile.language if family_profile else 'en')
    
    # Create new conversation
    conversation = ChatConversation(
        user_id=user_id,
        title='New Chat' if language == 'en' else 'محادثة جديدة',
        language=language
    )
    
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'conversation': conversation.to_dict()
    })


@chatbot_bp.route('/api/send-message', methods=['POST'])
@login_required
def send_message():
    """
    Send a message and get AI response
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    children = Child.query.filter_by(family_profile_id=family_profile.id).all() if family_profile else []
    
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    user_message = data.get('message')
    language = data.get('language', 'en')
    
    # Validate
    if not user_message or not user_message.strip():
        return jsonify({
            'success': False,
            'error': 'Message is required'
        }), 400
    
    # Get or create conversation
    if conversation_id:
        conversation = ChatConversation.query.filter_by(id=conversation_id, user_id=user_id).first()
        if not conversation:
            return jsonify({
                'success': False,
                'error': 'Conversation not found'
            }), 404
    else:
        # Create new conversation
        conversation = ChatConversation(
            user_id=user_id,
            title='New Chat' if language == 'en' else 'محادثة جديدة',
            language=language
        )
        db.session.add(conversation)
        db.session.flush()  # Get the ID
    
    # Check if this is the first message (before adding it!)
    is_first_message = len(conversation.messages) == 0
        
    # Save user message
    user_msg = ChatMessage(
        conversation_id=conversation.id,
        role='user',
        message_text=user_message.strip()
    )
    db.session.add(user_msg)

    # Get conversation history (for context)
    history = [msg.to_dict() for msg in conversation.messages]

    # Generate AI response
    try:
        ai_response = generate_chat_response(
            user=user,
            family_profile=family_profile,
            children=children,
            conversation_history=history,
            user_message=user_message,
            language=language
        )
        
        # Save AI response
        ai_msg = ChatMessage(
            conversation_id=conversation.id,
            role='assistant',
            message_text=ai_response
        )
        db.session.add(ai_msg)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        
        # Auto-generate title after 4 messages 
        message_count = len(conversation.messages) + 2  
        if message_count == 4:
            conversation.title = generate_conversation_title(user_message, language)
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'conversation_id': conversation.id,
            'user_message': user_msg.to_dict(),
            'ai_message': ai_msg.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in send_message: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate response'
        }), 500


@chatbot_bp.route('/api/conversation/<int:conversation_id>/title', methods=['PUT'])
@login_required
def update_conversation_title(conversation_id):
    """
    Update conversation title (user can edit)
    """
    user_id = session.get('user_id')
    
    data = request.get_json()
    new_title = data.get('title', '').strip()
    
    if not new_title:
        return jsonify({
            'success': False,
            'error': 'Title is required'
        }), 400
    
    # Get conversation and verify ownership
    conversation = ChatConversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    
    if not conversation:
        return jsonify({
            'success': False,
            'error': 'Conversation not found'
        }), 404
    
    # Update title
    conversation.title = new_title[:50]  # Limit to 50 chars
    db.session.commit()
    
    return jsonify({
        'success': True,
        'conversation': conversation.to_dict()
    })

@chatbot_bp.route('/api/conversation/<int:conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    """
    Delete a conversation
    """
    user_id = session.get('user_id')
    
    # Get conversation and verify ownership
    conversation = ChatConversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    
    if not conversation:
        return jsonify({
            'success': False,
            'error': 'Conversation not found'
        }), 404
    
    try:
        # Delete conversation (messages will be deleted automatically due to cascade)
        db.session.delete(conversation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conversation deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting conversation: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete conversation'
        }), 500