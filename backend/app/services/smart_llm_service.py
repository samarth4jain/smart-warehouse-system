import os
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SmartLLMService:
    """Smart LLM service that tries multiple approaches"""
    
    def __init__(self):
        self.llm = None
        self.service_type = None
        self._initialize_best_available_llm()
    
    def _initialize_best_available_llm(self):
        """Try different LLM approaches in order of preference"""
        
        # Method 1: Try Hugging Face Inference API (fastest to start)
        if self._try_huggingface_inference():
            return
        
        # Method 2: Fall back to Smart Mock Service
        self._initialize_smart_mock()
        
    def _try_huggingface_inference(self) -> bool:
        """Try to initialize HuggingFace Inference API"""
        try:
            model_name = os.getenv("LLM_MODEL_NAME", "microsoft/DialoGPT-medium")
            api_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
            
            if not api_token:
                logger.warning("No HuggingFace token found, skipping HF Inference API")
                return False
                
            api_url = f"https://api-inference.huggingface.co/models/{model_name}"
            
            # Test the API with a simple request
            test_wrapper = HuggingFaceInferenceWrapper(model_name, api_token, api_url)
            test_response = test_wrapper.generate_response("test", max_length=10)
            
            if test_response and "error" not in test_response.lower():
                self.llm = test_wrapper
                self.service_type = "huggingface_inference"
                logger.info(f"Successfully initialized HuggingFace Inference API with {model_name}")
                return True
            else:
                logger.warning(f"HuggingFace Inference API test failed: {test_response}")
                return False
                
        except Exception as e:
            logger.warning(f"Failed to initialize HuggingFace Inference API: {str(e)}")
            return False
    
    def _initialize_smart_mock(self):
        """Initialize the Smart Mock LLM service as fallback"""
        try:
            self.llm = SmartMockLLMService()
            self.service_type = "smart_mock"
            logger.info("Initialized Smart Mock LLM Service")
        except Exception as e:
            logger.error(f"Failed to initialize Smart Mock LLM: {str(e)}")
            raise
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using the available LLM service"""
        try:
            return self.llm.generate_response(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Error generating response with {self.service_type}: {str(e)}")
            return "I'm experiencing technical difficulties. Please try again."
    
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return self.llm is not None
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about current service"""
        return {
            "service_type": self.service_type,
            "available": self.is_available(),
        }


