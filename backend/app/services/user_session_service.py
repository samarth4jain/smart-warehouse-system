import uuid
import logging
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from ..models.database_models import User, ChatSession, ConversationContext, ChatMessage

logger = logging.getLogger(__name__)

class UserSessionService:
    """Service for managing users, sessions, and conversation context"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_user(self, username: str, email: str = None, full_name: str = None, role: str = "operator") -> User:
        """Get existing user or create new one"""
        try:
            # Try to find existing user
            user = self.db.query(User).filter(User.username == username).first()
            
            if not user:
                # Create new user
                user = User(
                    username=username,
                    email=email or f"{username}@warehouse.local",
                    full_name=full_name or username.title(),
                    role=role,
                    preferences={}
                )
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
                logger.info(f"Created new user: {username}")
            else:
                # Update last login
                user.last_login = datetime.utcnow()
                self.db.commit()
                
            return user
            
        except Exception as e:
            logger.error(f"Error getting/creating user {username}: {str(e)}")
            self.db.rollback()
            raise
    
    def create_session(self, user_id: int, initial_message: str = None) -> ChatSession:
        """Create a new chat session for a user"""
        try:
            session_id = str(uuid.uuid4())
            
            # Generate title from initial message (simplified)
            title = "New Conversation"
            if initial_message:
                # Take first 50 characters and clean up
                title = initial_message[:50].strip()
                if len(initial_message) > 50:
                    title += "..."
            
            session = ChatSession(
                session_id=session_id,
                user_id=user_id,
                title=title,
                context_summary="",
                is_active=True,
                total_messages=0
            )
            
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            
            logger.info(f"Created new session {session_id} for user {user_id}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating session for user {user_id}: {str(e)}")
            self.db.rollback()
            raise
    
    def get_session(self, session_id: str, user_id: int = None) -> Optional[ChatSession]:
        """Get an existing chat session"""
        try:
            query = self.db.query(ChatSession).filter(ChatSession.session_id == session_id)
            
            if user_id:
                query = query.filter(ChatSession.user_id == user_id)
            
            session = query.first()
            
            if session and session.is_active:
                # Update last activity
                session.last_activity = datetime.utcnow()
                self.db.commit()
                
            return session
            
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {str(e)}")
            return None
    
    def get_user_sessions(self, user_id: int, limit: int = 10) -> List[ChatSession]:
        """Get recent sessions for a user"""
        try:
            sessions = self.db.query(ChatSession).filter(
                ChatSession.user_id == user_id,
                ChatSession.is_active == True
            ).order_by(ChatSession.last_activity.desc()).limit(limit).all()
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting sessions for user {user_id}: {str(e)}")
            return []
    
    def add_context(self, session_id: int, context_type: str, context_key: str, 
                   context_value: Any, expires_in_hours: int = 24) -> ConversationContext:
        """Add context information to a session"""
        try:
            # Remove existing context with same key
            self.db.query(ConversationContext).filter(
                ConversationContext.session_id == session_id,
                ConversationContext.context_key == context_key
            ).delete()
            
            expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
            
            context = ConversationContext(
                session_id=session_id,
                context_type=context_type,
                context_key=context_key,
                context_value=context_value if isinstance(context_value, dict) else {"value": context_value},
                expires_at=expires_at
            )
            
            self.db.add(context)
            self.db.commit()
            self.db.refresh(context)
            
            return context
            
        except Exception as e:
            logger.error(f"Error adding context to session {session_id}: {str(e)}")
            self.db.rollback()
            raise
    
    def get_session_context(self, session_id: int) -> Dict[str, Any]:
        """Get all active context for a session"""
        try:
            now = datetime.utcnow()
            
            contexts = self.db.query(ConversationContext).filter(
                ConversationContext.session_id == session_id,
                ConversationContext.expires_at > now
            ).order_by(ConversationContext.relevance_score.desc()).all()
            
            context_dict = {}
            for ctx in contexts:
                context_dict[ctx.context_key] = {
                    "type": ctx.context_type,
                    "value": ctx.context_value,
                    "relevance": ctx.relevance_score,
                    "created": ctx.created_at
                }
            
            return context_dict
            
        except Exception as e:
            logger.error(f"Error getting context for session {session_id}: {str(e)}")
            return {}
    
    def update_session_summary(self, session_id: int, new_summary: str):
        """Update the context summary for a session"""
        try:
            session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if session:
                session.context_summary = new_summary
                self.db.commit()
                
        except Exception as e:
            logger.error(f"Error updating session summary {session_id}: {str(e)}")
    
    def save_message(self, session_id: int, user_id: int, user_message: str, 
                    bot_response: str, intent: str = None, context_used: Dict = None,
                    enhanced_mode: bool = False, processing_time: float = None,
                    confidence_score: float = None) -> ChatMessage:
        """Save a chat message to the database"""
        try:
            message = ChatMessage(
                session_id=session_id,
                user_id=user_id,
                user_message=user_message,
                bot_response=bot_response,
                intent=intent,
                context_used=context_used or {},
                enhanced_mode=enhanced_mode,
                processing_time=processing_time,
                confidence_score=confidence_score
            )
            
            self.db.add(message)
            
            # Update session message count
            session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if session:
                session.total_messages += 1
                session.last_activity = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(message)
            
            return message
            
        except Exception as e:
            logger.error(f"Error saving message for session {session_id}: {str(e)}")
            self.db.rollback()
            raise
    
    def get_conversation_history(self, session_id: int, limit: int = 20) -> List[ChatMessage]:
        """Get conversation history for a session"""
        try:
            messages = self.db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
            
            return list(reversed(messages))  # Return in chronological order
            
        except Exception as e:
            logger.error(f"Error getting conversation history for session {session_id}: {str(e)}")
            return []
    
    def cleanup_expired_context(self):
        """Clean up expired context entries"""
        try:
            now = datetime.utcnow()
            deleted = self.db.query(ConversationContext).filter(
                ConversationContext.expires_at < now
            ).delete()
            
            self.db.commit()
            logger.info(f"Cleaned up {deleted} expired context entries")
            
        except Exception as e:
            logger.error(f"Error cleaning up expired context: {str(e)}")
            self.db.rollback()
    
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user preferences for personalized responses"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user and user.preferences:
                return user.preferences
            return {}
            
        except Exception as e:
            logger.error(f"Error getting preferences for user {user_id}: {str(e)}")
            return {}
    
    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]):
        """Update user preferences"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                user.preferences = preferences
                user.updated_at = datetime.utcnow()
                self.db.commit()
                
        except Exception as e:
            logger.error(f"Error updating preferences for user {user_id}: {str(e)}")
            self.db.rollback()
