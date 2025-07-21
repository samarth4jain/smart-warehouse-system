import os
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema import BaseRetriever
from datetime import datetime, timedelta
import json

from ..models.database_models import (
    Product, Inventory, Vendor, Customer, InboundShipment, OutboundOrder,
    InboundItem, OutboundItem, StockMovement, User, ChatMessage, ChatSession,
    DemandForecast, ProductVelocity, StockAlert, WarehouseLayout, SpaceOptimization,
    SalesHistory, ConversationContext
)

logger = logging.getLogger(__name__)

class EnhancedWarehouseRAGService:
    """Enhanced RAG service for natural language warehouse data operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.vector_store = None
        self.retriever = None
        self.embeddings = None
        self._initialize_rag()
        
        # Intent patterns for natural language processing
        self.intent_patterns = {
            # Query operations
            'stock_check': [
                r'(?:what|show|check|display).*?(?:stock|inventory).*?(?:level|quantity)?.*?(?:of|for)\s+(\w+)',
                r'(?:how many|current stock).*?(\w+)',
                r'stock\s+(?:level|of)\s+(\w+)',
                r'(\w+)\s+(?:stock|inventory)',
                r'(?:check|show)\s+(\w+)',
                r'stock\s+(\w+)'
            ],
            'low_stock': [
                r'(?:show|list|find|what).*?(?:low|running low).*?stock',
                r'(?:products|items).*?(?:low|below|need).*?(?:stock|reorder)',
                r'(?:alert|warning).*?stock',
                r'low\s+stock',
                r'stock\s+alerts?',
                r'reorder\s+(?:alerts?|list)'
            ],
            'category_search': [
                r'(?:show|list|find).*?(?:products|items).*?(?:in|from).*?(?:category\s+)?(\w+)',
                r'(?:all|list).*?(\w+).*?(?:products|items)',
                r'products.*?category.*?(\w+)',
                r'(\w+)\s+(?:category|products)',
                r'list.*?(\w+)'
            ],
            
            # Data modification operations
            'add_stock': [
                r'add\s+(\d+).*?(?:units?|pieces?|pcs?).*?(?:to|of)\s+(\w+)',
                r'increase.*?(\w+).*?(?:by|to)\s+(\d+)',
                r'receive.*?(\d+).*?(\w+)',
                r'(?:inbound|received)\s+(\d+)\s+(\w+)',
                r'(\w+)\s+(?:\+|add)\s+(\d+)',
                r'stock\s+(\w+)\s+(?:\+|add)\s+(\d+)'
            ],
            'remove_stock': [
                r'remove\s+(\d+).*?(?:units?|pieces?|pcs?).*?(?:from|of)\s+(\w+)',
                r'decrease.*?(\w+).*?(?:by|to)\s+(\d+)',
                r'dispatch.*?(\d+).*?(\w+)',
                r'(?:outbound|shipped)\s+(\d+)\s+(\w+)',
                r'(\w+)\s+(?:\-|remove)\s+(\d+)',
                r'stock\s+(\w+)\s+(?:\-|remove)\s+(\d+)'
            ],
            'set_stock': [
                r'set.*?(\w+).*?(?:stock|to)\s+(\d+)',
                r'update.*?(\w+).*?(?:stock|to)\s+(\d+)',
                r'change.*?(\w+).*?(?:quantity|to)\s+(\d+)',
                r'(\w+)\s+(?:=|set to)\s+(\d+)',
                r'stock\s+(\w+)\s+(?:=|to)\s+(\d+)'
            ],
            
            # Product management
            'add_product': [
                r'(?:add|create).*?(?:new\s+)?product.*?(?:sku|code)?\s+(\w+)',
                r'new.*?product.*?(\w+)',
                r'create.*?(\w+)',
                r'add.*?(\w+)'
            ],
            'delete_product': [
                r'(?:delete|remove).*?product.*?(\w+)',
                r'discontinue.*?(\w+)',
                r'remove.*?(\w+)',
                r'delete.*?(\w+)'
            ],
            
            # Advanced operations
            'demand_forecast': [
                r'(?:generate|create|show).*?(?:demand|forecast)',
                r'predict.*?demand',
                r'forecast',
                r'demand.*?prediction'
            ],
            'space_optimization': [
                r'optimize.*?(?:layout|space|warehouse)',
                r'improve.*?(?:layout|space)',
                r'space.*?optimization',
                r'layout.*?optimization'
            ],
            'alerts': [
                r'(?:show|check|list).*?alerts?',
                r'what.*?(?:warnings?|alerts?)',
                r'stock.*?(?:alerts?|warnings?)',
                r'alerts?'
            ]
        }
    
    def _initialize_rag(self):
        """Initialize RAG components with enhanced capabilities"""
        try:
            # Initialize embeddings
            embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            self.embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
            
            # Initialize vector store
            vector_db_path = os.getenv("VECTOR_DB_PATH", "./data/chroma_db")
            os.makedirs(vector_db_path, exist_ok=True)
            
            self.vector_store = Chroma(
                persist_directory=vector_db_path,
                embedding_function=self.embeddings,
                collection_name="enhanced_warehouse_knowledge"
            )
            
            # Create retriever
            top_k = int(os.getenv("TOP_K_RETRIEVAL", "10"))
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": top_k}
            )
            
            # Index warehouse data
            self._index_comprehensive_warehouse_data()
            
            logger.info("Enhanced RAG service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize enhanced RAG service: {str(e)}")
            # Continue without vector store for basic operations
            self.vector_store = None
            self.retriever = None
    
    def process_natural_language_query(self, query: str, user_id: int = None) -> Dict[str, Any]:
        """Process natural language query and perform appropriate database operations"""
        
        try:
            # Clean and normalize query
            normalized_query = query.lower().strip()
            
            # Classify intent
            intent, entities = self._classify_intent(normalized_query)
            
            # Process based on intent
            if intent == 'stock_check':
                return self._handle_stock_check(entities, normalized_query)
            elif intent == 'low_stock':
                return self._handle_low_stock_query()
            elif intent == 'category_search':
                return self._handle_category_search(entities)
            elif intent == 'add_stock':
                return self._handle_add_stock(entities, user_id)
            elif intent == 'remove_stock':
                return self._handle_remove_stock(entities, user_id)
            elif intent == 'set_stock':
                return self._handle_set_stock(entities, user_id)
            elif intent == 'add_product':
                return self._handle_add_product(entities, normalized_query, user_id)
            elif intent == 'delete_product':
                return self._handle_delete_product(entities, user_id)
            elif intent == 'demand_forecast':
                return self._handle_demand_forecast()
            elif intent == 'space_optimization':
                return self._handle_space_optimization()
            elif intent == 'alerts':
                return self._handle_alerts_query()
            else:
                # Use RAG for general knowledge queries
                return self._handle_general_query(query)
                
        except Exception as e:
            logger.error(f"Error processing natural language query: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to process query: {str(e)}",
                "intent": "error",
                "action": "none"
            }
    
    def _classify_intent(self, query: str) -> Tuple[str, List[str]]:
        """Classify the intent of the query and extract entities"""
        
        entities = []
        
        # Try exact pattern matching first
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, query, re.IGNORECASE)
                if match:
                    entities = list(match.groups())
                    return intent, entities
        
        # Try keyword-based classification for more general queries
        query_lower = query.lower()
        
        # Stock checking keywords
        if any(word in query_lower for word in ['stock', 'inventory', 'level', 'quantity', 'how many']):
            # Try to extract product SKU from the query
            sku_match = re.search(r'\b([A-Z]{2,}\d{3,}|\w+\d+)\b', query, re.IGNORECASE)
            if sku_match:
                return 'stock_check', [sku_match.group(1)]
            elif 'electronics' in query_lower:
                return 'category_search', ['Electronics']
            elif 'tools' in query_lower:
                return 'category_search', ['Tools']
            elif 'office' in query_lower:
                return 'category_search', ['Office Supplies']
            elif 'components' in query_lower:
                return 'category_search', ['Components']
            else:
                return 'stock_check', []
        
        # Low stock alerts
        if any(phrase in query_lower for phrase in ['low stock', 'running low', 'need reorder', 'stock alert']):
            return 'low_stock', []
        
        # Category searches
        if any(word in query_lower for word in ['category', 'list', 'show all', 'all products']):
            if 'electronics' in query_lower:
                return 'category_search', ['Electronics']
            elif 'tools' in query_lower:
                return 'category_search', ['Tools']
            elif 'office' in query_lower:
                return 'category_search', ['Office Supplies']
            elif 'components' in query_lower:
                return 'category_search', ['Components']
            else:
                return 'category_search', []
        
        # Adding stock
        if any(word in query_lower for word in ['add', 'increase', 'receive']):
            # Try to extract quantity and SKU
            qty_match = re.search(r'(\d+)', query)
            sku_match = re.search(r'\b([A-Z]{2,}\d{3,}|\w+\d+)\b', query, re.IGNORECASE)
            if qty_match and sku_match:
                return 'add_stock', [qty_match.group(1), sku_match.group(1)]
        
        # Removing stock
        if any(word in query_lower for word in ['remove', 'decrease', 'dispatch']):
            qty_match = re.search(r'(\d+)', query)
            sku_match = re.search(r'\b([A-Z]{2,}\d{3,}|\w+\d+)\b', query, re.IGNORECASE)
            if qty_match and sku_match:
                return 'remove_stock', [qty_match.group(1), sku_match.group(1)]
        
        # Setting stock
        if any(phrase in query_lower for phrase in ['set', 'update', 'change']):
            qty_match = re.search(r'(\d+)', query)
            sku_match = re.search(r'\b([A-Z]{2,}\d{3,}|\w+\d+)\b', query, re.IGNORECASE)
            if qty_match and sku_match:
                return 'set_stock', [sku_match.group(1), qty_match.group(1)]
        
        # Forecasting
        if any(word in query_lower for word in ['forecast', 'predict', 'demand']):
            return 'demand_forecast', []
        
        # Space optimization
        if any(word in query_lower for word in ['optimize', 'layout', 'space']):
            return 'space_optimization', []
        
        # Alerts
        if any(word in query_lower for word in ['alert', 'warning', 'notification']):
            return 'alerts', []
        
        # Product management
        if 'delete' in query_lower or 'remove' in query_lower:
            sku_match = re.search(r'\b([A-Z]{2,}\d{3,}|\w+\d+)\b', query, re.IGNORECASE)
            if sku_match:
                return 'delete_product', [sku_match.group(1)]
        
        if any(phrase in query_lower for phrase in ['new product', 'add product', 'create product']):
            sku_match = re.search(r'\b([A-Z]{2,}\d{3,}|\w+\d+)\b', query, re.IGNORECASE)
            if sku_match:
                return 'add_product', [sku_match.group(1)]
        
        return 'general_query', []
    
    def _handle_stock_check(self, entities: List[str], query: str) -> Dict[str, Any]:
        """Handle stock level checking queries"""
        
        if not entities:
            # General stock overview
            products = self.db.query(Product).join(Inventory).limit(10).all()
            stock_info = []
            
            for product in products:
                inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
                stock_info.append({
                    "sku": product.sku,
                    "name": product.name,
                    "available": inventory.available_quantity if inventory else 0,
                    "total": inventory.quantity if inventory else 0,
                    "reserved": inventory.reserved_quantity if inventory else 0,
                    "location": product.location,
                    "reorder_level": product.reorder_level
                })
            
            return {
                "success": True,
                "intent": "stock_check",
                "action": "query",
                "data": stock_info,
                "message": f"Found {len(stock_info)} products with current stock levels",
                "summary": f"Showing stock levels for {len(stock_info)} products"
            }
        
        else:
            # Specific product stock check
            sku = entities[0].upper()
            product = self.db.query(Product).filter(Product.sku.ilike(f"%{sku}%")).first()
            
            if not product:
                # Try fuzzy matching
                products = self.db.query(Product).filter(
                    or_(
                        Product.name.ilike(f"%{sku}%"),
                        Product.sku.ilike(f"%{sku}%")
                    )
                ).limit(5).all()
                
                if products:
                    suggestions = [{"sku": p.sku, "name": p.name} for p in products]
                    return {
                        "success": False,
                        "intent": "stock_check",
                        "action": "suggestion",
                        "error": f"Product '{sku}' not found",
                        "suggestions": suggestions,
                        "message": f"Did you mean one of these products?"
                    }
                else:
                    return {
                        "success": False,
                        "intent": "stock_check", 
                        "action": "error",
                        "error": f"Product '{sku}' not found in database"
                    }
            
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
            
            return {
                "success": True,
                "intent": "stock_check",
                "action": "query",
                "data": {
                    "sku": product.sku,
                    "name": product.name,
                    "available": inventory.available_quantity if inventory else 0,
                    "total": inventory.quantity if inventory else 0,
                    "reserved": inventory.reserved_quantity if inventory else 0,
                    "location": product.location,
                    "reorder_level": product.reorder_level,
                    "unit_price": product.unit_price,
                    "category": product.category
                },
                "message": f"Stock level for {product.sku}: {inventory.available_quantity if inventory else 0} available",
                "alert": "LOW STOCK" if inventory and inventory.available_quantity <= product.reorder_level else None
            }
    
    def _handle_add_stock(self, entities: List[str], user_id: int = None) -> Dict[str, Any]:
        """Handle adding stock operations"""
        
        if len(entities) < 2:
            return {
                "success": False,
                "intent": "add_stock",
                "action": "error",
                "error": "Please specify both quantity and product SKU (e.g., 'add 50 units to ELEC001')"
            }
        
        try:
            quantity = int(entities[0])
            sku = entities[1].upper()
        except (ValueError, IndexError):
            return {
                "success": False,
                "intent": "add_stock",
                "action": "error", 
                "error": "Invalid quantity or SKU format"
            }
        
        # Find product
        product = self.db.query(Product).filter(Product.sku.ilike(f"%{sku}%")).first()
        if not product:
            return {
                "success": False,
                "intent": "add_stock",
                "action": "error",
                "error": f"Product '{sku}' not found"
            }
        
        # Update inventory
        try:
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
            if not inventory:
                # Create new inventory record
                inventory = Inventory(
                    product_id=product.id,
                    quantity=quantity,
                    reserved_quantity=0,
                    available_quantity=quantity
                )
                self.db.add(inventory)
            else:
                # Update existing inventory
                inventory.quantity += quantity
                inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
                inventory.last_updated = datetime.utcnow()
            
            # Create stock movement record
            movement = StockMovement(
                product_id=product.id,
                movement_type="inbound",
                quantity=quantity,
                reference_type="manual_adjustment",
                reference_id=None,
                reason="Manual stock addition via natural language",
                notes=f"Added {quantity} units via chatbot",
                created_by=f"user_{user_id}" if user_id else "system"
            )
            self.db.add(movement)
            
            self.db.commit()
            
            # Re-index for RAG
            self._update_rag_product_data(product.id)
            
            return {
                "success": True,
                "intent": "add_stock",
                "action": "insert",
                "data": {
                    "sku": product.sku,
                    "name": product.name,
                    "added_quantity": quantity,
                    "new_total": inventory.quantity,
                    "new_available": inventory.available_quantity
                },
                "message": f"Successfully added {quantity} units to {product.sku}. New total: {inventory.quantity}",
                "confirmation": f"✅ Stock updated: {product.sku} (+{quantity} units)"
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "intent": "add_stock",
                "action": "error",
                "error": f"Failed to update stock: {str(e)}"
            }
    
    def _handle_delete_product(self, entities: List[str], user_id: int = None) -> Dict[str, Any]:
        """Handle product deletion operations"""
        
        if not entities:
            return {
                "success": False,
                "intent": "delete_product",
                "action": "error",
                "error": "Please specify the product SKU to delete"
            }
        
        sku = entities[0].upper()
        
        # Find product
        product = self.db.query(Product).filter(Product.sku.ilike(f"%{sku}%")).first()
        if not product:
            return {
                "success": False,
                "intent": "delete_product",
                "action": "error",
                "error": f"Product '{sku}' not found"
            }
        
        # Check if product has active inventory
        inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
        if inventory and inventory.quantity > 0:
            return {
                "success": False,
                "intent": "delete_product",
                "action": "warning",
                "error": f"Cannot delete {sku}. Product has {inventory.quantity} units in stock. Please deplete stock first.",
                "data": {
                    "sku": product.sku,
                    "name": product.name,
                    "current_stock": inventory.quantity,
                    "suggestion": "Set stock to 0 first or transfer to another location"
                }
            }
        
        try:
            # Store product info for response
            product_info = {
                "sku": product.sku,
                "name": product.name,
                "category": product.category
            }
            
            # Delete related records first
            self.db.query(Inventory).filter(Inventory.product_id == product.id).delete()
            self.db.query(StockMovement).filter(StockMovement.product_id == product.id).delete()
            self.db.query(ProductVelocity).filter(ProductVelocity.product_id == product.id).delete()
            self.db.query(StockAlert).filter(StockAlert.product_id == product.id).delete()
            
            # Delete product
            self.db.delete(product)
            
            # Create deletion record
            movement = StockMovement(
                product_id=None,
                movement_type="deletion",
                quantity=0,
                reference_type="product_deletion",
                reference_id=product.id,
                reason=f"Product {sku} deleted via natural language",
                notes=f"Product {product.name} removed from system",
                created_by=f"user_{user_id}" if user_id else "system"
            )
            self.db.add(movement)
            
            self.db.commit()
            
            # Update RAG index
            self._remove_from_rag_index(product.id)
            
            return {
                "success": True,
                "intent": "delete_product",
                "action": "delete",
                "data": product_info,
                "message": f"Product {sku} ({product_info['name']}) has been successfully deleted",
                "confirmation": f"🗑️ Deleted: {sku} - {product_info['name']}"
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "intent": "delete_product",
                "action": "error",
                "error": f"Failed to delete product: {str(e)}"
            }
    
    def _handle_low_stock_query(self) -> Dict[str, Any]:
        """Handle low stock queries"""
        
        low_stock_products = self.db.query(Product, Inventory).join(Inventory).filter(
            Inventory.available_quantity <= Product.reorder_level
        ).all()
        
        if not low_stock_products:
            return {
                "success": True,
                "intent": "low_stock",
                "action": "query",
                "data": [],
                "message": "✅ No products with low stock levels",
                "summary": "All products are adequately stocked"
            }
        
        low_stock_data = []
        for product, inventory in low_stock_products:
            urgency = "CRITICAL" if inventory.available_quantity <= (product.reorder_level * 0.5) else "WARNING"
            low_stock_data.append({
                "sku": product.sku,
                "name": product.name,
                "current_stock": inventory.available_quantity,
                "reorder_level": product.reorder_level,
                "urgency": urgency,
                "location": product.location,
                "suggested_reorder": product.reorder_level * 2
            })
        
        return {
            "success": True,
            "intent": "low_stock",
            "action": "query",
            "data": low_stock_data,
            "message": f"⚠️ Found {len(low_stock_data)} products with low stock",
            "summary": f"{len(low_stock_data)} products need restocking"
        }
    
    def _index_comprehensive_warehouse_data(self):
        """Index comprehensive warehouse data for RAG"""
        
        if not self.vector_store:
            return
        
        try:
            # Check if already indexed
            if self.vector_store._collection.count() > 100:
                logger.info("Vector store already contains comprehensive data")
                return
            
            documents = []
            
            # Index all products with detailed information
            products = self.db.query(Product).all()
            for product in products:
                inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
                velocity = self.db.query(ProductVelocity).filter(ProductVelocity.product_id == product.id).first()
                
                content = f"""
                Product: {product.sku} - {product.name}
                Category: {product.category}
                Description: {product.description or 'No description'}
                Unit Price: ${product.unit_price}
                Reorder Level: {product.reorder_level}
                Location: {product.location or 'Not assigned'}
                Current Stock: {inventory.quantity if inventory else 0} total
                Available Stock: {inventory.available_quantity if inventory else 0} available
                Reserved Stock: {inventory.reserved_quantity if inventory else 0} reserved
                Stock Status: {'LOW STOCK' if inventory and inventory.available_quantity <= product.reorder_level else 'NORMAL'}
                Velocity: {velocity.velocity_category if velocity else 'unknown'} moving
                Last Updated: {inventory.last_updated if inventory else 'never'}
                
                Operations:
                - Check stock: "What is the stock level of {product.sku}?"
                - Add stock: "Add [quantity] to {product.sku}"
                - Remove stock: "Remove [quantity] from {product.sku}"
                - Update stock: "Set {product.sku} stock to [quantity]"
                """
                
                doc = Document(
                    page_content=content.strip(),
                    metadata={
                        "type": "product_detailed",
                        "sku": product.sku,
                        "product_id": product.id,
                        "category": product.category,
                        "stock_level": inventory.available_quantity if inventory else 0
                    }
                )
                documents.append(doc)
            
            # Index warehouse procedures and commands
            procedures = self._get_enhanced_procedures()
            for procedure in procedures:
                doc = Document(
                    page_content=procedure["content"],
                    metadata={
                        "type": "procedure",
                        "category": procedure["category"],
                        "title": procedure["title"]
                    }
                )
                documents.append(doc)
            
            # Index sample natural language commands
            nl_commands = self._get_natural_language_examples()
            for command in nl_commands:
                doc = Document(
                    page_content=command["content"],
                    metadata={
                        "type": "nl_command",
                        "intent": command["intent"],
                        "category": command["category"]
                    }
                )
                documents.append(doc)
            
            # Add documents to vector store
            if documents:
                chunk_size = int(os.getenv("CHUNK_SIZE", "800"))
                chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "100"))
                
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                
                split_docs = text_splitter.split_documents(documents)
                self.vector_store.add_documents(split_docs)
                self.vector_store.persist()
                
                logger.info(f"Indexed {len(split_docs)} enhanced document chunks")
                
        except Exception as e:
            logger.error(f"Error indexing enhanced warehouse data: {str(e)}")
    
    def _get_natural_language_examples(self) -> List[Dict[str, str]]:
        """Get natural language command examples for RAG"""
        
        return [
            {
                "intent": "stock_check",
                "category": "query",
                "content": """
                Stock Level Queries:
                - "What is the current stock of ELEC001?"
                - "How many units of wireless headphones do we have?"
                - "Show me stock levels for all electronics"
                - "Check inventory for product TOOL001"
                - "What's the available quantity of USB chargers?"
                """
            },
            {
                "intent": "stock_modification",
                "category": "operation",
                "content": """
                Stock Modification Commands:
                - "Add 100 units to ELEC001"
                - "Increase stock of COMP001 by 50"
                - "Remove 25 units from TOOL002"
                - "Set OFFC001 stock to 200"
                - "Decrease inventory of ELEC003 by 10"
                """
            },
            {
                "intent": "product_management",
                "category": "operation",
                "content": """
                Product Management Commands:
                - "Add new product with SKU NEWPROD001"
                - "Delete product OLDPROD001"
                - "Create product called 'Smart Speaker'"
                - "Remove discontinued item DISC001"
                - "Discontinue product TOOL999"
                """
            },
            {
                "intent": "analytics",
                "category": "analysis",
                "content": """
                Analytics and Reporting:
                - "Show me low stock alerts"
                - "Generate demand forecast"
                - "What products need reordering?"
                - "Optimize warehouse layout"
                - "Show overstock items"
                """
            }
        ]
    
    def _get_enhanced_procedures(self) -> List[Dict[str, str]]:
        """Get enhanced warehouse procedures"""
        
        return [
            {
                "title": "Natural Language Stock Operations",
                "category": "inventory",
                "content": """
                Natural Language Inventory Management:
                
                STOCK CHECKING:
                - Use product SKU or name in queries
                - Examples: "stock level of ELEC001", "how many headphones"
                - System shows: available, total, reserved quantities
                
                ADDING STOCK:
                - Format: "add [quantity] to [SKU]"
                - Examples: "add 50 units to ELEC001", "receive 100 COMP001"
                - Creates automatic stock movement record
                
                REMOVING STOCK:
                - Format: "remove [quantity] from [SKU]"
                - Examples: "remove 25 from TOOL001", "dispatch 10 ELEC002"
                - Updates available quantity immediately
                
                SETTING STOCK:
                - Format: "set [SKU] stock to [quantity]"
                - Examples: "set OFFC001 to 200", "update COMP005 to 150"
                - Adjusts total quantity to specified amount
                """
            },
            {
                "title": "Product Lifecycle Management",
                "category": "products",
                "content": """
                Product Management via Natural Language:
                
                ADDING PRODUCTS:
                - Use: "add new product [SKU]" or "create product [name]"
                - System will prompt for additional details
                - Automatically creates inventory record
                
                DELETING PRODUCTS:
                - Use: "delete product [SKU]" or "remove [SKU]"
                - System checks for existing stock first
                - Requires stock depletion before deletion
                
                PRODUCT INFORMATION:
                - Use: "show product [SKU]" or "details of [name]"
                - Displays full product information
                - Includes stock levels and location
                """
            },
            {
                "title": "Advanced Analytics Commands",
                "category": "analytics",
                "content": """
                Advanced Warehouse Analytics:
                
                LOW STOCK ALERTS:
                - "show low stock" or "what needs reordering"
                - Lists products below reorder level
                - Prioritizes by urgency (critical/warning)
                
                DEMAND FORECASTING:
                - "generate forecast" or "predict demand"
                - Uses historical data and trends
                - Provides weekly/monthly predictions
                
                SPACE OPTIMIZATION:
                - "optimize layout" or "improve warehouse space"
                - Analyzes product velocity and location
                - Suggests layout improvements
                
                OVERSTOCK ANALYSIS:
                - "show overstock" or "excess inventory"
                - Identifies products with too much stock
                - Suggests redistribution strategies
                """
            }
        ]
    
    def _update_rag_product_data(self, product_id: int):
        """Update RAG index when product data changes"""
        
        if not self.vector_store:
            return
        
        try:
            # This is a simplified approach - in production you might want
            # more sophisticated incremental updates
            logger.info(f"RAG index update triggered for product {product_id}")
            
        except Exception as e:
            logger.error(f"Error updating RAG index: {str(e)}")
    
    def _remove_from_rag_index(self, product_id: int):
        """Remove product from RAG index when deleted"""
        
        if not self.vector_store:
            return
        
        try:
            # This is a simplified approach - in production you might want
            # more sophisticated deletion from vector store
            logger.info(f"Product {product_id} removed from RAG index")
            
        except Exception as e:
            logger.error(f"Error removing from RAG index: {str(e)}")
    
    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Handle general queries using RAG"""
        
        if not self.retriever:
            return {
                "success": False,
                "intent": "general_query",
                "action": "error",
                "error": "RAG service not available for general queries"
            }
        
        try:
            # Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(query)
            
            if not docs:
                return {
                    "success": False,
                    "intent": "general_query", 
                    "action": "no_results",
                    "message": "No relevant information found for your query"
                }
            
            # Combine retrieved content
            context = "\n\n".join([doc.page_content for doc in docs[:3]])
            
            return {
                "success": True,
                "intent": "general_query",
                "action": "rag_response",
                "context": context,
                "message": "Found relevant information from warehouse knowledge base",
                "sources": len(docs)
            }
            
        except Exception as e:
            return {
                "success": False,
                "intent": "general_query",
                "action": "error",
                "error": f"Error retrieving information: {str(e)}"
            }
    
    def _handle_demand_forecast(self) -> Dict[str, Any]:
        """Handle demand forecasting requests"""
        
        try:
            # Get products with forecasting data
            forecasts = self.db.query(DemandForecast, Product).join(Product).limit(10).all()
            
            if not forecasts:
                return {
                    "success": True,
                    "intent": "demand_forecast",
                    "action": "generate",
                    "data": [],
                    "message": "No existing forecasts found. Generating new predictions...",
                    "summary": "Demand forecasting service would analyze historical data here"
                }
            
            forecast_data = []
            for forecast, product in forecasts:
                forecast_data.append({
                    "sku": product.sku,
                    "name": product.name,
                    "predicted_demand": forecast.predicted_demand,
                    "confidence": f"{forecast.confidence_level * 100:.1f}%",
                    "forecast_date": forecast.forecast_date.strftime("%Y-%m-%d"),
                    "forecast_type": forecast.forecast_type
                })
            
            return {
                "success": True,
                "intent": "demand_forecast",
                "action": "query",
                "data": forecast_data,
                "message": f"📈 Generated demand forecasts for {len(forecast_data)} products",
                "summary": f"Forecasting data available for {len(forecast_data)} products"
            }
            
        except Exception as e:
            return {
                "success": False,
                "intent": "demand_forecast",
                "action": "error",
                "error": f"Error generating forecast: {str(e)}"
            }
    
    def _handle_space_optimization(self) -> Dict[str, Any]:
        """Handle space optimization requests"""
        
        try:
            # Get space optimization suggestions
            optimizations = self.db.query(SpaceOptimization).filter(
                SpaceOptimization.status == "pending"
            ).limit(5).all()
            
            optimization_data = []
            for opt in optimizations:
                optimization_data.append({
                    "title": opt.title,
                    "description": opt.description,
                    "priority": opt.priority,
                    "expected_benefit": opt.expected_benefit,
                    "implementation_effort": opt.implementation_effort,
                    "affected_products": opt.affected_products or [],
                    "affected_zones": opt.affected_zones or []
                })
            
            return {
                "success": True,
                "intent": "space_optimization",
                "action": "analyze",
                "data": optimization_data,
                "message": f"🏗️ Found {len(optimization_data)} space optimization opportunities",
                "summary": f"Space optimization analysis complete - {len(optimization_data)} recommendations"
            }
            
        except Exception as e:
            return {
                "success": False,
                "intent": "space_optimization",
                "action": "error",
                "error": f"Error analyzing space optimization: {str(e)}"
            }
    
    def _handle_alerts_query(self) -> Dict[str, Any]:
        """Handle stock alerts queries"""
        
        try:
            alerts = self.db.query(StockAlert, Product).join(Product).filter(
                StockAlert.resolved == False
            ).order_by(StockAlert.severity.desc()).limit(10).all()
            
            alert_data = []
            for alert, product in alerts:
                alert_data.append({
                    "sku": product.sku,
                    "name": product.name,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "current_stock": alert.current_stock,
                    "recommended_stock": alert.recommended_stock,
                    "message": alert.message,
                    "urgency": alert.reorder_urgency,
                    "created_at": alert.created_at.strftime("%Y-%m-%d %H:%M")
                })
            
            return {
                "success": True,
                "intent": "alerts",
                "action": "query",
                "data": alert_data,
                "message": f"⚠️ Found {len(alert_data)} active stock alerts",
                "summary": f"Stock alerts: {len(alert_data)} requiring attention"
            }
            
        except Exception as e:
            return {
                "success": False,
                "intent": "alerts",
                "action": "error",
                "error": f"Error retrieving alerts: {str(e)}"
            }
    
    # Additional helper methods for more complex operations...
    
    def _handle_category_search(self, entities: List[str]) -> Dict[str, Any]:
        """Handle category-based product searches"""
        
        if not entities:
            # Show all categories
            categories = self.db.query(Product.category).distinct().all()
            category_list = [cat[0] for cat in categories if cat[0]]
            
            return {
                "success": True,
                "intent": "category_search",
                "action": "list_categories",
                "data": category_list,
                "message": f"Available categories: {', '.join(category_list)}",
                "summary": f"Found {len(category_list)} product categories"
            }
        
        category = entities[0].title()
        products = self.db.query(Product).filter(
            Product.category.ilike(f"%{category}%")
        ).all()
        
        if not products:
            return {
                "success": False,
                "intent": "category_search",
                "action": "not_found",
                "error": f"No products found in category '{category}'"
            }
        
        product_data = []
        for product in products:
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
            product_data.append({
                "sku": product.sku,
                "name": product.name,
                "stock": inventory.available_quantity if inventory else 0,
                "location": product.location,
                "price": product.unit_price
            })
        
        return {
            "success": True,
            "intent": "category_search",
            "action": "query",
            "data": product_data,
            "message": f"Found {len(product_data)} products in {category} category",
            "summary": f"{category} category: {len(product_data)} products"
        }
    
    def _handle_set_stock(self, entities: List[str], user_id: int = None) -> Dict[str, Any]:
        """Handle setting stock to specific levels"""
        
        if len(entities) < 2:
            return {
                "success": False,
                "intent": "set_stock",
                "action": "error",
                "error": "Please specify both product SKU and new quantity"
            }
        
        try:
            sku = entities[0].upper()
            new_quantity = int(entities[1])
        except (ValueError, IndexError):
            return {
                "success": False,
                "intent": "set_stock",
                "action": "error",
                "error": "Invalid SKU or quantity format"
            }
        
        # Find product
        product = self.db.query(Product).filter(Product.sku.ilike(f"%{sku}%")).first()
        if not product:
            return {
                "success": False,
                "intent": "set_stock",
                "action": "error",
                "error": f"Product '{sku}' not found"
            }
        
        try:
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
            if not inventory:
                # Create new inventory
                inventory = Inventory(
                    product_id=product.id,
                    quantity=new_quantity,
                    reserved_quantity=0,
                    available_quantity=new_quantity
                )
                self.db.add(inventory)
                movement_type = "adjustment"
                quantity_change = new_quantity
            else:
                # Update existing inventory
                old_quantity = inventory.quantity
                quantity_change = new_quantity - old_quantity
                movement_type = "adjustment"
                
                inventory.quantity = new_quantity
                inventory.available_quantity = new_quantity - inventory.reserved_quantity
                inventory.last_updated = datetime.utcnow()
            
            # Create stock movement
            movement = StockMovement(
                product_id=product.id,
                movement_type=movement_type,
                quantity=quantity_change,
                reference_type="manual_adjustment",
                reference_id=None,
                reason=f"Stock set to {new_quantity} via natural language",
                notes=f"Stock level adjusted to {new_quantity}",
                created_by=f"user_{user_id}" if user_id else "system"
            )
            self.db.add(movement)
            
            self.db.commit()
            
            return {
                "success": True,
                "intent": "set_stock",
                "action": "update",
                "data": {
                    "sku": product.sku,
                    "name": product.name,
                    "old_quantity": old_quantity if 'old_quantity' in locals() else 0,
                    "new_quantity": new_quantity,
                    "change": quantity_change,
                    "available": inventory.available_quantity
                },
                "message": f"Stock level for {product.sku} set to {new_quantity} units",
                "confirmation": f"📝 Updated: {product.sku} stock = {new_quantity}"
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "intent": "set_stock",
                "action": "error",
                "error": f"Failed to update stock: {str(e)}"
            }
    
    def _handle_remove_stock(self, entities: List[str], user_id: int = None) -> Dict[str, Any]:
        """Handle removing stock operations"""
        
        if len(entities) < 2:
            return {
                "success": False,
                "intent": "remove_stock",
                "action": "error",
                "error": "Please specify both quantity and product SKU"
            }
        
        try:
            quantity = int(entities[0])
            sku = entities[1].upper()
        except (ValueError, IndexError):
            return {
                "success": False,
                "intent": "remove_stock",
                "action": "error",
                "error": "Invalid quantity or SKU format"
            }
        
        # Find product
        product = self.db.query(Product).filter(Product.sku.ilike(f"%{sku}%")).first()
        if not product:
            return {
                "success": False,
                "intent": "remove_stock",
                "action": "error",
                "error": f"Product '{sku}' not found"
            }
        
        # Check current inventory
        inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
        if not inventory or inventory.available_quantity < quantity:
            available = inventory.available_quantity if inventory else 0
            return {
                "success": False,
                "intent": "remove_stock",
                "action": "insufficient_stock",
                "error": f"Insufficient stock. Available: {available}, Requested: {quantity}",
                "data": {
                    "sku": product.sku,
                    "available": available,
                    "requested": quantity
                }
            }
        
        try:
            # Update inventory
            inventory.quantity -= quantity
            inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
            inventory.last_updated = datetime.utcnow()
            
            # Create stock movement
            movement = StockMovement(
                product_id=product.id,
                movement_type="outbound",
                quantity=-quantity,  # Negative for outbound
                reference_type="manual_adjustment",
                reference_id=None,
                reason="Manual stock removal via natural language",
                notes=f"Removed {quantity} units via chatbot",
                created_by=f"user_{user_id}" if user_id else "system"
            )
            self.db.add(movement)
            
            self.db.commit()
            
            return {
                "success": True,
                "intent": "remove_stock",
                "action": "update",
                "data": {
                    "sku": product.sku,
                    "name": product.name,
                    "removed_quantity": quantity,
                    "new_total": inventory.quantity,
                    "new_available": inventory.available_quantity
                },
                "message": f"Successfully removed {quantity} units from {product.sku}. Remaining: {inventory.quantity}",
                "confirmation": f"✅ Stock updated: {product.sku} (-{quantity} units)",
                "alert": "LOW STOCK" if inventory.available_quantity <= product.reorder_level else None
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "intent": "remove_stock",
                "action": "error",
                "error": f"Failed to update stock: {str(e)}"
            }
    
    def _handle_add_product(self, entities: List[str], query: str, user_id: int = None) -> Dict[str, Any]:
        """Handle adding new products"""
        
        if not entities:
            return {
                "success": False,
                "intent": "add_product",
                "action": "error",
                "error": "Please specify product SKU or name"
            }
        
        # Extract product information from query
        sku = entities[0].upper()
        
        # Check if product already exists
        existing = self.db.query(Product).filter(Product.sku == sku).first()
        if existing:
            return {
                "success": False,
                "intent": "add_product",
                "action": "duplicate",
                "error": f"Product with SKU '{sku}' already exists",
                "data": {
                    "existing_sku": existing.sku,
                    "existing_name": existing.name
                }
            }
        
        # For now, create a basic product - in production you'd want to collect more details
        try:
            product = Product(
                sku=sku,
                name=f"New Product {sku}",
                description="Product added via natural language - please update details",
                category="Uncategorized",
                unit="pcs",
                unit_price=0.0,
                reorder_level=10,
                location="TBD"
            )
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            
            # Create initial inventory
            inventory = Inventory(
                product_id=product.id,
                quantity=0,
                reserved_quantity=0,
                available_quantity=0
            )
            self.db.add(inventory)
            self.db.commit()
            
            return {
                "success": True,
                "intent": "add_product",
                "action": "insert",
                "data": {
                    "sku": product.sku,
                    "name": product.name,
                    "id": product.id
                },
                "message": f"Created new product {sku}. Please update details like name, category, and price.",
                "confirmation": f"➕ Created: {sku}",
                "next_steps": "Update product details: name, category, price, description"
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "intent": "add_product",
                "action": "error",
                "error": f"Failed to create product: {str(e)}"
            }
