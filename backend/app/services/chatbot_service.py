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
        """Enhanced pattern matching with better intent recognition"""
        message_lower = message.lower()
        
        # Enhanced intent patterns with better coverage
        patterns = {
            "inventory_check": [
                r"(?:check|show|get|find|display|list|tell|give).*(?:inventory|stock|level|quantity|items?|products?)",
                r"(?:how many|how much|what.*quantity|do we have|is there|available|in stock)",
                r"(?:stock|inventory).*(?:level|status|check|information|report|summary)",
                r"(?:what.*(?:do we have|in stock|available)|show.*(?:stock|inventory))",
                r"(?:find|search|lookup|check).*(?:product|item|sku|code)",
                r"(?:search|find|lookup|locate|where).*(?:[A-Z]{2,}[0-9]{2,})",  # SKU pattern
                # Conversational patterns
                r"(?:got any|do.*have|is there|we.*have).*(?:laptop|mouse|keyboard|monitor|headphone|tablet)",
                r"(?:tell me about|show me|what about).*(?:inventory|stock|products?)",
                r"(?:available|have).*(?:laptop|mouse|keyboard|monitor|headphone|tablet|cable|charger)",
            ],
            "alerts_monitoring": [
                r"(?:low|running low|empty|out|critically low|almost empty).*(?:stock|inventory)",
                r"(?:what|which|any).*(?:items?|products?).*(?:low|running low|need reorder|critical)",
                r"(?:show|display|list|tell).*(?:low stock|alerts|warnings|problems|issues)",
                r"(?:any.*(?:problems|issues|alerts|warnings|red flags|trouble))",
                r"(?:what.*(?:needs attention|wrong|broken|critical|bad))",
                r"(?:everything.*(?:ok|okay|good|fine|running smooth))",
                r"(?:status|health|how.*things|problems|issues)",
                r"(?:are we|running|getting).*(?:low|out).*(?:on|of)",
                # Conversational patterns  
                r"(?:what needs|anything.*(?:wrong|broken|attention))",
                r"(?:how are things|everything.*(?:going|looking|running))",
                r"(?:any issues|problems today|need.*attention)",
            ],
            "product_search": [
                r"(?:find|search|locate|where|lookup).*(?:product|item|sku)",
                r"(?:where.*(?:is|can i find)|location.*(?:of|for))",
                r"(?:search|find|lookup|check).*(?:[A-Z]{2,}[0-9]{2,})",  # SKU pattern
                r"(?:details|information).*(?:about|for|on).*(?:product|item|sku)",
            ],
            "reporting_analytics": [
                r"(?:generate|create|show|display).*(?:report|analytics|summary|dashboard)",
                r"(?:performance|metrics|statistics|analytics|trends)",
                r"(?:warehouse.*(?:status|performance|analytics|overview))",
                r"(?:show.*(?:dashboard|analytics|metrics|status))",
            ],
            "help_general": [
                r"(?:help|what.*(?:do|can)|how.*work|assistance)",
                r"(?:support|guide|tutorial|instructions|examples)",
                r"(?:how.*use|what.*(?:features|capabilities|commands))",
                r"(?:can you|what can you|show me what)",
            ],
            "general_query": [
                r"(?:hello|hi|hey|good morning|good afternoon|thanks|thank you)",
                r"(?:bye|goodbye|see you|exit|quit)",
                r"(?:how are you|what.*up|how.*going)",
            ]
        }
        
        best_intent = "inventory_check"  # Default to most common intent
        best_confidence = 0.4  # Reduced default confidence
        matched_patterns = []
        
        # Score each intent based on pattern matches
        for intent, pattern_list in patterns.items():
            intent_score = 0
            matches = 0
            
            for pattern in pattern_list:
                if re.search(pattern, message_lower):
                    matches += 1
                    # Weight different types of matches
                    if intent in ["inventory_check", "alerts_monitoring"]:
                        intent_score += 0.8  # High confidence for core functions
                    else:
                        intent_score += 0.6
                    
                    matched_patterns.append(f"{intent}: {pattern}")
            
            # Calculate final confidence for this intent
            if matches > 0:
                confidence = min(0.9, intent_score / len(pattern_list) * (1 + matches * 0.1))
                if confidence > best_confidence:
                    best_intent = intent
                    best_confidence = confidence
        
        # Enhanced entity extraction
        entities = {}
        
        # SKU extraction (improved pattern)
        sku_patterns = [
            r"\b([A-Z]{2,}[0-9]{2,})\b",
            r"\b(SKU:?\s*[A-Z0-9]+)\b",
            r"\b(PROD[0-9]+)\b",
            r"\b([A-Z]+[0-9]+[A-Z]*)\b"
        ]
        
        for pattern in sku_patterns:
            sku_match = re.search(pattern, message, re.IGNORECASE)
            if sku_match:
                entities["sku"] = sku_match.group(1).upper().replace("SKU:", "").strip()
                break
        
        # Enhanced product type extraction
        product_keywords = {
            "laptop": ["laptop", "notebook", "computer"],
            "mouse": ["mouse", "mice"],
            "keyboard": ["keyboard", "keys"],
            "monitor": ["monitor", "screen", "display"],
            "headphone": ["headphone", "headset", "earphone", "earbuds"],
            "tablet": ["tablet", "ipad"],
            "cable": ["cable", "cord", "wire"],
            "charger": ["charger", "adapter", "power"],
            "phone": ["phone", "mobile", "smartphone"],
            "speaker": ["speaker", "audio"]
        }
        
        for product_type, keywords in product_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    entities["product_type"] = product_type
                    entities["product_keyword"] = keyword
                    break
            if "product_type" in entities:
                break
        
        # Quantity extraction
        quantity_match = re.search(r"(\d+)\s*(?:units?|pieces?|items?|pcs?)?", message_lower)
        if quantity_match:
            entities["quantity"] = int(quantity_match.group(1))
        
        # Action type extraction
        action_patterns = {
            "check": r"(?:check|show|display|get|find)",
            "update": r"(?:update|change|modify|set)",
            "add": r"(?:add|increase|put|receive)",
            "remove": r"(?:remove|decrease|take|ship)"
        }
        
        for action, pattern in action_patterns.items():
            if re.search(pattern, message_lower):
                entities["action"] = action
                break
        
        return best_intent, best_confidence, entities

    def _generate_fallback_response(self, message: str, intent: str) -> Dict:
        """Generate a helpful fallback response when processing fails"""
        
        # Enhanced fallback responses based on intent
        if intent == "inventory_check":
            return {
                "message": """Hey there! I'd love to help you check stock! 
                
Could you tell me which product you're asking about?

💡 **You can say things like:**
• 'Check stock for blue widgets'
• 'Do we have any PROD001?'
• 'How much inventory for laptops?'
• 'Show me SKU WIDGET001'

🔍 **Or try these formats:**
• Product name: "Check laptop inventory"
• SKU code: "Show me PROD001"
• Category: "Check electronics stock"

I'll give you detailed inventory information right away!""",
                "intent": intent,
                "confidence": 0.8,
                "suggestions": ["Specify product name", "Use SKU code", "Browse product catalog"],
                "actions": [],
                "success": True
            }
        
        elif intent == "alerts_monitoring":
            return {
                "message": """I can help you check what needs attention in your warehouse!

📊 **Here's what I can monitor:**
• Low stock alerts
• Items needing reorder
• Critical inventory levels
• System warnings

🚨 **Try asking:**
• "What items are running low?"
• "Show me critical alerts"
• "Any problems today?"
• "What needs my attention?"

I'll analyze your warehouse status and highlight anything important!""",
                "intent": intent,
                "confidence": 0.8,
                "suggestions": ["Check low stock", "View critical alerts", "System status"],
                "actions": [],
                "success": True
            }
        
        else:
            return {
                "message": f"""I understand you're asking about warehouse operations! 

**🏭 I can help you with:**
• **Inventory** - Stock levels, product search, availability
• **Alerts** - Low stock, critical items, system warnings  
• **Orders** - Shipment tracking, delivery status
• **Analytics** - Reports, trends, performance metrics

**💬 Natural Language Examples:**
• "Show me what's running low"
• "Check if we have laptops in stock"
• "Any problems I should know about?"
• "How are operations today?"

**🎯 Quick Commands:**
• Use product names: "laptop", "mouse", "headphones"
• Use SKU codes: "PROD001", "WIDGET123"
• Ask conversationally - I understand natural language!

What would you like me to help you with?""",
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
        sku = entities.get("sku")
        product_type = entities.get("product_type")
        product_keyword = entities.get("product_keyword")
        
        try:
            if sku:
                # Search by SKU
                search_term = sku
                products = self.db.query(Product).filter(Product.sku.ilike(f"%{sku}%")).all()
                if products:
                    product = products[0]  # Take first match
            
            elif product_type or product_keyword:
                # Search by product type or keyword
                search_term = product_type or product_keyword
                products = self.db.query(Product).filter(
                    Product.name.ilike(f"%{search_term}%") | 
                    Product.description.ilike(f"%{search_term}%") |
                    Product.category.ilike(f"%{search_term}%")
                ).all()
                
                if products:
                    product = products[0]  # Take first match for now
            
            if product:
                return self._generate_inventory_response(product, search_term, products if len(products) > 1 else None)
            elif search_term:
                return self._generate_product_not_found_response(search_term, message)
            else:
                return self._generate_need_product_info_response(message)
                
        except Exception as e:
            return self._generate_inventory_error_response(str(e))
    
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
    
    def _generate_inventory_response(self, product: Product, search_term: str, additional_products: List = None) -> Dict:
        """Generate detailed inventory response"""
        try:
            # Get inventory information
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
            
            if inventory:
                quantity = inventory.quantity
                location = inventory.location or "Not specified"
                
                # Determine stock status
                reorder_level = product.reorder_level or 10
                if quantity <= 0:
                    status = "🔴 OUT OF STOCK"
                    status_color = "critical"
                elif quantity <= reorder_level:
                    status = "🟡 LOW STOCK"
                    status_color = "warning"
                else:
                    status = "🟢 IN STOCK"
                    status_color = "good"
                
                message = f"""✅ Found **{product.name}** (SKU: {product.sku})

📦 **Stock Information:**
• **Quantity Available:** {quantity} {product.unit or 'units'}
• **Status:** {status}
• **Location:** {location}
• **Reorder Level:** {reorder_level} {product.unit or 'units'}

💰 **Product Details:**
• **Category:** {product.category or 'Uncategorized'}
• **Unit Price:** ${product.unit_price or 'N/A'}
• **Description:** {product.description or 'No description available'}"""

                # Add suggestions based on stock status
                suggestions = []
                actions = []
                
                if quantity <= 0:
                    suggestions = ["Check expected deliveries", "Set up restock alert", "Find alternative products"]
                    actions = ["reorder_product", "check_inbound"]
                elif quantity <= reorder_level:
                    suggestions = ["Consider reordering", "Check usage trends", "Set up auto-reorder"]
                    actions = ["reorder_product", "view_analytics"]
                else:
                    suggestions = ["Update stock levels", "Check product details", "View movement history"]
                    actions = ["update_stock", "view_details"]
                
                # Add information about additional matches if any
                if additional_products and len(additional_products) > 1:
                    message += f"\n\n💡 **Found {len(additional_products)} products matching '{search_term}'. Use more specific terms or SKU for exact matches.**"
                
                return {
                    "message": message,
                    "success": True,
                    "data": {
                        "product": {
                            "id": product.id,
                            "sku": product.sku,
                            "name": product.name,
                            "quantity": quantity,
                            "status": status_color,
                            "location": location,
                            "unit_price": product.unit_price
                        }
                    },
                    "suggestions": suggestions,
                    "actions": actions,
                    "action_taken": "inventory_checked"
                }
            else:
                return {
                    "message": f"Found product **{product.name}** (SKU: {product.sku}) but no inventory data available. This might be a new product not yet stocked.",
                    "success": True,
                    "suggestions": ["Add initial stock", "Check product setup", "Contact inventory team"],
                    "actions": ["add_stock"],
                    "action_taken": "product_found_no_inventory"
                }
                
        except Exception as e:
            return self._generate_inventory_error_response(f"Error retrieving inventory: {str(e)}")
    
    def _generate_product_not_found_response(self, search_term: str, original_message: str) -> Dict:
        """Generate response when product is not found"""
        return {
            "message": f"""🔍 I couldn't find any products matching "**{search_term}**" in our inventory.

**🎯 Here's what you can try:**
• **Use exact SKU:** Try the complete product SKU (e.g., "LAPTOP001")
• **Use different keywords:** Try "laptop", "mouse", "keyboard", etc.
• **Check spelling:** Make sure the product name is spelled correctly
• **Browse categories:** Ask "show me all electronics" or similar

**💡 Popular searches:**
• "Check laptop inventory"
• "Show me PROD001"
• "Do we have any monitors?"
• "What electronics do we have?"

Want me to show you all available products or help you search differently?""",
            "success": False,
            "suggestions": ["Try different keywords", "Use exact SKU", "Browse all products", "Check spelling"],
            "actions": ["browse_products", "search_help"],
            "action_taken": "product_not_found"
        }
    
    def _generate_need_product_info_response(self, original_message: str) -> Dict:
        """Generate response when no product information is provided"""
        return {
            "message": """I'd love to help you check inventory! Could you tell me which product you're looking for?

**🔍 You can search by:**
• **Product name:** "laptop", "wireless mouse", "keyboard"
• **SKU code:** "PROD001", "LAPTOP001", "MOUSE123"
• **Category:** "electronics", "office supplies"

**💬 Try saying:**
• "Check laptop inventory"
• "Show me SKU PROD001"  
• "Do we have any wireless mice?"
• "How much stock for headphones?"

**📦 Or ask for:**
• "Show me all products"
• "What's in stock today?"
• "List electronics inventory"

What product would you like me to check for you?""",
            "success": True,
            "suggestions": ["Specify product name", "Use SKU code", "Browse categories", "Show all products"],
            "actions": ["browse_products", "search_by_category"],
            "action_taken": "awaiting_product_info"
        }
    
    def _generate_inventory_error_response(self, error_details: str) -> Dict:
        """Generate response for inventory system errors"""
        return {
            "message": """I'm currently having trouble connecting to the inventory system. Here's what I can help with offline:

🔍 **For Inventory Queries**: Try "Check stock SKU: PROD001"
📦 **For Stock Updates**: Try "Add 50 units SKU: PROD001" 
🚛 **For Orders**: Try "Check order status ORD001"
📊 **For Reports**: Try "Show warehouse efficiency report"

🔧 **Tip**: Make sure the backend server is running on localhost:8000

Please try your request again in a moment.""",
            "success": False,
            "suggestions": ["Try again later", "Check system status", "Contact IT support"],
            "actions": ["retry_request", "check_status"],
            "action_taken": "system_error"
        }
    
    def _handle_layman_alerts(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Enhanced alerts and monitoring handler"""
        try:
            # Get low stock items
            low_stock_items = self.db.query(Product, Inventory).join(
                Inventory, Product.id == Inventory.product_id
            ).filter(
                Inventory.quantity <= Product.reorder_level
            ).all()
            
            # Get out of stock items
            out_of_stock_items = self.db.query(Product, Inventory).join(
                Inventory, Product.id == Inventory.product_id
            ).filter(
                Inventory.quantity <= 0
            ).all()
            
            if not low_stock_items and not out_of_stock_items:
                return {
                    "message": """🎉 **Great news! Everything looks good in your warehouse!**

✅ **Current Status:**
• **No critical stock alerts**
• **No items requiring immediate attention**
• **All products above reorder levels**

📊 **Quick Stats:**
• System running smoothly
• Inventory levels healthy
• No urgent actions needed

💡 **Proactive Tips:**
• Consider checking weekly trends
• Review seasonal demand patterns  
• Verify reorder level settings

Keep up the excellent warehouse management!""",
                    "success": True,
                    "suggestions": ["View inventory trends", "Check weekly reports", "Review reorder levels"],
                    "actions": ["view_analytics", "generate_report"],
                    "action_taken": "no_alerts_found"
                }
            
            # Build alert message
            alert_message = "🚨 **Warehouse Alert Summary**\n\n"
            total_issues = len(out_of_stock_items) + len(low_stock_items)
            
            if out_of_stock_items:
                alert_message += f"🔴 **CRITICAL - {len(out_of_stock_items)} Out of Stock:**\n"
                for product, inventory in out_of_stock_items[:5]:  # Show max 5
                    alert_message += f"• **{product.name}** (SKU: {product.sku}) - Location: {inventory.location or 'Not specified'}\n"
                
                if len(out_of_stock_items) > 5:
                    alert_message += f"• ... and {len(out_of_stock_items) - 5} more items\n"
                alert_message += "\n"
            
            if low_stock_items:
                low_only = [item for item in low_stock_items if item not in out_of_stock_items]
                if low_only:
                    alert_message += f"🟡 **WARNING - {len(low_only)} Low Stock:**\n"
                    for product, inventory in low_only[:5]:  # Show max 5
                        alert_message += f"• **{product.name}** (SKU: {product.sku}) - Qty: {inventory.quantity}/{product.reorder_level}\n"
                    
                    if len(low_only) > 5:
                        alert_message += f"• ... and {len(low_only) - 5} more items\n"
                    alert_message += "\n"
            
            alert_message += f"""📋 **Recommended Actions:**
• **Immediate:** Reorder {len(out_of_stock_items)} out-of-stock items
• **Soon:** Review {len(low_stock_items)} low-stock items
• **Planning:** Check supplier lead times
• **Analytics:** Review demand patterns

💡 **Need help with any specific items? Just ask me about them!**"""

            suggestions = ["Reorder critical items", "Check supplier status", "View detailed reports", "Set up auto-reorder"]
            actions = ["reorder_items", "contact_suppliers", "generate_report"]
            
            return {
                "message": alert_message,
                "success": True,
                "data": {
                    "total_alerts": total_issues,
                    "out_of_stock": len(out_of_stock_items),
                    "low_stock": len(low_stock_items),
                    "critical_items": [{"sku": p.sku, "name": p.name, "quantity": i.quantity} 
                                     for p, i in out_of_stock_items[:10]]
                },
                "suggestions": suggestions,
                "actions": actions,
                "action_taken": "alerts_checked"
            }
            
        except Exception as e:
            return {
                "message": f"""I'm having trouble accessing the alert system right now.

**What I can help with:**
• Manual inventory checks
• Product information lookup
• General warehouse questions

**Try asking:**
• "Check specific product stock"
• "Show me laptop inventory"
• "Help with warehouse operations"

Error details: {str(e)}""",
                "success": False,
                "suggestions": ["Try specific product check", "Contact system admin", "Try again later"],
                "actions": ["check_specific_product", "contact_support"],
                "action_taken": "alert_system_error"
            }
    
    def _handle_layman_help(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Enhanced help handler with comprehensive guidance"""
        return {
            "message": """🤖 **Smart Warehouse AI Assistant - Help Guide**

**🏭 What I Can Do For You:**

**📦 Inventory Management:**
• Check stock levels: "How many laptops do we have?"
• Find products: "Show me SKU PROD001"
• Search by category: "List all electronics"

**🚨 Alerts & Monitoring:**
• Check alerts: "What needs attention?"
• Low stock: "Show me items running low"
• System status: "How are things looking?"

**📊 Reports & Analytics:**
• Warehouse status: "Show me dashboard"
• Performance metrics: "Generate warehouse report"
• Trends: "How are we doing this week?"

**💬 Natural Language Examples:**
• "Do we have any wireless mice in stock?"
• "What items are critically low?"
• "I need to check our laptop inventory"
• "Are we running out of anything?"
• "Show me what needs reordering"

**🎯 Pro Tips:**
• Use product names OR SKU codes
• Ask conversational questions - I understand natural language!
• Be specific for better results: "laptop" vs "electronic devices"
• I can handle typos and different phrasings

**🔍 Quick Commands:**
• "help" - Show this guide
• "status" - System overview
• "alerts" - Check urgent items

**Need help with something specific? Just ask me in your own words!**""",
            "success": True,
            "suggestions": [
                "Check inventory", 
                "View alerts", 
                "Generate reports", 
                "Ask specific questions"
            ],
            "actions": ["check_inventory", "view_alerts", "generate_report"],
            "action_taken": "help_provided"
        }
    
    def _handle_layman_general(self, message: str, entities: Dict, context: Dict, response_style: str) -> Dict:
        """Handle general queries and greetings"""
        message_lower = message.lower()
        
        # Greeting responses
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return {
                "message": """👋 **Hello! I'm your Smart Warehouse AI Assistant!**

I'm here to help you manage your warehouse operations efficiently. 

**🚀 Ready to help you with:**
• **Inventory checks** - Stock levels, product searches
• **Alert monitoring** - Low stock, urgent items  
• **System status** - Overall warehouse health
• **Reports** - Analytics and performance data

**💬 Just ask me naturally:**
• "What's running low in inventory?"
• "Check if we have laptops in stock"
• "Show me today's alerts"
• "How are warehouse operations?"

**What can I help you with today?**""",
                "success": True,
                "suggestions": ["Check inventory", "View alerts", "System status", "Show help"],
                "actions": ["check_inventory", "view_alerts", "get_status"],
                "action_taken": "greeting_provided"
            }
        
        # Farewell responses
        elif any(farewell in message_lower for farewell in ["bye", "goodbye", "see you", "thanks", "thank you"]):
            return {
                "message": """👋 **Thanks for using Smart Warehouse AI!**

I hope I was able to help you with your warehouse operations today.

**📞 Remember, I'm always here to assist with:**
• Inventory management
• Stock alerts and monitoring  
• Warehouse analytics
• System status checks

**🎯 Feel free to come back anytime you need help with:**
• "What's running low?"
• "Check product inventory"
• "Show me warehouse status"

Have a great day and keep those operations running smoothly! 🏭✨""",
                "success": True,
                "suggestions": ["Check back later", "Bookmark for quick access"],
                "actions": [],
                "action_taken": "farewell_provided"
            }
        
        # Default general response
        else:
            return {
                "message": """🤖 **I'm your Smart Warehouse AI Assistant!**

I understand you're asking about warehouse operations. Here's how I can help:

**🎯 Popular Requests:**
• **"What's running low?"** - Check alerts and low stock
• **"Check laptop inventory"** - Specific product searches
• **"Show me warehouse status"** - Overall system health
• **"Help"** - Complete guide and examples

**💡 Natural Language Tips:**
• Ask in your own words - I understand conversational language
• Use product names or SKU codes
• Be as specific or general as you'd like

**🔍 Not sure what to ask?** Try:
• "Show me what needs attention"
• "Check all inventory levels"  
• "Help with warehouse operations"

What specific area of warehouse management can I help you with?""",
                "success": True,
                "suggestions": ["Check inventory", "View alerts", "Get help", "System status"],
                "actions": ["check_inventory", "view_alerts", "show_help"],
                "action_taken": "general_guidance_provided"
            }
