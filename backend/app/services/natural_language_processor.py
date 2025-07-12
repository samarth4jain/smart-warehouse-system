import re
import string
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import difflib

class NaturalLanguageProcessor:
    """Enhanced natural language processing for conversational warehouse operations"""
    
    def __init__(self):
        self.setup_language_patterns()
        self.setup_entity_extractors()
        self.setup_intent_weights()
        self.setup_layman_synonyms()
        self.setup_common_phrases()
    
    def setup_layman_synonyms(self):
        """Setup synonyms for technical terms to understand layman language"""
        self.synonyms = {
            "inventory": ["stock", "items", "products", "goods", "stuff", "materials", "supplies"],
            "quantity": ["amount", "number", "count", "how many", "how much"],
            "available": ["have", "got", "left", "remaining", "in stock", "on hand"],
            "delivery": ["shipment", "package", "order", "truck", "goods arriving"],
            "dispatch": ["send", "ship", "deliver", "send out", "get out"],
            "location": ["where", "place", "spot", "area", "zone"],
            "urgent": ["asap", "quick", "fast", "priority", "rush", "immediately"],
            "check": ["look", "see", "find", "search", "tell me"],
            "update": ["change", "fix", "correct", "adjust", "modify"],
            "status": ["condition", "state", "how is", "what's up with"]
        }
    
    def setup_common_phrases(self):
        """Setup common conversational phrases that users might use"""
        self.common_phrases = {
            "greeting": [
                r"^(hi|hello|hey|good\s+(morning|afternoon|evening))",
                r"^(what's\s+up|how\s+are\s+you|howdy)"
            ],
            "polite_requests": [
                r"(please|could\s+you|can\s+you|would\s+you)",
                r"(i\s+need|i\s+want|help\s+me)"
            ],
            "uncertainty": [
                r"(not\s+sure|don't\s+know|confused|unclear)",
                r"(maybe|perhaps|possibly|might)"
            ],
            "urgency": [
                r"(urgent|asap|immediately|right\s+now|quickly)",
                r"(rush|priority|emergency|critical)"
            ]
        }

    def setup_language_patterns(self):
        """Setup comprehensive language patterns for intent recognition"""
        self.intent_patterns = {
            "inventory_check": {
                "patterns": [
                    # Formal queries
                    r"check\s+(stock|inventory|available|quantity)",
                    r"how\s+much\s+.+\s+(stock|available|left|remaining)",
                    r"what\s+.+\s+(stock|inventory|quantity)",
                    r"show\s+me\s+.+\s+(stock|inventory|levels)",
                    r"(stock|inventory)\s+(level|status|check)",
                    
                    # Very casual/layman queries
                    r"do\s+we\s+have\s+.+",
                    r"got\s+any\s+.+",
                    r"is\s+there\s+.+\s+(left|available)",
                    r"any\s+.+\s+(in\s+stock|available|left)",
                    r"tell\s+me\s+about\s+.+",
                    r"what\s+about\s+.+",
                    r"where\s+.+\s+(is|are)",
                    r"find\s+.+",
                    r"look\s+for\s+.+",
                    r"search\s+.+",
                    
                    # Question formats
                    r"how\s+many\s+.+\s+(do\s+we\s+have|are\s+there)",
                    r"how\s+much\s+.+\s+(is\s+left|do\s+we\s+have)",
                    r"what's\s+the\s+(count|amount|number)\s+of\s+.+",
                    r"can\s+i\s+(see|check|find)\s+.+",
                    
                    # Product-specific
                    r".+\s+(available|in\s+stock)\?",
                    r"status\s+of\s+.+",
                    r"where\s+is\s+.+",
                    r"locate\s+.+",
                    
                    # Natural speech patterns
                    r"i\s+need\s+to\s+(check|see|find)\s+.+",
                    r"let\s+me\s+(check|see)\s+.+",
                    r"can\s+you\s+(tell\s+me|show\s+me)\s+.+",
                    r"i'm\s+looking\s+for\s+.+",
                    r"do\s+you\s+know\s+.+\s+(stock|inventory)"
                ],
                "keywords": ["stock", "inventory", "available", "quantity", "check", "show", "find", "search", "where", "locate", "have", "any", "left", "count", "amount"]
            },
            
            "inbound_operations": {
                "patterns": [
                    # Formal operations
                    r"gate\s+in\s+.+",
                    r"receive\s+(delivery|shipment|goods)",
                    r"(delivery|shipment)\s+arrived",
                    r"process\s+(delivery|shipment|receiving)",
                    
                    # Very casual language
                    r"truck\s+(arrived|is\s+here|came\s+in|just\s+got\s+here)",
                    r"delivery\s+(is\s+here|came|arrived|just\s+came)",
                    r"goods\s+(arrived|came\s+in|delivered|are\s+here)",
                    r"vendor\s+(delivery|shipment|truck|is\s+here)",
                    r"we\s+got\s+a\s+(delivery|shipment|truck)",
                    r"something\s+(arrived|came\s+in|is\s+here)",
                    r"(supplier|vendor)\s+.+\s+(here|arrived|came)",
                    r"package\s+(arrived|came|is\s+here)",
                    
                    # Action-oriented casual language
                    r"let's\s+(receive|process|handle)\s+.+",
                    r"need\s+to\s+(receive|process|handle)\s+.+",
                    r"can\s+(we|you)\s+(receive|process|handle)\s+.+",
                    r"time\s+to\s+(receive|process)\s+.+",
                    r"ready\s+to\s+(receive|process)\s+.+",
                    
                    # Natural descriptions
                    r"there's\s+a\s+(delivery|truck|shipment)\s+.+",
                    r"we\s+have\s+a\s+(delivery|shipment)\s+.+",
                    r"just\s+got\s+.+\s+(delivered|shipped)",
                    r"new\s+(shipment|delivery|goods)\s+.+"
                ],
                "keywords": ["gate", "receive", "delivery", "shipment", "arrived", "truck", "vendor", "supplier", "goods", "package", "came", "here"]
            },
            
            "outbound_operations": {
                "patterns": [
                    # Formal dispatch
                    r"dispatch\s+.+",
                    r"ship\s+(order|out)\s+.+",
                    r"send\s+out\s+.+",
                    r"process\s+(outbound|shipping|dispatch)",
                    
                    # Very casual shipping language
                    r"ready\s+to\s+(ship|send|go\s+out)",
                    r"customer\s+(order|wants|needs)\s+.+",
                    r"pack\s+(and\s+ship|up)\s+.+",
                    r"send\s+to\s+customer\s+.+",
                    r"fulfill\s+(order|customer)\s+.+",
                    r"get\s+.+\s+out\s+(the\s+door|to\s+customer)",
                    r"load\s+(the\s+truck|up)\s+.+",
                    r"ship\s+.+\s+to\s+customer",
                    r"send\s+out\s+the\s+.+",
                    r"prepare\s+.+\s+for\s+(shipping|delivery)",
                    
                    # Time-sensitive casual language
                    r"urgent\s+(order|shipment|delivery)",
                    r"rush\s+(order|delivery|this)",
                    r"asap\s+.+",
                    r"priority\s+(order|shipment)",
                    r"needs\s+to\s+go\s+out\s+(today|now|asap)",
                    r"customer\s+waiting\s+for\s+.+",
                    
                    # Natural requests
                    r"can\s+we\s+(ship|send)\s+.+",
                    r"time\s+to\s+(ship|send|dispatch)\s+.+",
                    r"let's\s+(ship|send|get\s+out)\s+.+",
                    r"we\s+need\s+to\s+(ship|send)\s+.+"
                ],
                "keywords": ["dispatch", "ship", "send", "outbound", "customer", "order", "pack", "fulfill", "urgent", "rush", "deliver", "load"]
            },
            
            "stock_management": {
                "patterns": [
                    # Adding stock - formal
                    r"add\s+(\d+|\w+)\s+.+",
                    r"received\s+(\d+|\w+)\s+.+",
                    r"increase\s+.+\s+by\s+(\d+|\w+)",
                    r"update\s+.+\s+to\s+(\d+|\w+)",
                    
                    # Very casual stock updates
                    r"we\s+got\s+(more|\d+)\s+.+",
                    r"just\s+(received|got)\s+.+",
                    r"need\s+to\s+(add|update|change|fix)\s+.+",
                    r"put\s+(\d+|\w+)\s+.+\s+in\s+(system|computer)",
                    r"count\s+shows\s+(\d+|\w+)\s+.+",
                    r"we\s+got\s+\d+\s+.+\s+(today|yesterday|this\s+morning)",
                    r"\d+\s+more\s+\w+\s+(came\s+in|arrived)",
                    r"found\s+(\d+|\w+)\s+more\s+.+",
                    
                    # Corrections and adjustments
                    r"fix\s+.+\s+(count|quantity|stock|number)",
                    r"correct\s+.+\s+(stock|inventory|count)",
                    r"adjust\s+.+",
                    r"the\s+(count|number)\s+is\s+wrong\s+for\s+.+",
                    r"actually\s+we\s+have\s+(\d+|\w+)\s+.+",
                    
                    # Natural language patterns
                    r"i\s+counted\s+(\d+|\w+)\s+.+",
                    r"there\s+are\s+(\d+|\w+)\s+.+\s+(here|now)",
                    r"we\s+have\s+(\d+|\w+)\s+.+\s+(now|total)",
                    r"inventory\s+shows\s+(\d+|\w+)\s+but\s+we\s+have\s+(\d+|\w+)"
                ],
                "keywords": ["add", "received", "update", "adjust", "fix", "correct", "count", "increase", "change", "got", "more", "came"]
            },
            
            "order_status": {
                "patterns": [
                    # Direct status checks
                    r"(order|shipment)\s+status\s+.+",
                    r"check\s+(order|shipment)\s+.+",
                    r"where\s+is\s+(order|shipment)\s+.+",
                    r"status\s+of\s+.+",
                    
                    # Customer-focused casual language
                    r"customer\s+(asking|called)\s+about\s+.+",
                    r"when\s+will\s+.+\s+(ship|arrive|be\s+ready)",
                    r"is\s+.+\s+(ready|shipped|done|finished)",
                    r"what's\s+happening\s+with\s+.+",
                    r"what's\s+the\s+deal\s+with\s+.+",
                    r"any\s+update\s+on\s+.+",
                    
                    # Tracking casual language
                    r"track\s+.+",
                    r"trace\s+.+",
                    r"follow\s+up\s+on\s+.+",
                    r"check\s+up\s+on\s+.+",
                    r"see\s+what's\s+up\s+with\s+.+",
                    
                    # Natural inquiries
                    r"how\s+is\s+.+\s+(going|doing)",
                    r"did\s+.+\s+(ship|go\s+out|leave)",
                    r"has\s+.+\s+(shipped|left|gone\s+out)",
                    r"customer\s+wants\s+to\s+know\s+about\s+.+"
                ],
                "keywords": ["status", "check", "order", "shipment", "where", "when", "track", "customer", "ready", "update", "happening"]
            },
            
            "alerts_monitoring": {
                "patterns": [
                    # Low stock casual language
                    r"running\s+(low|out)\s+(on\s+)?+.+",
                    r"need\s+(more|to\s+order)\s+.+",
                    r"(almost|nearly)\s+(empty|out)\s+(of\s+)?.+",
                    r"getting\s+low\s+(on\s+)?.+",
                    r"we're\s+(low|out)\s+(on\s+)?.+",
                    
                    # General alerts casual
                    r"what\s+needs\s+(attention|fixing|help)",
                    r"any\s+(problems|issues|alerts|warnings)",
                    r"anything\s+(wrong|broken|bad)",
                    r"show\s+me\s+(warnings|alerts|issues|problems)",
                    r"what's\s+(wrong|broken|critical|bad)",
                    r"is\s+everything\s+(ok|okay|good)",
                    r"any\s+red\s+flags",
                    
                    # Monitoring casual language
                    r"how\s+are\s+things\s+(going|looking)",
                    r"system\s+(status|health|check|okay)",
                    r"overall\s+(status|health|picture)",
                    r"dashboard\s+(summary|overview)",
                    r"give\s+me\s+the\s+(rundown|summary|overview)",
                    
                    # Natural expressions
                    r"anything\s+i\s+should\s+know\s+about",
                    r"what's\s+happening\s+around\s+here",
                    r"any\s+issues\s+today",
                    r"everything\s+running\s+smooth"
                ],
                "keywords": ["low", "alerts", "problems", "issues", "attention", "reorder", "running", "critical", "wrong", "broken", "empty"]
            },
            
            "reporting_analytics": {
                "patterns": [
                    # Reports casual
                    r"show\s+me\s+(report|summary|analytics|numbers)",
                    r"give\s+me\s+(report|summary|the\s+numbers)",
                    r"how\s+are\s+the\s+(numbers|stats|metrics)",
                    r"what\s+are\s+our\s+(numbers|stats)",
                    r"(daily|weekly|monthly)\s+(report|summary|numbers)",
                    r"performance\s+(report|metrics|data|numbers)",
                    
                    # Analytics requests casual
                    r"what's\s+our\s+(performance|metrics|stats)",
                    r"how\s+are\s+we\s+doing",
                    r"are\s+we\s+doing\s+(good|well|okay)",
                    r"sales\s+(data|numbers|figures|stats)",
                    r"inventory\s+(turnover|velocity|analysis|stats)",
                    r"business\s+(overview|summary|stats)",
                    
                    # Forecasting casual (if Phase 3 enabled)
                    r"what\s+do\s+we\s+expect\s+.+",
                    r"predict\s+.+\s+(demand|sales|requirements)",
                    r"forecast\s+.+",
                    r"what\s+will\s+we\s+need\s+.+",
                    r"future\s+(demand|requirements|needs)",
                    r"upcoming\s+(demand|orders|requirements)",
                    
                    # Natural business questions
                    r"how's\s+business\s+(going|doing)",
                    r"what's\s+the\s+(picture|situation|story)",
                    r"give\s+me\s+the\s+(big\s+picture|overview)",
                    r"what\s+should\s+i\s+know\s+about\s+.+"
                ],
                "keywords": ["report", "summary", "analytics", "performance", "forecast", "predict", "data", "metrics", "numbers", "stats"]
            },
            
            "help_general": {
                "patterns": [
                    r"help\s*$",
                    r"what\s+can\s+you\s+do",
                    r"how\s+do\s+i\s+.+",
                    r"what\s+commands\s+.+",
                    r"i\s+don't\s+know\s+how\s+.+",
                    r"confused\s+.+",
                    r"need\s+help\s+.+",
                    r"how\s+to\s+.+",
                    r"i'm\s+(lost|confused|stuck)",
                    r"not\s+sure\s+(what\s+to\s+do|how\s+to)",
                    r"can\s+you\s+help\s+me",
                    r"what\s+are\s+my\s+options",
                    r"show\s+me\s+what\s+you\s+can\s+do"
                ],
                "keywords": ["help", "how", "what", "commands", "confused", "don't know", "lost", "stuck", "options"]
            }
        }
    
    def setup_entity_extractors(self):
        """Setup enhanced entity extraction patterns for better layman language understanding"""
        self.entity_patterns = {
            "sku": [
                r"(?:sku|SKU)\s*:?\s*([A-Z0-9\-_]+)",
                r"product\s+(?:code|id|number)\s*:?\s*([A-Z0-9\-_]+)",
                r"item\s+(?:code|number|id)\s*:?\s*([A-Z0-9\-_]+)",
                r"\b([A-Z]{2,}[0-9]{2,})\b",  # Pattern like PROD001
                r"code\s*:?\s*([A-Z0-9\-_]+)",
                r"part\s+(?:number|#)\s*:?\s*([A-Z0-9\-_]+)",
            ],
            "quantity": [
                # Formal quantity patterns
                r"(\d+)\s*(?:units?|pieces?|items?|pcs?|pc)",
                r"(\d+)\s*(?:of|x|\*)",
                r"quantity\s*:?\s*(\d+)",
                r"amount\s*:?\s*(\d+)",
                r"count\s*:?\s*(\d+)",
                
                # Casual quantity patterns
                r"(\d+)\s+(?:more|extra|additional)",
                r"about\s+(\d+)",
                r"around\s+(\d+)",
                r"roughly\s+(\d+)",
                r"(\d+)\s+(?:total|altogether)",
                r"(\d+)\s+(?:in\s+total|all\s+together)",
                
                # Natural language quantities
                r"(\d+)\s+(?:units?\s+)?(?:of\s+)?",
                r"we\s+(?:got|have|received)\s+(\d+)",
                r"there\s+are\s+(\d+)",
                r"found\s+(\d+)",
                r"counted\s+(\d+)",
            ],
            "order_number": [
                r"(?:order|ord)\s*:?\s*([A-Z0-9\-_]+)",
                r"order\s+(?:number|#|id)\s*:?\s*([A-Z0-9\-_]+)",
                r"\b(ORD[0-9]+)\b",
                r"order\s+([A-Z0-9\-_]+)",
                r"customer\s+order\s+([A-Z0-9\-_]+)",
            ],
            "shipment_number": [
                r"(?:shipment|ship)\s*:?\s*([A-Z0-9\-_]+)",
                r"shipment\s+(?:number|#|id)\s*:?\s*([A-Z0-9\-_]+)",
                r"\b(SH[0-9]+)\b",
                r"delivery\s+(?:number|#|id)\s*:?\s*([A-Z0-9\-_]+)",
                r"truck\s+(?:number|#|id)\s*:?\s*([A-Z0-9\-_]+)",
            ],
            "product_name": [
                # Quoted names
                r"product\s+(?:named?\s+)?['\"]([^'\"]+)['\"]",
                r"item\s+(?:called\s+)?['\"]([^'\"]+)['\"]",
                r"['\"]([^'\"]+)['\"]",
                
                # Natural references
                r"(?:for|of|about)\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+(?:sku|SKU|product|item))",
                r"(?:check|find|look\s+for)\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+(?:stock|inventory))",
                r"([a-zA-Z\s]+)\s+(?:available|in\s+stock|inventory)",
                
                # Common product references
                r"(?:this|that|the)\s+([a-zA-Z\s]+)(?:\s+(?:product|item))?",
            ],
            "location": [
                r"(?:location|area|zone|section)\s*:?\s*([A-Z0-9\-_]+)",
                r"(?:in|at|from)\s+(?:location|area|zone|section)\s+([A-Z0-9\-_]+)",
                r"rack\s+([A-Z0-9\-_]+)",
                r"shelf\s+([A-Z0-9\-_]+)",
                r"warehouse\s+([A-Z0-9\-_]+)",
            ],
            "time_reference": [
                r"(today|yesterday|tomorrow)",
                r"(this\s+(?:morning|afternoon|evening|week|month))",
                r"(last\s+(?:week|month|year))",
                r"(\d+)\s+(?:days?|weeks?|months?)\s+ago",
                r"(urgent|asap|immediately|right\s+now)",
            ]
        }
    
    def setup_intent_weights(self):
        """Setup weights for intent classification confidence"""
        self.intent_weights = {
            "pattern_match": 0.6,
            "keyword_density": 0.3,
            "entity_presence": 0.1
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Enhanced entity extraction with fuzzy matching and context awareness"""
        entities = {}
        text_processed = self.preprocess_text(text)
        text_upper = text.upper()
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    if entity_type == "quantity":
                        # Handle different quantity formats
                        quantity_value = matches[0]
                        if quantity_value.isdigit():
                            entities[entity_type] = int(quantity_value)
                        else:
                            # Try to extract number from text
                            num_match = re.search(r'\d+', quantity_value)
                            if num_match:
                                entities[entity_type] = int(num_match.group())
                    elif entity_type == "product_name":
                        # Clean up product name
                        product_name = matches[0].strip()
                        if len(product_name) > 2:  # Avoid single characters
                            entities[entity_type] = product_name.title()
                    elif entity_type in ["sku", "order_number", "shipment_number", "location"]:
                        entities[entity_type] = matches[0].upper()
                    else:
                        entities[entity_type] = matches[0]
                    break
        
        # Additional fuzzy matching for product names if no explicit entity found
        if "product_name" not in entities and "sku" not in entities:
            # Try to find product references in natural language
            product_hints = self._extract_product_hints(text_processed)
            if product_hints:
                entities["product_name"] = product_hints
        
        # Extract urgency indicators
        urgency_patterns = [
            r"\b(urgent|asap|immediately|priority|rush|critical|emergency)\b",
            r"\bright\s+now\b",
            r"\bas\s+soon\s+as\s+possible\b"
        ]
        
        for pattern in urgency_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                entities["urgency"] = True
                break
        
        return entities
    
    def _extract_product_hints(self, text: str) -> Optional[str]:
        """Extract potential product references from natural language"""
        # Common patterns where product names might appear
        product_patterns = [
            r"(?:check|find|look\s+for|search|about|of|for)\s+(?:the\s+)?([a-zA-Z][a-zA-Z\s]{2,})(?:\s+(?:stock|inventory|available|left))",
            r"(?:do\s+we\s+have|got\s+any|is\s+there)\s+(?:any\s+)?([a-zA-Z][a-zA-Z\s]{2,})(?:\s+(?:left|available|in\s+stock))?",
            r"([a-zA-Z][a-zA-Z\s]{2,})\s+(?:available|inventory|stock|quantity)",
            r"(?:add|received|got)\s+(?:\d+\s+)?([a-zA-Z][a-zA-Z\s]{2,})",
            r"where\s+(?:is|are)\s+(?:the\s+)?([a-zA-Z][a-zA-Z\s]{2,})"
        ]
        
        for pattern in product_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                product_hint = match.group(1).strip()
                # Filter out common non-product words
                exclude_words = {"stock", "inventory", "quantity", "available", "items", "products", "goods", "stuff"}
                if product_hint.lower() not in exclude_words and len(product_hint) > 2:
                    return product_hint.title()
        
        return None
    
    def classify_intent_enhanced(self, message: str) -> Tuple[str, float, Dict]:
        """Enhanced intent classification with confidence scoring and context awareness"""
        message_clean = self.preprocess_text(message)
        message_lower = message_clean.lower()
        
        # Extract conversational context
        conversational_context = self.extract_conversational_context(message)
        
        # Extract entities first
        entities = self.extract_entities(message)
        
        # Score each intent
        intent_scores = {}
        
        for intent, config in self.intent_patterns.items():
            score = 0.0
            
            # Pattern matching score
            pattern_matches = 0
            for pattern in config["patterns"]:
                if re.search(pattern, message_lower):
                    pattern_matches += 1
            
            if pattern_matches > 0:
                pattern_score = min(pattern_matches / len(config["patterns"]), 1.0)
                score += pattern_score * self.intent_weights["pattern_match"]
            
            # Keyword density score
            keyword_matches = sum(1 for keyword in config["keywords"] if keyword in message_lower)
            if keyword_matches > 0:
                keyword_score = min(keyword_matches / len(config["keywords"]), 1.0)
                score += keyword_score * self.intent_weights["keyword_density"]
            
            # Entity presence bonus
            if entities and self._has_relevant_entities(intent, entities):
                score += self.intent_weights["entity_presence"]
            
            intent_scores[intent] = score
        
        # Find best intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            best_confidence = intent_scores[best_intent]
        else:
            best_intent = "help_general"
            best_confidence = 0.1
        
        # If confidence is too low, classify as general/help
        if best_confidence < 0.3:
            if conversational_context["is_greeting"]:
                best_intent = "help_general"
                best_confidence = 0.8
            else:
                best_intent = "help_general"
                best_confidence = 0.5
        
        return best_intent, best_confidence, entities
    
    def _has_relevant_entities(self, intent: str, entities: Dict) -> bool:
        """Check if entities are relevant to the intent"""
        entity_relevance = {
            "inventory_check": ["sku", "product_name", "location"],
            "inbound_operations": ["shipment_number", "quantity"],
            "outbound_operations": ["order_number", "sku"],
            "stock_management": ["sku", "product_name", "quantity"],
            "order_status": ["order_number"],
            "alerts_monitoring": [],
            "reporting_analytics": ["time_reference"],
            "help_general": []
        }
        
        relevant_entities = entity_relevance.get(intent, [])
        return any(entity in entities for entity in relevant_entities)
    
    def generate_contextual_response(self, intent: str, entities: Dict, context: Dict) -> Dict:
        """Generate contextual response suggestions and formatting"""
        response_context = {
            "tone": "professional",
            "urgency_level": "normal",
            "suggestions": [],
            "follow_up_questions": [],
            "formatting_hints": {}
        }
        
        # Determine tone based on intent and context
        if intent == "help_general":
            response_context["tone"] = "helpful"
            response_context["suggestions"] = [
                "Ask about stock levels",
                "Check order status", 
                "Process deliveries",
                "View reports"
            ]
        elif intent == "alerts_monitoring":
            response_context["tone"] = "informative"
            response_context["urgency_level"] = "high" if entities.get("urgency") else "normal"
        elif intent == "inventory_check":
            response_context["tone"] = "informative"
            if not entities.get("sku") and not entities.get("product_name"):
                response_context["follow_up_questions"] = [
                    "Which product would you like me to check?",
                    "Do you have a SKU or product name?"
                ]
        elif intent == "stock_management":
            response_context["tone"] = "confirmatory"
            if entities.get("urgency"):
                response_context["urgency_level"] = "high"
        
        # Add urgency indicators
        if entities.get("urgency") or context.get("confidence", 0) > 0.8:
            response_context["urgency_level"] = "high"
        
        return response_context
    
    def _has_relevant_entities(self, intent: str, entities: Dict) -> bool:
        """Check if extracted entities are relevant to the intent"""
        relevant_entities = {
            "inventory_check": ["sku", "product_name"],
            "inbound_operations": ["shipment_number", "quantity"],
            "outbound_operations": ["order_number"],
            "stock_management": ["sku", "quantity", "product_name"],
            "order_status": ["order_number"],
        }
        
        if intent in relevant_entities:
            return any(entity in entities for entity in relevant_entities[intent])
        
        return True  # For other intents, any entity is considered relevant
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text to normalize and expand synonyms"""
        text = text.lower().strip()
        
        # Expand synonyms to technical terms
        for technical_term, synonyms in self.synonyms.items():
            for synonym in synonyms:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(synonym) + r'\b'
                text = re.sub(pattern, technical_term, text)
        
        return text
    
    def extract_conversational_context(self, text: str) -> Dict[str, Any]:
        """Extract conversational context like tone, urgency, politeness"""
        context = {
            "is_greeting": False,
            "is_polite": False,
            "is_urgent": False,
            "is_uncertain": False,
            "tone": "neutral"
        }
        
        text_lower = text.lower()
        
        # Check for greeting
        for pattern in self.common_phrases["greeting"]:
            if re.search(pattern, text_lower):
                context["is_greeting"] = True
                context["tone"] = "friendly"
                break
        
        # Check for politeness
        for pattern in self.common_phrases["polite_requests"]:
            if re.search(pattern, text_lower):
                context["is_polite"] = True
                break
        
        # Check for urgency
        for pattern in self.common_phrases["urgency"]:
            if re.search(pattern, text_lower):
                context["is_urgent"] = True
                context["tone"] = "urgent"
                break
        
        # Check for uncertainty
        for pattern in self.common_phrases["uncertainty"]:
            if re.search(pattern, text_lower):
                context["is_uncertain"] = True
                context["tone"] = "helpful"
                break
        
        return context

    def generate_contextual_response(self, intent: str, entities: Dict, context: Dict = None) -> Dict[str, Any]:
        """Generate contextual response suggestions based on intent and entities"""
        response_context = {
            "intent": intent,
            "entities": entities,
            "confidence_level": "high" if context and context.get("confidence", 0) > 0.7 else "medium",
            "suggested_actions": [],
            "clarification_needed": []
        }
        
        # Add intent-specific context
        if intent == "inventory_check":
            if "sku" in entities:
                response_context["suggested_actions"] = ["show_stock_details", "show_location", "show_history"]
            elif "product_name" in entities:
                response_context["suggested_actions"] = ["find_product", "show_similar_products"]
            else:
                response_context["clarification_needed"] = ["product_identifier"]
        
        elif intent == "stock_management":
            if "sku" in entities and "quantity" in entities:
                response_context["suggested_actions"] = ["update_stock", "confirm_operation", "show_new_levels"]
            else:
                if "sku" not in entities:
                    response_context["clarification_needed"].append("product_identifier")
                if "quantity" not in entities:
                    response_context["clarification_needed"].append("quantity")
        
        elif intent == "inbound_operations":
            if "shipment_number" in entities:
                response_context["suggested_actions"] = ["process_gate_in", "show_shipment_details", "update_status"]
            else:
                response_context["clarification_needed"] = ["shipment_identifier"]
        
        elif intent == "outbound_operations":
            if "order_number" in entities:
                response_context["suggested_actions"] = ["process_dispatch", "show_order_details", "update_status"]
            else:
                response_context["clarification_needed"] = ["order_identifier"]
        
        return response_context
    
    def suggest_corrections(self, message: str, available_skus: List[str] = None, available_orders: List[str] = None) -> Dict[str, List[str]]:
        """Suggest corrections for misspelled or unclear entities"""
        suggestions = {}
        entities = self.extract_entities(message)
        
        # Suggest SKU corrections
        if "sku" in entities and available_skus:
            sku = entities["sku"]
            close_matches = difflib.get_close_matches(sku, available_skus, n=3, cutoff=0.6)
            if close_matches:
                suggestions["sku"] = close_matches
        
        # Suggest order number corrections
        if "order_number" in entities and available_orders:
            order = entities["order_number"]
            close_matches = difflib.get_close_matches(order, available_orders, n=3, cutoff=0.6)
            if close_matches:
                suggestions["order_number"] = close_matches
        
        return suggestions
    
    def extract_time_context(self, message: str) -> Dict[str, Any]:
        """Extract time-related context from message"""
        time_patterns = {
            "urgent": [r"urgent", r"asap", r"rush", r"priority", r"immediately", r"now"],
            "today": [r"today", r"this\s+morning", r"this\s+afternoon"],
            "tomorrow": [r"tomorrow", r"next\s+day"],
            "this_week": [r"this\s+week", r"by\s+friday"],
            "specific_time": [r"at\s+(\d{1,2}(?::\d{2})?(?:\s*[ap]m)?)", r"by\s+(\d{1,2}(?::\d{2})?(?:\s*[ap]m)?)"]
        }
        
        time_context = {}
        message_lower = message.lower()
        
        for time_type, patterns in time_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message_lower)
                if match:
                    if time_type == "specific_time":
                        time_context[time_type] = match.group(1)
                    else:
                        time_context[time_type] = True
                    break
        
        return time_context
