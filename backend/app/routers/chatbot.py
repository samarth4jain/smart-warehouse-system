from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..services.enhanced_chatbot_service import EnhancedChatbotService
from ..services.chatbot_service import ChatbotService  # Keep as fallback

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    message: str
    intent: str
    data: Optional[dict] = None
    actions: List[str] = []
    success: bool = True
    timestamp: datetime
    enhanced_mode: bool = False

class SystemStatus(BaseModel):
    llm_service: bool
    rag_service: bool
    enhanced_mode: bool

@router.post("/message", response_model=ChatResponse)
async def process_chat_message(chat_message: ChatMessage, db: Session = Depends(get_db)):
    """Process a chat message and return bot response"""
    
    try:
        # Try enhanced service first
        enhanced_service = EnhancedChatbotService(db)
        
        if enhanced_service.is_enhanced_mode_available():
            response = enhanced_service.process_message(
                user_message=chat_message.message,
                session_id=chat_message.session_id,
                user_id=chat_message.user_id
            )
            
            return ChatResponse(
                message=response["message"],
                intent=response["intent"],
                data=response.get("data"),
                actions=response.get("actions", []),
                success=response["success"],
                timestamp=datetime.utcnow(),
                enhanced_mode=True
            )
        
        else:
            # Fallback to original rule-based service
            service = ChatbotService(db)
            response = service.process_message(
                user_message=chat_message.message,
                session_id=chat_message.session_id,
                user_id=chat_message.user_id
            )
            
            return ChatResponse(
                message=response["message"],
                intent=response["intent"],
                data=response.get("data"),
                actions=response.get("actions", []),
                success=response["success"],
                timestamp=datetime.utcnow(),
                enhanced_mode=False
            )
            
    except Exception as e:
        # Ultimate fallback
        return ChatResponse(
            message="I apologize, but I'm experiencing technical difficulties. Please try again or contact support.",
            intent="error",
            data=None,
            actions=[],
            success=False,
            timestamp=datetime.utcnow(),
            enhanced_mode=False
        )

@router.get("/status", response_model=SystemStatus)
async def get_system_status(db: Session = Depends(get_db)):
    """Get chatbot system status"""
    try:
        enhanced_service = EnhancedChatbotService(db)
        status = enhanced_service.get_system_status()
        
        return SystemStatus(
            llm_service=status["llm_service"],
            rag_service=status["rag_service"],
            enhanced_mode=status["enhanced_mode"]
        )
    except Exception as e:
        return SystemStatus(
            llm_service=False,
            rag_service=False,
            enhanced_mode=False
        )

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50, db: Session = Depends(get_db)):
    """Get chat history for a session"""
    from ..models.database_models import ChatMessage as ChatMessageModel
    
    messages = db.query(ChatMessageModel).filter(
        ChatMessageModel.session_id == session_id
    ).order_by(ChatMessageModel.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": msg.id,
            "user_message": msg.user_message,
            "bot_response": msg.bot_response,
            "intent": msg.intent,
            "action_taken": msg.action_taken,
            "success": msg.success,
            "created_at": msg.created_at
        } for msg in messages
    ]

@router.get("/stats")
async def get_chat_stats(db: Session = Depends(get_db)):
    """Get chatbot usage statistics"""
    from ..models.database_models import ChatMessage as ChatMessageModel
    from sqlalchemy import func
    
    # Total messages
    total_messages = db.query(func.count(ChatMessageModel.id)).scalar()
    
    # Messages by intent
    intent_stats = db.query(
        ChatMessageModel.intent,
        func.count(ChatMessageModel.id).label('count')
    ).group_by(ChatMessageModel.intent).all()
    
    # Success rate
    successful_messages = db.query(func.count(ChatMessageModel.id)).filter(
        ChatMessageModel.success == True
    ).scalar()
    
    success_rate = (successful_messages / total_messages * 100) if total_messages > 0 else 0
    
    return {
        "total_messages": total_messages,
        "success_rate": round(success_rate, 2),
        "intent_distribution": [
            {"intent": intent, "count": count} for intent, count in intent_stats
        ]
    }
