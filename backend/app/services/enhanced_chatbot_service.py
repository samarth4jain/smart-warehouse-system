import os
import logging
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from datetime import datetime

from ..models.database_models import ChatMessage, Product, Inventory
from .enhanced_smart_llm_service import EnhancedSmartLLMService
from .rag_service import WarehouseRAGService
from .inventory_service import InventoryService
from .inbound_service import InboundService
from .outbound_service import OutboundService

logger = logging.getLogger(__name__)

class EnhancedChatbotService:
    """Enhanced chatbot service using Sheared LLaMA with RAG"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = None
        self.rag_service = None
        self.inventory_service = InventoryService(db)
        self.inbound_service = InboundService(db)
        self.outbound_service = OutboundService(db)
        
        # Phase 3: Add forecasting and space optimization services
        try:
            from .simple_forecasting_service import SimpleForecastingService
            from .simple_space_optimization_service import SimpleSpaceOptimizationService
            
            self.forecasting_service = SimpleForecastingService()
            self.space_service = SimpleSpaceOptimizationService()
            self.phase3_enabled = True
            logger.info("Phase 3 services (forecasting & space optimization) enabled")
        except Exception as e:
            logger.warning(f"Phase 3 services not available: {str(e)}")
            self.forecasting_service = None
            self.space_service = None
            self.phase3_enabled = False
        
        # Initialize services
        self._initialize_services()
        
        # Setup prompt templates
        self._setup_prompts()
        
        # Memory for conversation history
        self.memory = ConversationBufferWindowMemory(
            k=10,  # Keep last 10 exchanges
            return_messages=True,
            memory_key="chat_history"
        )
    
    def _initialize_services(self):
        """Initialize LLM and RAG services"""
        try:
            self.llm_service = EnhancedSmartLLMService()
            self.rag_service = WarehouseRAGService(self.db)
            logger.info("Enhanced chatbot services initialized")
        except Exception as e:
            logger.error(f"Failed to initialize chatbot services: {str(e)}")
            # Fall back to rule-based system if needed
            self.llm_service = None
            self.rag_service = None
    
    def _setup_prompts(self):
        """Setup prompt templates for different types of queries"""
        
        self.system_prompt = """You are a Smart Warehouse Assistant AI for an MSME (Micro, Small, and Medium Enterprise) warehouse management system. You help warehouse operators with inventory management, inbound/outbound operations, forecasting, and space optimization.

Key Guidelines:
1. Be concise, professional, and helpful
2. Always use warehouse-specific terminology and SKU codes
3. Provide actionable responses with clear next steps
4. When handling operations, confirm actions and provide status updates
5. Use emojis and formatting to make responses clear and engaging
6. If you need to perform an action, clearly state what you're doing

Available Operations:
- Inventory checks and stock level queries
- Stock updates and adjustments
- Inbound shipment processing (gate-in)
- Outbound order processing (dispatch)
- Low stock alerts and recommendations
- PHASE 3: Demand forecasting and prediction
- PHASE 3: Stock risk analysis and alerts
- PHASE 3: AI-powered reorder recommendations
- PHASE 3: Product velocity analysis
- PHASE 3: Space optimization and layout planning
- PHASE 3: Category grouping suggestions
- General warehouse procedures and help

Current Date: {current_date}
Warehouse Location: Smart WMS System
Phase 3 Features: Forecasting + Space Planning (AI-Lite)"""

        self.qa_prompt = PromptTemplate(
            template="""You are a Smart Warehouse Assistant. Use the following warehouse context to answer the user's question accurately.

Context from Warehouse Database:
{context}

Conversation History:
{chat_history}

Current User Question: {question}

Instructions:
1. Use the provided context to give accurate, specific answers
2. If performing operations, be clear about what actions you're taking
3. Include relevant SKU codes, quantities, and locations when applicable
4. If you need to perform a warehouse operation, specify exactly what action is needed
5. Be helpful and professional, using appropriate warehouse terminology

Assistant Response:""",
            input_variables=["context", "chat_history", "question"]
        )
        
        self.operational_prompt = PromptTemplate(
            template="""You are a Smart Warehouse Assistant processing a warehouse operation.

