import os
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema import BaseRetriever
from ..models.database_models import Product, Inventory, Vendor, Customer, InboundShipment, OutboundOrder

logger = logging.getLogger(__name__)

class WarehouseRAGService:
    """RAG service for warehouse knowledge retrieval"""
    
    def __init__(self, db: Session):
        self.db = db
        self.vector_store = None
        self.retriever = None
        self.embeddings = None
        self._initialize_rag()
    
    def _initialize_rag(self):
        """Initialize RAG components"""
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
                collection_name="warehouse_knowledge"
            )
            
            # Create retriever
            top_k = int(os.getenv("TOP_K_RETRIEVAL", "5"))
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": top_k}
            )
            
            # Index warehouse data
            self._index_warehouse_data()
            
            logger.info("RAG service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {str(e)}")
            raise
    
    def _index_warehouse_data(self):
        """Index warehouse data into vector store"""
        try:
            # Check if data is already indexed
            if self.vector_store._collection.count() > 0:
                logger.info("Vector store already contains data, skipping indexing")
                return
            
            documents = []
            
            # Index product information
            products = self.db.query(Product).all()
            for product in products:
                inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
                
                content = f"""
                Product Information:
                SKU: {product.sku}
                Name: {product.name}
                Description: {product.description or 'No description'}
                Category: {product.category}
                Unit: {product.unit}
                Unit Price: ${product.unit_price}
                Reorder Level: {product.reorder_level}
                Location: {product.location or 'Not specified'}
                Current Stock: {inventory.quantity if inventory else 0}
                Available Stock: {inventory.available_quantity if inventory else 0}
                Reserved Stock: {inventory.reserved_quantity if inventory else 0}
                """
                
                doc = Document(
                    page_content=content.strip(),
                    metadata={
                        "type": "product",
                        "sku": product.sku,
                        "product_id": product.id,
                        "category": product.category
                    }
                )
                documents.append(doc)
            
            # Index vendor information
            vendors = self.db.query(Vendor).all()
            for vendor in vendors:
                content = f"""
                Vendor Information:
                Name: {vendor.name}
                Contact Person: {vendor.contact_person or 'Not specified'}
                Phone: {vendor.phone or 'Not specified'}
                Email: {vendor.email or 'Not specified'}
                Address: {vendor.address or 'Not specified'}
                """
                
                doc = Document(
                    page_content=content.strip(),
                    metadata={
                        "type": "vendor",
                        "vendor_id": vendor.id,
                        "name": vendor.name
                    }
                )
                documents.append(doc)
            
            # Index customer information
            customers = self.db.query(Customer).all()
            for customer in customers:
                content = f"""
                Customer Information:
                Name: {customer.name}
                Contact Person: {customer.contact_person or 'Not specified'}
                Phone: {customer.phone or 'Not specified'}
                Email: {customer.email or 'Not specified'}
                Address: {customer.address or 'Not specified'}
                """
                
                doc = Document(
                    page_content=content.strip(),
                    metadata={
                        "type": "customer",
                        "customer_id": customer.id,
                        "name": customer.name
                    }
                )
                documents.append(doc)
            
            # Index operational procedures
            procedures = self._get_warehouse_procedures()
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
            
            # Split and add documents to vector store
            if documents:
                chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
                chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
                
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    length_function=len,
                )
                
                split_docs = text_splitter.split_documents(documents)
                self.vector_store.add_documents(split_docs)
                self.vector_store.persist()
                
                logger.info(f"Indexed {len(split_docs)} document chunks into vector store")
            
        except Exception as e:
            logger.error(f"Error indexing warehouse data: {str(e)}")
            raise
    
    def _get_warehouse_procedures(self) -> List[Dict[str, str]]:
        """Get warehouse operational procedures"""
        return [
            {
                "title": "Inventory Check Procedure",
                "category": "inventory",
                "content": """
                To check inventory levels:
                1. Use SKU codes to identify products (format: PROD001, PROD002, etc.)
                2. Available quantity = Total quantity - Reserved quantity
                3. Reserved quantity is stock allocated to pending orders
                4. Check location codes for physical warehouse location
                5. Monitor reorder levels for low stock alerts
                """
            },
            {
                "title": "Stock Update Procedure",
                "category": "inventory",
                "content": """
                To update stock levels:
                1. For receiving inventory: Add quantity to current stock
                2. For adjustments: Set new quantity level
                3. Always record reason for stock movements
                4. Update available quantity automatically
                5. Create stock movement record for audit trail
                """
            },
            {
                "title": "Inbound Gate-In Procedure",
                "category": "inbound",
                "content": """
                For processing inbound shipments:
                1. Verify shipment number (format: SH001, SH002, etc.)
                2. Check vendor information and expected delivery date
                3. Update shipment status to 'arrived' upon gate-in
                4. Proceed with quality check and receiving process
                5. Update inventory levels after quality approval
                """
            },
            {
                "title": "Outbound Dispatch Procedure",
                "category": "outbound",
                "content": """
                For processing outbound orders:
                1. Verify order number (format: ORD001, ORD002, etc.)
                2. Check customer information and delivery address
                3. Update order status to 'dispatched' when ready
                4. Generate tracking information if available
                5. Notify customer of dispatch
                """
            },
            {
                "title": "Low Stock Alert Procedure",
                "category": "alerts",
                "content": """
                For managing low stock alerts:
                1. Monitor products where available quantity < reorder level
                2. Prioritize fast-moving and critical items
                3. Check vendor information for reordering
                4. Review historical demand patterns
                5. Create purchase orders for replenishment
                """
            }
        ]
    
    def retrieve_relevant_info(self, query: str, top_k: Optional[int] = None) -> List[Document]:
        """Retrieve relevant information for a query"""
        try:
            if not self.retriever:
                logger.warning("Retriever not initialized")
                return []
            
            # Use custom top_k if provided
            if top_k:
                retriever = self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": top_k}
                )
                return retriever.get_relevant_documents(query)
            
            return self.retriever.get_relevant_documents(query)
            
        except Exception as e:
            logger.error(f"Error retrieving relevant info: {str(e)}")
            return []
    
    def get_context_for_query(self, query: str) -> str:
        """Get formatted context string for a query"""
        try:
            relevant_docs = self.retrieve_relevant_info(query)
            
            if not relevant_docs:
                return "No relevant warehouse information found."
            
            context_parts = []
            for i, doc in enumerate(relevant_docs, 1):
                context_parts.append(f"Context {i}:\n{doc.page_content}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting context: {str(e)}")
            return "Error retrieving warehouse context."
    
    def update_product_info(self, product_id: int):
        """Update specific product information in vector store"""
        try:
            # This would be called when product data changes
            # For now, we'll implement a simple re-indexing
            # In production, you'd want to update only the specific document
            logger.info(f"Product {product_id} updated, consider re-indexing")
            
        except Exception as e:
            logger.error(f"Error updating product info: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if RAG service is available"""
        return self.vector_store is not None and self.retriever is not None