class HuggingFaceInferenceWrapper:
    """Wrapper for Hugging Face Inference API"""
    
    def __init__(self, model_name: str, api_token: str, api_url: str):
        self.model_name = model_name
        self.api_token = api_token
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {api_token}"}
    
    def generate_response(self, prompt: str, max_length: int = 100, **kwargs) -> str:
        """Generate response using HuggingFace Inference API"""
        try:
            # Format prompt for instruction-following models like Sheared LLaMA
            if "llama" in self.model_name.lower():
                formatted_prompt = f"<s>[INST] {prompt} [/INST]"
            else:
                formatted_prompt = prompt
            
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "").strip()
                    return generated_text if generated_text else "No response generated"
                else:
                    return "Invalid response format"
            else:
                logger.error(f"HF API error {response.status_code}: {response.text}")
                return f"API Error: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error calling HuggingFace API: {str(e)}")
            return f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if HF Inference API is available"""
        try:
            test_response = self.generate_response("test", max_length=5)
            return "error" not in test_response.lower()
        except:
            return False


class SmartMockLLMService:
    """Intelligent mock LLM service with warehouse-specific knowledge"""
    
    def __init__(self):
        self.warehouse_knowledge = {
            "inventory": {
                "PROD001": {"name": "Wireless Bluetooth Headphones", "stock": 137, "location": "A1-01"},
                "PROD002": {"name": "Smartphone Case", "stock": 89, "location": "A1-02"},
                "PROD003": {"name": "USB Cable", "stock": 45, "location": "B2-03"},
                "PROD004": {"name": "Laptop Charger", "stock": 23, "location": "B2-04"},
                "PROD005": {"name": "Wireless Mouse", "stock": 67, "location": "C1-05"},
                "PROD006": {"name": "Tablet Screen Protector", "stock": 8, "location": "C1-06"},  # Low stock
            },
            "shipments": {
                "SH001": {"vendor": "ABC Suppliers Ltd", "status": "arrived", "items": 150},
                "SH002": {"vendor": "TechParts Inc", "status": "in_transit", "items": 200},
            },
            "orders": {
                "ORD001": {"customer": "TechCorp Solutions", "status": "dispatched", "items": 5},
                "ORD002": {"customer": "Office Depot", "status": "ready", "items": 12},
            }
        }
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate intelligent warehouse-specific responses"""
        prompt_lower = prompt.lower()
        
        # Stock Check Responses
        if "check stock" in prompt_lower or "stock level" in prompt_lower:
            return self._handle_stock_check(prompt)
        
        # Inventory Summary
        elif "inventory summary" in prompt_lower or "show inventory" in prompt_lower:
            return self._generate_inventory_summary()
        
        # Inbound Operations
        elif "gate in" in prompt_lower or "inbound" in prompt_lower or "delivery arrived" in prompt_lower:
            return self._handle_inbound_operation(prompt)
        
        # Outbound Operations
        elif "dispatch" in prompt_lower or "ship order" in prompt_lower or "outbound" in prompt_lower:
            return self._handle_outbound_operation(prompt)
        
        # Stock Updates
        elif "update stock" in prompt_lower or "add inventory" in prompt_lower:
            return self._handle_stock_update(prompt)
        
        # Low Stock Alerts
        elif "low stock" in prompt_lower or "running low" in prompt_lower:
            return self._generate_low_stock_alert()
        
        # Help and Procedures
        elif "help" in prompt_lower or "what can you" in prompt_lower:
            return self._generate_help_response()
        
        elif "procedure" in prompt_lower or "how do i" in prompt_lower:
            return self._generate_procedure_guidance(prompt)
        
        # Vendor Information
        elif "vendor" in prompt_lower:
            return self._generate_vendor_info()
        
        # Categories
        elif "categories" in prompt_lower or "product categories" in prompt_lower:
            return self._generate_category_info()
        
        # General Greetings
        elif any(word in prompt_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return self._generate_greeting()
        
        # Default intelligent response
        else:
            return self._generate_default_response(prompt)
    
    def _handle_stock_check(self, prompt: str) -> str:
        """Handle stock check queries"""
        # Extract SKU from prompt
        words = prompt.upper().split()
        sku = None
        for i, word in enumerate(words):
            if word == "SKU:" and i + 1 < len(words):
                sku = words[i + 1]
                break
            elif word.startswith("PROD"):
                sku = word
                break
        
        if sku and sku in self.warehouse_knowledge["inventory"]:
            item = self.warehouse_knowledge["inventory"][sku]
            stock_status = "LOW STOCK" if item["stock"] < 20 else "IN STOCK"
            return (f"Stock Check Results\n\n"
                   f"Product: {item['name']}\n"
                   f"SKU: {sku}\n"
                   f"Available: {item['stock']} units\n"
                   f"Location: {item['location']}\n"
                   f"Status: {stock_status}\n\n"
                   f"{'Consider reordering soon!' if item['stock'] < 20 else 'Stock levels are healthy.'}")
        elif sku:
            return (f"Product Not Found\n\n"
                   f"SKU '{sku}' was not found in our inventory system.\n"
                   f"Please verify the SKU and try again.")
        else:
            return ("Stock Check Help\n\n"
                   "Please specify a SKU to check stock levels.\n"
                   f"Example: 'check stock SKU: PROD001'\n\n"
                   f"Available SKUs: {', '.join(self.warehouse_knowledge['inventory'].keys())}")
    
    def _generate_inventory_summary(self) -> str:
        """Generate comprehensive inventory summary"""
        total_items = sum(item["stock"] for item in self.warehouse_knowledge["inventory"].values())
        low_stock_items = [sku for sku, item in self.warehouse_knowledge["inventory"].items() 
                          if item["stock"] < 20]
        
        summary = (f"Warehouse Inventory Summary\n\n"
                  f"**Total Products**: {len(self.warehouse_knowledge['inventory'])} SKUs\n"
                  f"**Total Units**: {total_items} items\n"
                  f"**Low Stock Alerts**: {len(low_stock_items)} items\n\n")
        
        if low_stock_items:
            summary += " **Items Requiring Attention**:\n"
            for sku in low_stock_items:
                item = self.warehouse_knowledge["inventory"][sku]
                summary += f" {sku}: {item['name']} ({item['stock']} units)\n"
        
        return summary
    
    def _handle_inbound_operation(self, prompt: str) -> str:
        """Handle inbound operations"""
        words = prompt.upper().split()
        shipment_id = None
        for word in words:
            if word.startswith("SH"):
                shipment_id = word
                break
        
        if shipment_id and shipment_id in self.warehouse_knowledge["shipments"]:
            shipment = self.warehouse_knowledge["shipments"][shipment_id]
            return (f"**Inbound Processing Complete**\n\n"
                   f"**Shipment ID**: {shipment_id}\n"
                   f"**Vendor**: {shipment['vendor']}\n"
                   f"Status: {shipment['status'].title()}\n"
                   f"**Items Received**: {shipment['items']} units\n\n"
                   f"Next steps: Quality inspection and put-away process initiated.")
        else:
            return ("**Inbound Operation**\n\n"
                   "Ready to process inbound shipment!\n\n"
                   "Please provide shipment details:\n"
                   " Shipment ID (e.g., SH001)\n"
                   " Vendor information\n"
                   " Expected items count\n\n"
                   "Example: 'gate in shipment SH001'")
    
    def _handle_outbound_operation(self, prompt: str) -> str:
        """Handle outbound operations"""
        words = prompt.upper().split()
        order_id = None
        for word in words:
            if word.startswith("ORD"):
                order_id = word
                break
        
        if order_id and order_id in self.warehouse_knowledge["orders"]:
            order = self.warehouse_knowledge["orders"][order_id]
            return (f"Outbound Processing Complete\n\n"
                   f"**Order ID**: {order_id}\n"
                   f"**Customer**: {order['customer']}\n"
                   f"Status: {order['status'].title()}\n"
                   f"**Items**: {order['items']} units\n\n"
                   f"Order successfully prepared for dispatch!")
        else:
            return ("Outbound Operation\n\n"
                   "Ready to process outbound order!\n\n"
                   "Please provide order details:\n"
                   " Order ID (e.g., ORD001)\n"
                   " Customer information\n"
                   " Items to dispatch\n\n"
                   "Example: 'dispatch order ORD001'")
    
    def _handle_stock_update(self, prompt: str) -> str:
        """Handle stock update operations"""
        return ("Stock Update Processed\n\n"
               "Inventory levels have been updated successfully!\n\n"
               "Updated information:\n"
               " Quantity adjusted\n"
               " Location verified\n"
               " System records updated\n"
               " Audit trail created\n\n"
               "Tip: Use 'check stock SKU: [product]' to verify current levels.")
    
    def _generate_low_stock_alert(self) -> str:
        """Generate low stock alert"""
        low_stock_items = [(sku, item) for sku, item in self.warehouse_knowledge["inventory"].items() 
                          if item["stock"] < 20]
        
        if low_stock_items:
            alert = "Low Stock Alert\n\n"
            for sku, item in low_stock_items:
                alert += f" {sku}: {item['name']} - Only {item['stock']} units remaining\n"
            alert += "\nAction Required: Consider placing reorders for these items."
            return alert
        else:
            return "Stock Levels Healthy\n\nAll products are currently well-stocked. No immediate reorders needed."
    
    def _generate_help_response(self) -> str:
        """Generate comprehensive help response"""
        return ("Smart Warehouse Assistant - Help Guide\n\n"
               "I can help you with these warehouse operations:\n\n"
               "Inventory Management\n"
               " 'check stock SKU: PROD001' - Check specific product stock\n"
               " 'show inventory summary' - Get overall inventory status\n"
               " 'what products are running low?' - Low stock alerts\n\n"
               "Inbound Operations\n"
               " 'gate in shipment SH001' - Process incoming shipments\n"
               " 'delivery arrived from vendor' - General inbound processing\n\n"
               "Outbound Operations\n"
               " 'dispatch order ORD001' - Process outgoing orders\n"
               " 'ship order ORD002' - Prepare orders for shipping\n\n"
               "Updates & Reporting\n"
               " 'update stock received 25 units SKU: PROD003' - Stock adjustments\n"
               " 'add inventory 100 units PROD005' - Add new inventory\n\n"
               "Pro Tips: Be specific with SKUs, order IDs, and shipment numbers for best results!")
    
    def _generate_procedure_guidance(self, prompt: str) -> str:
        """Generate procedure guidance"""
        if "inbound" in prompt.lower():
            return ("Inbound Shipment Procedure\n\n"
                   "**Step 1**: Verify shipment details and documentation\n"
                   "**Step 2**: Check shipment ID and vendor information\n"
                   "**Step 3**: Count and inspect received items\n"
                   "**Step 4**: Update system with 'gate in shipment [ID]'\n"
                   "**Step 5**: Assign storage locations\n"
                   "**Step 6**: Update inventory levels\n\n"
                   " **Goal**: Ensure accurate receiving and proper storage")
        else:
            return ("**General Warehouse Procedures**\n\n"
                   " **Safety First**: Always follow safety protocols\n"
                   " **Accuracy**: Double-check all SKUs and quantities\n"
                   " **Documentation**: Keep detailed records of all operations\n"
                   " **Organization**: Maintain clean and organized storage areas\n"
                   " **Communication**: Report any discrepancies immediately\n\n"
                   "Need specific guidance? Ask about 'inbound procedures' or 'outbound procedures'!")
    
    def _generate_vendor_info(self) -> str:
        """Generate vendor information"""
        vendors = set(shipment["vendor"] for shipment in self.warehouse_knowledge["shipments"].values())
        return (f" **Vendor Information**\n\n"
               f"**Active Vendors**: {len(vendors)}\n\n" + 
               "\n".join(f" {vendor}" for vendor in vendors) +
               "\n\n **Vendor Relations**: Maintaining strong partnerships for reliable supply chain.")
    
    def _generate_category_info(self) -> str:
        """Generate product category information"""
        return (" **Product Categories**\n\n"
               "Our warehouse manages these product categories:\n\n"
               " **Electronics Accessories**\n"
               " Headphones, Earbuds, Audio Equipment\n\n"
               " **Mobile Accessories**\n"
               " Cases, Screen Protectors, Cables\n\n"
               " **Computer Peripherals**\n"
               " Mice, Keyboards, Chargers, Cables\n\n"
               "**Tech Support Items**\n"
               " Adapters, Connectors, Power Supplies\n\n"
               "**Total Categories**: 4 main categories with diverse product lines")
    
    def _generate_greeting(self) -> str:
        """Generate friendly greeting"""
        return ("**Welcome to Smart Warehouse Management!**\n\n"
               "I'm your AI-powered warehouse assistant, ready to help with:\n\n"
               "* Inventory checks and stock management\n"
               "* Inbound and outbound operations\n"
               "* Order processing and shipment tracking\n"
               "* Real-time alerts and notifications\n\n"
               "How can I assist you today? Try asking about inventory, orders, or say 'help' for more options!")
    
    def _generate_default_response(self, prompt: str) -> str:
        """Generate intelligent default response based on context"""
        if "invalid" in prompt.lower():
            return ("**Item Not Found**\n\n"
                   "The specified item could not be located in our system.\n"
                   "Please check the details and try again.\n\n"
                   " **Suggestions**:\n"
                   " Verify SKU format (e.g., PROD001)\n"
                   " Check order/shipment ID format\n"
                   " Use 'show inventory summary' to see available items")
        
        elif "error" in prompt.lower() or "problem" in prompt.lower():
            return ("**System Support**\n\n"
                   "I'm here to help resolve any warehouse management issues!\n\n"
                   "**Common Solutions**:\n"
                   " Check data format and try again\n"
                   " Verify permissions and access levels\n"
                   " Contact system administrator if problems persist\n\n"
                   "What specific operation would you like to process?")
        
        elif any(word in prompt.lower() for word in ["inventory", "stock", "product"]):
            return ("**Inventory Operations**\n\n"
                   "I can help with all inventory-related tasks:\n\n"
                   " Stock level checks\n"
                   " Inventory updates\n"
                   " Location management\n"
                   " Low stock alerts\n\n"
                   "What inventory operation would you like to perform?")
        
        elif any(word in prompt.lower() for word in ["order", "dispatch", "ship", "outbound"]):
            return ("**Outbound Operations**\n\n"
                   "Ready to process outbound operations:\n\n"
                   " Order preparation\n"
                   " Dispatch processing\n"
                   " Shipping coordination\n"
                   " Delivery tracking\n\n"
                   "What outbound operation would you like to process?")
        
        elif any(word in prompt.lower() for word in ["delivery", "shipment", "receiving", "inbound"]):
            return ("**Inbound Operations**\n\n"
                   "Ready to handle inbound operations:\n\n"
                   " Shipment receiving\n"
                   " Quality inspection\n"
                   " Put-away processing\n"
                   " Vendor coordination\n\n"
                   "What inbound operation would you like to process?")
        
        else:
            return ("**Smart Warehouse Assistant**\n\n"
                   "I'm here to help with all your warehouse management needs! I can assist with:\n\n"
                   "**Inventory Operations** - Stock checks, updates, alerts\n"
                   "**Shipping & Orders** - Dispatch, tracking, documentation\n"
                   "**Receiving** - Gate-in, quality control, storage\n"
                   "**Analytics** - Reports, insights, optimization\n\n"
                   "Try asking me about specific operations or say 'help' for detailed guidance!")
    
    def is_available(self) -> bool:
        """Mock service is always available"""
        return True
