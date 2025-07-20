import re
from typing import Dict, List, Tuple, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..models.database_models import (
    Product, Inventory, InboundShipment, InboundItem, 
    OutboundOrder, OutboundItem, Vendor, Customer, ChatMessage, StockMovement
)
from .inventory_service import InventoryService
from .inbound_service import InboundService
from .outbound_service import OutboundService
from .enhanced_nlp_processor import EnhancedNLPProcessor

class ChatbotService:
    """Enhanced chatbot service with natural language understanding for layman queries"""
    
    def __init__(self, db: Session):
        self.db = db
        self.inventory_service = InventoryService(db)
        self.inbound_service = InboundService(db)
        self.outbound_service = OutboundService(db)
        self.enhanced_nlp = EnhancedNLPProcessor()  # Enhanced NLP processor
        
        # Phase 3 services (if available)
        try:
            from .forecasting_service import ForecastingService
            from .space_optimization_service import SpaceOptimizationService
            
            self.forecasting_service = ForecastingService()
            self.space_service = SpaceOptimizationService()
            self.phase3_enabled = True
        except Exception:
            self.forecasting_service = None
            self.space_service = None
            self.phase3_enabled = False

    def process_message(self, user_message: str, session_id: str = "default", user_id: str = "anonymous") -> Dict:
        """Process user message with enhanced natural language understanding for layman queries"""
        original_message = user_message.strip()
        
        # Enhanced error handling and validation
        if not original_message:
            return {
                "message": "I didn't receive a message. Please try asking me something about your warehouse operations.",
                "intent": "empty_input",
                "confidence": 1.0,
                "entities": {},
                "context": {},
                "success": False,
                "suggestions": ["Check inventory", "View alerts", "Get help", "System status"]
            }
        
        # Enhanced message preprocessing
        processed_message = self._preprocess_message(original_message)
        
        try:
            # Use enhanced NLP for better layman language understanding
            nlp_result = self.enhanced_nlp.process_layman_query(processed_message)
            
            intent = nlp_result["intent"]
            confidence = nlp_result["confidence"]
            entities = nlp_result["entities"]
            context = nlp_result["context"]
            response_style = nlp_result["response_style"]
            
            # Fallback to original NLP if confidence is low or enhanced NLP fails
            if confidence < 0.4:
                try:
                    intent, confidence, entities = self.nlp.classify_intent_enhanced(processed_message)
                    context = self.nlp.extract_conversational_context(processed_message)
                    response_style = "casual" if context.get("formality") != "formal" else "formal"
                    
                    # Boost confidence if we found good entities
                    if entities and len(entities) > 0:
                        confidence = min(0.8, confidence + 0.2)
                        
                except Exception as nlp_error:
                    # Fallback to basic pattern matching
                    intent, confidence, entities = self._basic_pattern_matching(processed_message)
                    context = {"formality": "casual", "urgency": "normal"}
                    response_style = "casual"
            
        except Exception as e:
            # Robust error handling - don't let NLP errors break the chatbot
            print(f"Warning: NLP processing failed: {e}")
            intent, confidence, entities = self._basic_pattern_matching(processed_message)
            context = {"formality": "casual", "urgency": "normal"}
            response_style = "casual"
        
        # Process based on enhanced intent with context awareness
        response_data = self._process_enhanced_intent_with_context(
            intent, original_message, entities, context, response_style
        )
        
        # Add conversational elements based on context
        response_data = self._enhance_response_with_personality(response_data, context, response_style)
        
        # Enhanced response validation
        if not response_data or not response_data.get("message"):
            response_data = self._generate_fallback_response(original_message, intent)
        
        # Save chat message with enhanced error handling
        try:
            chat_message = ChatMessage(
                user_message=original_message,
                bot_response=response_data["message"],
                intent=intent,
                action_taken=response_data.get("action_taken", ""),
                success=response_data.get("success", True),
                session_id=session_id,
                user_id=user_id
            )
            self.db.add(chat_message)
            self.db.commit()
        except Exception as db_error:
            # If database save fails, log it but don't break the response
            print(f"Warning: Could not save chat message to database: {db_error}")
            try:
                self.db.rollback()
            except:
                pass  # Even rollback might fail in some cases
        
        return {
            "message": response_data["message"],
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "context": context,
            "data": response_data.get("data"),
            "actions": response_data.get("actions", []),
            "suggestions": response_data.get("suggestions", []),
            "success": response_data.get("success", True),
            "enhanced_mode": True,
            "response_time": datetime.now().isoformat()
        }

    def _preprocess_message(self, message: str) -> str:
        """Enhanced message preprocessing"""
        # Remove extra whitespace
        message = ' '.join(message.split())
        
        # Fix common typos and expand contractions
        contractions = {
            "whats": "what is",
            "wheres": "where is",
            "hows": "how is", 
            "cant": "cannot",
            "dont": "do not",
            "wont": "will not",
            "shouldnt": "should not",
            "couldnt": "could not",
            "wouldnt": "would not",
            "thats": "that is",
            "theres": "there is",
            "theyre": "they are",
            "youre": "you are",
            "im": "i am",
            "ive": "i have",
            "weve": "we have"
        }
        
        for contraction, expansion in contractions.items():
            message = message.replace(contraction, expansion)
        
        return message.strip()

    def _basic_pattern_matching(self, message: str) -> Tuple[str, float, Dict]:
        """Basic pattern matching fallback when NLP fails"""
        message_lower = message.lower()
        
        # Basic intent patterns
        patterns = {
            "inventory_check": [
                r"(?:check|show|get|find|display|list).*(?:inventory|stock|level|quantity)",
                r"(?:how many|how much|what.*quantity).*(?:do we have|in stock|available)",
                r"(?:stock|inventory).*(?:level|status|check|information)"
            ],
            "low_stock_alert": [
                r"(?:low|running low|empty|out).*(?:stock|inventory)",
                r"(?:what|which|any).*(?:items|products).*(?:low|running low|need reorder)",
                r"(?:show|display|list).*(?:low stock|reorder)"
            ],
            "product_search": [
                r"(?:find|search|locate|where).*(?:product|item)",
                r"(?:where|location).*(?:of|for|is)",
                r"(?:search|find|lookup|check).*(?:[A-Z]{2,}[0-9]{2,})"  # SKU pattern
            ],
            "help": [
                r"(?:help|what.*do|how.*work|what.*can)",
                r"(?:support|assistance|guide|tutorial)",
                r"(?:how.*use|instructions)"
            ],
            "status": [
                r"(?:status|health|how.*things|everything.*ok)",
                r"(?:system.*status|overall.*status)",
                r"(?:any.*problems|any.*issues|any.*alerts)"
            ]
        }
        
        best_intent = "general_query"
        best_confidence = 0.3
        
        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, message_lower):
                    confidence = 0.7 if intent == "help" else 0.6
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = confidence
                        break
        
        # Extract basic entities
        entities = {}
        
        # SKU extraction
        sku_match = re.search(r"([A-Z]{2,}[0-9]{2,})", message, re.IGNORECASE)
        if sku_match:
            entities["sku"] = sku_match.group(1).upper()
        
        # Product name extraction
        product_keywords = ["mouse", "keyboard", "laptop", "monitor", "headphone", "tablet", "cable", "charger"]
        for keyword in product_keywords:
            if keyword in message_lower:
                entities["product_type"] = keyword
                break
        
        return best_intent, best_confidence, entities

    def _generate_fallback_response(self, message: str, intent: str) -> Dict:
        """Generate a helpful fallback response when processing fails"""
        return {
            "message": f"""I understand you're asking about "{message}". While I'm processing your request, here's what I can help you with:

**Warehouse Operations I Support:**
• **Inventory Management** - Check stock levels, find products, monitor alerts
• **Order Processing** - Track shipments, manage deliveries, update status
• **Analytics & Reports** - Performance metrics, trends, insights
• **System Monitoring** - Alerts, health checks, operational status

**Try These Examples:**
• "Show low stock items"
• "Check laptop inventory" 
• "What needs attention today?"
• "Generate performance report"

**Natural Language Support:**
Feel free to ask in your own words - I understand conversational language and can help with complex warehouse management tasks.

What specific area would you like me to help you with?""",
            "success": True,
            "action_taken": "provided_help_and_examples",
            "data": None,
            "suggestions": ["Check inventory", "View alerts", "Generate reports", "Get system status"]
        }

    def _process_enhanced_intent_with_context(self, intent: str, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Process intent with enhanced understanding, context awareness, and appropriate response style"""
        try:
            if intent == "inventory_check":
                return self._handle_layman_inventory_check(message, entities, context, response_style)
            elif intent == "inbound_operations":
                return self._handle_layman_inbound(message, entities, context, response_style)
            elif intent == "outbound_operations":
                return self._handle_layman_outbound(message, entities, context, response_style)
            elif intent == "stock_update":
                return self._handle_layman_stock_update(message, entities, context, response_style)
            elif intent == "order_status":
                return self._handle_layman_order_status(message, entities, context, response_style)
            elif intent == "alerts_monitoring":
                return self._handle_layman_alerts(message, entities, context, response_style)
            elif intent == "reporting_analytics":
                return self._handle_layman_reporting(message, entities, context, response_style)
            elif intent == "help_general":
                return self._handle_layman_help(message, entities, context, response_style)
            else:
                return self._handle_layman_general(message, entities, context, response_style)
        except Exception as e:
            error_msg = self._get_error_message(str(e), response_style)
            return {
                "message": error_msg,
                "success": False,
                "action_taken": "error_occurred",
                "suggestions": self._get_error_suggestions(response_style)
            }

    def _handle_layman_inventory_check(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Enhanced inventory check handler for layman language"""
        
        # Check if we have specific product identification
        product = None
        search_term = None
        
        if "sku" in entities:
            search_term = entities["sku"]
            product = self.inventory_service.get_product_by_sku(search_term)
        elif "product_name" in entities:
            search_term = entities["product_name"]
            # Try to find product by name (fuzzy matching)
            product = self._find_product_by_name(search_term)
        
        if product:
            return self._generate_inventory_response(product, response_style, context)
        elif search_term:
            return self._generate_product_not_found_response(search_term, response_style, context)
        else:
            return self._generate_need_product_info_response(response_style, context)
    
    def _find_product_by_name(self, product_name: str) -> Optional[Product]:
        """Find product by name with fuzzy matching for layman queries"""
        # First try exact match
        products = self.db.query(Product).all()
        
        # Try exact match (case insensitive)
        for product in products:
            if product.name.lower() == product_name.lower():
                return product
        
        # Try partial match
        for product in products:
            if product_name.lower() in product.name.lower() or product.name.lower() in product_name.lower():
                return product
        
        # Try fuzzy matching on words
        product_words = product_name.lower().split()
        for product in products:
            product_name_words = product.name.lower().split()
            if any(word in product_name_words for word in product_words):
                return product
        
        return None
    
    def _generate_inventory_response(self, product: Product, response_style: str, context: Dict) -> Dict:
        """Generate appropriate inventory response based on style and context"""
        inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
        
        if not inventory:
            return self._generate_no_inventory_response(product, response_style)
        
        stock_level = inventory.available_quantity
        reorder_level = product.reorder_level or 10
        
        # Determine stock status
        if stock_level <= 0:
            status = "empty"
        elif stock_level <= reorder_level:
            status = "low"
        else:
            status = "good"
        
        # Generate response based on style and status
        if response_style == "casual":
            response_msg = self._generate_casual_inventory_response(product, inventory, status, context)
        elif response_style == "urgent":
            response_msg = self._generate_urgent_inventory_response(product, inventory, status, context)
        else:
            response_msg = self._generate_formal_inventory_response(product, inventory, status, context)
        
        # Generate suggestions based on status
        suggestions = self._generate_inventory_suggestions(status, product)
        
        return {
            "message": response_msg,
            "data": {
                "product": product.name,
                "sku": product.sku,
                "available": stock_level,
                "reserved": inventory.reserved_quantity,
                "total": inventory.quantity,
                "status": status,
                "reorder_level": reorder_level
            },
            "suggestions": suggestions,
            "success": True,
            "action_taken": f"inventory_check_for_{product.sku}"
        }
    
    def _generate_casual_inventory_response(self, product: Product, inventory: Inventory, status: str, context: Dict) -> str:
        """Generate casual response for inventory check"""
        greeting = self._get_casual_greeting(context)
        
        if status == "empty":
            return f"{greeting}Uh oh! We're completely out of **{product.name}** 😟\n\n" \
                   f"📦 Available: 0 {product.unit}\n" \
                   f"🔒 Reserved: {inventory.reserved_quantity} {product.unit}\n" \
                   f"📍 Location: {product.location or 'Not specified'}\n\n" \
                   f"💡 **Action needed**: Time to reorder!"
        
        elif status == "low":
            return f"{greeting}Heads up! We're running low on **{product.name}** 🔔\n\n" \
                   f"📦 Available: {inventory.available_quantity} {product.unit}\n" \
                   f"🔒 Reserved: {inventory.reserved_quantity} {product.unit}\n" \
                   f"📍 Location: {product.location or 'Not specified'}\n" \
                   f"⚠️ Reorder level: {product.reorder_level or 10} {product.unit}\n\n" \
                   f"💡 **Suggestion**: Might want to reorder soon!"
        
        else:
            return f"{greeting}Good news! We've got plenty of **{product.name}** ✅\n\n" \
                   f"📦 Available: {inventory.available_quantity} {product.unit}\n" \
                   f"🔒 Reserved: {inventory.reserved_quantity} {product.unit}\n" \
                   f"📍 Location: {product.location or 'Not specified'}\n\n" \
                   f"💡 **Status**: Stock levels look healthy!"
    
    def _generate_urgent_inventory_response(self, product: Product, inventory: Inventory, status: str, context: Dict) -> str:
        """Generate urgent response for inventory check"""
        if status == "empty":
            return f"🚨 **CRITICAL ALERT**: {product.name} is OUT OF STOCK!\n\n" \
                   f"📦 Available: 0 {product.unit}\n" \
                   f"📍 Location: {product.location or 'Not specified'}\n" \
                   f"⚡ **IMMEDIATE ACTION REQUIRED**: Emergency reorder needed!"
        
        elif status == "low":
            return f"🔔 **URGENT WARNING**: {product.name} critically low!\n\n" \
                   f"📦 Available: {inventory.available_quantity} {product.unit}\n" \
                   f"⚠️ Reorder level: {product.reorder_level or 10} {product.unit}\n" \
                   f"📍 Location: {product.location or 'Not specified'}\n" \
                   f"⚡ **ACTION NEEDED**: Reorder ASAP!"
        
        else:
            return f"✅ **URGENT CHECK COMPLETE**: {product.name} adequately stocked\n\n" \
                   f"📦 Available: {inventory.available_quantity} {product.unit}\n" \
                   f"📍 Location: {product.location or 'Not specified'}\n" \
                   f"💡 **Status**: Stock levels sufficient for urgent needs"
    
    def _generate_formal_inventory_response(self, product: Product, inventory: Inventory, status: str, context: Dict) -> str:
        """Generate formal response for inventory check"""
        status_text = {
            "empty": "OUT OF STOCK",
            "low": "LOW STOCK ALERT", 
            "good": "STOCK ADEQUATE"
        }
        
        return f"**INVENTORY REPORT - {status_text[status]}**\n\n" \
               f"Product: {product.name}\n" \
               f"SKU: {product.sku}\n" \
               f"Available Quantity: {inventory.available_quantity} {product.unit}\n" \
               f"Reserved Quantity: {inventory.reserved_quantity} {product.unit}\n" \
               f"Total Inventory: {inventory.quantity} {product.unit}\n" \
               f"Location: {product.location or 'Not specified'}\n" \
               f"Reorder Level: {product.reorder_level or 10} {product.unit}\n\n" \
               f"Status: {status_text[status]}"

    def _get_casual_greeting(self, context: Dict) -> str:
        """Get appropriate casual greeting based on context"""
        if context.get("is_greeting"):
            return "Hey there! "
        elif context.get("is_urgent"):
            return ""
        elif context.get("is_polite"):
            return "Sure thing! "
        else:
            return ""
    
    def _generate_inventory_suggestions(self, status: str, product: Product) -> List[str]:
        """Generate suggestions based on inventory status"""
        if status == "empty":
            return [
                "Reorder this product immediately",
                "Check supplier availability",
                "Look for alternative products",
                "Set up low stock alerts"
            ]
        elif status == "low":
            return [
                "Reorder this product soon",
                "Check usage patterns",
                "Adjust reorder levels",
                "Review supplier lead times"
            ]
        else:
            return [
                "Update stock count if needed",
                "Check product location",
                "Review product details",
                "Set up automated reordering"
            ]
    
    def _generate_product_not_found_response(self, search_term: str, response_style: str, context: Dict) -> Dict:
        """Generate response when product is not found"""
        if response_style == "casual":
            message = f"Hmm, I couldn't find anything for '{search_term}' 🤔\n\n" \
                     f"💡 **Try these instead:**\n" \
                     f"• Use the exact product name\n" \
                     f"• Try a SKU code (like PROD001)\n" \
                     f"• Check for typos\n" \
                     f"• Ask me to 'show all products'"
        elif response_style == "urgent":
            message = f"⚠️ **PRODUCT NOT FOUND**: '{search_term}'\n\n" \
                     f"🔍 **IMMEDIATE ACTIONS**:\n" \
                     f"• Verify product name/SKU\n" \
                     f"• Check product database\n" \
                     f"• Contact system administrator"
        else:
            message = f"**PRODUCT SEARCH RESULT**: No matches found\n\n" \
                     f"Search term: '{search_term}'\n" \
                     f"Recommendations:\n" \
                     f"• Verify product name or SKU code\n" \
                     f"• Use exact product naming\n" \
                     f"• Check product database integrity"
        
        return {
            "message": message,
            "success": False,
            "action_taken": f"product_not_found_{search_term}",
            "suggestions": ["Try different search terms", "View all products", "Check product catalog"]
        }
    
    def _generate_need_product_info_response(self, response_style: str, context: Dict) -> Dict:
        """Generate response when more product information is needed"""
        if response_style == "casual":
            message = "I'd love to help you check stock! 😊\n\n" \
                     "Could you tell me which product you're asking about?\n\n" \
                     "💡 **You can say things like:**\n" \
                     "• 'Check stock for blue widgets'\n" \
                     "• 'Do we have any PROD001?'\n" \
                     "• 'How much inventory for laptops?'\n" \
                     "• 'Show me SKU WIDGET001'"
        elif response_style == "urgent":
            message = "⚡ **URGENT INVENTORY CHECK** - Product identification required\n\n" \
                     "Please specify:\n" \
                     "• Product name\n" \
                     "• SKU code\n" \
                     "• Product category"
        else:
            message = "**INVENTORY QUERY** - Additional information required\n\n" \
                     "Please provide:\n" \
                     "• Product name or SKU code\n" \
                     "• Specific product identifier\n\n" \
                     "Format examples:\n" \
                     "• 'Check stock SKU: PROD001'\n" \
                     "• 'Inventory status for Product Name'"
        
        return {
            "message": message,
            "success": True,
            "action_taken": "requested_product_info",
            "suggestions": ["Specify product name", "Use SKU code", "Browse product catalog"]
        }

    def _get_error_message(self, error: str, response_style: str) -> str:
        """Generate appropriate error message based on response style"""
        if response_style == "casual":
            return f"Oops! Something went wrong 😅\n\nI ran into this issue: {error}\n\nLet me try to help you another way!"
        elif response_style == "urgent":
            return f"🚨 **SYSTEM ERROR** - {error}\n\n⚡ **IMMEDIATE ACTION**: Contact system administrator"
        else:
            return f"**SYSTEM ERROR OCCURRED**\n\nError Details: {error}\n\nPlease try again or contact technical support."
    
    def _get_error_suggestions(self, response_style: str) -> List[str]:
        """Generate error suggestions based on response style"""
        if response_style == "urgent":
            return ["Contact system administrator", "Try basic commands", "Check system status"]
        else:
            return ["Try rephrasing your request", "Ask for help", "Use simpler commands", "Check system status"]

    # Placeholder methods for other layman handlers (to be implemented)
    def _handle_layman_inbound(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle inbound operations with layman language"""
        # Use existing implementation for now, but with enhanced response style
        return self._handle_conversational_inbound(message, entities, context)
    
    def _handle_layman_outbound(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle outbound operations with layman language"""
        return self._handle_conversational_outbound(message, entities, context)
    
    def _handle_layman_stock_update(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle stock updates with layman language"""
        return self._handle_conversational_stock_update(message, entities, context)
    
    def _handle_layman_order_status(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle order status with layman language"""
        return self._handle_conversational_order_status(message, entities, context)
    
    def _handle_layman_alerts(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle alerts monitoring with layman language"""
        return self._handle_conversational_alerts(message, entities, context)
    
    def _handle_layman_reporting(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle reporting with layman language"""
        return self._handle_conversational_reporting(message, entities, context)
    
    def _handle_layman_help(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle help requests with layman language"""
        return self._handle_conversational_help_enhanced(message, entities, context, response_style)
    
    def _handle_layman_general(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle general queries with layman language"""
        return self._handle_conversational_general_enhanced(message, entities, context, response_style)

    # Enhanced personality method to handle different response styles
    def _enhance_response_with_personality(self, response_data: Dict, context: Dict, response_style: str = "casual") -> Dict:
        """Enhanced personality based on context and response style"""
        # Add greeting if context suggests it
        if context.get("is_greeting") and not response_data["message"].lower().startswith(("hi", "hello", "hey")):
            if response_style == "casual":
                response_data["message"] = "Hey there! " + response_data["message"]
            elif response_style == "formal":
                response_data["message"] = "Hello. " + response_data["message"]
        
        # Add politeness acknowledgment
        if context.get("is_polite") and response_style == "casual":
            response_data["message"] = response_data["message"].replace("I'd love to help", "I'd be happy to help")
        
        # Add urgency indicators
        if context.get("is_urgent") or response_style == "urgent":
            if "suggestions" in response_data:
                response_data["suggestions"].insert(0, "Handle this urgently")
        
        return response_data
    
    def _handle_conversational_help_enhanced(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Enhanced help handler with different response styles"""
        
        if response_style == "casual":
            help_text = """
Hey! I'm your warehouse assistant and I'm here to make things easy! 😊

**Here's what I can help you with:**

🔍 **Check Stock** (just ask naturally!)
• "Do we have any blue widgets?"
• "How much inventory do we have for laptops?"
• "Check stock for PROD001"
• "Where are the red chairs?"

📦 **Manage Deliveries**
• "Truck just arrived!"
• "We got a delivery for shipment SH001"
• "Need to receive goods"

🚚 **Handle Orders**
• "Customer needs their order shipped"
• "Dispatch order ORD001"
• "Is order ready to go out?"

**Stock Updates**
• "We just got 50 more widgets"
• "Add 25 units to inventory"
• "Fix the count for PROD001"

⚠️ **Check Alerts**
• "What needs attention?"
• "Any low stock items?"
• "Show me problems"

Just talk to me naturally - I understand casual language!
            """
        elif response_style == "urgent":
            help_text = """
🚨 **URGENT SYSTEM HELP** 

**IMMEDIATE OPERATIONS AVAILABLE:**

⚡ **Critical Stock Checks**
• "URGENT: Check stock for [PRODUCT]"
• "Emergency inventory status"

⚡ **Priority Operations**  
• "RUSH order [ORDER_NUMBER]"
• "ASAP dispatch [ORDER_NUMBER]"
• "Emergency reorder [PRODUCT]"

⚡ **Alert Management**
• "Critical alerts"
• "System status check"
• "Emergency procedures"

**FORMAT FOR URGENT REQUESTS:**
Start with "URGENT:", "ASAP:", or "PRIORITY:"
            """
        else:
            help_text = """
**SMART WAREHOUSE ASSISTANT - COMMAND REFERENCE**

**Inventory Management:**
• Stock Level Queries: "Check stock SKU: [SKU]" or "Inventory for [Product Name]"
• Location Queries: "Where is [Product]?" or "Location of SKU: [SKU]"

**Inbound Operations:**
• Gate-In Processing: "Gate in shipment [SHIPMENT_ID]"
• Delivery Processing: "Process delivery [SHIPMENT_ID]"

**Outbound Operations:**
• Order Dispatch: "Dispatch order [ORDER_ID]"
• Shipping Status: "Check order status [ORDER_ID]"

**Stock Management:**
• Manual Updates: "Add [QUANTITY] units SKU: [SKU]"
• Stock Adjustments: "Update stock [SKU] to [QUANTITY]"

**Monitoring & Alerts:**
• Low Stock Alerts: "Show low stock alerts"
• System Status: "System health check"

**Reporting:**
• Inventory Summary: "Show inventory summary"
• Performance Metrics: "Generate daily report"
            """
        
        return {
            "message": help_text.strip(),
            "success": True,
            "action_taken": "help_provided",
            "suggestions": [
                "Try asking about stock",
                "Check order status", 
                "View inventory alerts",
                "Process deliveries"
            ]
        }
    
    def _handle_conversational_general_enhanced(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Enhanced general handler with context awareness"""
        
        # Try to extract any useful information from the message
        if "thank" in message.lower():
            if response_style == "casual":
                response = "You're welcome! Happy to help! 😊\n\nAnything else I can do for you?"
            else:
                response = "You're welcome. Is there anything else I can assist you with?"
        
        elif context.get("is_greeting"):
            if response_style == "casual":
                response = "Hey there! 👋 I'm your warehouse assistant!\n\nI can help you check stock, process orders, manage deliveries, and lots more.\n\nWhat would you like to do today?"
            elif response_style == "urgent":
                response = "⚡ **WAREHOUSE SYSTEM READY**\n\nEmergency operations available. What urgent task do you need assistance with?"
            else:
                response = "Hello. I am the Smart Warehouse Assistant.\n\nI can help with inventory management, order processing, and warehouse operations.\n\nHow may I assist you today?"
        
        elif context.get("is_uncertain"):
            if response_style == "casual":
                response = "No worries! I'm here to help figure things out 😊\n\nTry asking me about:\n• Stock levels\n• Order status\n• Processing deliveries\n• Or just say 'help' for more options!"
            else:
                response = "I understand you need assistance. I can help with warehouse operations including inventory checks, order processing, and system monitoring.\n\nPlease let me know what specific task you need help with."
        
        else:
            if response_style == "casual":
                response = "I'm here to help with your warehouse operations! 🏭\n\nI can check stock, process orders, handle deliveries, and much more.\n\nTry asking me something like:\n• 'Do we have any laptops?'\n• 'Process the delivery that just arrived'\n• 'Show me low stock alerts'\n\nOr just type 'help' to see everything I can do!"
            elif response_style == "urgent":
                response = "⚡ **SYSTEM STANDING BY**\n\nReady for urgent warehouse operations.\n\nAvailable functions:\n• Emergency stock checks\n• Priority order processing\n• Critical alert monitoring\n\nPlease specify your urgent request."
            else:
                response = "I am ready to assist with warehouse management operations.\n\nAvailable services:\n• Inventory management and stock level queries\n• Inbound and outbound order processing\n• System monitoring and alert management\n• Reporting and analytics\n\nPlease specify your request or type 'help' for detailed command reference."
        
        suggestions = []
        if response_style == "casual":
            suggestions = [
                "Ask about stock levels",
                "Check order status",
                "Process a delivery",
                "View alerts",
                "Get help"
            ]
        elif response_style == "urgent":
            suggestions = [
                "Emergency stock check",
                "Priority order processing",
                "Critical alerts",
                "System status"
            ]
        else:
            suggestions = [
                "Inventory management",
                "Order processing",
                "System monitoring",
                "View help documentation"
            ]
        
        return {
            "message": response,
            "success": True,
            "action_taken": "general_assistance_provided",
            "suggestions": suggestions
        }
    
    def _handle_conversational_alerts(self, message: str, entities: Dict, context: Dict) -> Dict:
        """Handle alerts and monitoring queries conversationally"""
        greeting = self._get_casual_greeting(context)
        
        try:
            # Get low stock items
            low_stock_products = []
            products = self.db.query(Product).all()
            
            for product in products:
                inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
                if inventory and inventory.available_quantity <= (product.reorder_level or 10):
                    low_stock_products.append({
                        "product": product,
                        "inventory": inventory,
                        "status": "empty" if inventory.available_quantity <= 0 else "low"
                    })
            
            if not low_stock_products:
                response_msg = f"{greeting}Great news! Everything looks good in the warehouse!\n\n" \
                              f"✅ **All products are well-stocked**\n" \
                              f"📈 **No low stock alerts**\n" \
                              f"🔄 **All systems running smoothly**\n\n" \
                              f"💡 **Keep up the good work!**"
                
                return {
                    "message": response_msg,
                    "data": {"low_stock_count": 0, "status": "healthy"},
                    "suggestions": ["Check specific products", "View inventory summary", "Add stock"],
                    "success": True,
                    "action_taken": "alerts_check_healthy"
                }
            
            # Format low stock items
            critical_items = [item for item in low_stock_products if item["status"] == "empty"]
            low_items = [item for item in low_stock_products if item["status"] == "low"]
            
            response_msg = f"{greeting}Here's what needs attention in our warehouse! 🔔\n\n"
            
            if critical_items:
                response_msg += "🚨 **CRITICAL - OUT OF STOCK:**\n"
                for item in critical_items[:3]:  # Show top 3
                    product = item["product"]
                    response_msg += f"• **{product.name}** - Location: {product.location or 'Not specified'}\n"
                if len(critical_items) > 3:
                    response_msg += f"• ... and {len(critical_items) - 3} more items\n"
                response_msg += "\n"
            
            if low_items:
                response_msg += "⚠️ **LOW STOCK:**\n"
                for item in low_items[:5]:  # Show top 5
                    product = item["product"]
                    inventory = item["inventory"]
                    response_msg += f"• **{product.name}** - {inventory.available_quantity} {product.unit} left\n"
                if len(low_items) > 5:
                    response_msg += f"• ... and {len(low_items) - 5} more items\n"
            
            response_msg += f"\n💡 **Action needed**: Consider reordering {len(low_stock_products)} items"
            
            return {
                "message": response_msg,
                "data": {
                    "low_stock_count": len(low_stock_products),
                    "critical_count": len(critical_items),
                    "low_count": len(low_items),
                    "items": [{"name": item["product"].name, "sku": item["product"].sku, 
                              "available": item["inventory"].available_quantity,
                              "status": item["status"]} for item in low_stock_products]
                },
                "suggestions": ["Reorder critical items", "View specific product", "Update stock levels"],
                "success": True,
                "action_taken": f"alerts_check_found_{len(low_stock_products)}_items"
            }
            
        except Exception as e:
            return {
                "message": f"{greeting}Sorry, I had trouble checking the alerts. Please try again! 😅",
                "success": False,
                "action_taken": "alerts_check_error",
                "suggestions": ["Try again", "Check specific products", "Contact support"]
            }

    def _handle_conversational_reporting(self, message: str, entities: Dict, context: Dict) -> Dict:
        """Handle reporting and analytics queries conversationally"""
        greeting = self._get_casual_greeting(context)
        
        try:
            # Get dashboard data
            inventory_service = InventoryService(self.db)
            inventory_summary = inventory_service.get_inventory_summary()
            
            # Calculate total value
            total_value = self.db.query(func.sum(Inventory.quantity * Product.unit_price)).join(
                Product, Inventory.product_id == Product.id
            ).scalar() or 0
            
            # Get operation counts
            pending_inbound = self.db.query(func.count(InboundShipment.id)).filter(
                InboundShipment.status.in_(["pending", "arrived"])
            ).scalar()
            
            pending_outbound = self.db.query(func.count(OutboundOrder.id)).filter(
                OutboundOrder.status.in_(["pending", "picking", "packed"])
            ).scalar()
            
            # Recent activity
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_movements = self.db.query(func.count(StockMovement.id)).filter(
                StockMovement.created_at >= week_ago
            ).scalar()
            
            response_msg = f"{greeting}Here's how things are looking in our warehouse!\n\n"
            response_msg += f"📦 **Inventory Overview:**\n"
            response_msg += f"• Total Products: {inventory_summary['total_products']}\n"
            response_msg += f"• Total Value: ${total_value:,.2f}\n"
            response_msg += f"• Low Stock Items: {inventory_summary['low_stock_count']}\n\n"
            
            response_msg += f"🚛 **Operations:**\n"
            response_msg += f"• Pending Inbound: {pending_inbound} shipments\n"
            response_msg += f"• Pending Outbound: {pending_outbound} orders\n"
            response_msg += f"• Recent Activity: {recent_movements} movements (7 days)\n\n"
            
            # Overall health assessment
            if inventory_summary['low_stock_count'] == 0 and pending_inbound == 0 and pending_outbound == 0:
                response_msg += "✅ **Status**: Everything running smoothly!"
            elif inventory_summary['low_stock_count'] > 5:
                response_msg += "⚠️ **Status**: Some attention needed on stock levels"
            else:
                response_msg += "👍 **Status**: Operations looking good!"
            
            return {
                "message": response_msg,
                "data": {
                    "inventory": inventory_summary,
                    "operations": {
                        "pending_inbound": pending_inbound,
                        "pending_outbound": pending_outbound,
                        "recent_movements": recent_movements
                    },
                    "total_value": total_value
                },
                "suggestions": ["Check low stock", "View detailed reports", "Check operations"],
                "success": True,
                "action_taken": "reporting_overview"
            }
            
        except Exception as e:
            return {
                "message": f"{greeting}Sorry, I had trouble getting the warehouse status. Please try again! 😅",
                "success": False,
                "action_taken": "reporting_error",
                "suggestions": ["Try again", "Check specific areas", "Contact support"]
            }