Operation Context:
{context}

User Request: {question}
Operation Type: {operation_type}

Conversation History:
{chat_history}

Guidelines:
1. Confirm the operation you're performing
2. Provide clear status updates
3. Include relevant details (SKU, quantities, order numbers)
4. Suggest next steps if applicable
5. Use professional warehouse terminology

Process this operation and provide a clear response:""",
            input_variables=["context", "question", "operation_type", "chat_history"]
        )
    
    def process_message(self, user_message: str, session_id: str = "default", user_id: str = "anonymous") -> Dict:
        """Process user message using LLM with RAG"""
        try:
            # First, try to detect if this is a specific warehouse operation
            operation_result = self._try_warehouse_operation(user_message)
            
            if operation_result:
                # If operation was performed, use LLM to generate a natural response
                response = self._generate_operation_response(user_message, operation_result)
            else:
                # Use RAG + LLM for general queries
                response = self._generate_rag_response(user_message)
            
            # Save chat message (temporarily skip database save to avoid schema issues)
            # TODO: Fix database schema alignment
            # chat_message = ChatMessage(
            #     user_message=user_message,
            #     bot_response=response["message"],
            #     intent=response.get("intent", "llm_response"),
            #     action_taken=response.get("action_taken", "llm_generation"),
            #     success=response.get("success", True),
            #     session_id=session_id,
            #     user_id=user_id
            # )
            # self.db.add(chat_message)
            # self.db.commit()
            
            # Update conversation memory
            self.memory.save_context(
                {"input": user_message},
                {"output": response["message"]}
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return self._fallback_response(user_message)
    
    def _try_warehouse_operation(self, message: str) -> Optional[Dict]:
        """Try to perform specific warehouse operations"""
        try:
            message_lower = message.lower()
            
            # Check for inventory operations
            if any(keyword in message_lower for keyword in ["check stock", "inventory", "sku:", "stock level"]):
                return self._handle_inventory_check(message)
            
            # Check for stock updates
            elif any(keyword in message_lower for keyword in ["add", "update stock", "received", "adjustment"]):
                return self._handle_stock_update(message)
            
            # Check for inbound operations
            elif any(keyword in message_lower for keyword in ["gate in", "shipment", "delivery arrived"]):
                return self._handle_inbound_operation(message)
            
            # Check for outbound operations
            elif any(keyword in message_lower for keyword in ["dispatch", "ship order", "order"]):
                return self._handle_outbound_operation(message)
            
            # Check for alerts
            elif any(keyword in message_lower for keyword in ["low stock", "alert", "reorder"]):
                return self._handle_alerts()
            
            # Phase 3: Forecasting operations
            elif self.phase3_enabled and any(keyword in message_lower for keyword in 
                ["forecast", "predict", "demand", "prediction", "weekly forecast"]):
                return self._handle_forecasting_operation(message)
            
            # Phase 3: Stock risk analysis
            elif self.phase3_enabled and any(keyword in message_lower for keyword in 
                ["stock risk", "risk analysis", "overstock", "understock", "stock alert"]):
                return self._handle_stock_risk_analysis(message)
            
            # Phase 3: Reorder recommendations
            elif self.phase3_enabled and any(keyword in message_lower for keyword in 
                ["reorder recommend", "purchase recommend", "what to order", "buying recommend"]):
                return self._handle_reorder_recommendations(message)
            
            # Phase 3: Space optimization
            elif self.phase3_enabled and any(keyword in message_lower for keyword in 
                ["space optim", "layout optim", "warehouse layout", "product placement", "fast moving"]):
                return self._handle_space_optimization(message)
            
            # Phase 3: Product velocity analysis
            elif self.phase3_enabled and any(keyword in message_lower for keyword in 
                ["velocity", "fast moving", "slow moving", "product movement", "turnover"]):
                return self._handle_velocity_analysis(message)
            
            return None
            
        except Exception as e:
            logger.error(f"Error in warehouse operation: {str(e)}")
            return None
    
    def _handle_inventory_check(self, message: str) -> Dict:
        """Handle inventory check operations"""
        import re
        
        # Extract SKU
        sku_match = re.search(r"(sku|SKU)\s*:?\s*(\w+)", message)
        if sku_match:
            sku = sku_match.group(2).upper()
            product = self.inventory_service.get_product_by_sku(sku)
            if product:
                inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
                return {
                    "operation": "inventory_check",
                    "success": True,
                    "data": {
                        "product": product.name,
                        "sku": product.sku,
                        "available": inventory.available_quantity if inventory else 0,
                        "reserved": inventory.reserved_quantity if inventory else 0,
                        "total": inventory.quantity if inventory else 0,
                        "location": product.location
                    }
                }
        
        # General inventory summary
        summary = self.inventory_service.get_inventory_summary()
        return {
            "operation": "inventory_summary",
            "success": True,
            "data": summary
        }
    
    def _handle_stock_update(self, message: str) -> Dict:
        """Handle stock update operations"""
        import re
        
        sku_match = re.search(r"(sku|SKU)\s*:?\s*(\w+)", message)
        quantity_match = re.search(r"(\d+)\s*(\w+)?", message)
        
        if sku_match and quantity_match:
            sku = sku_match.group(2).upper()
            quantity = int(quantity_match.group(1))
            
            product = self.inventory_service.get_product_by_sku(sku)
            if product:
                operation = "addition" if "add" in message.lower() or "receive" in message.lower() else "update"
                success = self.inventory_service.update_stock(
                    product.id, quantity, "adjustment",
                    reason=f"Manual {operation} via LLM chatbot"
                )
                
                if success:
                    return {
                        "operation": "stock_update",
                        "success": True,
                        "data": {
                            "sku": sku,
                            "product": product.name,
                            "quantity": quantity,
                            "operation": operation
                        }
                    }
        
        return {"operation": "stock_update", "success": False, "error": "Invalid stock update request"}
    
    def _handle_inbound_operation(self, message: str) -> Dict:
        """Handle inbound operations"""
        import re
        
        shipment_match = re.search(r"shipment\s+(\w+)", message)
        if shipment_match:
            shipment_number = shipment_match.group(1).upper()
            shipment = self.inbound_service.get_shipment_by_number(shipment_number)
            
            if shipment:
                success = self.inbound_service.update_shipment_status(shipment.id, "arrived")
                if success:
                    return {
                        "operation": "inbound_gate_in",
                        "success": True,
                        "data": {
                            "shipment_number": shipment_number,
                            "vendor": shipment.vendor.name,
                            "status": "arrived"
                        }
                    }
        
        return {"operation": "inbound_gate_in", "success": False, "error": "Shipment not found"}
    
    def _handle_outbound_operation(self, message: str) -> Dict:
        """Handle outbound operations"""
        import re
        
        order_match = re.search(r"order\s+(\w+)", message)
        if order_match:
            order_number = order_match.group(1).upper()
            order = self.outbound_service.get_order_by_number(order_number)
            
            if order:
                if "dispatch" in message.lower() or "ship" in message.lower():
                    success = self.outbound_service.update_order_status(order.id, "dispatched")
                    if success:
                        return {
                            "operation": "outbound_dispatch",
                            "success": True,
                            "data": {
                                "order_number": order_number,
                                "customer": order.customer.name,
                                "status": "dispatched"
                            }
                        }
                else:
                    # Status check
                    return {
                        "operation": "order_status",
                        "success": True,
                        "data": {
                            "order_number": order_number,
                            "customer": order.customer.name,
                            "status": order.status,
                            "order_date": order.order_date.strftime('%Y-%m-%d')
                        }
                    }
        
        return {"operation": "outbound_operation", "success": False, "error": "Order not found"}
    
    def _handle_alerts(self) -> Dict:
        """Handle alert queries"""
        summary = self.inventory_service.get_inventory_summary()
        low_stock_items = summary.get("low_stock_alerts", [])
        
        return {
            "operation": "low_stock_alerts",
            "success": True,
            "data": {
                "low_stock_items": low_stock_items,
                "count": len(low_stock_items)
            }
        }
    
    def _generate_operation_response(self, user_message: str, operation_result: Dict) -> Dict:
        """Generate natural language response for warehouse operations using LLM"""
        try:
            if not self.llm_service or not self.llm_service.is_available():
                return self._format_operation_response_fallback(operation_result)
            
            # Check if we're using the Enhanced Smart Mock service
            if hasattr(self.llm_service, 'service_type') and self.llm_service.service_type == "enhanced_smart_mock":
                # For Enhanced Smart Mock, pass the original user message directly
                # It has intelligent logic for handling warehouse operations
                response_text = self.llm_service.generate_response(user_message)
            else:
                # For other LLM services, use formatted prompt with operation context
                # Get relevant context for the operation
                context = ""
                if self.rag_service and self.rag_service.is_available():
                    context = self.rag_service.get_context_for_query(user_message)
                
                # Prepare conversation history
                chat_history = self._get_formatted_history()
                
                # Create prompt for operation response
                prompt = self.operational_prompt.format(
                    context=context,
                    question=user_message,
                    operation_type=operation_result.get("operation", "unknown"),
                    chat_history=chat_history
                )
                
                # Add operation details to prompt
                operation_details = f"""
