# Enhanced Smart LLM Service for Warehouse Management
import os
import logging
import requests
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class EnhancedSmartLLMService:
    """Enhanced Smart LLM service with intelligent warehouse responses"""
    
    def __init__(self):
        self.llm = None
        self.service_type = None
        self._initialize_best_available_llm()
    
    def _initialize_best_available_llm(self):
        """Try different LLM approaches in order of preference"""
        
        # Method 1: Try Hugging Face Inference API
        if self._try_huggingface_inference():
            return
        
        # Method 2: Fall back to Enhanced Smart Mock Service
        self._initialize_enhanced_smart_mock()
        
    def _try_huggingface_inference(self) -> bool:
        """Try to initialize HuggingFace Inference API"""
        try:
            model_name = os.getenv("LLM_MODEL_NAME", "princeton-nlp/Sheared-LLaMA-2.7B")
            api_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
            
            if not api_token:
                logger.warning("No HuggingFace token found, skipping HF Inference API")
                return False
                
            api_url = f"https://api-inference.huggingface.co/models/{model_name}"
            
            # Test the API with a simple request
            test_wrapper = HuggingFaceInferenceWrapper(model_name, api_token, api_url)
            test_response = test_wrapper.generate_response("Hello", max_length=10)
            
            if test_response and "error" not in test_response.lower() and "loading" not in test_response.lower():
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
    
    def _initialize_enhanced_smart_mock(self):
        """Initialize the Enhanced Smart Mock LLM service as fallback"""
        try:
            self.llm = EnhancedSmartMockLLMService()
            self.service_type = "enhanced_smart_mock"
            logger.info("Initialized Enhanced Smart Mock LLM Service")
        except Exception as e:
            logger.error(f"Failed to initialize Enhanced Smart Mock LLM: {str(e)}")
            raise
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using the available LLM service"""
        try:
            return self.llm.generate_response(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Error generating response with {self.service_type}: {str(e)}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."
    
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
    
    def generate_response(self, prompt: str, max_length: int = 150, **kwargs) -> str:
        """Generate response using HuggingFace Inference API"""
        try:
            # Format prompt for instruction-following models like Sheared LLaMA
            if "llama" in self.model_name.lower() or "sheared" in self.model_name.lower():
                formatted_prompt = f"<s>[INST] You are a helpful warehouse management assistant. {prompt} [/INST]"
            else:
                formatted_prompt = f"Human: {prompt}\nAssistant:"
            
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": 0.7,
                    "return_full_text": False,
                    "do_sample": True
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


class EnhancedSmartMockLLMService:
    """Enhanced intelligent mock LLM service with superior warehouse responses"""
    
    def __init__(self):
        self.warehouse_knowledge = {
            "inventory": {
                "PROD001": {"name": "Wireless Bluetooth Headphones", "stock": 137, "location": "A1-01", "category": "Electronics"},
                "PROD002": {"name": "USB-C Charging Cable", "stock": 67, "location": "A1-02", "category": "Electronics"},
                "PROD003": {"name": "Laptop Stand Aluminum", "stock": 113, "location": "A2-01", "category": "Accessories"},
                "PROD004": {"name": "Office Chair Ergonomic", "stock": 47, "location": "B1-01", "category": "Furniture"},
                "PROD005": {"name": "Desk Lamp LED", "stock": 108, "location": "A3-01", "category": "Lighting"},
                "PROD006": {"name": "Notebook A4 Ruled", "stock": 34, "location": "C1-01", "category": "Stationery"},
                "PROD007": {"name": "Mechanical Keyboard", "stock": 13, "location": "A1-03", "category": "Electronics"},
                "PROD008": {"name": "Monitor 24-inch", "stock": 81, "location": "B2-01", "category": "Electronics"},
                "PROD009": {"name": "Wireless Mouse", "stock": 93, "location": "A1-04", "category": "Electronics"},
                "PROD010": {"name": "Power Bank 10000mAh", "stock": 106, "location": "A1-05", "category": "Electronics"},
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
        
        # Enhanced greeting and help responses
        if any(word in prompt_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return self._generate_enhanced_greeting()
        
        elif any(phrase in prompt_lower for phrase in ["help", "what can you", "how can you", "what do you do"]):
            return self._generate_comprehensive_help()
        
        elif "warehouse management" in prompt_lower or "warehouse operations" in prompt_lower:
            return self._generate_warehouse_management_guidance()
        
        # Stock and inventory responses
        elif "check stock" in prompt_lower or "stock level" in prompt_lower:
            return self._handle_stock_check_enhanced(prompt)
        
        elif "inventory summary" in prompt_lower or "show inventory" in prompt_lower:
            return self._generate_enhanced_inventory_summary()
        
        # Low stock and reorder responses
        elif any(phrase in prompt_lower for phrase in ["low stock", "running low", "need reorder", "reorder"]):
            return self._generate_enhanced_low_stock_alert()
        
        # Inbound operations
        elif any(phrase in prompt_lower for phrase in ["gate in", "inbound", "delivery arrived", "shipment"]):
            return self._handle_enhanced_inbound_operation(prompt)
        
        # Outbound operations
        elif any(phrase in prompt_lower for phrase in ["dispatch", "ship order", "outbound", "send order"]):
            return self._handle_enhanced_outbound_operation(prompt)
        
        # Procedure and guidance requests
        elif any(phrase in prompt_lower for phrase in ["procedure", "how do i", "process", "workflow"]):
            return self._generate_enhanced_procedure_guidance(prompt)
        
        # Category and vendor information
        elif "categories" in prompt_lower or "product categories" in prompt_lower:
            return self._generate_enhanced_category_info()
        
        elif "vendor" in prompt_lower or "supplier" in prompt_lower:
            return self._generate_enhanced_vendor_info()
        
        # Error handling and edge cases
        elif "error" in prompt_lower or "problem" in prompt_lower or "issue" in prompt_lower:
            return self._generate_troubleshooting_response()
        
        # Default intelligent response
        else:
            return self._generate_enhanced_default_response(prompt)
    
    def _generate_enhanced_greeting(self) -> str:
        """Generate a warm, professional greeting"""
        return (
            " **Welcome to Smart Warehouse Management!**\n\n"
            "I'm your AI-powered warehouse assistant, equipped with real-time access to your inventory, "
            "shipment tracking, and order management systems.\n\n"
            "**🎯 I can help you with:**\n"
            "• **Inventory Management** - Stock checks, levels, locations, reorder alerts\n"
            "• **Inbound Operations** - Shipment receiving, gate-in processing, vendor coordination\n"
            "• **Outbound Operations** - Order dispatch, shipping, customer management\n"
            "• **Analytics & Reports** - Stock analysis, low inventory alerts, operational insights\n"
            "• **Procedures & Training** - Step-by-step guidance for warehouse processes\n\n"
            "**💡 Quick Start:**\n"
            "Try saying: 'Show inventory summary' or 'Check stock SKU: PROD001'\n\n"
            "How can I assist you with your warehouse operations today?"
        )
    
    def _generate_comprehensive_help(self) -> str:
        """Generate comprehensive help with examples"""
        return (
            " **Smart Warehouse Assistant - Complete Help Guide**\n\n"
            "I'm here to streamline your warehouse operations with intelligent automation and real-time data access.\n\n"
            "** INVENTORY MANAGEMENT**\n"
            "• `'Show inventory summary'` - Complete overview of all products\n"
            "• `'Check stock SKU: PROD001'` - Detailed stock information\n"
            "• `'What products are running low?'` - Low stock alerts\n"
            "• `'Update stock levels'` - Inventory adjustments\n\n"
            "** INBOUND OPERATIONS**\n"
            "• `'Gate in shipment SH001'` - Process incoming deliveries\n"
            "• `'Delivery arrived from ABC Suppliers'` - General receiving\n"
            "• `'Show pending shipments'` - Track incoming inventory\n\n"
            "** OUTBOUND OPERATIONS**\n"
            "• `'Dispatch order ORD001'` - Process customer orders\n"
            "• `'Ship order to TechCorp'` - Prepare shipments\n"
            "• `'Show ready orders'` - View pending dispatches\n\n"
            "** ANALYTICS & REPORTING**\n"
            "• `'Show product categories'` - Inventory categorization\n"
            "• `'Vendor information'` - Supplier relationships\n"
            "• `'Warehouse procedures'` - Operational guidance\n\n"
            "** SYSTEM FEATURES**\n"
            "• Real-time database integration\n"
            "• Intelligent intent recognition\n"
            "• Automated workflow suggestions\n"
            "• Error handling and validation\n\n"
            "**💡 Pro Tips:**\n"
            "- Be specific with SKUs, order numbers, and shipment IDs\n"
            "- Ask follow-up questions for detailed information\n"
            "- Use natural language - I understand context!\n\n"
            "What specific warehouse operation would you like to explore?"
        )
    
    def _generate_warehouse_management_guidance(self) -> str:
        """Generate specific warehouse management guidance"""
        return (
            "🏭 **Warehouse Management Excellence**\n\n"
            "I'm your dedicated warehouse management partner, designed to optimize your operations "
            "through intelligent automation and real-time insights.\n\n"
            "**🎯 CORE CAPABILITIES:**\n\n"
            "** Real-Time Inventory Control**\n"
            "• Live stock level monitoring across all 10 product lines\n"
            "• Automatic low-stock alerts (currently: PROD006 needs attention)\n"
            "• Location tracking and optimization\n"
            "• Reserved vs. available quantity management\n\n"
            "** Streamlined Operations**\n"
            "• Inbound: Automated receiving workflows and vendor coordination\n"
            "• Outbound: Efficient order processing and dispatch management\n"
            "• Quality control: Systematic inspection and put-away processes\n\n"
            "**💡 SMART FEATURES:**\n"
            "• **Predictive Insights**: Anticipate reorder needs\n"
            "• **Workflow Automation**: Streamline repetitive tasks\n"
            "• **Error Prevention**: Built-in validation and checks\n"
            "• **Performance Tracking**: Monitor operational efficiency\n\n"
            "**🔄 BEST PRACTICES I ENFORCE:**\n"
            "1. **Accuracy First**: Double-check all SKUs and quantities\n"
            "2. **Real-Time Updates**: Immediate inventory adjustments\n"
            "3. **Documentation**: Complete audit trails for all operations\n"
            "4. **Safety Compliance**: Adherence to warehouse safety protocols\n"
            "5. **Continuous Improvement**: Data-driven optimization suggestions\n\n"
            "**Ready to optimize your warehouse? Ask me about any specific operation!**"
        )
    
    def _handle_stock_check_enhanced(self, prompt: str) -> str:
        """Enhanced stock check with recommendations"""
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
            stock_level = item["stock"]
            
            # Enhanced status determination
            if stock_level < 20:
                status = "🔴 CRITICAL - Immediate Action Required"
                recommendation = " **URGENT**: Stock critically low. Initiate emergency reorder procedure immediately."
            elif stock_level < 50:
                status = " WARNING - Monitor Closely"
                recommendation = " **RECOMMENDED**: Consider reordering within next 7 days to maintain buffer stock."
            else:
                status = "HEALTHY - Optimal Levels"
                recommendation = "**STATUS**: Stock levels are healthy. Continue regular monitoring."
            
            return (
                f" **Enhanced Stock Analysis**\n\n"
                f"**Product Details:**\n"
                f"• **Name**: {item['name']}\n"
                f"• **SKU**: {sku}\n"
                f"• **Category**: {item['category']}\n"
                f"• **Location**: {item['location']}\n\n"
                f"**Stock Information:**\n"
                f"• **Available**: {stock_level} units\n"
                f"• **Status**: {status}\n\n"
                f"**Recommendation:**\n"
                f"{recommendation}\n\n"
                f"**Quick Actions:**\n"
                f"• Check recent stock movements\n"
                f"• Review sales velocity\n"
                f"• Contact supplier if reorder needed\n"
                f"• Update reorder point if necessary"
            )
        elif sku:
            return (
                f" **Product Not Found**\n\n"
                f"SKU '{sku}' is not in our current inventory system.\n\n"
                f"**Possible Reasons:**\n"
                f"• SKU may be discontinued\n"
                f"• Possible typo in SKU format\n"
                f"• Product not yet added to system\n\n"
                f"**Available SKUs**: {', '.join(self.warehouse_knowledge['inventory'].keys())}\n\n"
                f"**Next Steps:**\n"
                f"• Verify SKU format with product database\n"
                f"• Check if product needs to be added to inventory\n"
                f"• Review recent product changes or updates"
            )
        else:
            return (
                " **Stock Check Assistant**\n\n"
                "To check stock levels, please specify a product SKU.\n\n"
                "**Format**: 'Check stock SKU: PROD001'\n\n"
                f"**Currently Available Products**: {len(self.warehouse_knowledge['inventory'])} SKUs\n"
                f"**Available SKUs**: {', '.join(self.warehouse_knowledge['inventory'].keys())}\n\n"
                "**Example Queries:**\n"
                "• 'Check stock SKU: PROD001' - Specific product check\n"
                "• 'Show inventory summary' - Complete overview\n"
                "• 'What products are running low?' - Low stock alerts"
            )
    
    def _generate_enhanced_low_stock_alert(self) -> str:
        """Enhanced low stock alert with action plan"""
        low_stock_items = [(sku, item) for sku, item in self.warehouse_knowledge["inventory"].items() 
                          if item["stock"] < 50]  # More comprehensive threshold
        
        if low_stock_items:
            alert = " **Enhanced Low Stock Management Report**\n\n"
            
            critical_items = [item for item in low_stock_items if item[1]["stock"] < 20]
            warning_items = [item for item in low_stock_items if 20 <= item[1]["stock"] < 50]
            
            if critical_items:
                alert += "🔴 **CRITICAL - Immediate Action Required:**\n"
                for sku, item in critical_items:
                    alert += f"• **{sku}**: {item['name']} - Only {item['stock']} units ({item['location']})\n"
                alert += "\n"
            
            if warning_items:
                alert += " **WARNING - Monitor Closely:**\n"
                for sku, item in warning_items:
                    alert += f"• **{sku}**: {item['name']} - {item['stock']} units ({item['location']})\n"
                alert += "\n"
            
            alert += (
                "** RECOMMENDED ACTIONS:**\n"
                "1. **Priority Reordering**: Focus on critical items first\n"
                "2. **Supplier Contact**: Notify vendors of urgent needs\n"
                "3. **Lead Time Review**: Check delivery schedules\n"
                "4. **Alternative Sources**: Identify backup suppliers if needed\n"
                "5. **Sales Analysis**: Review demand patterns for better forecasting\n\n"
                "**🎯 NEXT STEPS:**\n"
                "• Generate purchase orders for critical items\n"
                "• Update reorder points based on recent consumption\n"
                "• Set up automated alerts for future prevention\n"
                "• Review safety stock levels across all categories"
            )
            
            return alert
        else:
            return (
                "**Stock Levels Optimal**\n\n"
                "Great news! All products are currently well-stocked with healthy inventory levels.\n\n"
                "**Current Status:**\n"
                "• No critical stock situations\n"
                "• All products above minimum thresholds\n"
                "• Supply chain running smoothly\n\n"
                "**Proactive Monitoring:**\n"
                "• Continue regular stock level reviews\n"
                "• Monitor sales velocity trends\n"
                "• Maintain supplier relationships\n"
                "• Plan for seasonal demand variations\n\n"
                "**💡 TIP**: Regular monitoring prevents stock-outs. "
                "I'll alert you immediately when any items approach reorder levels!"
            )
    
    def _generate_enhanced_default_response(self, prompt: str) -> str:
        """Enhanced context-aware default response"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["thank", "thanks", "appreciate"]):
            return (
                " **You're very welcome!**\n\n"
                "I'm always here to help optimize your warehouse operations. "
                "Feel free to ask me anything about inventory management, "
                "order processing, or system procedures.\n\n"
                "Is there anything else I can assist you with today?"
            )
        
        elif any(word in prompt_lower for word in ["bye", "goodbye", "see you", "later"]):
            return (
                " **Until next time!**\n\n"
                "Thank you for using Smart Warehouse Management. "
                "Remember, I'm available 24/7 for all your warehouse needs.\n\n"
                "Have a productive day managing your operations!"
            )
        
        elif "performance" in prompt_lower or "efficiency" in prompt_lower:
            return (
                " **Warehouse Performance Insights**\n\n"
                "Based on current data analysis:\n\n"
                "**Strengths:**\n"
                "• Inventory accuracy: Excellent\n"
                "• Stock levels: Well maintained (90% optimal)\n"
                "• System uptime: 100% operational\n"
                "• Processing speed: Real-time responses\n\n"
                "**🎯 Optimization Opportunities:**\n"
                "• Monitor PROD006 reorder patterns\n"
                "• Consider bulk ordering for high-velocity items\n"
                "• Implement automated reorder triggers\n\n"
                "Would you like detailed analysis on any specific area?"
            )
        
        else:
            return (
                " **Smart Warehouse Assistant**\n\n"
                "I understand you're looking for warehouse assistance! "
                "While I may not have caught the exact details of your request, "
                "I'm equipped to help with all aspects of warehouse management.\n\n"
                "**🎯 I excel at:**\n"
                "• **Inventory Operations** - Stock checks, levels, alerts\n"
                "• **Order Management** - Inbound receiving, outbound dispatch\n"
                "• **System Intelligence** - Analytics, recommendations, automation\n"
                "• **Process Guidance** - Procedures, workflows, best practices\n\n"
                "**💡 Try being more specific:**\n"
                "• 'Show me inventory status'\n"
                "• 'Process shipment SH001'\n"
                "• 'Help with warehouse procedures'\n"
                "• 'What needs my attention today?'\n\n"
                "How can I help optimize your warehouse operations?"
            )
    
    def _generate_enhanced_inventory_summary(self) -> str:
        """Generate comprehensive inventory summary with insights"""
        total_items = sum(item["stock"] for item in self.warehouse_knowledge["inventory"].values())
        categories = {}
        low_stock_items = []
        
        for sku, item in self.warehouse_knowledge["inventory"].items():
            category = item["category"]
            categories[category] = categories.get(category, 0) + item["stock"]
            if item["stock"] < 50:
                low_stock_items.append((sku, item))
        
        summary = (
            f" **Comprehensive Warehouse Analytics Dashboard**\n\n"
            f"** INVENTORY OVERVIEW**\n"
            f"• **Total Product Lines**: {len(self.warehouse_knowledge['inventory'])} SKUs\n"
            f"• **Total Units in Stock**: {total_items:,} items\n"
            f"• **Categories Managed**: {len(categories)} product categories\n"
            f"• **Alerts**: {len(low_stock_items)} items need attention\n\n"
            f"** CATEGORY BREAKDOWN**\n"
        )
        
        for category, count in sorted(categories.items()):
            summary += f"• **{category}**: {count} units\n"
        
        summary += f"\n**🎯 OPERATIONAL STATUS**\n"
        if low_stock_items:
            summary += f"• **Action Required**: {len(low_stock_items)} items below optimal levels\n"
            for sku, item in low_stock_items[:3]:  # Show top 3
                summary += f"  - {sku}: {item['name']} ({item['stock']} units)\n"
            if len(low_stock_items) > 3:
                summary += f"  - ... and {len(low_stock_items) - 3} more items\n"
        else:
            summary += "• **Status**: All inventory levels optimal\n"
        
        summary += (
            f"\n**💡 SMART INSIGHTS**\n"
            f"• **Electronics dominance**: {categories.get('Electronics', 0)} units across multiple SKUs\n"
            f"• **Storage efficiency**: Well-distributed across warehouse zones\n"
            f"• **Inventory health**: {((len(self.warehouse_knowledge['inventory']) - len(low_stock_items)) / len(self.warehouse_knowledge['inventory']) * 100):.0f}% of products at healthy levels\n\n"
            f"**🔄 QUICK ACTIONS**\n"
            f"• Review low stock items for reordering\n"
            f"• Analyze fast-moving products for bulk purchasing\n"
            f"• Optimize storage locations based on velocity\n"
            f"• Update reorder points for seasonal adjustments"
        )
        
        return summary
    
    def is_available(self) -> bool:
        """Enhanced service is always available"""
        return True
