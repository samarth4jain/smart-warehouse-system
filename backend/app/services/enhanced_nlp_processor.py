import re
import string
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import difflib

class EnhancedNLPProcessor:
    """Enhanced natural language processing for layman warehouse queries"""
    
    def __init__(self):
        self.setup_enhanced_patterns()
        self.setup_layman_language()
        self.setup_response_templates()
    
    def setup_enhanced_patterns(self):
        """Setup enhanced patterns for better layman language understanding"""
        self.intent_patterns = {
            "alerts_monitoring": {
                "casual_patterns": [
                    r"what\s+needs\s+(?:attention|fixing|help)",
                    r"any\s+(?:problems|issues|alerts|warnings)",
                    r"anything\s+(?:wrong|broken|bad)",
                    r"show\s+me\s+(?:warnings|alerts|issues|problems)",
                    r"what's\s+(?:wrong|broken|critical|bad)",
                    r"is\s+everything\s+(?:ok|okay|good)",
                    r"any\s+red\s+flags",
                    r"show\s+(?:me\s+)?low\s+stock",
                    r"(?:display|list|get)\s+low\s+stock",
                    r"what\s+(?:items|products)\s+(?:are\s+)?(?:running\s+)?low",
                    r"how\s+are\s+things\s+(?:going|looking)",
                    r"what\s+needs\s+attention\s+(?:around\s+here)?",
                    r"anything\s+i\s+should\s+know\s+about",
                    r"what's\s+happening\s+around\s+here",
                    r"any\s+issues\s+today",
                    r"everything\s+running\s+smooth",
                    r"running\s+(?:low|out)\s+(?:on\s+)?(.+)",
                    r"need\s+(?:more|to\s+order)\s+(.+)",
                    r"(almost|nearly)\s+(empty|out)\s+(of\s+)?(.+)",
                    r"getting\s+low\s+(?:on\s+)?(.+)",
                    r"we're\s+(?:low|out)\s+(?:on\s+)?(.+)",
                    r"(?:show\s+|list\s+)?(?:any\s+)?low\s+stock(?:\s+items?)?",
                    r"(?:what\s+)?(?:items?\s+)?(?:are\s+)?(?:running\s+)?low",
                    r"(?:show\s+)?(?:me\s+)?(?:all\s+)?low\s+stock",
                    r"(?:which|what)\s+(?:items?|products?)\s+(?:are\s+)?(?:running\s+)?low",
                ],
                "formal_patterns": [
                    r"system\s+(?:status|health|check|okay)",
                    r"overall\s+(?:status|health|picture)",
                    r"dashboard\s+(?:summary|overview)",
                    r"low\s+stock\s+(?:alerts?|items?|report)",
                    r"stock\s+alerts?",
                    r"(?:show|display|list)\s+(?:all\s+)?alerts",
                ]
            },
            
            "inventory_check": {
                "casual_patterns": [
                    r"do\s+we\s+have\s+(?:any\s+)?(.+?)(?:\s+left|\s+available|\s+in\s+stock|\?|$)",
                    r"got\s+any\s+(.+?)(?:\s+left|\s+available|\?|$)",
                    r"is\s+there\s+(?:any\s+)?(.+?)(?:\s+left|\s+available|\s+in\s+stock|\?|$)",
                    r"check\s+(?:if\s+we\s+have\s+)?(.+?)(?:\s+stock|\s+inventory|\?|$)",
                    r"how\s+much\s+(.+?)\s+(?:do\s+we\s+have|is\s+left|available)",
                    r"how\s+many\s+(.+?)\s+(?:do\s+we\s+have|are\s+there|left)",
                    r"where\s+(?:is|are)\s+(?:the\s+)?(.+?)(?:\s+located|\?|$)",
                    r"find\s+(?:me\s+)?(.+?)(?:\s+stock|\s+inventory|\?|$)",
                    r"search\s+(?:for\s+)?(.+?)(?:\s+stock|\s+inventory|\?|$)",
                    r"tell\s+me\s+about\s+(.+?)(?:\s+stock|\s+inventory|\?|$)",
                    r"what\s+about\s+(.+?)(?:\s+stock|\s+inventory|\?|$)",
                    r"(.+?)\s+(?:available|in\s+stock|inventory)\?",
                    r"can\s+you\s+(?:help\s+me\s+)?check\s+(?:stock|inventory)(?:\s+for\s+(.+?))?",
                    r"help\s+me\s+check\s+(?:stock|inventory)(?:\s+for\s+(.+?))?",
                    r"check\s+(?:the\s+)?stock(?:\s+for\s+(.+?))?",
                    r"check\s+(?:the\s+)?inventory(?:\s+for\s+(.+?))?",
                    r"show\s+(?:me\s+)?(?:all\s+)?(?:the\s+)?(.+?)(?:\s+we\s+have|\s+in\s+stock|\?|$)",
                    r"list\s+(?:all\s+)?(?:the\s+)?(.+?)(?:\s+we\s+have|\s+in\s+stock|\?|$)",
                    r"what\s+(.+?)\s+(?:do\s+we\s+have|are\s+available)",
                    r"what\s+(?:kind\s+of\s+)?(.+?)\s+(?:do\s+we\s+stock|are\s+in\s+inventory)",
                    r"show\s+me\s+(?:the\s+)?(.+?)(?:\s+(?:product|item|stock|inventory|info|details)|\s+SKU|\s+PROD|$)",
                    r"(.+?)\s+inventory",
                    r"(.+?)\s+stock",
                    r"^([A-Za-z0-9\s\-_]+?)(?:\s+available|\s+status|\?|$)",  # Simple product names
                ],
                "formal_patterns": [
                    r"check\s+stock\s+(?:for\s+)?(.+)",
                    r"inventory\s+status\s+(?:for\s+)?(.+)",
                    r"stock\s+level\s+(?:for\s+)?(.+)",
                    r"(?:sku|SKU)\s*:?\s*([A-Z0-9\-_]+)",
                    r"show\s+(?:all\s+)?(?:products|inventory|stock)",
                    r"list\s+(?:all\s+)?(?:products|inventory|stock)",
                ]
            },
            
            "stock_update": {
                "casual_patterns": [
                    r"we\s+(?:got|received|have)\s+(\d+)\s+(?:more\s+)?(.+?)(?:\s+today|\s+yesterday|\?|$)",
                    r"just\s+(?:got|received)\s+(\d+)\s+(.+?)(?:\?|$)",
                    r"add\s+(\d+)\s+(.+?)(?:\s+to\s+(?:stock|inventory)|\?|$)",
                    r"put\s+(\d+)\s+(.+?)\s+in\s+(?:the\s+)?system",
                    r"update\s+(.+?)\s+(?:to\s+|with\s+)?(\d+)",
                    r"fix\s+(.+?)\s+(?:count|stock|inventory)",
                    r"correct\s+(.+?)\s+(?:to\s+)?(\d+)",
                    r"actually\s+(?:we\s+have\s+)?(\d+)\s+(.+)",
                    r"counted\s+(\d+)\s+(.+)",
                    r"there\s+are\s+(\d+)\s+(.+)",
                    r"got\s+(\d+)\s+more\s+(.+?)(?:\s+today|\s+yesterday|\?|$)",
                    r"received\s+(\d+)\s+(.+?)(?:\s+today|\s+yesterday|\?|$)",
                ],
                "formal_patterns": [
                    r"stock\s+adjustment\s+(.+?)\s+(\d+)",
                    r"inventory\s+update\s+(.+?)\s+(\d+)",
                ]
            },
            
            "inbound_operations": {
                "casual_patterns": [
                    r"truck\s+(?:arrived|is\s+here|came|just\s+got\s+here)",
                    r"delivery\s+(?:is\s+here|arrived|came|just\s+arrived)",
                    r"(?:supplier|vendor)\s+(?:delivery|truck|shipment)\s+(?:arrived|is\s+here)",
                    r"we\s+(?:got|have)\s+a\s+(?:delivery|shipment|truck)",
                    r"something\s+(?:arrived|came\s+in|is\s+here)",
                    r"goods\s+(?:arrived|came\s+in|delivered)",
                    r"shipment\s+(.+?)\s+(?:arrived|is\s+here|came)",
                    r"need\s+to\s+(?:receive|process)\s+(.+)",
                    r"let's\s+(?:receive|process)\s+(.+)",
                ],
                "formal_patterns": [
                    r"gate\s+in\s+(.+)",
                    r"receive\s+shipment\s+(.+)",
                    r"process\s+delivery\s+(.+)",
                ]
            },
            
            "outbound_operations": {
                "casual_patterns": [
                    r"customer\s+(?:wants|needs|ordered)\s+(.+)",
                    r"send\s+(?:out\s+)?(.+?)\s+to\s+customer",
                    r"ship\s+(.+?)\s+(?:to\s+customer|out|today)",
                    r"get\s+(.+?)\s+out\s+(?:the\s+door|today)",
                    r"pack\s+(?:up\s+)?(.+?)(?:\s+for\s+shipping|$)",
                    r"fulfill\s+order\s+(.+)",
                    r"(.+?)\s+(?:ready\s+to\s+ship|needs\s+to\s+go\s+out)",
                    r"urgent\s+(?:order|delivery)\s+(.+)",
                    r"rush\s+(.+)",
                    r"priority\s+(?:order|shipment)\s+(.+)",
                ],
                "formal_patterns": [
                    r"dispatch\s+order\s+(.+)",
                    r"ship\s+order\s+(.+)",
                    r"process\s+outbound\s+(.+)",
                ]
            },
            
            "reporting_analytics": {
                "casual_patterns": [
                    r"how\s+(?:is|are)\s+(?:things|business|everything)\s+(?:going|looking)",
                    r"give\s+me\s+(?:a\s+)?(?:summary|overview|report)",
                    r"what's\s+(?:the\s+)?(?:status|situation|picture)",
                    r"how\s+(?:is|are)\s+we\s+doing",
                    r"(?:warehouse|business|inventory)\s+(?:status|overview|summary)",
                    r"(?:overall|general)\s+(?:status|picture|health)",
                    r"tell\s+me\s+about\s+(?:the\s+)?(?:warehouse|business|inventory)",
                    r"(?:what's\s+)?(?:happening|going\s+on)\s+(?:in\s+the\s+)?(?:warehouse|business)",
                    r"(?:inventory|warehouse|business)\s+(?:report|analytics|metrics)",
                ],
                "formal_patterns": [
                    r"inventory\s+status",
                    r"warehouse\s+status", 
                    r"business\s+status",
                    r"dashboard\s+(?:overview|summary)",
                    r"analytics\s+(?:report|overview)",
                    r"performance\s+(?:report|metrics)",
                ]
            }
        }
    
    def setup_layman_language(self):
        """Setup layman language translations"""
        self.layman_translations = {
            # Synonyms for technical terms (be careful not to break common phrases)
            "inventory": ["stock", "stuff", "items", "products", "goods", "materials"],
            "quantity": ["amount", "number", "count", "how many", "how much"],
            "location": ["where", "place", "spot", "area"],
            "urgent": ["asap", "quick", "fast", "rush", "immediately"],
            "check": ["look", "see", "find", "search"],
            "update": ["change", "fix", "correct", "adjust"],
            
            # Common phrases
            "greetings": ["hi", "hello", "hey", "good morning", "good afternoon"],
            "polite": ["please", "could you", "can you", "would you", "help me"],
            "uncertainty": ["not sure", "don't know", "confused", "maybe"],
        }
    
    def setup_response_templates(self):
        """Setup response templates for different scenarios"""
        self.response_templates = {
            "inventory_found": {
                "casual": "Good news! We've got {quantity} {product} available. {status_message}",
                "formal": "Product: {product}\nAvailable: {quantity} units\nStatus: {status_message}",
                "urgent": "⚡ URGENT: {product} - {quantity} available. {status_message}"
            },
            "inventory_low": {
                "casual": "Heads up! We're running low on {product} - only {quantity} left. Might want to reorder soon.",
                "formal": "Low Stock Alert: {product}\nCurrent Stock: {quantity}\nRecommendation: Reorder required",
                "urgent": "🚨 CRITICAL: {product} critically low ({quantity} remaining)!"
            },
            "inventory_empty": {
                "casual": "Uh oh! We're completely out of {product}. Time to reorder!",
                "formal": "Stock Status: Out of Stock\nProduct: {product}\nAction Required: Immediate reorder",
                "urgent": "🚨 OUT OF STOCK: {product} - Zero inventory!"
            },
            "need_more_info": {
                "casual": "I'd love to help! Could you tell me which product you're asking about?",
                "formal": "Please specify the product SKU or name for inventory lookup.",
                "urgent": "Product identification required for urgent request."
            }
        }
    
    def process_layman_query(self, message: str) -> Dict[str, Any]:
        """Process layman language queries with enhanced understanding"""
        
        # Normalize the message
        normalized_message = self.normalize_message(message)
        
        # Extract conversational context
        context = self.extract_context(message)
        
        # Classify intent with enhanced patterns
        intent, confidence = self.classify_intent_enhanced(normalized_message)
        
        # Extract entities with fuzzy matching
        entities = self.extract_entities_enhanced(message, intent)
        
        # Determine response style
        response_style = self.determine_response_style(context, entities)
        
        return {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "context": context,
            "response_style": response_style,
            "normalized_message": normalized_message
        }
    
    def normalize_message(self, message: str) -> str:
        """Normalize message by expanding synonyms and cleaning text"""
        normalized = message.lower().strip()
        
        # Expand synonyms
        for technical_term, synonyms in self.layman_translations.items():
            for synonym in synonyms:
                if isinstance(synonym, str):
                    pattern = r'\b' + re.escape(synonym) + r'\b'
                    normalized = re.sub(pattern, technical_term, normalized)
        
        return normalized
    
    def extract_context(self, message: str) -> Dict[str, Any]:
        """Extract conversational context from the message"""
        context = {
            "is_greeting": False,
            "is_polite": False,
            "is_urgent": False,
            "is_uncertain": False,
            "tone": "neutral",
            "formality": "casual"
        }
        
        message_lower = message.lower()
        
        # Check for greetings
        if any(greeting in message_lower for greeting in self.layman_translations["greetings"]):
            context["is_greeting"] = True
            context["tone"] = "friendly"
        
        # Check for politeness
        if any(polite in message_lower for polite in self.layman_translations["polite"]):
            context["is_polite"] = True
        
        # Check for urgency
        if any(urgent in message_lower for urgent in self.layman_translations["urgent"]):
            context["is_urgent"] = True
            context["tone"] = "urgent"
        
        # Check for uncertainty
        if any(uncertain in message_lower for uncertain in self.layman_translations["uncertainty"]):
            context["is_uncertain"] = True
            context["tone"] = "helpful"
        
        # Determine formality
        if re.search(r'(sku|SKU|inventory|dispatch)', message):
            context["formality"] = "formal"
        else:
            context["formality"] = "casual"
        
        return context
    
    def classify_intent_enhanced(self, message: str) -> Tuple[str, float]:
        """Enhanced intent classification for layman language"""
        best_intent = "help_general"
        best_confidence = 0.0
        
        for intent, pattern_groups in self.intent_patterns.items():
            confidence = 0.0
            
            # Check casual patterns (higher weight for layman language)
            for pattern in pattern_groups.get("casual_patterns", []):
                if re.search(pattern, message, re.IGNORECASE):
                    confidence = max(confidence, 0.8)
            
            # Check formal patterns
            for pattern in pattern_groups.get("formal_patterns", []):
                if re.search(pattern, message, re.IGNORECASE):
                    confidence = max(confidence, 0.9)
            
            if confidence > best_confidence:
                best_intent = intent
                best_confidence = confidence
        
        return best_intent, best_confidence
    
    def extract_entities_enhanced(self, message: str, intent: str) -> Dict[str, Any]:
        """Enhanced entity extraction with intent-aware patterns"""
        entities = {}
        
        # Extract based on intent
        if intent == "inventory_check":
            entities.update(self._extract_inventory_entities(message))
        elif intent == "stock_update":
            entities.update(self._extract_stock_update_entities(message))
        elif intent in ["inbound_operations", "outbound_operations"]:
            entities.update(self._extract_operation_entities(message))
        
        # Always try to extract common entities
        entities.update(self._extract_common_entities(message))
        
        return entities
    
    def _extract_inventory_entities(self, message: str) -> Dict[str, Any]:
        """Extract entities for inventory queries"""
        entities = {}
        
        # Try to extract product name from casual patterns
        casual_product_patterns = [
            # Pattern for "check inventory for X", "check stock for X"
            r"check\s+(?:inventory|stock)\s+(?:for\s+)?(.+?)(?:\?|$)",
            r"inventory\s+(?:check\s+)?(?:for\s+)?(.+?)(?:\?|$)",
            r"stock\s+(?:check\s+)?(?:for\s+)?(.+?)(?:\?|$)",
            # Basic existence queries
            r"do\s+we\s+have\s+(?:any\s+)?(.+?)(?:\s+left|\s+available|\s+in\s+stock|\?|$)",
            r"got\s+any\s+(.+?)(?:\s+left|\s+available|\?|$)",
            r"have\s+(?:any\s+)?(.+?)(?:\s+in\s+stock|\?|$)",
            # Quantity queries
            r"how\s+much\s+(.+?)\s+(?:do\s+we\s+have|is\s+left)",
            r"how\s+many\s+(.+?)\s+(?:do\s+we\s+have|are\s+left)",
            # Location queries
            r"where\s+(?:is|are)\s+(?:the\s+)?(.+?)(?:\s+located|\?|$)",
            # Simple product name (fallback for single words or phrases)
            r"^([A-Za-z][A-Za-z0-9\s]{2,})(?:\?|$)"
        ]
        
        for pattern in casual_product_patterns:
            match = re.search(pattern, message.strip(), re.IGNORECASE)
            if match:
                product_name = match.group(1).strip()
                # Clean up the product name
                product_name = re.sub(r'[?!.,]', '', product_name)
                product_name = product_name.strip()
                if len(product_name) > 2 and not product_name.lower() in ['stock', 'inventory', 'any', 'some']:
                    entities["product_name"] = product_name.title()
                    break
        
        # Try to extract SKU
        sku_patterns = [
            r"(?:sku|SKU)\s*:?\s*([A-Z0-9\-_]+)",
            r"\b([A-Z]{2,}[0-9]{2,})\b"
        ]
        
        for pattern in sku_patterns:
            match = re.search(pattern, message)
            if match:
                entities["sku"] = match.group(1).upper()
                break
        
        return entities
    
    def _extract_stock_update_entities(self, message: str) -> Dict[str, Any]:
        """Extract entities for stock update operations"""
        entities = {}
        
        # Extract quantity and product name from casual patterns
        quantity_product_patterns = [
            r"(?:got|received|have)\s+(\d+)\s+(?:more\s+)?(.+?)(?:\s+today|\s+yesterday|$)",
            r"add\s+(\d+)\s+(.+?)(?:\s+to\s+(?:stock|inventory)|$)",
            r"put\s+(\d+)\s+(.+?)\s+in\s+(?:the\s+)?system",
            r"actually\s+(?:we\s+have\s+)?(\d+)\s+(.+)",
            r"counted\s+(\d+)\s+(.+)",
        ]
        
        for pattern in quantity_product_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                entities["quantity"] = int(match.group(1))
                product_name = match.group(2).strip()
                if len(product_name) > 2:
                    entities["product_name"] = product_name.title()
                break
        
        return entities
    
    def _extract_operation_entities(self, message: str) -> Dict[str, Any]:
        """Extract entities for inbound/outbound operations"""
        entities = {}
        
        # Extract order/shipment numbers
        order_patterns = [
            r"order\s+([A-Z0-9\-_]+)",
            r"shipment\s+([A-Z0-9\-_]+)",
            r"\b(ORD[0-9]+)\b",
            r"\b(SH[0-9]+)\b"
        ]
        
        for pattern in order_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                number = match.group(1).upper()
                if number.startswith('ORD'):
                    entities["order_number"] = number
                elif number.startswith('SH'):
                    entities["shipment_number"] = number
                break
        
        return entities
    
    def _extract_common_entities(self, message: str) -> Dict[str, Any]:
        """Extract common entities that appear across intents"""
        entities = {}
        
        # Extract urgency indicators
        urgency_patterns = [
            r"\b(urgent|asap|immediately|priority|rush|critical)\b",
            r"right\s+now",
            r"as\s+soon\s+as\s+possible"
        ]
        
        for pattern in urgency_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                entities["urgency"] = True
                break
        
        # Extract time references
        time_patterns = [
            r"\b(today|tomorrow|yesterday)\b",
            r"this\s+(morning|afternoon|evening|week)",
            r"\d+\s+(minutes?|hours?|days?)\s+ago"
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                entities["time_reference"] = match.group(0)
                break
        
        return entities
    
    def determine_response_style(self, context: Dict, entities: Dict) -> str:
        """Determine the appropriate response style"""
        if entities.get("urgency") or context.get("is_urgent"):
            return "urgent"
        elif context.get("formality") == "formal":
            return "formal"
        else:
            return "casual"
    
    def generate_response(self, template_key: str, response_style: str, **kwargs) -> str:
        """Generate a response using the appropriate template and style"""
        template_group = self.response_templates.get(template_key, {})
        template = template_group.get(response_style, template_group.get("casual", ""))
        
        try:
            return template.format(**kwargs)
        except KeyError:
            # Fallback to basic template
            return f"Here's the information about {kwargs.get('product', 'your request')}: {kwargs.get('quantity', 'N/A')}"