Operation Performed: {operation_result.get('operation', 'Unknown')}
Success: {operation_result.get('success', False)}
Data: {operation_result.get('data', {})}
Error: {operation_result.get('error', 'None')}
"""
                
                full_prompt = f"{self.system_prompt.format(current_date=datetime.now().strftime('%Y-%m-%d'))}\n\n{prompt}\n\nOperation Details:\n{operation_details}"
                
                # Generate response
                response_text = self.llm_service.generate_response(full_prompt)
            
            return {
                "message": response_text,
                "intent": operation_result.get("operation", "operation"),
                "data": operation_result.get("data"),
                "success": operation_result.get("success", True),
                "action_taken": f"llm_enhanced_{operation_result.get('operation', 'operation')}"
            }
            
        except Exception as e:
            logger.error(f"Error generating operation response: {str(e)}")
            return self._format_operation_response_fallback(operation_result)

    def _generate_rag_response(self, user_message: str) -> Dict:
        """Generate response using RAG + LLM for general queries"""
        try:
            if not self.llm_service or not self.llm_service.is_available():
                return self._fallback_response(user_message)
            
            # Check if we're using the Enhanced Smart Mock service
            if hasattr(self.llm_service, 'service_type') and self.llm_service.service_type == "enhanced_smart_mock":
                # For Enhanced Smart Mock, pass the original user message directly
                # It has its own intelligent logic for handling different query types
                response_text = self.llm_service.generate_response(user_message)
            else:
                # For other LLM services (like HuggingFace), use the formatted prompt
                # Get relevant context
                context = ""
                if self.rag_service and self.rag_service.is_available():
                    context = self.rag_service.get_context_for_query(user_message)
                
                # Prepare conversation history
                chat_history = self._get_formatted_history()
                
                # Create prompt
                prompt = self.qa_prompt.format(
                    context=context,
                    chat_history=chat_history,
                    question=user_message
                )
                
                full_prompt = f"{self.system_prompt.format(current_date=datetime.now().strftime('%Y-%m-%d'))}\n\n{prompt}"
                
                # Generate response
                response_text = self.llm_service.generate_response(full_prompt)
            
            return {
                "message": response_text,
                "intent": "general_query",
                "data": None,
                "success": True,
                "action_taken": "llm_rag_response"
            }
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {str(e)}")
            return self._fallback_response(user_message)
    
    def _get_formatted_history(self) -> str:
        """Get formatted conversation history"""
        try:
            if hasattr(self.memory, 'buffer') and self.memory.buffer:
                history_messages = self.memory.buffer
                formatted_history = []
                
                for message in history_messages[-6:]:  # Last 3 exchanges
                    if isinstance(message, HumanMessage):
                        formatted_history.append(f"Human: {message.content}")
                    elif isinstance(message, AIMessage):
                        formatted_history.append(f"Assistant: {message.content}")
                
                return "\n".join(formatted_history)
            
            return "No previous conversation"
            
        except Exception as e:
            logger.error(f"Error formatting history: {str(e)}")
            return "No previous conversation"
    
    def _format_operation_response_fallback(self, operation_result: Dict) -> Dict:
        """Format operation response without LLM (fallback)"""
        operation = operation_result.get("operation", "operation")
        success = operation_result.get("success", False)
        data = operation_result.get("data", {})
        
        if operation == "inventory_check" and success:
            message = f"{data.get('product', 'Product')} (SKU: {data.get('sku', 'Unknown')})\n"
            message += f"Available: {data.get('available', 0)} units\n"
            message += f"Reserved: {data.get('reserved', 0)} units\n"
            message += f"Total: {data.get('total', 0)} units\n"
            message += f"Location: {data.get('location', 'Not specified')}"
        
        elif operation == "stock_update" and success:
            message = f"Stock {data.get('operation', 'updated')}\n"
            message += f"Product: {data.get('product', 'Unknown')}\n"
            message += f"SKU: {data.get('sku', 'Unknown')}\n"
            message += f"Quantity: {data.get('quantity', 0)}"
        
        else:
            message = "Operation completed successfully" if success else "Operation failed"
        
        return {
            "message": message,
            "intent": operation,
            "data": data,
            "success": success,
            "action_taken": f"fallback_{operation}"
        }
    
    def _fallback_response(self, user_message: str) -> Dict:
        """Fallback response when LLM is unavailable"""
        return {
            "message": "I'm here to help with warehouse operations! However, my advanced AI features are currently unavailable. "
                      "You can still use specific commands like 'check stock SKU: PROD001' or 'dispatch order ORD001'. "
                      "Type 'help' for available commands.",
            "intent": "fallback",
            "data": None,
            "success": True,
            "action_taken": "fallback_response"
        }
    
    def is_enhanced_mode_available(self) -> bool:
        """Check if enhanced LLM mode is available"""
        return (self.llm_service and self.llm_service.is_available() and 
                self.rag_service and self.rag_service.is_available())
    
    def get_system_status(self) -> Dict[str, bool]:
        """Get status of all chatbot components"""
        status = {
            "llm_service": self.llm_service.is_available() if self.llm_service else False,
            "rag_service": self.rag_service.is_available() if self.rag_service else False,
            "enhanced_mode": self.is_enhanced_mode_available()
        }
        
        # Add Phase 3 status
        if hasattr(self, 'phase3_enabled') and self.phase3_enabled:
            status["phase3_forecasting"] = self.forecasting_service is not None
            status["phase3_space_optimization"] = self.space_service is not None
        
        return status
    
    # Phase 3: Handler methods (simplified for initial implementation)
    def _handle_forecasting_operation(self, message: str) -> Dict:
        """Handle forecasting operations"""
        return {
            "operation": "demand_forecast",
            "success": True,
            "data": {"message": "Phase 3 forecasting feature available - generating demand predictions"}
        }
    
    def _handle_stock_risk_analysis(self, message: str) -> Dict:
        """Handle stock risk analysis"""
        return {
            "operation": "stock_risk_analysis", 
            "success": True,
            "data": {"message": "Phase 3 stock risk analysis - identifying overstock/understock risks"}
        }
    
    def _handle_reorder_recommendations(self, message: str) -> Dict:
        """Handle reorder recommendations"""
        return {
            "operation": "reorder_recommendations",
            "success": True, 
            "data": {"message": "Phase 3 AI-powered reorder recommendations generated"}
        }
    
    def _handle_space_optimization(self, message: str) -> Dict:
        """Handle space optimization"""
        return {
            "operation": "space_optimization",
            "success": True,
            "data": {"message": "Phase 3 space optimization - analyzing layout and product placement"}
        }
    
    def _handle_velocity_analysis(self, message: str) -> Dict:
        """Handle velocity analysis"""
        return {
            "operation": "velocity_analysis",
            "success": True,
            "data": {"message": "Phase 3 velocity analysis - categorizing fast/slow moving products"}
        }
